"""교정용 DOCX·복사용 입력·읽기 증거 대조. 내부 Word 렌더가 필요하다."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from zipfile import ZipFile
import json,re,csv,statistics,subprocess
from docx import Document
from lxml import etree
from PIL import Image
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text('utf-8-sig'))
def digest(p):return sha256(Path(p).read_bytes()).hexdigest()
def norm(s):return re.sub(r'[\s\u200b\u00ad\ufeff]','',s)
def write(p,j):(ROOT/p).write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def rows(p):
 with (ROOT/p).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
spec=[('chapter10','chapter10-final-v2',19,17),('chapter11','chapter11-final',18,14),('chapter12','chapter12-final-v3',25,20),('chapter13','chapter13-final-v2',21,6),('appendix','appendix-final',17,4)]
queryrecords=read('editorial/remaining-query-ui.json')['records']
assert len(queryrecords)==35 and all(r['parser_error'] is False for r in queryrecords)
querymap={r['id']:r for r in queryrecords}
expected_hits=[27,4,2,2,1,1,0,0,0,0,69,126,13,7,438]+[0]*16+[69,328,29,0]
assert [r['hits'] for r in queryrecords]==expected_hits
allinputs=[];allimages=[];allurls=[];allxml=[];reports=[]
basepath=ROOT/'tools/assets/bookk-B5.docx'
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
selected=read('editorial/remaining-illustrations.json')
generated=Path(selected['generated_directory'])
for art in selected['selected']:assert digest(generated/art['original'])==digest(ROOT/art['path'])
rejected=digest(generated/selected['rejected'][0]['original'])
for s in read('editorial/remaining-screenshot-provenance.json'):
 assert digest(ROOT/s['file'])==s['sha256'] and digest(ROOT/s['source'])==s['source_sha256']
for stem,render,count,ninputs in spec:
 source=read(f'manuscript/volume02-{stem}.json')
 blocks=[b for p in source['pages'] for b in p['blocks']]
 inputs=[b for b in blocks if b['type'] in ('command','query')]
 manifest=read(f'examples/{stem}/manifest.json')
 assert len(inputs)==len(manifest)==ninputs
 for b,m in zip(inputs,manifest):
  assert (b['id'],b['text'],b['where'])==(m['id'],m['input'],m['where'])
  assert (ROOT/f'examples/{stem}'/m['file']).read_text('utf8').rstrip()==b['text']
  if b['id'].startswith('Q'):
   r=querymap[b['id']];assert norm(b['text'])==norm(r['query']) and r['index']=='wazuh-alerts-*'
 allinputs.extend(inputs)
 docpath=ROOT/f'manuscript/volume02-{stem}.docx';doc=Document(docpath)
 assert doc.paragraphs[0].style.name=='Title'
 with ZipFile(docpath) as z,ZipFile(basepath) as base:
  xml=etree.fromstring(z.read('word/document.xml'));bxml=etree.fromstring(base.read('word/document.xml'))
  sect=xml.find('.//w:sectPr',ns);bs=bxml.find('.//w:sectPr',ns);geometry={}
  for tag in ('pgSz','pgMar'):
   a,b=sect.find('w:'+tag,ns),bs.find('w:'+tag,ns);assert dict(a.attrib)==dict(b.attrib)
   geometry[tag]={etree.QName(k).localname:v for k,v in a.attrib.items()}
  assert z.read('word/theme/theme1.xml')==base.read('word/theme/theme1.xml')
  media={n:sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('word/media/')}
  assert rejected not in media.values()
  doc_text=''.join(xml.itertext())
  allxml.append('\n'.join(z.read(n).decode('utf8','replace') for n in z.namelist() if n.endswith('.xml')))
 images=[b for b in blocks if b['type']=='image'];assert len(images)==len(doc.inline_shapes)==len(media)
 imagechecks=[]
 for b,shape in zip(images,doc.inline_shapes):
  asset=ROOT/b['path'];h=digest(asset);assert h in media.values()
  with Image.open(asset) as im:
   assert abs(shape.width/shape.height-im.width/im.height)<.005
   imagechecks.append({'path':b['path'],'sha256':h,'size':list(im.size),'mode':im.mode,'alpha_range':im.getchannel('A').getextrema() if im.mode=='RGBA' else None,'embedded_hash_match':True,'aspect_preserved':True})
 allimages.extend(imagechecks)
 pdfpath=ROOT/f'build/remaining/{render}.pdf';pdf=PdfReader(pdfpath);assert len(pdf.pages)==count
 pdftexts=[p.extract_text() for p in pdf.pages];pdftext='\n'.join(pdftexts)
 urls=[b['url'] for b in blocks if b['type']=='link']
 for url in urls:assert norm(url) in norm(pdftext) and norm(url) in norm(doc_text),url
 for b in inputs:assert norm(b['text']) in norm(pdftext),(stem,b['id'])
 for b in blocks:
  if b['type']=='code':assert norm(b['text']) in norm(pdftext)
 allurls.extend(urls)
 fonts=set()
 for p in pdf.pages:
  for f in p.get('/Resources').get_object().get('/Font',{}).values():fonts.add(str(f.get_object().get('/BaseFont')))
 for name in ['Consolas','BookkMyungjo','BookkGothic']:assert any(name in f for f in fonts)
 finalpages={p.name:digest(p) for p in sorted((ROOT/f'build/remaining/{render}-pages').glob('page-*.png'))};assert len(finalpages)==count
 previous=ROOT/f'build/remaining/{stem}-final-pages';same=[];changed=[]
 if render!=stem+'-final':
  for name,h in finalpages.items():
   (same if (previous/name).exists() and digest(previous/name)==h else changed).append(int(Path(name).stem.split('-')[-1]))
 else:same=list(range(1,count+1))
 approved_changes={'chapter10':[18,19],'chapter12':[8,15,16,18,19,21,23,24,25],'chapter13':[20,21]}
 assert changed==approved_changes.get(stem,[])
 counts=Counter(b['id'][0] for b in inputs)
 report={'date':'2026-11-03','artifact':stem,'status':'draft reviewed','docx':str(docpath.relative_to(ROOT)).replace('\\','/'),'docx_sha256':digest(docpath),'manuscript_sha256':digest(ROOT/f'manuscript/volume02-{stem}.json'),'page_count':count,'internal_render':str(pdfpath.relative_to(ROOT)).replace('\\','/'),'internal_render_sha256':digest(pdfpath),'render_method':'Hidden Microsoft Word COM and pypdfium2; PDF only for internal QA','template_sha256':digest(basepath),'geometry_twips':geometry,'theme_matches_template':True,'first_paragraph_style':'Title','pdf_fonts':sorted(fonts),'copy_inputs':{'total':len(inputs),'shell':counts['C'],'dql':counts['Q'],'dev_tools_fragments':counts['D'],'manifest_matches':True,'all_input_text_in_render':True,'ui_evidence':'remaining-query-ui.json'},'full_urls_verified_in_docx_and_render':urls,'images':imagechecks,'visual_review':{'previous_final_individually_viewed':list(range(1,count+1)),'final_pages_unchanged_hash_match':same,'final_changed_pages_individually_viewed':changed,'final_page_sha256':finalpages,'result':'No clipping, distorted images, detached captions or missing URL characters observed.'},'validation_limits':'Read-only observations plus source screenshots. No new attack, service stop, firewall/protection change, synthetic generation/ingestion/deletion. Empty synthetic results are not positive-path verification. Arithmetic fixtures are constructed. See remaining-review.md and artifact review.'}
 write(f'editorial/{stem}-qa.json',report);reports.append(report)

assert len(allinputs)==61 and Counter(b['id'][0] for b in allinputs)=={'C':19,'Q':35,'D':7}
assert len(allimages)==24 and Counter(b['path'].split('/')[1] for b in allimages)=={'screenshots':12,'figures':8,'illustrations':4}
assert len(allurls)==27
inputmap={b['id']:b['text'] for b in allinputs}
checks=read('editorial/evidence/remaining/2026-11-03/request-checks.json')['records']
parsed=[r for r in checks if r['id'].endswith('-bash-parse')]
assert len(parsed)==19
for r in parsed:
 assert r['exit_code']==0 and not r['stderr']
 assert r['reader_input']==inputmap[r['id'].removesuffix('-bash-parse')]
ps=read('editorial/remaining-powershell-parse.json');assert ps['errors']==[] and ps['input']==inputmap['C10-01']
requests={'D12-01':inputmap['D12-01'],'D12-02':inputmap['D12-02'],'D12-05':inputmap['D12-05']}
for ch,ids,name in [(12,['D12-03','D12-04'],'ip-profile'),(13,['D13-01','D13-02'],'hourly-risk')]:
 text='\n'.join(inputmap[i] for i in ids)
 assert (ROOT/f'examples/chapter{ch}/{name}.http').read_text('utf8').rstrip()==text
 requests[name]=text
for key,s in requests.items():
 assert s.startswith('GET ')
 if '\n' in s:json.loads(s.split('\n',1)[1])
finalfield=read('editorial/evidence/remaining/2026-11-03/fieldcaps-final-check.json')['records'][0]
finalhours=read('editorial/evidence/remaining/2026-11-03/hourly-final-checks.json')['records']
for key,s in requests.items():
 r=finalfield if key=='D12-01' else finalhours[0] if key=='hourly-risk' else next(r for r in checks if r['id']==key)
 assert r['reader_input']==s and r['exit_code']==0 and not r['stderr'],key
 d=json.loads(r['stdout']);assert 'error' not in d and d.get('_shards',{}).get('failed',0)==0
 if key!='D12-01':assert d['hits']['total']['value']==0 and d['hits']['total']['relation']=='eq'
rolling=[]
for r,n in zip(finalhours,[47,72]):
 d=json.loads(r['stdout']);bs=d['aggregations']['hours']['buckets'];assert len(bs)==n and d['_shards']['failed']==0
 for i,b in enumerate(bs):assert b['risk_24h']['value']==sum(x['risk']['value'] for x in bs[max(0,i-23):i+1])
 rolling.append({'id':r['id'],'buckets':n,'documents':d['hits']['total']['value'],'current_plus_prior_23_sum_matches':True})
off=json.loads(next(r['stdout'] for r in checks if r['id']=='offhour-populated-smoke'))['aggregations']['scope']['buckets']['all']
assert off['doc_count']==17610 and off['off']['doc_count']==10459 and abs(off['ratio']['value']-10459/17610)<1e-12
for r in checks:
 assert r['exit_code']==0 and not r['stderr'],r['id']
finalstate=checks[-1]['stdout'];assert len(re.findall(r', Active$',finalstate,re.M))==6
scores=rows('examples/chapter13/score-worked.csv');assert [float(r['score']) for r in scores]==[48,1,100,20,50]
assert float(scores[2]['raw_total'])==123
weights=rows('examples/chapter13/rule-weight-worked.csv');assert [r['rounded'] for r in weights]==['0.74','0.69','0.64','0.57']
hourfixture=rows('examples/chapter13/hourly-worked.csv');assert len(hourfixture)==48
assert [int(hourfixture[i]['risk_24h']) for i in [23,24,46,47]]==[150,175,175,25]
for i,r in enumerate(hourfixture):assert int(r['risk_24h'])==sum(int(x['risk']) for x in hourfixture[max(0,i-23):i+1])
mu=statistics.mean([10,10,10,100]);sd=statistics.pstdev([10,10,10,100]);burst=(sd-mu)/(sd+mu)
assert mu==32.5 and round(sd,2)==38.97 and round(burst,4)==.0905
assert 3/(3+1)==.75
profile=rows('examples/chapter12/ip-profile-worksheet.csv');assert len(profile)==5 and 'interval_std_s' in profile[0]
coverage=read('editorial/module01-coverage.json');assert sorted(r['exercise'] for r in coverage['exercises'])==list(range(31,62))+[63]
assert all(r['status']=='draft' for r in coverage['exercises']+coverage['advanced'])
paths=subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=ROOT,text=True).splitlines()
paths+=subprocess.check_output(['git','diff','--name-only'],cwd=ROOT,text=True).splitlines()
assert all('REV01' not in p and not re.search(r'(chapter0[1-9]|volume02-chapter0[1-9])',p) for p in paths)
assert all(not p.endswith('.pdf') and not p.startswith('build/') for p in paths)
patterns=[r'gh[pousr]_[A-Za-z0-9]{20,}',r'github_pat_[A-Za-z0-9_]{20,}',r'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----']
for p in paths:
 a=ROOT/p;assert a.stat().st_size<50*1024*1024
 if a.suffix in ('.md','.json','.txt','.dql','.py','.http','.csv'):assert not any(re.search(rx,a.read_text('utf-8-sig')) for rx in patterns),'Credential signature '+p
assert not any(re.search(rx,'\n'.join(allxml)) for rx in patterns)
result={'date':'2026-11-03','status':'13 chapters and appendix draft complete; publication proofreading remains','new_artifacts':[{'docx':r['docx'],'sha256':r['docx_sha256'],'pages':r['page_count']} for r in reports],'new_total_pages':sum(r['page_count'] for r in reports),'copy_inputs':61,'dql_ui':35,'shell_syntax':19,'powershell_syntax':1,'complete_get_requests':5,'images':24,'reference_url_occurrences':27,'rolling_window_checks':rolling,'offhour_current_data':{'documents':17610,'offhour':10459,'ratio':off['ratio']['value']},'arithmetic':{'score_cases':[48,1,100,20,50],'raw_max':123,'rounded_rule_weights':['0.74','0.69','0.64','0.57'],'burst_mean':mu,'burst_population_std':sd,'burstiness':burst,'hourly_boundary_expected':[150,175,175,25],'precision_example':.75},'final_agents_active':6,'scope':{'prior_chapters_unchanged':True,'rev01_unchanged':True,'no_combined_book':True,'no_distributed_pdf':True,'no_attack_or_security_setting_change':True,'no_synthetic_generation_ingestion_deletion':True},'credential_signature_scan':'no matches in new/changed text and DOCX XML','review':'remaining-review.md'}
write('editorial/remaining-delivery.json',result)
print(json.dumps({'result':'pass','pages':100,'inputs':61,'dql':35,'images':24,'urls':27,'get_requests':5},ensure_ascii=False))
