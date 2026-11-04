"""보존한 증거의 발췌본과 복사용 예제를 REV01에 고정한다. 네트워크에 접속하지 않는다."""
from pathlib import Path
import json, shutil, hashlib

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'examples/rev01'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n','utf8')

def main():
    for stem in [f'chapter{n:02}' for n in range(1,14)]+['appendix']:
        shutil.copytree(ROOT/'examples'/stem,OUT/stem,dirs_exist_ok=True)
    manifest=[]
    groups={n:[] for n in range(1,14)}
    paths=['editorial/evidence/analysis-revision/2026-11-04/evidence.json',
           'editorial/evidence/analysis-revision/2026-11-04/followup.json']
    assignments={
      'windows-selected':[2,3,4,5,6,7], 'ch01-record':[1], 'ch02-session':[2],
      'ch03-account-logon':[3], 'ch04-registration':[4], 'ch04-writer':[4],
      'ch05-scriptblocks':[5], 'ch05-pid':[5], 'ch06-processes':[6],
      'ch06-original-archives':[6], 'ch06-original-alerts':[6],
      'ch07-defender':[7], 'ch08-sca':[8], 'ch10-ar':[10],
      'ch11-high':[11], 'ch11-session':[11], 'ch12-live-ip':[12,13],
      'ch12-live-all':[12,13]}
    for rel in paths:
        f=ROOT/rel;d=json.loads(f.read_text('utf8'))
        for i,r in enumerate(d['records']):
            for n in assignments.get(r['case'],[]):
                # 이미 선택된 필드만 옮긴다. 전체 SSH 출력이나 설정 파일을 재배포하지 않는다.
                groups[n].append({'case':r['case'],'source':rel,'source_sha256':sha(f),
                  'pointer':f'/records/{i}','index':r.get('index'),
                  'query':r.get('query'),'total':r.get('total'),
                  'returned':len(r.get('hits',[])),'records':r.get('hits',[])})
    rel='editorial/evidence/chapter01/2026-11-03/wazuh-alert-excerpts.json'
    f=ROOT/rel;arr=json.loads(f.read_text('utf8'))
    groups[1].append({'case':'original-alert-fields','source':rel,'source_sha256':sha(f),
       'pointer':'/','returned':len(arr),'records':arr})
    for n,records in groups.items():
        if not records: continue
        name=f'chapter{n:02}.json';f=OUT/'records'/name
        save(f,{'chapter':n,'kind':'saved-evidence-excerpts',
          'scope':'보존 자료의 필드 발췌. 전체 로그나 SIEM 복원용 자료가 아니다.',
          'cases':records})
        manifest.append({'file':name,'sha256':sha(f),'cases':[r['case'] for r in records],
                         'returned':sum(r['returned'] for r in records)})
    rel='editorial/evidence/analysis-revision/2026-11-04/aggregation-responses.json'
    f=ROOT/rel;dest=OUT/'records/aggregation-responses.json';shutil.copy2(f,dest)
    manifest.append({'file':dest.name,'sha256':sha(dest),'source':rel,'source_sha256':sha(f)})
    save(OUT/'records/manifest.json',{'schema':1,'files':manifest,
      'notes':['system·eventdata는 원래 data.win에서 선택해 저장한 필드다. original-alert-fields 사례는 data.win 구조를 유지한다.',
       'total은 원래 검색의 전체 건수, returned는 이 파일에 남아 있는 문서 수다. 같다고 가정하지 않는다.',
       '9장은 본문의 경보 필드·캡처와 examples/rev01/chapter09의 기존 자료를 사용한다. 보존하지 않은 원문을 재구성하지 않는다.',
       '동일 원본이 서로 다른 사례 또는 alerts·archives에 중복될 수 있다. 파일의 배열 길이를 전체 사건 수로 집계하지 않는다.']})
    (OUT/'records/README.md').write_text('''# 보존 기록으로 조사하기

이 디렉터리는 2026-11-03~04에 이미 보존한 조회 자료에서 선택한 필드를 그대로 옮긴다. 이번 교정에서 공격·환경 변경·새 수집 시험은 하지 않았다. 원본 경로, SHA-256, JSON 위치는 각 사례의 `source`, `source_sha256`, `pointer`에서 찾는다.

`cases[].records`는 해당 사례의 발췌 문서다. 대부분은 `system`과 `eventdata`가 원래 `data.win`에서 선택된 평탄한 구조다. 1장 `original-alert-fields`만 원래 `data.win` 구조를 유지한다. 없는 값은 추정하여 채우지 않았다. `total`은 조회 전체 건수이고 `returned`는 보존한 수이므로 표본과 모집단을 구분한다.

부록의 CA-01~CA-04를 Windows PowerShell에서 실행하면 로컬 파일만 읽는다. 경보 인덱스에 업로드하거나 기존 경보를 덮어쓰는 절차는 포함하지 않는다. Windows 전체 이벤트·인덱스 매핑·규칙·수집 설정을 복원하는 스냅샷이 아니다.

9장은 별도의 발췌 JSON을 새로 만들지 않았다. 본문의 저장 화면·원문 발췌와 기존 복사용 예제를 사용한다. 12~13장의 90일 합성 원자료도 이 묶음에 포함되어 있지 않다. 69건의 실제 실습 조회와 합성 계산 연습을 구분한다.
''','utf8')

if __name__=='__main__':main()
