# 해킹·침해대응 실무 with Wazuh 2권

가제: **Windows 침해 탐지와 통합 보안관제**

Module 01의 Windows 실습과 통합 보안관제, 장기 로그 분석을 책으로 구성하는 집필 저장소다. 1권의 실습 01~30·62에 이어 **31~61·63**을 다룬다. Module 02·03은 이번 범위에 포함하지 않는다.

지정 원전: https://docs.google.com/presentation/d/1o0H_2DDHBp8p2HvlSnEPbx6-jdURYzew

- [2권 작업 목차](editorial/volume02-plan.md)
- [1장 Windows 실습 환경과 로그 수집 DOCX](manuscript/volume02-chapter01.docx)
- [1장 원고 JSON](manuscript/volume02-chapter01.json)
- [2장 로그온 실패와 원격 접속 DOCX · 39쪽](manuscript/volume02-chapter02.docx)
- [3장 자격증명과 계정 권한의 변화 DOCX · 41쪽](manuscript/volume02-chapter03.docx)
- [2장 복사용 입력 36개](examples/chapter02/README.md) · [3장 복사용 입력 33개](examples/chapter03/README.md)
- [2장 집필·검토 기록](editorial/chapter02-review.md) · [3장 집필·검토 기록](editorial/chapter03-review.md)
- [1·2권 삽화 전체 점검](editorial/illustration-audit.md)
- [복사용 명령과 검색식](examples/chapter01/README.md)
- [출처와 검증 범위](editorial/chapter01-review.md)

현재는 **1~3장 초안**이다. 2장은 실습 31~34, 3장은 35~37·50을 다룬다. 제한된 실습 입력, 원본 이벤트, Wazuh 검색·화면, 조사·대응과 원상복구를 확인했다. 실제 해시 공격이나 원격 이동을 수행한 것으로 표현하지 않는다. 나머지 장은 작업 목차에 배분했다. 챕터별 DOCX를 제공하며 합본과 배포용 PDF는 만들지 않는다. REV01과 강의 저장소는 수정하지 않았다.

사용자 요청에 따라 1·2권 인물 삽화를 전부 점검해 반복 배치 15곳을 교체했다. 2·3장의 신규 4곳을 포함해 현재 27곳에 서로 다른 그림 27개를 사용한다. 화풍을 유지하며 인물·장소·행동·소품을 달리했다. 생성 프롬프트와 출처는 editorial의 삽화 기록에 있다.

## 재생성

Python에 python-docx와 Pillow가 필요하다. tools/assets/bookk-B5.docx와 본문 지정 글꼴을 사용한다.

```powershell
python tools/create_chapter01.py
python tools/build_chapter01.py
python tools/create_chapter02.py
python tools/build_chapter02.py
python tools/create_chapter03.py
python tools/build_chapter03.py
```

조판 검사는 Windows Word에서 tools/render_word.ps1로 build 내부 PDF를 만든 뒤 tools/render_pages.py로 전체 페이지를 렌더한다. Python 렌더에는 pypdfium2·pypdf가 필요하다. PDF와 페이지 PNG는 검토용이며 배포하지 않는다.
