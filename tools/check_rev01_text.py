"""임시 Word PDF의 입력·URL·판형·쪽 번호를 원고와 대조한다."""
from pathlib import Path
import json, re, hashlib
import pypdfium2 as pdfium
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]

def norm(s):
    return re.sub(r'\s+', '', s).replace('\u00ad','').replace('\u200b','')

def main():
    reports=[]; errors=[]
    preview=ROOT/'build/REV01/fullpages'; preview.mkdir(parents=True,exist_ok=True)
    for f in sorted((ROOT/'manuscript/REV01').glob('*.json')):
        stem=f.stem.replace('volume02-','')
        source=json.loads(f.read_text('utf8'))
        path=ROOT/'build/REV01/render'/f'{stem}.pdf'
        doc=pdfium.PdfDocument(path); texts=[]; footers=[]
        for i in range(len(doc)):
            page=doc[i]; w,h=page.get_size(); tp=page.get_textpage()
            if abs(w*25.4/72-188)>.1 or abs(h*25.4/72-263)>.1:
                errors.append([stem,i+1,'page size'])
            body=tp.get_text_bounded(left=0,bottom=90,right=w,top=h-70)
            texts.append(body)
            footer=tp.get_text_bounded(left=0,bottom=0,right=w,top=90).strip()
            footers.append(footer)
            if footer!=str(i+1): errors.append([stem,i+1,'footer',footer])
            if not body.strip():errors.append([stem,i+1,'blank body'])
            if i==min(4,len(doc)-1):
                page.render(scale=1.5).to_pil().save(preview/f'{stem}.png')
            tp.close(); page.close()
        text=norm('\n'.join(texts))
        # Word가 줄 끝의 하이픈을 별도 글리프로 내보낼 때 PDFium은
        # U+FFFE로 추출한다. 임의 치환 대신 독립 추출기의 실제 매핑과 대조한다.
        alt=[]
        for i, page in enumerate(PdfReader(path).pages):
            lines=page.extract_text().splitlines()
            assert lines[1].strip()==str(i+1), (stem,i+1,'unexpected extraction order')
            alt.extend(lines[2:])
        alternate_text=norm('\n'.join(alt))
        blocks=[b for s in source['sections'] for b in s['blocks']]
        inputs=[b for b in blocks if b['type'] in ('command','query')]
        urls=[b for b in blocks if b['type']=='link']
        missing_inputs=[b['id'] for b in inputs if norm(b['text']) not in text and norm(b['text']) not in alternate_text]
        missing_urls=[b['url'] for b in urls if norm(b['url']) not in text and norm(b['url']) not in alternate_text]
        errors += [[stem,'missing input',x] for x in missing_inputs]
        errors += [[stem,'missing URL',x] for x in missing_urls]
        reports.append({'document':f.with_suffix('.docx').name,'pages':len(doc),
            'inputs_checked':len(inputs),'urls_checked':len(urls),
            'missing_inputs':missing_inputs,'missing_urls':missing_urls,
            'page_number_sequence':footers,
            'pdf_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
        doc.close()
    result={'documents':reports,'errors':errors}
    (ROOT/'editorial/REV01/text-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf8')
    print(json.dumps({'pages':sum(d['pages'] for d in reports),
        'inputs':sum(d['inputs_checked'] for d in reports),
        'urls':sum(d['urls_checked'] for d in reports),'errors':errors},ensure_ascii=False,indent=2))
    if errors:raise SystemExit(1)

if __name__=='__main__':main()
