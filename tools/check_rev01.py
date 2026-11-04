"""REV01 원고·입력·그림·참조의 정적 검토. 실습 명령은 실행하지 않는다."""
from pathlib import Path
from collections import Counter
import json,hashlib,re,zipfile
from docx import Document
from lxml import etree
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def sha_lf(p):return hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest()
def blocks(d):return [b for s in d.get('sections',d.get('pages',[])) for b in s['blocks']]
def main():
 import argparse
 parser=argparse.ArgumentParser()
 parser.add_argument('--check-originals',action='store_true',help='저자 작업 시작 시점의 로컬 초안 해시까지 대조한다. 당시 미커밋 변경도 포함한다.')
 args=parser.parse_args()
 errors=[];stats=[];inputs={};references=[]
 for f in sorted((ROOT/'manuscript/REV01').glob('*.json')):
  d=json.loads(f.read_text('utf8'));bs=blocks(d);stem=f.stem.replace('volume02-','')
  if stem.startswith('chapter'):
   titles=Counter(s['title'] for s in d['sections'])
   for title in ['핵심 정리','확인 문제','스스로 조사하기','더 읽을거리']:
    if titles[title]!=1:errors.append([stem,'장말 제목',title,titles[title]])
  src=ROOT/'manuscript'/f.name
  if src.exists() and args.check_originals:
   before=blocks(json.loads(src.read_text('utf8')))
   old={b['id']:b['text'] for b in before if b['type'] in ('command','query')}
   now={b['id']:b['text'] for b in bs if b['type'] in ('command','query')}
   for k,v in old.items():
    if now.get(k)!=v:errors.append([stem,'기존 입력 누락/변경',k])
   oc=Counter(b['caption'] for b in before if b['type']=='image');nc=Counter(b['caption'] for b in bs if b['type']=='image')
   if oc!=nc:errors.append([stem,'그림 목록 차이',dict(oc-nc),dict(nc-oc)])
  for b in bs:
   if b['type'] in ('command','query'):
    if b['id'] in inputs:errors.append([stem,'중복 입력 번호',b['id']])
    inputs[b['id']]=b
    ext='.dql' if b['id'].startswith('Q') else '.http' if b['id'].startswith('D') else '.txt'
    path=ROOT/'examples/rev01'/stem/(b['id']+ext)
    if not path.exists() or path.read_text('utf8').rstrip()!=b['text'].rstrip():errors.append([stem,'복사용 파일 차이',b['id']])
   if b['type']=='table':
    if len(b['head'])!=len(b['widths']) or sum(b['widths'])>127:errors.append([stem,'표 폭',b['head']])
   for k in ['text','why','result','caption']:
    if isinstance(b.get(k),str):references += re.findall(r'\b[CQD](?:\d{2}|A)-\d{2}\b',b[k])
  doc=Document(f.with_suffix('.docx'));section=doc.sections[0]
  if abs(section.page_width.mm-188)>0.1 or abs(section.page_height.mm-263)>0.1:errors.append([stem,'판형'])
  with zipfile.ZipFile(f.with_suffix('.docx')) as z:
   embedded={hashlib.sha256(z.read(x)).hexdigest() for x in z.namelist() if x.startswith('word/media/')}
   for b in bs:
    if b['type']=='image' and sha(ROOT/b['path']) not in embedded:errors.append([stem,'내장 그림 불일치',b['path']])
  stats.append({'document':f.with_suffix('.docx').name,'inputs':sum(b['type'] in ('command','query') for b in bs),'images':sum(b['type']=='image' for b in bs),'sections':len(d['sections'])})
 for ref in sorted(set(references)-set(inputs)):errors.append(['입력 참조 없음',ref])
 if args.check_originals:
  for row in json.loads((ROOT/'editorial/REV01/source-baseline.json').read_text('utf8')):
   if sha(ROOT/row['path'])!=row['sha256']:errors.append(['기존 초안 변경',row['path']])
 # 출처의 실제 필드와 배포 발췌본을 대조한다.
 for f in sorted((ROOT/'examples/rev01/records').glob('chapter*.json')):
  d=json.loads(f.read_text('utf8'))
  for c in d['cases']:
   source=ROOT/c['source']
   source_hash=sha_lf(source) if c.get('source_hash_basis')=='LF-normalized UTF-8 bytes' else sha(source)
   if source_hash!=c['source_sha256']:errors.append(['출처 해시',f.name,c['case']])
   data=json.loads(source.read_text('utf8'))
   if c['pointer']=='/':expected=data
   else:expected=data['records'][int(c['pointer'].split('/')[-1])]['hits']
   if c['records']!=expected:errors.append(['발췌 변형',f.name,c['case']])
 output={'documents':stats,'total_inputs':sum(x['inputs'] for x in stats),'total_images':sum(x['images'] for x in stats),'local_original_baseline_checked':args.check_originals,'errors':errors}
 (ROOT/'editorial/REV01/static-check.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n','utf8')
 print(json.dumps(output,ensure_ascii=False,indent=2))
 if errors:raise SystemExit(1)
if __name__=='__main__':main()
