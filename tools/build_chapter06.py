from pathlib import Path
from figures import *
from layout import build
from docx import Document
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/figures/chapter06';OUT.mkdir(parents=True,exist_ok=True)

im,d=canvas(650)
for i,(title,sub,c) in enumerate([('Sysmon 10','접근 주체 · LSASS 대상 · 허용 권한',BLUE),('Sysmon 3','연결 프로세스 · 출발지 · 목적지',CREAM),('Sysmon 22','질의 프로세스 · 이름 · 응답 상태',RUST)]):
 y=20+i*210;box(d,(55,y,1225,y+170),title,sub,c)
im.save(OUT/'evidence.png')

im,d=canvas(600)
for x,y,title,sub,c in [(25,20,'프로세스 접근','Sysmon 10 · 주체와 권한',BLUE),(675,20,'덤프 파일 작성','실제 파일 · 크기 · 생성 시각',CREAM),(675,340,'인증 자료 해석','추출 결과와 사용 가능성',RUST),(25,340,'다른 호스트의 인증','계정 · 출발지 · 대상 · 결과',BLUE)]:
 box(d,(x,y,x+580,y+190),title,sub,c,size=36)
arrow(d,(615,115),(665,115));arrow(d,(965,225),(965,325));arrow(d,(665,435),(615,435))
d.text((90,565),'각 단계의 결과를 별도로 확인한다',font=font(34),fill=INK)
im.save(OUT/'lsass.png')

im,d=canvas(630)
box(d,(40,20,1240,190),'Windows 게스트  172.30.70.2','PowerShell의 정상 HTTP 요청',BLUE)
arrow(d,(640,205),(640,285))
box(d,(40,300,1240,470),'kt66 내부 WAF  10.20.32.80:80','서버가 반환한 상태 코드 · 최종 주소 · 본문',CREAM)
d.text((75,510),'게스트 관찰: Sysmon 3의 프로세스와 연결',font=font(34),fill=INK)
d.text((75,565),'서버 관찰: 접근 로그의 요청과 응답',font=font(34),fill=INK)
im.save(OUT/'network.png')

im,d=canvas(680)
box(d,(40,20,1240,190),'이름 조회  Sysmon 22','질의 이름 · 프로세스 · 상태 · 결과',BLUE)
arrow(d,(325,205),(325,285));arrow(d,(955,205),(955,285))
box(d,(25,300,605,475),'성공한 응답','주소를 반환한 사실',CREAM)
box(d,(675,300,1255,475),'이름 부재 응답','주소를 얻지 못한 사실',RUST)
arrow(d,(325,490),(325,560))
d.text((45,590),'후속 접속은 Sysmon 3 등에서 따로 확인',font=font(37),fill=INK)
im.save(OUT/'dns.png')

im,d=canvas(670)
for i,(title,sub,c) in enumerate([('osquery  PID 5156','LSASS 접근 · sourceProcessGUID',BLUE),('PowerShell  PID 8080','HTTP 연결 3건 · 같은 processGuid',CREAM),('별도 PowerShell  PID 1540','DNS 질의 2건 · 같은 processGuid',RUST)]):
 y=20+i*215;box(d,(45,y,1235,y+180),title,sub,c,size=37)
im.save(OUT/'correlation.png')

build(ROOT/'manuscript/volume02-chapter06.docx',ROOT/'manuscript/volume02-chapter06.json')
doc=Document(ROOT/'manuscript/volume02-chapter06.docx')
doc.paragraphs[0].style=doc.styles['Title']
doc.save(ROOT/'manuscript/volume02-chapter06.docx')
