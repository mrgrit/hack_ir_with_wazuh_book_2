"""초안 이관 뒤 한 번 적용한 편집 패치. 이후 편집 원본은 manuscript/REV01/*.json이다."""
from pathlib import Path
from copy import deepcopy
import json,re,csv
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'manuscript/REV01'
def p(t):return {'type':'p','text':t}
def sec(t,b):return {'title':t,'kind':'body','level':'section','break':False,'blocks':b}
def save(f,d):f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n','utf8')
def load(n):return json.loads((OUT/f'volume02-{n}.json').read_text('utf8'))

def main():
 ap=load('appendix');refs=load('references')
 # 원전 실습 번호는 저자용 대응표로 옮긴다.
 coverage=deepcopy(ap['sections'][0]['blocks'][1:])
 save(ROOT/'editorial/REV01/slide-coverage.json',coverage)
 ap['sections'][0]['blocks'][1]['head'][2]='조사 기준'
 criteria=['원본·수집·검색 대조','실패 사유·잠금·세션','인증·허가·실제 사용','등록·실행·현재 상태','인자·코드·프로세스 관계','접근 권한·연결·응답','삭제 대상·탐지·조치','영향 조건·적용값·보완','파일·해시·원문 판정','공백 범위·대응 효과','관측 위치·귀속·인계','모집단·연결 근거·오류']
 for row,criterion in zip(ap['sections'][0]['blocks'][1]['rows'],criteria):row[2]=criterion
 ap['sections'][0]['blocks']=ap['sections'][0]['blocks'][:2]
 s=next(s for s in ap['sections'] if s['title']=='I  예제 파일과 재검토')
 s['blocks']=[b for b in s['blocks'] if '검증·촬영' not in b.get('text','')]
 s['title']='I  예제 파일 이용'
 index=ap['sections'].pop() # 전체 입력 색인은 기계 검색 가능한 CSV로 제공한다.
 assert index['title']=='입력 색인'
 f=ROOT/'examples/rev01/input-index.csv'
 with f.open('w',encoding='utf-8-sig',newline='') as stream:
  w=csv.writer(stream);w.writerow(index['blocks'][1]['head']);w.writerows(index['blocks'][1]['rows'])
 # 동일한 문제를 장말 한곳에 모으고 해설은 부록으로 분리한다.
 questions={
  8:['xz 패키지가 설치되어 있는데 CVE 검색은 0건이다. 영향 여부를 판단하려면 어떤 버전·배포판·출처를 대조해야 하는가?',
     '같은 CVE의 등급이 Wazuh와 제조사 공지에서 다르다. 두 평가를 기록할 때 어떤 정보가 필요한가?',
     'SCA의 root 로그인 검사가 Failed이고 적용값은 without-password이다. 허용되는 인증 방식과 검사 기준을 어떻게 구분하는가?',
     '현재 SCA는 Passed인데 지난주의 failed 경보가 검색된다. 보완의 완료 시각을 어떤 자료로 정하는가?',
     '보완 뒤 취약점 목록이 비었다. 작업 종결 전에 어떤 수집 상태와 서비스 결과를 확인해야 하는가?'],
  12:['검색 결과 전체 수와 terms 버킷 건수의 합이 다르다. 어떤 응답 필드를 먼저 읽는가?',
      '서로 다른 agent.name이 세 개이면 침해된 시스템도 세 개인가? 대상 수를 계산하려면 무엇이 필요한가?',
      'IP 피벗에 잡히지 않는 후속 sudo 기록을 시간선에 넣으려면 어떤 연결 근거가 필요한가?'],
  13:['시간상 가까운 bastion 로그인과 web 파일 변경을 같은 사용자에게 귀속하려면 어떤 증거가 필요한가?',
      '판정에 사용한 campaign 정답 라벨로 같은 자료의 성능을 평가하면 어떤 문제가 생기는가?',
      '미확인 연결을 제외하자 위험도 순위가 바뀌었다. 보고서에는 어떤 점수와 가정을 남기는가?']}
 added_answers={12:'전체 수의 relation, timed_out, _shards.failed를 먼저 확인하고 terms의 sum_other_doc_count·doc_count_error_upper_bound를 읽는다. agent.name은 수집 주체이므로 실제 대상은 목적지·서비스·자산 목록과 대조한다. IP 없는 sudo는 같은 호스트의 계정·세션·TTY·로그온 시각 등으로 연결하고 시간만 일치하면 후보로 남긴다.',
 13:'호스트 이동은 원격 접속·프로세스·세션·파일 작성자 등의 연결 증거가 필요하다. 정답 라벨을 입력으로 사용하면 평가 답이 새어 들어가므로 관측 필드로 만든 판정과 별도로 평가한다. 확인된 연결만 사용한 점수와 후보를 포함한 민감도 결과, 산식 버전·기간·제외 근거를 함께 남긴다.'}
 allinputs=[]
 for n in range(1,14):
  stem=f'chapter{n:02}';d=load(stem);qs=[]
  for s in d['sections']:
   s['title']=re.sub(r'실습 \d+(?:의)?\s*(?:—\s*)?','',s['title']).replace('작업 폴더','작업 디렉터리')
   if s['title']=='에이전트가 읽는 채널 확인하기' and n==1:s['title']='1.3  에이전트가 읽는 채널 확인하기';s['level']='section'
   if s['title']=='2.7  핵심 정리':s['title']='2.7  조사 근거 점검'
   if s['title']=='확인 문제':
    qs.extend(b for b in s['blocks'] if not b.get('text','').startswith('다음 장에서는'));s['remove']=True
   else:
    j=next((j for j,b in enumerate(s['blocks']) if b.get('type')=='h' and b.get('text')=='확인 문제'),None)
    if j is not None:qs+=s['blocks'][j+1:];s['blocks']=s['blocks'][:j]
   for b in s['blocks']:
    for k in ['text','why','result','caption','where']:
     if not isinstance(b.get(k),str) or b['type']=='code' or (b['type'] in ('command','query') and k=='text'):continue
     b[k]=b[k].replace('폴더','디렉터리').replace('출발지 주소','출발지 IP').replace('응답 코드','HTTP 상태 코드') if 'HTTP' in b[k] or 'http' in b[k] else b[k].replace('폴더','디렉터리')
    if b['type'] in ('command','query'):allinputs.append((stem,s['title'],b))
  d['sections']=[s for s in d['sections'] if not s.get('remove')]
  # 한 문단에 붙은 다섯 질문을 실제 번호 목록으로 나눈다.
  expanded=[]
  for b in qs:
   if '①' in b.get('text',''):
    expanded += [p(f'{i}. {t.strip()}') for i,t in enumerate(re.split('[①②③④⑤⑥⑦]',b['text'])[1:],1)]
   else:expanded.append(b)
  if n in questions:expanded=[p(f'{i}. {t}') for i,t in enumerate(questions[n],1)]
  assert expanded,(n,'문제 없음')
  pos=next(i for i,s in enumerate(d['sections']) if s['title']=='스스로 조사하기')
  d['sections'].insert(pos,sec('확인 문제',expanded))
  # 편집 메모와 첫 페이지 역할을 분리한다.
  if n==1:
   intro=next(s for s in d['sections'] if s['title']=='머리말')
   intro_images=[b for b in intro['blocks'] if b['type']=='image']
   intro['blocks']=[p('경보는 조사할 대상을 가리킨다. 침해 판단에는 실행 결과와 영향의 증거가 더 필요하다. 이 책은 Windows 원본에서 Wazuh 검색으로 이동하고, 다시 원본으로 돌아가 그 차이를 설명하는 방법을 다룬다.'),
     p('조사자는 입력·응답·수집·규칙·대응을 한 줄의 성공 여부로 줄이지 않는다. 무엇이 일어났고 어느 구간이 보이지 않는지 알아야 다음 수집과 대응을 선택할 수 있기 때문이다. 독자는 매 장에서 먼저 결과를 예측하고, 관찰한 값으로 예측을 고친 뒤 다른 설명이 가능한지 확인한다.'),
     p('Windows 인증과 지속화, 프로세스와 통신, 보호 기능과 파일 판정을 차례로 읽는다. 이어 수집 장애와 자동 대응, 네트워크 관제, 장기 집계와 위험도 평가로 조사 범위를 넓힌다. 마지막에는 서로 다른 기록을 무리하게 합치지 않고 근거 수준을 구분한 조사 보고서를 완성한다.')]
   intro['blocks']+=intro_images
  save(OUT/f'volume02-{stem}.json',d)
 for n,a in added_answers.items():ap['sections'].append(sec(f'{n}장 확인 문제 해설',[p(a)]))
 # 읽기 전용 오프라인 예제. 시스템 접근이나 Wazuh 적재를 하지 않는다.
 new=[
 {'type':'command','id':'CA-01','where':'Windows PC · PowerShell · 내려받은 저장소 루트',
  'text':"Test-Path .\\examples\\rev01\\records\\manifest.json\n$manifest = Get-Content `\n  .\\examples\\rev01\\records\\manifest.json `\n  -Raw -Encoding UTF8 | ConvertFrom-Json\n$manifest.files | Format-Table file,returned",
  'purpose':'로컬 보존 자료의 위치와 포함 범위를 확인한다.',
  'syntax':'Test-Path는 경로 존재 여부를 반환한다. 점과 역슬래시(.\\)는 현재 디렉터리다. Get-Content의 -Raw는 파일 전체를 한 문자열로 읽고 -Encoding UTF8은 문자 인코딩을 지정한다. 파이프(|)로 문자열을 ConvertFrom-Json에 전달해 속성으로 읽을 수 있는 객체로 바꾼다. 백틱(`)은 다음 줄로 명령을 잇는다. $manifest는 읽은 값을 보관하는 변수다.',
  'why':'보존 파일 목록을 읽는다.','result':'첫 줄 True를 확인한다. False이면 탐색기에서 저장소 루트를 연 뒤 그 위치에서 PowerShell을 다시 연다. returned가 없는 집계 파일은 검색 응답 전체이므로 사례 문서 수와 비교하지 않는다.'},
 {'type':'command','id':'CA-02','where':'Windows PC · PowerShell · 같은 저장소 루트',
  'text':"Get-FileHash .\\examples\\rev01\\records\\chapter01.json `\n  -Algorithm SHA256 | Format-List\n$manifest.files | Where-Object file -eq 'chapter01.json' |\n  Format-List file,sha256",
  'purpose':'내려받은 1장 자료가 제공된 해시와 같은지 확인한다.',
  'syntax':'Get-FileHash는 파일 내용의 해시를 계산한다. -Algorithm SHA256으로 방식을 지정한다. Where-Object는 file 속성이 작은따옴표 안 이름과 같은(-eq) 항목을 고른다. 해시의 영문 대소문자는 비교 결과에 영향을 주지 않는다.',
  'why':'SHA-256 대조.','result':'두 해시가 같으면 같은 파일 내용을 읽은 것이다. 사건의 사실성이나 수집 완전성을 해시만으로 평가하지 않는다. 다르면 파일을 실행하거나 내용을 임의 보충하지 말고 내려받은 버전과 manifest를 함께 확인한다.'},
 {'type':'command','id':'CA-03','where':'Windows PC · PowerShell · 같은 저장소 루트',
  'text':"$bundle = Get-Content `\n  .\\examples\\rev01\\records\\chapter01.json `\n  -Raw -Encoding UTF8 | ConvertFrom-Json\n$case = $bundle.cases |\n  Where-Object case -eq 'original-alert-fields'\n$case.records | ForEach-Object {\n  $_.rule | Format-List\n  $_.data.win.system | Format-List\n  $_.data.win.eventdata | Format-List\n}",
  'purpose':'1장의 규칙 제목과 원본 필드를 직접 대조한다.',
  'syntax':'cases와 records는 파일 안 배열이다. ForEach-Object는 배열의 각 객체를 중괄호({ }) 안에서 처리한다. $_는 현재 객체이며 점(.)으로 그 속성에 접근한다. Format-List는 속성을 세로로 펼친다.',
  'why':'1장의 저장 필드를 읽는다.','result':'RecordID 9115의 규칙 60200, logonType 8, processName의 sshd.exe를 찾는다. system.processID와 eventdata.processId도 구분한다.'},
 {'type':'command','id':'CA-04','where':'Windows PC · PowerShell · 같은 저장소 루트',
  'text':"$bundle = Get-Content `\n  .\\examples\\rev01\\records\\chapter06.json `\n  -Raw -Encoding UTF8 | ConvertFrom-Json\n$bundle.cases | Where-Object {\n  $_.case -like 'ch06-original-*'\n} | Select-Object case,total,returned\n$case = $bundle.cases |\n  Where-Object case -eq 'ch06-original-archives'\n$case.records | ForEach-Object {\n  $_.system | Format-List\n  $_.eventdata | Format-List\n}",
  'purpose':'같은 여섯 원본의 archives 수집과 alerts 경보 결과를 비교한다.',
  'syntax':'-like는 패턴 비교이며 별표(*)는 뒤의 임의 문자열과 일치한다. Select-Object는 표시할 속성을 고른다. 이 발췌본은 원래 data.win.system·eventdata를 system·eventdata로 저장했다. 1장의 original-alert-fields 구조와 구분한다.',
  'why':'6장의 여섯 원본을 읽는다.','result':'archives의 total.value와 returned는 6, alerts는 0이다. 원본 번호 9407·9451·9454·9455·9461·9462를 대조한다. 조회 조건은 각 case의 query에서 확인한다. 전체 챕터 파일의 배열 길이를 이 검색의 건수로 세지 않는다.'}]
 ap['sections'].insert(15,sec('J  보존 기록을 로컬에서 읽기',[p('Windows PC에 저장소 전체를 내려받는다. 탐색기에서 examples와 manuscript가 함께 있는 최상위 디렉터리를 연 뒤 주소 표시줄에 powershell을 입력하여 그 위치의 PowerShell을 연다. 아래 명령은 로컬 JSON 파일만 조회한다. 다른 장을 읽을 때는 chapterNN.json과 cases 목록을 먼저 확인한다.')]+new+[p('조회만 했다면 원상복구할 설정은 없다. PowerShell 창을 닫아 임시 변수를 정리하고 작성한 조사 메모는 보존한다. 전체 입력 색인은 examples/rev01/input-index.csv에서 검색한다.')]))
 for b in new:allinputs.append(('appendix','J  보존 기록을 로컬에서 읽기',b))
 # 역할·용법·첫 사용을 찾는 짧은 사전. 문법 해설은 본문에 남긴다.
 glossary=[]
 for term,role in [('Get-WinEvent','Windows 채널의 원본 이벤트를 조회한다.'),('Get-Content','텍스트 파일의 내용을 읽는다.'),('Get-FileHash','분석 사본의 내용 동일성을 확인한다.'),('auditpol','감사 정책과 하위 범주를 조회한다.'),('docker exec','지정 컨테이너의 대화형 셸을 연다.'),('grep','원본 파일에서 식에 맞는 줄을 찾는다.'),('sed','선택한 줄·구간을 출력한다.'),('awk','필드와 조건에 따라 텍스트를 처리한다.'),('less','파일을 화면 단위로 읽고 검색한다.'),('osqueryi','현재 운영체제 정보를 SQL로 조회한다.'),('certutil','인코딩된 파일과 복원 결과를 비교한다.'),('pgrep','실행 중인 프로세스를 조건으로 찾는다.'),('exit','현재 셸을 종료하고 이전 실행 위치로 돌아간다.')]:
  hit=next(((stem,b) for stem,_,b in allinputs if term in b['text']),None)
  if hit:glossary.append([term,role,hit[1]['id']])
 ap['sections'].insert(16,sec('K  자주 쓰는 도구 찾기',[p('같은 도구를 다시 사용할 때는 아래 입력 번호에서 역할과 기본 구문을 찾는다. 각 장에 새로 등장하는 옵션·정규표현식·실행 위치는 해당 입력에서 확인한다.'),{'type':'table','head':['도구','이 책에서의 역할','첫 입력'],'rows':glossary,'widths':[32,71,24]}]))
 save(OUT/'volume02-appendix.json',ap)
 # 복사용 입력과 원고를 한 원본으로 맞춘다. 이전 부가 예제는 그대로 보존한다.
 grouped={}
 for stem,title,b in allinputs:
  ext='.dql' if b['id'].startswith('Q') else '.http' if b['id'].startswith('D') else '.txt'
  out=ROOT/'examples/rev01'/stem;out.mkdir(exist_ok=True,parents=True)
  (out/(b['id']+ext)).write_text(b['text']+'\n','utf8')
  grouped.setdefault(stem,[]).append({'id':b['id'],'file':b['id']+ext,'where':b['where'],'section':title,'input':b['text']})
 # 원래 부록 검색 입력도 보존한다.
 for s in ap['sections']:
  for b in s['blocks']:
   if b['type'] in ('command','query') and b['id'].startswith('QA-'):
    grouped['appendix'].append({'id':b['id'],'file':b['id']+'.dql','where':b['where'],'section':s['title'],'input':b['text']})
 for stem,rows in grouped.items():save(ROOT/'examples/rev01'/stem/'manifest.json',rows)

if __name__=='__main__':main()
