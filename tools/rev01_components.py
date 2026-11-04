"""부크크 원본 DOCX에서 첫 구역의 판형·여백·테마를 상속하는 저자용 조판기."""
import argparse

import json
from copy import deepcopy
from pathlib import Path
from docx import Document
from docx.shared import Mm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT

ROOT=Path(__file__).resolve().parents[1]
BODY='부크크 명조 Light'
HEAD='부크크 고딕 Light'
MONO='Consolas'

def font(r,name=BODY,size=10.5):
    r.font.name=name; r.font.size=Pt(size);r.font.color.rgb=RGBColor(0,0,0)
    rf=r._r.get_or_add_rPr().get_or_add_rFonts()
    for x in ['ascii','hAnsi','cs']:rf.set(qn('w:'+x),name)
    rf.set(qn('w:eastAsia'),BODY if name==MONO else name)
    return r

def runs(p,text,name,size):
    # **강조**는 제목·강조용 고딕으로 표시한다. 화면의 메뉴·버튼 이름에 쓴다.
    if '**' not in text or name==MONO:
        font(p.add_run(text),name,size);return
    for n,part in enumerate(text.split('**')):
        if part:font(p.add_run(part),HEAD if n%2 else name,size)

def para(parent,text='',size=10.5,name=BODY,after=6,keep=False,align=None,indent=0,hanging=0):
    p=parent.add_paragraph()
    pf=p.paragraph_format;pf.space_before=Pt(0);pf.space_after=Pt(after);pf.line_spacing=1.35
    pf.first_line_indent=Mm(-hanging);pf.left_indent=Mm(indent);pf.right_indent=Mm(0)
    pf.keep_with_next=keep;pf.keep_together=True;pf.widow_control=True
    p.alignment=align or WD_ALIGN_PARAGRAPH.LEFT
    snap=OxmlElement('w:snapToGrid');snap.set(qn('w:val'),'0');p._p.get_or_add_pPr().append(snap)
    runs(p,text,name,size)
    return p

def border(pr,tag='w:pBdr'):
    b=OxmlElement(tag)
    for side in ['top','left','bottom','right']:
        el=OxmlElement('w:'+side)
        for k,v in [('val','single'),('sz','4'),('space','4'),('color','000000')]:el.set(qn('w:'+k),v)
        b.append(el)
    pr.append(b)

def table(doc,block):
    widths=block.get('widths') or [40,87]
    t=doc.add_table(rows=1,cols=len(block['head']));t.autofit=False;t.alignment=WD_TABLE_ALIGNMENT.CENTER
    t.style='Normal Table'
    for col,w in zip(t.columns,widths):col.width=Mm(w)
    for n,vals in enumerate([block['head']]+block['rows']):
        row=t.rows[0] if n==0 else t.add_row()
        trpr=row._tr.get_or_add_trPr();trpr.append(OxmlElement('w:cantSplit'))
        if n==0:trpr.append(OxmlElement('w:tblHeader'))
        for cell,txt,w in zip(row.cells,vals,widths):
            cell.width=Mm(w);cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            pr=cell._tc.get_or_add_tcPr();border(pr,'w:tcBorders')
            for edge in pr.findall('.//'+qn('w:tcBorders')+'/*'):
                edge.attrib.pop(qn('w:space'),None)
            mar=OxmlElement('w:tcMar')
            for k,v in [('top',55),('bottom',55),('left',85),('right',85)]:
                e=OxmlElement('w:'+k);e.set(qn('w:w'),str(v));e.set(qn('w:type'),'dxa');mar.append(e)
            pr.append(mar)
            old=cell.paragraphs[0]
            cell._tc.remove(old._p)
            # keep=True인 표는 마지막 행 전까지 다음 행과 같은 쪽에 둔다.
            para(cell,txt,size=10,name=HEAD if n==0 else BODY,after=0,keep=bool(block.get('keep')) and n<len(block['rows']))
    para(doc,'',size=1,after=3).paragraph_format.line_spacing=1

BOX_LABEL={'predict':'먼저 예측','caution':'주의','blind':'보이지 않는 것','field':'현장 노트','answer':'해설'}

def box(doc,block):
    """상자 4종: 먼저 예측·주의·보이지 않는 것·현장 노트. 한 칸 표로 만들어 한 쪽에 둔다."""
    t=doc.add_table(rows=1,cols=1);t.autofit=False;t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.columns[0].width=Mm(127)
    row=t.rows[0];row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
    cell=t.cell(0,0);cell.width=Mm(127);pr=cell._tc.get_or_add_tcPr();border(pr,'w:tcBorders')
    for edge in pr.findall('.//'+qn('w:tcBorders')+'/*'):
        edge.attrib.pop(qn('w:space'),None)
    mar=OxmlElement('w:tcMar')
    for k,v in [('top',90),('bottom',70),('left',140),('right',140)]:
        e=OxmlElement('w:'+k);e.set(qn('w:w'),str(v));e.set(qn('w:type'),'dxa');mar.append(e)
    pr.append(mar)
    cell._tc.remove(cell.paragraphs[0]._p)
    label=block.get('title') or BOX_LABEL[block['kind']]
    para(cell,label,name=HEAD,size=10,after=3,keep=True)
    texts=block['text'] if isinstance(block.get('text'),list) else ([block['text']] if block.get('text') else [])
    for n,txt in enumerate(texts):para(cell,txt,size=10,after=3 if n<len(texts)-1 or block.get('items') else 1)
    for n,item in enumerate(block.get('items',[])):
        para(cell,'• '+item,size=10,after=2,indent=4,hanging=4)
    para(doc,'',size=1,after=5).paragraph_format.line_spacing=1

def items(doc,block):
    numbered=block.get('style')=='number'
    for n,item in enumerate(block['items']):
        mark=f'{n+1}. ' if numbered else '• '
        # 네 항목 이하의 짧은 목록만 한 쪽에 묶는다. 긴 목록은 쪽 사이에서 나뉠 수 있다.
        para(doc,mark+item,after=3 if n<len(block['items'])-1 else 7,indent=5,hanging=5,keep=len(block['items'])<=4 and n<len(block['items'])-1)
