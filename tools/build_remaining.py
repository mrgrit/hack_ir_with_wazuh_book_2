"""2권 10~13장·부록: 관계 도식과 DOCX. 기존 장은 변경하지 않는다."""
from pathlib import Path
from figures import *
from layout import build
from docx import Document
ROOT=Path(__file__).resolve().parents[1]
def vertical(ch,name,rows):
 out=ROOT/'assets/figures'/ch;out.mkdir(parents=True,exist_ok=True)
 im,d=canvas(len(rows)*180)
 for i,(title,sub) in enumerate(rows):
  y=i*180+12;box(d,(35,y,1230,y+125),title,sub,[BLUE,CREAM,RUST][i%3],size=38)
  if i<len(rows)-1:arrow(d,(640,y+139),(640,y+170))
 im.save(out/(name+'.png'))
vertical('chapter10','collection',[
 ('에이전트의 연결','keepalive · Active / Disconnected'),
 ('대상 로그의 수집','프로세스 · 파일 · 읽기 권한'),
 ('관리자와 인덱서의 처리','디코더 · 규칙 · 저장 · 오류'),
 ('대시보드의 최근 이벤트','데이터 보기 · 기간 · 필터')])
vertical('chapter10','response',[
 ('원인 경보','5712 · 5763 / 경보 id'),
 ('대상 에이전트의 실행 요청','firewall-drop / add'),
 ('실제 방화벽과 통신 결과','대상 IP · 규칙 · 서비스 영향'),
 ('해제 요청과 복구 확인','delete · 규칙 소멸 · 정상 경로')])
vertical('chapter11','sensors',[
 ('네트워크 관측','패킷 · 요청 · Suricata EVE'),
 ('Wazuh 에이전트 수집','ips의 eve.json / JSON'),
 ('관리자 경보와 호스트 기록 대조','시각 · 주소 · 포트 · URL'),
 ('실제 영향 조사','인증 · 프로세스 · 파일 · 데이터')])
vertical('chapter11','daily',[
 ('검토 범위와 수집 상태','기간 · 시간대 · 공백'),
 ('고위험 후보와 전후 기록','원인 · 낮은 레벨 · 상태 점검'),
 ('담당자와 다음 행동','증거 · 영향 · 기한'),
 ('재확인과 마감','조치 결과 · 지연 경보 · 원상복구')])
vertical('chapter12','pivot',[
 ('조사 범위 고정','합성 표시 · 기간 · 시간대'),
 ('IP에서 계정·호스트로 피벗','원문 식별자 · IP 없는 기록 보존'),
 ('같은 모집단의 집계','문서 · 날짜 · 규칙 · 분모'),
 ('비교표와 원문 대조','누락 · 중복 · 미귀속 · 다음 조사')])
vertical('chapter13','linking',[
 ('직접 주소가 있는 이벤트','IP · 계정 · 호스트 · 시각'),
 ('같은 호스트·계정의 후보','세션 · PID · TTY로 연결 검토'),
 ('다른 호스트의 후속 기록','이동 증거가 없으면 미귀속'),
 ('근거 수준을 보존한 시간선','직접 · 연결 · 후보 · 미귀속')])
out=ROOT/'assets/figures/chapter13';out.mkdir(parents=True,exist_ok=True)
im,d=canvas(510)
box(d,(30,25,1250,140),'보고 대상: 8월 13일 하루','KST 00:00부터 24개 시간 버킷',BLUE,38)
box(d,(30,230,885,380),'앞 23시간','8월 12일 01:00~23:00',CREAM,38)
box(d,(920,230,1250,380),'현재 시간','13일 00:00',RUST,34)
d.line((40,420,1240,420),fill=INK,width=4)
d.text((275,450),'첫 보고 버킷의 24시간 이동 합',font=font(36,True),fill=INK)
im.save(out/'window.png')
vertical('appendix','check-path',[
 ('원본과 생성 정책','컴퓨터 · 채널 · 감사 · 필터'),
 ('에이전트','읽기 · 연결 · 설정 · 오류'),
 ('관리자','디코더 · 규칙 · 저장 기준'),
 ('인덱서와 화면','적재 · 보존 · 기간 · 필터')])
for stem in ['chapter10','chapter11','chapter12','chapter13','appendix']:
 path=ROOT/f'manuscript/volume02-{stem}.docx'
 build(path,ROOT/f'manuscript/volume02-{stem}.json')
 doc=Document(path);doc.paragraphs[0].style=doc.styles['Title'];doc.save(path)
