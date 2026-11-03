"""원고 JSON과 개념 도식으로 편집용 DOCX를 조판한다."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from layout import build

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/figures/chapter01'
OUT.mkdir(parents=True,exist_ok=True)
INK='#202b35';BLUE='#c2d6d9';CREAM='#f1e6ce';RUST='#dfb19c';WHITE='#ffffff';GRAY='#ced0c9'
font_path='C:/Windows/Fonts/malgun.ttf'
bold_path='C:/Windows/Fonts/malgunbd.ttf'
def font(size=36,bold=False):return ImageFont.truetype(bold_path if bold else font_path,size)
def canvas(height):
    im=Image.new('RGB',(1280,height),WHITE)
    return im,ImageDraw.Draw(im)
def box(d,rect,title,sub=None,fill=CREAM,title_size=40):
    x,y,r,b=rect
    for sy in range(y+10,b+13,9):
        for sx in range(x+10,r+13,9):d.rectangle((sx,sy,sx+3,sy+3),fill=GRAY)
    d.rectangle(rect,fill=fill,outline=INK,width=4)
    lines=title.split('\n');lineh=title_size+13
    total=len(lines)*lineh+(55 if sub else 0)
    yy=(y+b-total)/2
    for line in lines:
        bb=d.textbbox((0,0),line,font=font(title_size,True));assert bb[2] < r-x-25,(title,bb,r-x)
        d.text(((x+r-bb[2])/2,yy),line,font=font(title_size,True),fill=INK);yy+=lineh
    if sub:
        bb=d.textbbox((0,0),sub,font=font(34));assert bb[2]<r-x-25,(sub,bb,r-x)
        d.text(((x+r-bb[2])/2,yy+3),sub,font=font(34),fill=INK)
def arrow(d,start,end):
    x,y=start;u,v=end;d.line((x,y,u,v),fill=INK,width=5)
    if u==x:d.polygon([(u,v),(u-12,v-20),(u+12,v-20)],fill=INK)
    else:d.polygon([(u,v),(u-20,v-12),(u-20,v+12)],fill=INK)
def save(im,name):im.save(OUT/(name+'.png'))

im,d=canvas(660)
box(d,(25,20,600,225),'1 대상 식별','컴퓨터 · 계정 · 시각',BLUE)
box(d,(680,20,1255,225),'2 생성 확인','센서 · 채널 · 감사',CREAM)
box(d,(680,390,1255,620),'3 수집 확인','원본 · 에이전트 · 매니저',RUST)
box(d,(25,390,600,620),'4 기록 대조','동일 이벤트 · 조사 근거',BLUE)
arrow(d,(605,120),(670,120));arrow(d,(970,235),(970,380))
d.line((670,500,610,500),fill=INK,width=5);d.polygon([(610,500),(630,488),(630,512)],fill=INK)
save(im,'readiness')

im,d=canvas(790)
d.rectangle((10,10,1265,775),outline=INK,width=5)
d.text((34,22),'독자의 Windows PC',font=font(40,True),fill=INK)
d.rectangle((40,105,1235,744),outline=INK,width=4,fill='#f7f5ef')
d.text((65,120),'VMware  Ubuntu VM  kt66',font=font(39,True),fill=INK)
d.text((65,177),'예시 주소 192.168.0.107',font=font(34),fill=INK)
d.rectangle((75,260,765,700),outline=INK,width=4,fill=BLUE)
d.text((100,280),'Docker  kt66-windows-user',font=font(38,True),fill=INK)
d.text((100,340),'QEMU/KVM',font=font(36),fill=INK)
box(d,(110,440,730,650),'Windows 게스트','KT66-WIN-01',CREAM,38)
box(d,(875,440,1200,650),'Wazuh 매니저','kt66-siem',RUST,36)
arrow(d,(775,550),(865,550))
save(im,'topology')

im,d=canvas(650)
box(d,(25,20,1255,190),'컴퓨터 + 채널','예  KT66-WIN-01 / Security',BLUE)
d.line((640,200,640,235),fill=INK,width=5)
d.line((315,235,970,235),fill=INK,width=5)
arrow(d,(315,235),(315,275));arrow(d,(970,235),(970,275))
box(d,(25,280,605,480),'이벤트 종류','공급자 + EventID',CREAM)
box(d,(680,280,1255,480),'개별 기록','EventRecordID + 시각',RUST)
d.text((90,530),'예  보안 감사 / 4624',font=font(36),fill=INK)
d.text((740,530),'예  9115 / UTC 시각',font=font(36),fill=INK)
d.text((100,595),'사건 종류가 같아도 개별 기록은 서로 다르다',font=font(38,True),fill=INK)
save(im,'event-model')

im,d=canvas(790)
nodes=[('1 Windows 원본','채널 · 정책 · 필터',BLUE),('2 에이전트 수집','설정 · 서비스 · 동작 로그',CREAM),('3 매니저와 경보','연결 · 규칙 · 저장 조건',RUST),('4 Discover 검색','데이터 보기 · 기간 · 필드',BLUE)]
for i,(title,sub,fill) in enumerate(nodes):
    y=15+i*195;box(d,(110,y,1170,y+150),title,sub,fill)
    if i<3:arrow(d,(640,y+160),(640,y+188))
save(im,'troubleshoot')

build(ROOT/'manuscript/volume02-chapter01.docx',ROOT/'manuscript/volume02-chapter01.json')
