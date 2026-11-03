"""4장 이후의 원고 블록과 복사용 입력을 저장하는 저자용 도구."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
WIN='Windows 실습 게스트 · 관리자 Windows PowerShell'
HOST='kt66 Ubuntu VM · 터미널'
BASE='agent.name:"windows-user"'
SYSMON='data.win.system.channel:"Microsoft-Windows-Sysmon/Operational"'
def p(t):return {'type':'p','text':t}
def h(t):return {'type':'h','text':t}
def code(t):return {'type':'code','text':t}
def table(head,rows,widths):return {'type':'table','head':head,'rows':rows,'widths':widths,'keep':True}
def image(path,caption,width=127):return {'type':'image','path':path,'caption':caption,'width_mm':width}
def cmd(cid,text,why,result,where=WIN):return {'type':'command','id':cid,'where':where,'text':text,'why':why,'result':result}
def query(qid,text,why,result,index='wazuh-archives-*'):return {'type':'query','id':qid,'where':'Windows PC · Wazuh Discover · '+index+' · DQL','text':text,'why':why,'result':result}
def link(title,url):return {'type':'link','text':title,'url':url}
def save(chapter,title,pages,notes):
 stem=f'volume02-chapter{chapter:02}'
 data={'title':title,'series':'해킹·침해대응 실무 with Wazuh 2권','comments':notes,'pages':pages}
 (ROOT/'manuscript'/f'{stem}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 dest=ROOT/'examples'/f'chapter{chapter:02}';dest.mkdir(parents=True,exist_ok=True);manifest=[]
 for pg in pages:
  for b in pg['blocks']:
   if b['type'] not in ('command','query'):continue
   name=b['id']+('.dql' if b['type']=='query' else '.txt')
   (dest/name).write_text(b['text']+'\n',encoding='utf8')
   manifest.append({'id':b['id'],'file':name,'where':b['where'],'section':pg['title'],'input':b['text']})
 (dest/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 (dest/'README.md').write_text(f'# {chapter}장 복사용 입력\n\n본문의 사전 확인부터 한 블록씩 입력한다. 전체를 일괄 실행하지 않는다. 같은 PowerShell 창의 변수를 유지한다. 예제 번호·시각·GUID는 자신의 기록으로 바꾼다. 삭제 명령은 이번에 만든 고유 이름과 파일에만 적용한다.\n\n'+ '\n'.join(f"- [{m['file']}]({m['file']}) — {m['where']}" for m in manifest)+'\n',encoding='utf8')
 (dest/'observation-template.md').write_text(f'# {chapter}장 조사 기록\n\n- 실행 위치와 계정, 시작·종료 시각/시간대:\n- 사전 객체와 수집·보호 상태:\n- 입력, 응답, 실제 실행/파일 결과:\n- 원본 컴퓨터·채널·EventID·EventRecordID:\n- ProcessGuid 또는 ScriptBlockId / 원본 시각:\n- Wazuh 데이터 보기·검색식·대응 필드:\n- 확인된 사실, 승인 내역, 추가 조사:\n- 원상복구 대상과 재조회 결과:\n',encoding='utf8')
 print(stem,len(pages),'sections',len(manifest),'inputs')
