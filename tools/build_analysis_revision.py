"""기존 그림을 보존하며 보강한 장별 DOCX를 만든다."""
from pathlib import Path
import shutil,json,hashlib
from docx import Document
from revise_analysis import apply_existing
from layout import build
ROOT=Path(__file__).resolve().parents[1]
def main():
 out=ROOT/'build/analysis-revision';base=out/'baseline';base.mkdir(parents=True,exist_ok=True)
 for f in sorted((ROOT/'manuscript').glob('*.docx')):
  if not (base/f.name).exists():shutil.copy2(f,base/f.name)
 apply_existing()
 for ch in list(range(1,14))+['appendix']:
  stem='appendix' if ch=='appendix' else f'chapter{ch:02}'
  f=ROOT/f'manuscript/volume02-{stem}.docx'
  build(f,f.with_suffix('.json'))
  d=Document(f);d.paragraphs[0].style=d.styles['Title'];d.save(f)
if __name__=='__main__':main()
