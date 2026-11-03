from pathlib import Path
from figures import *
from layout import build
from docx import Document
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/figures/chapter09';OUT.mkdir(parents=True,exist_ok=True)

im,d=canvas(760)
for x,title,sub,fill in [(25,'호스트 상태','Rootcheck',BLUE),(445,'파일 변화','FIM',CREAM),(865,'파일 내용','ClamAV',RUST)]:
 box(d,(x,20,x+390,180),title,sub,fill,size=38)
arrow(d,(220,195),(220,440));arrow(d,(640,195),(640,245));arrow(d,(1060,195),(1060,440))
box(d,(425,260,855,420),'외부 해시 조회','VirusTotal',CREAM,size=36)
arrow(d,(640,435),(640,475))
box(d,(25,490,1255,665),'Wazuh 경보에서 연결','호스트 · 경로 · 해시 · 시각',BLUE,size=42)
d.text((155,700),'권한 이상 · 파일 탐지 · 실제 실행을 구분하여 조사',font=font(34),fill=INK)
im.save(OUT/'three-paths.png')

im,d=canvas(960)
for i,(title,sub,c) in enumerate([
 ('web의 FIM 경보','path · md5_after · id',BLUE),
 ('관리자 서버의 연동','해시로 기존 보고서 조회',CREAM),
 ('VirusTotal 응답','등록 여부 · 탐지 수 · 분석 시각',RUST),
 ('Wazuh의 별도 경보','source.file · source.md5 · source.alert_id',BLUE)]):
 y=15+i*240;box(d,(40,y,1240,y+170),title,sub,c,size=39)
 if i<3:arrow(d,(640,y+185),(640,y+230))
im.save(OUT/'vt-flow.png')

im,d=canvas(700)
for i,(title,sub,c) in enumerate([
 ('web의 감시 프로그램','clamdscan으로 clamd에 검사 요청',BLUE),
 ('새로운 FOUND 출력 줄','kt66-seen으로 중복 확인',CREAM),
 ('전용 수집 로그','/var/log/kt66-clamav.log',RUST),
 ('Wazuh 에이전트와 관리자','localfile · clamd 디코더 · 52502',BLUE)]):
 y=15+i*170;box(d,(40,y,1240,y+125),title,sub,c,size=39)
 if i<3:arrow(d,(640,y+137),(640,y+160))
im.save(OUT/'clam-flow.png')
output=ROOT/'manuscript/volume02-chapter09.docx'
build(output,ROOT/'manuscript/volume02-chapter09.json')
doc=Document(output);doc.paragraphs[0].style=doc.styles['Title'];doc.save(output)
