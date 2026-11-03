"""원고·복사 파일·원본 로그 대응과 DOCX 기하·참고 URL을 검사한다."""
import argparse,json,re,hashlib
from pathlib import Path
from collections import Counter
from xml.etree import ElementTree as ET
from zipfile import ZipFile
from docx import Document
from docx.oxml.ns import qn

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--pdf',type=Path)
args=parser.parse_args()
data=json.loads((ROOT/'manuscript/volume02-chapter01.json').read_text(encoding='utf8'))
manifest=json.loads((ROOT/'examples/chapter01/manifest.json').read_text(encoding='utf8'))
blocks=[b for pg in data['pages'] for b in pg['blocks']]
inputs={b['id']:b['text'] for b in blocks if b['type'] in ('command','query')}
assert len(inputs)==len(manifest)==19
for m in manifest:
    assert inputs[m['id']]==m['input']
    assert (ROOT/'examples/chapter01'/m['file']).read_text(encoding='utf8').rstrip('\n')==m['input']
images=[b for b in blocks if b['type']=='image']
assert len(images)==6 and all((ROOT/b['path']).is_file() for b in images)
docpath=ROOT/'manuscript/volume02-chapter01.docx';doc=Document(docpath)
template=Document(ROOT/'tools/assets/bookk-B5.docx')
for attr in ['page_width','page_height','top_margin','bottom_margin','left_margin','right_margin','gutter']:
    assert getattr(doc.sections[0],attr)==getattr(template.sections[0],attr),attr
assert len(doc.inline_shapes)==6
assert doc.paragraphs[0].style.name=='Title'
for p in doc.paragraphs:
    for r in p.runs:
        if r.text and r.font.color.rgb is not None:assert str(r.font.color.rgb)=='000000'
with ZipFile(docpath) as z:
    xml=ET.fromstring(z.read('word/document.xml'))
    runs=''.join(n.text or '' for n in xml.iter(qn('w:t')))
    for b in blocks:
        if b['type']=='link':assert b['url'] in runs,b['url']
    assert '\ufffd' not in runs
ev=ROOT/'editorial/evidence/chapter01/2026-11-03'
alerts=json.loads((ev/'wazuh-alert-excerpts.json').read_text(encoding='utf8'))
ns={'e':'http://schemas.microsoft.com/win/2004/08/events/event'}
for name,event_id in [('security_xml.xml','4624'),('sysmon_xml.xml','1')]:
    root=ET.fromstring((ev/name).read_text(encoding='utf8'))
    original={x.tag.split('}')[-1]:x.text for x in root.find('e:System',ns)}
    ed={x.attrib['Name']:x.text for x in root.findall('e:EventData/e:Data',ns)}
    a=next(x for x in alerts if x['data']['win']['system']['eventID']==event_id)
    w=a['data']['win'];s=w['system'];d=w['eventdata']
    for key,mapped in [('EventID','eventID'),('EventRecordID','eventRecordID'),('Channel','channel'),('Computer','computer')]:
        assert original[key]==s[mapped],(name,key)
    assert root.find('e:System/e:TimeCreated',ns).attrib['SystemTime']==s['systemTime']
    if event_id=='4624':
        assert ed['TargetUserName']==d['targetUserName']
        assert ed['LogonType']==d['logonType']=='8'
        assert ed['ProcessName']==d['processName'].replace('\\\\','\\')
    else:
        assert root.find('e:System/e:Execution',ns).attrib['ProcessID']==s['processID']=='4440'
        assert ed['ProcessId']==d['processId']=='8752'
        assert ed['Image']==d['image'].replace('\\\\','\\')
checks=json.loads((ev/'copy-command-checks.json').read_text(encoding='utf8'))
assert all(x['exit_code']==0 and not x['stderr'] for x in checks['records'])
coverage=json.loads((ROOT/'editorial/module01-coverage.json').read_text(encoding='utf8'))
numbers=[x['exercise'] for x in coverage['exercises']]
assert sorted(numbers)==list(range(31,62))+[63]
assert all(v==1 for v in Counter(numbers).values())
page_count=None
if args.pdf:
    from pypdf import PdfReader
    pdf=PdfReader(args.pdf);page_count=len(pdf.pages)
    text=''.join((p.extract_text() or '') for p in pdf.pages)
    flat=re.sub(r'\s+','',text)
    for b in blocks:
        if b['type']=='link':assert b['url'] in flat,('rendered URL',b['url'])
    assert page_count==30
print(json.dumps({'copy_examples':len(inputs),'images':len(images),'matched_event_records':2,
 'coverage_exercises':len(numbers),'template_geometry':'identical','full_reference_urls':'present',
 'rendered_pages':page_count,'docx_sha256':hashlib.sha256(docpath.read_bytes()).hexdigest()},ensure_ascii=False,indent=2))
