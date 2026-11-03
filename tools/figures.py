"""관계·흐름 도식용 공통 그리기 도구. 실제 UI와 인물 삽화에는 사용하지 않는다."""
from PIL import Image,ImageDraw,ImageFont
INK='#202b35';BLUE='#c2d6d9';CREAM='#f1e6ce';RUST='#dfb19c';GRAY='#ced0c9'
def font(n,bold=False):return ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf' if bold else 'C:/Windows/Fonts/malgun.ttf',n)
def canvas(height):
 im=Image.new('RGB',(1280,height),'white');return im,ImageDraw.Draw(im)
def box(d,r,title,sub='',fill=CREAM,size=39):
 x,y,u,v=r
 for sy in range(y+12,v+13,10):
  for sx in range(x+12,u+13,10):d.rectangle((sx,sy,sx+3,sy+3),fill=GRAY)
 d.rectangle(r,fill=fill,outline=INK,width=4)
 lines=title.split('\n');yy=(y+v-len(lines)*(size+14)-(50 if sub else 0))/2
 for t in lines:
  w=d.textbbox((0,0),t,font=font(size,True))[2];assert w<u-x-25,(t,w,u-x)
  d.text(((x+u-w)/2,yy),t,font=font(size,True),fill=INK);yy+=size+14
 if sub:
  w=d.textbbox((0,0),sub,font=font(32))[2];assert w<u-x-25,(sub,w,u-x)
  d.text(((x+u-w)/2,yy+5),sub,font=font(32),fill=INK)
def arrow(d,a,b):
 x,y=a;u,v=b;d.line((x,y,u,v),fill=INK,width=5)
 if v>y:d.polygon([(u,v),(u-12,v-20),(u+12,v-20)],fill=INK)
 elif u>x:d.polygon([(u,v),(u-20,v-12),(u-20,v+12)],fill=INK)
 else:d.polygon([(u,v),(u+20,v-12),(u+20,v+12)],fill=INK)
