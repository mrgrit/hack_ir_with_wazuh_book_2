from pathlib import Path
from figures import *
from layout import build
from docx import Document
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/figures/chapter07';OUT.mkdir(parents=True,exist_ok=True)

im,d=canvas(770)
for i,(title,sub,c) in enumerate([
 ('Windows 원본 채널','생성 · 채널 용량 · 덮어쓰기',BLUE),
 ('Wazuh 에이전트와 관리자','읽기 조건 · 전송 · 분석 · 저장',CREAM),
 ('인덱스와 검색','색인 · 보존 기간 · 접근 권한 · 검색',RUST)]):
 y=20+i*260;box(d,(45,y,1235,y+180),title,sub,c,size=38)
 if i<2:arrow(d,(640,y+195),(640,y+245))
im.save(OUT/'preservation.png')

im,d=canvas(700)
box(d,(25,20,1255,200),'Security  1102','Security 감사 로그 삭제의 기록',BLUE,size=40)
box(d,(25,265,1255,445),'System  104','다른 로그 삭제의 기록',CREAM,size=40)
arrow(d,(640,460),(640,510))
box(d,(25,525,1255,680),'LogFileCleared.Channel','실제로 지운 대상 채널 확인',RUST,size=38)
im.save(OUT/'clear-target.png')

im,d=canvas(790)
box(d,(210,20,1070,185),'1116  탐지','탐지 ID · 대상 · 시각',BLUE,size=42)
arrow(d,(450,200),(325,290));arrow(d,(830,200),(955,290))
box(d,(25,305,605,505),'1117  조치','조치 종류 · 오류 · 추가 작업',CREAM,size=38)
box(d,(675,305,1255,505),'1118 · 1119  오류','실패 원인 · 잔존 상태',RUST,size=38)
arrow(d,(325,520),(450,610));arrow(d,(955,520),(830,610))
box(d,(120,625,1160,775),'현재 상태와 후속 활동','활성 위협 · 재탐지 · 보호 상태',BLUE,size=38)
im.save(OUT/'defender-states.png')

im,d=canvas(810)
for i,(title,sub,c) in enumerate([
 ('09:56:49.229  원본 1116','RecordId 46 · 위협 탐지',BLUE),
 ('09:57:12.603  원본 1117','RecordId 47 · 격리 조치',CREAM),
 ('09:57:14.288  Wazuh 문서','1117 수집 · 경보 62124',RUST)]):
 y=20+i*260;box(d,(45,y,1235,y+180),title,sub,c,size=38)
 if i<2:arrow(d,(640,y+195),(640,y+245))
d.text((65,780),'2026-11-02 UTC · 사건 연결은 같은 탐지 ID로 대조',font=font(29),fill=INK)
im.save(OUT/'timeline.png')

output=ROOT/'manuscript/volume02-chapter07.docx'
build(output,ROOT/'manuscript/volume02-chapter07.json')
doc=Document(output)
doc.paragraphs[0].style=doc.styles['Title']
doc.save(output)
