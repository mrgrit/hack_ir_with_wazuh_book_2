"""10~13장과 부록의 읽기 요청·빈 양식·가정값 계산 연습을 저장한다."""
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
import json,csv
ROOT=Path(__file__).resolve().parents[1]
def write(rel,text):
 p=ROOT/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.rstrip()+'\n',encoding='utf8')
def csvout(rel,fields,rows):
 with (ROOT/rel).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def joined(ch,ids,name):
 m=json.loads((ROOT/f'examples/chapter{ch}/manifest.json').read_text('utf8'))
 text='\n'.join(next(r['input'] for r in m if r['id']==i) for i in ids)
 json.loads(text.split('\n',1)[1]);write(f'examples/chapter{ch}/{name}',text)
joined(12,['D12-03','D12-04'],'ip-profile.http')
joined(13,['D13-01','D13-02'],'hourly-risk.http')
fields=['ip','start_inclusive','end_exclusive','time_zone','index','documents','level_ge5_documents','sensor_count','target_system_count','rule_types_ge5','active_days','interval_mean_s','interval_median_s','interval_std_s','max_level','fw_drop','ips_allowed','ips_blocked','web_403_candidate','web_200_candidate','offhour_ratio','holiday_ratio','reputation','burstiness','missing_fields','evidence_ids','next_action']
csvout('examples/chapter12/ip-profile-worksheet.csv',fields,[{'ip':i,'time_zone':'Asia/Seoul'} for i in ['185.220.158.180','162.142.241.68','','','']])
sf=['case','stage','max_level','rule_types_ge5','fw_drop','ips_blocked','web_403_candidate','ips_allowed','web_200_candidate','documents','offhour_ratio','holiday_ratio','reputation','burstiness','target_systems','active_days']
rows=[
 ['A','auth',10,4,80,0,0,1,0,100,.8,.4,80,.7,2,9],
 ['B','none',5,1,0,0,0,0,0,20,.1,0,0,.1,1,2],
 ['C','evasion',15,15,50,50,50,1,1,100,.8,.4,100,.7,3,20],
 ['D','recon',7,2,100,0,0,0,0,9,.9,.9,50,.6,1,2],
 ['E','access',8,3,0,0,0,0,1,10,.6,.3,20,.5,3,20]]
stages={'none':0,'recon':4,'exploit':10,'auth':14,'access':30,'privesc':38,'persist':46,'c2':54,'evasion':60}
worked=[]
for vals in rows:
 r=dict(zip(sf,vals));n=r['max_level']
 pts={'stage_points':stages[r['stage']],'level_points':8 if n>=12 else 5 if n>=10 else 3 if n>=7 else 0,'type_points':min(r['rule_types_ge5'],10),'block_points':sum(3 for f in ('fw_drop','ips_blocked','web_403_candidate') if r[f]>=50),'allowed_points':(3 if r['ips_allowed'] else 0)+(6 if r['web_200_candidate'] else 0),'offhour_points':5 if r['documents']>=10 and r['offhour_ratio']>.6 else 0,'holiday_points':3 if r['documents']>=10 and r['holiday_ratio']>.3 else 0,'reputation_points':r['reputation']/10,'burst_points':3 if r['burstiness']>.5 else 0,'system_points':3 if r['target_systems']>=3 else 0,'days_points':3 if r['active_days']>=20 else 0}
 total=sum(pts.values());worked.append({**r,**pts,'raw_total':total,'score':min(100,total),'provenance':'constructed arithmetic fixture; not observed IP'})
assert [r['score'] for r in worked]==[48,1,100,20,50]
csvout('examples/chapter13/score-worked.csv',list(worked[0]),worked)
csvout('examples/chapter13/ip-score-worksheet.csv',sf+['evidence_ids','confirmed_lower','candidate_upper','unknown_fields','next_action'],[{'case':str(i)} for i in range(1,6)])
weights=[]
for rule,level,foreign,rep,off,follow in [(31106,12,1,69,1,.60),(4151,10,1,69,.80,.60),(86601,6,.83,68,.83,.67),(5716,5,1,66,1,.50)]:
 v=Decimal('.45')*Decimal(str(follow))+Decimal('.25')*Decimal(level)/15+Decimal('.10')*Decimal(str(foreign))+Decimal('.10')*Decimal(rep)/100+Decimal('.10')*Decimal(str(off))
 weights.append({'rule':rule,'level':level,'foreign_ratio':foreign,'reputation':rep,'offhour_ratio':off,'followup_ratio':follow,'weight':str(v),'rounded':str(v.quantize(Decimal('.01'),rounding=ROUND_HALF_UP)),'source':'printed source inputs; not current rule settings'})
assert [r['rounded'] for r in weights]==['0.74','0.69','0.64','0.57']
csvout('examples/chapter13/rule-weight-worked.csv',list(weights[0]),weights)
hours=[]
for hour in range(48):
 risk=150 if hour==23 else 25 if hour==24 else 0
 hours.append({'hour_offset':hour,'risk':risk,'risk_24h':sum(r['risk'] for r in hours[max(0,hour-23):])+risk,'window_complete':hour>=23,'provenance':'constructed fixture, empty hours included'})
assert [hours[i]['risk_24h'] for i in (23,24,46,47)]==[150,175,175,25]
csvout('examples/chapter13/hourly-worked.csv',list(hours[0]),hours)
template='''# 조사 기록

- 시작 포함·끝 제외 시각 / 시간대 / 인덱스:
- 대상 호스트·계정·실행 위치 / 수집·보호 상태:
- 입력 / 응답 코드·본문·상태:
- 원본 컴퓨터·채널·EventID·RecordID 또는 파일·시각:
- Wazuh agent / rule / id / _index / _id:
- 연결 근거: 직접·세션 연결·후보·미귀속, IP·PID·GUID·TTY:
- 확인된 사실과 실제 영향:
- 미확인 가설·반증 자료·수집 공백:
- 조치 담당자·승인 범위·기한·영향:
- 재조회·서비스·보호 상태·원상복구:
'''
write('examples/appendix/investigation-template.md',template)
extra={10:'Linux 컨테이너는 본문 순서대로 진입하고 exit로 나온다. 조회만 하며 중지·차단 명령은 제공하지 않는다.',11:'현재 Suricata 검색 0건과 원전 결과 화면을 구분한다. 일일 검색 저장은 알림 예약이 아니다.',12:'ip-profile.http는 D12-03·04를 합친 GET 요청이다. CSV는 빈 조사 양식이다. C12-02 파일 생성은 선택 절차이며 저자는 실행하지 않았다. 데이터가 없으면 강사에게 준비 범위를 확인한다.',13:'hourly-risk.http는 D13-01·02를 합친 GET 요청이다. score-worked.csv의 A~E 및 hourly-worked.csv는 산식 확인용 가정값이다. 실제 IP·탐지 성능 측정값이 아니다. 빈 값은 미확인이며 0과 구분한다. rule-weight-worked.csv는 원전 인쇄 입력값의 재계산이다.'}
for ch in range(10,14):
 dest=ROOT/f'examples/chapter{ch}';m=json.loads((dest/'manifest.json').read_text('utf8'))
 write(f'examples/chapter{ch}/README.md',f'# {ch}장 복사용 입력\n\n본문의 실행 위치·선행 조건을 읽고 한 블록씩 입력한다. 예시 주소·계정·시각·ID는 자신의 기록으로 바꾼다. 전체 파일을 일괄 실행하지 않는다.\n\n{extra[ch]}\n\n'+'\n'.join(f"- [{r['file']}]({r['file']}) — {r['where']}" for r in m))
 write(f'examples/chapter{ch}/observation-template.md',template)
write('examples/appendix/README.md','# 부록 복사용 입력\n\nQA-01~04는 Wazuh Discover의 DQL이다. investigation-template.md는 조사 기록 양식이다. 예시 주소·기간·계정은 자신의 원문에서 확인한다.')
print('complete requests 2; profile/score worksheets 2; arithmetic fixtures 3; investigation templates and READMEs saved')
