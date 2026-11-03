# 해킹·침해대응 실무 with Wazuh 2권

가제: **Windows 침해 탐지와 통합 보안관제**

Module 01의 Windows 실습과 통합 보안관제, 장기 로그 분석을 책으로 구성하는 집필 저장소다. 1권의 실습 01~30·62에 이어 **31~61·63**을 다룬다. Module 02·03은 이번 범위에 포함하지 않는다.

지정 원전: https://docs.google.com/presentation/d/1o0H_2DDHBp8p2HvlSnEPbx6-jdURYzew

- [2권 작업 목차](editorial/volume02-plan.md)
- [1장 Windows 실습 환경과 로그 수집 DOCX](manuscript/volume02-chapter01.docx)
- [1장 원고 JSON](manuscript/volume02-chapter01.json)
- [복사용 명령과 검색식](examples/chapter01/README.md)
- [출처와 검증 범위](editorial/chapter01-review.md)

현재는 **1장 초안**이다. 나머지 장은 작업 목차에 배분했다. 챕터별 교정용 DOCX를 제공하며 합본과 배포용 PDF는 만들지 않는다. 1권·REV01·강의 저장소는 수정하지 않는다.

## 재생성

Python에 python-docx와 Pillow가 필요하다. tools/assets/bookk-B5.docx와 본문 지정 글꼴을 사용한다.

```powershell
python tools/create_chapter01.py
python tools/build_chapter01.py
```

조판 검사는 Windows Word에서 tools/render_word.ps1로 build 내부 PDF를 만든 뒤 tools/render_pages.py로 전체 페이지를 렌더한다. Python 렌더에는 pypdfium2·pypdf가 필요하다. PDF와 페이지 PNG는 검토용이며 배포하지 않는다.
