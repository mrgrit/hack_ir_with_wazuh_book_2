"""REV01 배포물의 링크·입력 색인·최종 파일 해시 검사."""
from pathlib import Path
import re,json,csv,hashlib

ROOT=Path(__file__).resolve().parents[1]

def main():
    errors=[];links=0
    files=[ROOT/'README.md']+list((ROOT/'manuscript/REV01').glob('*.md'))+list((ROOT/'examples/rev01').rglob('*.md'))+list((ROOT/'editorial/REV01').glob('*.md'))
    for f in files:
        for target in re.findall(r'\]\(([^)]+)\)',f.read_text('utf8')):
            if re.match(r'https?://|#',target):continue
            links+=1
            if not (f.parent/target.split('#')[0]).resolve().exists():errors.append([f.relative_to(ROOT).as_posix(),target])
    manifest=json.loads((ROOT/'editorial/REV01/output-manifest.json').read_text('utf8'))
    for d in manifest['documents']:
        for fmt in ['json','docx']:
            if hashlib.sha256((ROOT/d[fmt]).read_bytes()).hexdigest()!=d[fmt+'_sha256']:errors.append(['hash',d[fmt]])
    with (ROOT/'examples/rev01/input-index.csv').open(encoding='utf-8-sig') as f:index=list(csv.DictReader(f))
    if len(index)!=manifest['total_inputs']:errors.append(['input index count',len(index)])
    for row in index:
        if not (ROOT/'examples/rev01'/row['파일']).exists():errors.append(['input file',row['파일']])
    result={'links_checked':links,'input_index':len(index),'errors':errors}
    (ROOT/'editorial/REV01/package-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if errors:raise SystemExit(1)

if __name__=='__main__':main()
