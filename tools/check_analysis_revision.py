"""본문·예제·DOCX·렌더의 일치와 이전 승인 페이지 대응을 점검한다."""
from pathlib import Path
import json,hashlib,re,zipfile,sys
import pypdfium2 as pdfium
from pypdf import PdfReader
from lxml import etree
from docx import Document
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'build/analysis-revision'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
def sha(b):return hashlib.sha256(b).hexdigest()
def norm(t):return re.sub(r'\s+','',t).replace('\u00ad','')
def old_pdf(stem):
 d=json.loads((ROOT/'editorial'/f'{stem}-qa.json').read_text(encoding='utf8'))
 fallback={'chapter01':'build/chapter01/volume02-chapter01-final.pdf','chapter02':'build/chapter02/chapter02-final.pdf','chapter03':'build/chapter03/chapter03-final2.pdf','chapter04':'build/ch04-final.pdf','chapter05':'build/ch05-final2.pdf'}
 return ROOT/(d['internal_render'] if 'internal_render'in d else fallback[stem])
def render_and_map(stem):
 out=OUT/'render'/stem;out.mkdir(parents=True,exist_ok=True)
 old=pdfium.PdfDocument(old_pdf(stem));oldhash={}
 for i in range(len(old)):
  im=old[i].render(scale=1.7).to_pil().convert('RGB')
  # 본문·머리글·페이지 번호를 포함해 비교. 하단 7%의 빈 여백만 제외.
  h=sha(im.crop((0,0,im.width,int(im.height*.93))).tobytes());oldhash.setdefault(h,[]).append(i+1)
 old.close()
 d=pdfium.PdfDocument(OUT/'render'/f'{stem}.pdf');pages=[]
 for i in range(len(d)):
  page=d[i];im=page.render(scale=1.7).to_pil().convert('RGB');f=out/f'page-{i+1:02}.png';im.save(f)
  h=sha(im.crop((0,0,im.width,int(im.height*.93))).tobytes())
  text=page.get_textpage().get_text_range()
  pages.append({'page':i+1,'png':str(f.relative_to(ROOT)).replace('\\','/'),'sha256':sha(f.read_bytes()),'body_sha256':h,'same_as_prior_pages':oldhash.get(h,[]),'characters':len(text),'start':text[:80],'end':text[-120:]})
 d.close();(out/'pages.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 return pages
def structural(stem):
 src=ROOT/f'manuscript/volume02-{stem}.json';docx=src.with_suffix('.docx');data=json.loads(src.read_text(encoding='utf8'))
 blocks=[b for pg in data['pages'] for b in pg['blocks']];inputs=[b for b in blocks if b['type'] in ('query','command')]
 assert len({b['id'] for b in inputs})==len(inputs),(stem,'duplicate input')
 z=zipfile.ZipFile(docx);xml=etree.fromstring(z.read('word/document.xml'));body=''.join(xml.xpath('//w:t/text()',namespaces=NS))
 for b in inputs:
  ext='.dql' if b['type']=='query' else '.txt';f=ROOT/'examples'/stem/(b['id']+ext)
  assert f.read_text(encoding='utf8').rstrip()==b['text'].rstrip(),str(f)
  assert norm(b['text']) in norm(body),(stem,b['id'],'DOCX input mismatch')
 manifest=json.loads((ROOT/'examples'/stem/'manifest.json').read_text(encoding='utf8'))
 assert {m['id']:m['input'] for m in manifest}=={b['id']:b['text'] for b in inputs}
 media={sha(z.read(n)) for n in z.namelist() if n.startswith('word/media/')}
 for b in blocks:
  if b['type']=='image':assert sha((ROOT/b['path']).read_bytes()) in media,(stem,b['path'])
 d=Document(docx);base=Document(ROOT/'tools/assets/bookk-B5.docx')
 for prop in ['page_width','page_height','top_margin','bottom_margin','left_margin','right_margin']:
  assert getattr(d.sections[0],prop)==getattr(base.sections[0],prop),(stem,prop)
 pdf=PdfReader(OUT/'render'/f'{stem}.pdf');text=''.join(p.extract_text() for p in pdf.pages)
 urls=[b['url'] for b in blocks if b['type']=='link']
 for url in urls:assert norm(url) in norm(text),(stem,'PDF URL',url)
 assert not re.search(r'gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]+|-----BEGIN .*PRIVATE KEY',body),(stem,'secret signature')
 return {'docx_sha256':sha(docx.read_bytes()),'manuscript_sha256':sha(src.read_bytes()),'pages':len(pdf.pages),'inputs':len(inputs),'new_dql':len([b for b in inputs if b.get('revision')]),'figures':len([b for b in blocks if b['type']=='image']),'full_urls':len(urls),'checks':'input files and DOCX text, manifest, image hashes, template geometry, PDF full URLs, credential signatures passed'}
def main():
 stems=sys.argv[1:] or [f'chapter{x:02}' for x in range(1,14)]+['appendix']
 allresults={}
 for stem in stems:
  r=structural(stem);r['page_review']=render_and_map(stem);allresults[stem]=r
  print(stem,r['pages'],'pages;',sum(not p['same_as_prior_pages'] for p in r['page_review']),'changed',flush=True)
 (OUT/'checks.json').write_text(json.dumps(allresults,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
if __name__=='__main__':main()
