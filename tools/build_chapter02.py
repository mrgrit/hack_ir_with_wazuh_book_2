"""2장의 개념 도식과 편집용 DOCX를 만든다."""
from pathlib import Path
from figures import *
from layout import build
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/figures/chapter02';OUT.mkdir(parents=True,exist_ok=True)
im,d=canvas(570)
for r,title,sub,color in [((25,20,600,205),'1 실패 사유','4625 · 계정과 상태 코드',BLUE),((680,20,1255,205),'2 계정 잠금','4740 · 현재 Lockout',CREAM),((680,350,1255,535),'3 원격 로그온','4624 · 유형 10',RUST),((25,350,600,535),'4 조사와 원상복구','승인 여부 · 세션 · 파일',BLUE)]:box(d,r,title,sub,color)
arrow(d,(610,115),(670,115));arrow(d,(970,220),(970,335));arrow(d,(670,445),(610,445));im.save(OUT/'sequence.png')
im,d=canvas(550)
box(d,(25,20,580,215),'kt66-attacker','10.20.30.202 · RDP 입력',BLUE)
box(d,(700,20,1255,215),'Windows 게스트','접속 경로 10.20.70.10',CREAM)
arrow(d,(590,120),(690,120));arrow(d,(970,230),(970,320))
box(d,(700,330,1255,515),'Security 이벤트','계정 · 유형 · 원본 주소',CREAM)
box(d,(25,330,580,515),'Wazuh 경보','agent.name = windows-user',RUST)
arrow(d,(690,425),(590,425));im.save(OUT/'path.png')
im,d=canvas(610)
box(d,(25,20,590,200),'암호 오류 누적','4625 · 0xc000006a',BLUE)
box(d,(690,20,1255,200),'임계값 도달','Lockout True · 4740',RUST)
arrow(d,(600,110),(680,110));arrow(d,(970,215),(970,355))
box(d,(690,370,1255,560),'잠금 기간 경과','Lockout False 확인',CREAM)
box(d,(25,370,590,560),'이후 정상 자격증명','4624 · 유형과 주소 확인',BLUE)
arrow(d,(680,465),(600,465));d.text((40,250),'잠금 발생과 잠긴 계정의 추가 접속 실패는 별개의 기록이다',font=font(34),fill=INK);im.save(OUT/'lockout.png')
im,d=canvas(710)
for i,(title,sub,color) in enumerate([('1 관찰 확정','원본 기록 · 계정 · 시각 · 주소',BLUE),('2 원인과 승인 확인','사용자 · 장비 · 업무 · 후속 활동',CREAM),('3 대응 결과 확인','접속 제한 · 계정 복구 · 정상 업무',RUST)]):
 y=20+i*230;box(d,(125,y,1155,y+180),title,sub,color)
 if i<2:arrow(d,(640,y+192),(640,y+218))
im.save(OUT/'decision.png')
build(ROOT/'manuscript/volume02-chapter02.docx',ROOT/'manuscript/volume02-chapter02.json')
