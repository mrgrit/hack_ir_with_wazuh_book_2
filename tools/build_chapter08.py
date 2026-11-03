from pathlib import Path
from figures import *
from layout import build
from docx import Document
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/figures/chapter08';OUT.mkdir(parents=True,exist_ok=True)

im,d=canvas(810)
box(d,(25,20,605,185),'호스트의 설치 정보','Syscollector · OS · 패키지',BLUE,size=36)
box(d,(675,20,1255,185),'취약점 자료','Wazuh CTI · 제조사 정보',CREAM,size=36)
arrow(d,(315,200),(450,280));arrow(d,(965,200),(830,280))
box(d,(185,295,1095,460),'관리자 서버에서 대조','제품 · 버전 · 영향 범위',RUST,size=38)
arrow(d,(640,475),(640,540))
box(d,(185,555,1095,720),'Inventory 현재 상태','wazuh-states-vulnerabilities-*',BLUE,size=38)
d.text((200,760),'경보 이력은 생성 조건과 보존 기간을 별도로 확인',font=font(32),fill=INK)
im.save(OUT/'vulnerability-flow.png')

im,d=canvas(1000)
for i,(title,sub,c) in enumerate([
 ('검색 조건','화면 · 필드 · 고정 에이전트 · 필터',BLUE),
 ('설치 정보 수집','연결 · 수집 시각 · 실제 버전 대조',CREAM),
 ('대조와 저장','CTI 갱신 · 기능 활성화 · 인덱서 연결',RUST),
 ('근거에 맞게 기록','영향 없음 · 평가 불가 · 추가 확인',BLUE)]):
 y=20+i*250;box(d,(45,y,1235,y+175),title,sub,c,size=39)
 if i<3:arrow(d,(640,y+190),(640,y+240))
im.save(OUT/'missing-results.png')

im,d=canvas(670)
box(d,(185,20,1095,185),'에이전트의 SCA 정책 검사','파일 · 명령 출력 · 레지스트리',BLUE,size=38)
arrow(d,(450,200),(325,300));arrow(d,(830,200),(955,300))
box(d,(25,320,605,525),'현재 상태','정책 · 체크 ID · 결과',CREAM,size=38)
box(d,(675,320,1255,525),'경보 이력','상태 변화 · 시각 · 보존',RUST,size=38)
d.text((105,585),'동일 에이전트 · 정책 · 체크 ID로 연결하고 시각을 대조',font=font(34),fill=INK)
im.save(OUT/'sca-state.png')

output=ROOT/'manuscript/volume02-chapter08.docx'
build(output,ROOT/'manuscript/volume02-chapter08.json')
doc=Document(output);doc.paragraphs[0].style=doc.styles['Title'];doc.save(output)
