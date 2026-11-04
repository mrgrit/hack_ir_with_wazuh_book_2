"""Word 임시 PDF의 모든 쪽을 렌더하고 판면 밖 텍스트를 찾는다. 배포 PDF를 만들지 않는다."""
from pathlib import Path
import json,hashlib
import pypdfium2 as pdfium
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
def main():
 qa=ROOT/'build/REV01/visual';qa.mkdir(parents=True,exist_ok=True)
 reports=[]
 for path in sorted((ROOT/'build/REV01/render').glob('*.pdf')):
  doc=pdfium.PdfDocument(path);pages=[]
  for i in range(len(doc)):
   page=doc[i];tp=page.get_textpage();w,h=page.get_size();bad=[];bottom=0
   for k in range(tp.count_chars()):
    char=tp.get_text_range(k,1)
    if not char.strip():continue
    x0,y0,x1,y1=tp.get_charbox(k);top=h-y1;bot=h-y0
    if 70<top<640:
     bottom=max(bottom,bot)
     if x0<77 or x1>462 or bot>629:bad.append({'char':char,'box':[round(x,2) for x in [x0,top,x1,bot]]})
   text=tp.get_text_range();pages.append({'page':i+1,'chars':len(text),'outliers':bad,'bottom':round(bottom,2)})
   im=page.render(scale=2).to_pil().convert('RGB').crop((140,96,round(w*2)-130,1332))
   canvas=Image.new('RGB',(im.width,im.height+32),'white');canvas.paste(im,(0,32));ImageDraw.Draw(canvas).text((10,8),f'{path.stem} / {i+1:03}',fill='black')
   canvas.save(qa/f'{path.stem}-{i+1:03}.png')
   tp.close();page.close()
  for start in range(0,len(doc),4):
   ims=[Image.open(qa/f'{path.stem}-{j+1:03}.png') for j in range(start,min(start+4,len(doc)))]
   w,h=ims[0].size;sheet=Image.new('RGB',(w*2+12,h*2+12),(220,220,220))
   for j,im in enumerate(ims):sheet.paste(im,((j%2)*(w+12),(j//2)*(h+12)))
   sheet.save(qa/f'review-{path.stem}-{start+1:03}.jpg',quality=92)
  reports.append({'file':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'pages':pages})
  print(path.name,len(doc),'pages, outlier pages',sum(bool(p['outliers']) for p in pages),flush=True);doc.close()
 (ROOT/'editorial/REV01/render-check.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n','utf8')
 print('total',sum(len(x['pages']) for x in reports))
if __name__=='__main__':main()
