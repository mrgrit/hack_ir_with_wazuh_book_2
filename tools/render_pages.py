import sys,json
from pathlib import Path
import pypdfium2 as pdfium
from PIL import Image,ImageDraw
from pypdf import PdfReader
p=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
d=pdfium.PdfDocument(p);meta=[]
for i in range(len(d)):
 pg=d[i];im=pg.render(scale=1.7).to_pil();im.save(out/f'page-{i+1:02}.png')
 t=pg.get_textpage().get_text_range();meta.append({'page':i+1,'length':len(t),'start':t[:100],'end':t[-100:]})
for i in range(0,len(d),4):
 contact=Image.new('RGB',(1100,1580),'#c0c0c0');dr=ImageDraw.Draw(contact)
 for j in range(min(4,len(d)-i)):
  im=Image.open(out/f'page-{i+j+1:02}.png');im.thumbnail((540,755));x=(j%2)*550;y=(j//2)*790
  contact.paste(im,(x,y+25));dr.text((x+10,y+5),str(i+j+1),fill='black')
 contact.save(out/f'contact-{i+1:02}.png')
(out/'pages.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf8')
print(len(d),'pages rendered')
