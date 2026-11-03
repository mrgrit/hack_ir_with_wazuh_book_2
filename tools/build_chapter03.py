"""3장의 관계 도식과 챕터별 DOCX를 만든다."""
from pathlib import Path
from figures import *
from layout import build
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/figures/chapter03';OUT.mkdir(parents=True,exist_ok=True)
im,d=canvas(650)
for i,(a,b,c) in enumerate([('인증','누가 어떤 자격증명을 제시했는가',BLUE),('권한','어떤 자원·그룹에 접근했는가',CREAM),('감사','어떤 기록 설정이 달라졌는가',RUST)]):
 y=20+i*210;box(d,(85,y,1195,y+170),a,b,c)
 if i<2:arrow(d,(640,y+181),(640,y+201))
im.save(OUT/'questions.png')
im,d=canvas(520)
box(d,(25,20,1255,190),'유형 9 · NewCredentials','현재 로컬 문맥을 바탕으로 새 로그온 세션',CREAM)
arrow(d,(330,202),(330,300));arrow(d,(950,202),(950,300))
box(d,(25,315,615,490),'로컬 대상 계정','kt66student',BLUE)
box(d,(665,315,1255,490),'외부 인증용 이름','CORP / fakeadmin',RUST)
im.save(OUT/'credentials.png')
im,d=canvas(650)
for i,(a,b,c) in enumerate([('4648 · 자격증명 제시','kt66student가 victim 자격증명 사용',BLUE),('4624 · 인증 성공','victim · 유형 3 · NTLM',CREAM),('공유 권한 검사','C$ 접근 거부 · 오류 5',RUST)]):
 y=20+i*210;box(d,(85,y,1195,y+170),a,b,c)
 if i<2:arrow(d,(640,y+181),(640,y+201))
im.save(OUT/'access.png')
im,d=canvas(680)
box(d,(25,20,600,210),'4720 · 계정 생성','targetSid = 새 계정 SID',BLUE)
box(d,(680,20,1255,210),'4732 · 그룹에 추가','memberSid = 같은 계정 SID',CREAM)
arrow(d,(610,115),(670,115))
box(d,(680,390,1255,640),'변경된 로컬 그룹','targetSid = S-1-5-32-544',RUST)
arrow(d,(970,225),(970,375))
box(d,(25,390,600,640),'변경 수행자','subjectUserName / LogonId',BLUE)
arrow(d,(610,515),(670,515))
d.text((40,280),'구성원 SID · 그룹 SID · 수행자 세션을 구분한다',font=font(38),fill=INK)
im.save(OUT/'membership.png')
build(ROOT/'manuscript/volume02-chapter03.docx',ROOT/'manuscript/volume02-chapter03.json')
