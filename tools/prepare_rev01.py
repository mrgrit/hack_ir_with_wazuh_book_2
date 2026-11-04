"""초안의 독립 사본을 순서대로 교정한다. REV01 JSON이 출판 편집 원본이다."""
from pathlib import Path
from copy import deepcopy
import json,re,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'manuscript/REV01'
def p(text):return {'type':'p','text':text}
def box(kind,text,title=None):
 b={'type':'box','kind':kind,'text':text}
 if title:b['title']=title
 return b
def sec(title,blocks,level='section',br=False):return {'title':title,'kind':'body','level':level,'break':br,'blocks':blocks}
def allblocks(d):return [b for s in d['pages'] for b in s['blocks']]
def replace(d,old,new):
 found=0
 for b in allblocks(d):
  for k in ['text','why','result','caption','where']:
   if isinstance(b.get(k),str) and old in b[k]:b[k]=b[k].replace(old,new);found+=1
 if not found:raise ValueError('교정 대상 없음: '+old)
def main():
 cfg=json.loads((ROOT/'tools/rev01_changes.json').read_text('utf8'))
 bibliography=[];refidx={};changes=[];answers=[];assets={}
 for n in list(range(1,14))+['appendix']:
  stem=f'chapter{n:02}' if isinstance(n,int) else n
  src=ROOT/f'build/REV01/baseline/volume02-{stem}.json'
  if not src.exists():src=ROOT/f'manuscript/volume02-{stem}.json'
  baseline=json.loads((ROOT/'editorial/REV01/source-baseline.json').read_text('utf8'))
  expected=next(x['sha256'] for x in baseline if x['path']==f'manuscript/volume02-{stem}.json')
  if hashlib.sha256(src.read_bytes()).hexdigest()!=expected:raise ValueError('이관 기준 원고가 바뀜: '+str(src))
  d=json.loads(src.read_text('utf8'));original=deepcopy(d);c=cfg.get(stem,{})
  # 제작 이력은 저자 기록에 보존하고 본문에서는 관찰값의 성격을 구체화한다.
  for old,new in c.get('replace',[]):replace(d,old,new)
  for edit in c.get('blocks',[]):
   s=d['pages'][edit['page']]
   if 'set' in edit:s['blocks'][edit['block']]=edit['set']
   elif 'insert' in edit:s['blocks'].insert(edit['block'],edit['insert'])
  for edit in c.get('inputs',[]):
   b=next(b for b in allblocks(d) if b.get('id')==edit['id']);b.update({k:v for k,v in edit.items() if k!='id'})
  for i in c.get('remove_pages',[]):
   if '해설' in d['pages'][i]['title']:answers.append(sec(str(n)+'장 확인 문제 해설',d['pages'][i]['blocks']))
   d['pages'][i]['omit']=True
  refs=[];sections=[]
  for i,s in enumerate(d['pages']):
   if s.get('omit'):continue
   if s['title'].startswith('참고자료'):
    for b in s['blocks']:
     if b['type']!='link':continue
     u=b['url']
     if u not in refidx:
      refidx[u]=f'R{len(bibliography)+1:03}';bibliography.append({'type':'link','text':refidx[u]+'  '+b['text'],'url':u})
     refs.append((refidx[u],b))
    continue
   if s['kind']=='cover':
    s['blocks']=[b for b in s['blocks'] if b.get('text')!='챕터별 교정용 초안']
   s['break']=s['kind']=='cover' or (n==1 and i in (1,2))
   # 절 번호는 본래 절의 첫 제목에만 둔다. 이어지는 소주제는 하위 제목으로 조판한다.
   numbered=re.match(r'^\d+\.\d+\s+',s['title'])
   s['level']='section' if numbered or s['kind']=='cover' or i==0 else 'subsection'
   s['title']=re.sub(r'실습 \d+(?:[·~]\d+)?\s*·\s*','',s['title'])
   if s['title'].endswith('장 마무리'):s['title']=re.sub('장 마무리$','핵심 정리',s['title'])
   if s['title'] in ('확인 문제와 해설','점검 문제','확인 문제와 조사 기록','확인 문제와 판단 근거'):
    s['title']='확인 문제'
   if n==8 and i==31:
    answers.append(sec('8장 확인 문제 해설',s['blocks'][1::2]));s['blocks']=s['blocks'][::2]
   if n in (6,7) and s['title']=='확인 문제':
    questions=[];original_answers=[]
    for b in s['blocks']:
     if re.match(r'^\d+\.',b.get('text','')):
      txt=b['text'];cut=txt.find('인가.')+3 if '인가.' in txt else -1
      if cut<3:cut=txt.find('것인가.')+4 if '것인가.' in txt else -1
      if cut<3:cut=txt.find('는가.')+3 if '는가.' in txt else -1
      if cut>=3:questions.append(p(txt[:cut].rstrip('.').rstrip()+'?'));original_answers.append(p(txt))
      else:questions.append(b)
    answers.append(sec(str(n)+'장 확인 문제 해설',original_answers));s['blocks']=questions
   embedded=next((j for j,b in enumerate(s['blocks']) if b.get('type')=='h' and b.get('text')=='확인 문제와 해설'),None)
   if embedded is not None:
    old=s['blocks'][embedded+1:];ans=[];qs=[]
    for b in old:
     if '?' in b.get('text',''):
      q,a=b['text'].split('?',1);qs.append(p(q+'?'));ans.append(p(a.strip()))
    answers.append(sec(str(n)+'장 확인 문제 해설',ans))
    s['blocks']=s['blocks'][:embedded]+[{'type':'h','text':'확인 문제'}]+qs
   # 해설은 문제 뒤에 붙이지 않고 부록 해설로 이동한다.
   anspos=next((j for j,b in enumerate(s['blocks']) if b.get('type')=='h' and b.get('text')=='해설'),None)
   if anspos is not None:
    answers.append(sec(str(n)+'장 확인 문제 해설',s['blocks'][anspos+1:]));s['blocks']=s['blocks'][:anspos]
   elif i in c.get('answer_pages',[]):
    answers.append(sec(str(n)+'장 확인 문제 해설',s['blocks'][1:2]));s['blocks']=s['blocks'][:1]+s['blocks'][2:]
   sections.append(s)
  if isinstance(n,int):
   start=next(s for s in sections if s['title'].startswith(f'{n}장 '))
   start['blocks'][0]=p(c['opening'])
   start['blocks'].insert(1,{'type':'list','items':c['goals']})
   start['blocks'].insert(2,box('predict',c['predict']))
   if n==1:
    sections.insert(2,sec('일러두기',[p('1권의 kt66·Wazuh 환경과 별도 Windows 게스트를 준비한 뒤 시작한다. 새 설치는 kt66의 Windows 안내와 부록의 준비 항목을 따른다. 각 명령의 실행 위치를 확인하고 준비·입력·원본·검색·판정·원상복구를 한 기록에 남긴다.'),p('본문의 번호 입력은 examples/rev01/chapterNN에서 복사한다. 처음 등장한 도구와 기호는 해당 절에서 설명하며 이후에는 명령 번호로 다시 찾는다. C는 터미널 입력, Q는 DQL, D는 Dev Tools 요청이다. 자동 줄바꿈으로 두 줄에 보이는 한 줄 명령은 복사용 파일의 원래 줄 단위로 입력한다.'),p('1~4장은 입력과 대조를 단계별로 안내한다. 5~9장은 경보에서 원본으로 거슬러 올라가는 분석을 더한다. 10~13장은 조사 조건과 보고서의 근거를 독자가 정한다. 각 장의 독립 과제는 해설을 보기 전에 결론과 반증 조건을 작성한다.'),p('서로 다른 실습은 별개의 사례로 유지한다. 장을 관통하는 것은 조사 기록이다. 같은 날짜·계정·IP만으로 사건을 합치지 않고, 세션·GUID·경로·해시로 확인한 연결과 미확인 연결을 나눈다.')],br=True))
    qidx=next(i for i,s in enumerate(sections) if s['title']=='Wazuh에서 같은 범위 검색하기')
    sections.insert(qidx,sec('수집 경로와 보존 자료',[p('alerts는 경보로 저장된 문서, archives는 보관 설정을 거친 수집 문서다. archives 조회는 관리자 설정의 logall_json, Filebeat의 archives 활성화, 실제 색인과 데이터 보기 준비가 모두 필요하다. 설정만 켰다고 과거 이벤트가 자동으로 채워지는 것은 아니다.'),p('현재 준비 상태는 C03-12·C03-13의 읽기 명령으로 확인한다. Discover에서 wazuh-archives-*를 선택하고 이미 확인한 원본 번호·시각으로 검색한다. 데이터 보기가 없거나 적재가 준비되지 않았다면 해당 원본 Windows 이벤트를 보존하고 관리자에게 수집 경로 확인을 요청한다.'),p('실습 환경에 예시 시각의 자료가 없으면 examples/rev01/records의 장별 JSON과 manifest.json을 사용한다. 각 묶음은 원래 보존 자료에서 발췌한 필드와 출처를 담는다. 텍스트 편집기나 부록의 PowerShell 조회로 읽는다. 원본 전체와 SIEM 설정을 복원하는 스냅샷은 아니므로 없는 필드와 집계 모집단을 새로 만들어 해석하지 않는다.')]))
   # 각 장의 관찰 한계는 관련 분석 지점에 놓는다.
   for target,kind,text in c.get('callouts',[]):
    s=next(s for s in sections if target in s['title']);s['blocks'].append(box(kind,text))
   summary=sec('핵심 정리', [{'type':'list','items':c['summary']}])
   # 기존 정리표는 살리고 새 핵심 정리는 장말 문제 바로 앞에 둔다.
   qpos=next((i for i,s in enumerate(sections) if s['title']=='확인 문제'),len(sections))
   sections.insert(qpos,summary)
   sections.append(sec('스스로 조사하기', [p(c['exercise']),p('결과는 관찰한 사실, 가능한 다른 설명, 추가로 확인할 증거, 대응 조건으로 나누어 적는다. 해설은 부록의 장별 해설과 대조한다.')]))
   answers.append(sec(f'{n}장 독립 과제 해설',[p(c['answer'])]))
   sections.append(sec('다음 조사로 이어가기',[p(c['bridge'])]))
   picked=[]
   for term,note in c['reading']:
    rid,b=next((rid,b) for rid,b in refs if term in b['text'])
    picked.append(p(f"[{rid}] {b['text']}. {note}"))
   picked.append(p('자료의 전체 URL은 별도 「참고문헌」에서 번호로 찾는다.'))
   sections.append(sec('더 읽을거리',picked))
  # 1장의 무번호 소주제를 조사 순서별 큰 절로 묶는다.
  if n==1:
   mapping={'Windows 게스트가 있는 위치':'1.1  대상과 준비 상태','이벤트를 구분하는 세 가지 값':'1.2  원본 이벤트의 식별','에이전트 수집 설정 읽기':'1.3  수집 경로 확인','수집 경로와 보존 자료':'1.4  검색 준비와 보존 자료','Wazuh에서 같은 범위 검색하기':'1.5  원본과 Wazuh 대조','검색 결과가 없을 때 확인할 순서':'1.6  조사 기록과 완료 판단'}
   for s in sections:
    if s['title'] in mapping:s['title']=mapping[s['title']];s['level']='section'
  # 본문 표에서 원전 실습 번호만 나열한 행은 조사 내용으로 표시한다.
  for s in sections:
   for b in s['blocks']:
    if b['type']=='table' and b['head'][0]=='실습':
     b['head'][0]='사례'
     for row in b['rows']:
      row[0]=re.sub(r'^\d+\s*','',row[0]) or row[1].split(' · ')[0]
  d['sections']=sections;d.pop('pages');d['comments']='REV01 교정본. 검증 이력은 editorial/REV01/review.md.'
  # 기존 그림을 최신 자산의 독립 사본으로 고정한다.
  for s in sections:
   for b in s['blocks']:
    if b['type']=='image':
     old=ROOT/b['path'];h=hashlib.sha256(old.read_bytes()).hexdigest();rel='assets/REV01/'+h[:12]+'-'+old.name
     dest=ROOT/rel;dest.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(old,dest)
     assets[rel]={'source':b['path'],'sha256':h};b['path']=rel
    for k in ['text','why','result','caption','where']:
     if not isinstance(b.get(k),str) or b['type'] in ('code','link') or (b['type'] in ('command','query') and k=='text'):continue
     b[k]=b[k].replace('kt66 Ubuntu VM의 터미널','kt66 VM · 터미널').replace('kt66 Ubuntu VM · 터미널','kt66 VM · 터미널').replace('kt66 VM · 호스트 터미널','kt66 VM · 터미널').replace('Windows 실습 게스트의 관리자 PowerShell','Windows 실습 게스트 · 관리자 PowerShell').replace('폴더','디렉터리').replace('페이지','쪽')
     b[k]=b[k].replace('examples/chapter','examples/rev01/chapter').replace('examples/appendix','examples/rev01/appendix')
  (OUT/f'volume02-{stem}.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n','utf8')
  changes.append({'chapter':stem,'before_sections':len(original['pages']),'after_sections':len(sections),'edits':c})
 # 부록에 분리한 해설과 도구 색인을 추가한다.
 f=OUT/'volume02-appendix.json';ap=json.loads(f.read_text('utf8'));ap['sections']+=answers
 index=[]
 for f2 in sorted(OUT.glob('volume02-chapter*.json')):
  d=json.loads(f2.read_text('utf8'))
  for s in d['sections']:
   for b in s['blocks']:
    if b['type'] in ('command','query'):index.append([b['id'],s['title'],b['where']])
 ap['sections'].append(sec('입력 색인',[p('번호가 붙은 입력의 본문 위치를 찾는다. 해당 절에서 선행 변수와 원상복구 조건을 확인한 뒤 실행한다.'),{'type':'table','head':['번호','본문 위치','실행 위치'],'widths':[21,58,48],'rows':index}]))
 f.write_text(json.dumps(ap,ensure_ascii=False,indent=2)+'\n','utf8')
 rd={'title':'참고문헌','series':'해킹·침해대응 실무 with Wazuh 2권','sections':[sec('참고문헌',[p('각 장의 더 읽을거리와 함께 사용하는 전체 자료 목록이다. 고정 커밋 자료는 본문의 실습 버전을, 최신 공식 문서는 개념과 필드의 정의를 확인하는 데 사용한다.')]+bibliography)]}
 (OUT/'volume02-references.json').write_text(json.dumps(rd,ensure_ascii=False,indent=2)+'\n','utf8')
 for name,data in [('changes.json',changes),('assets.json',assets)]:
  (ROOT/'editorial/REV01'/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n','utf8')
if __name__=='__main__':main()
