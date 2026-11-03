# 해킹·침해대응 실무 with Wazuh 2권

가제: **Windows 침해 탐지와 통합 보안관제**

Module 01의 Windows 실습과 통합 보안관제, 장기 로그 분석을 책으로 구성하는 집필 저장소다. 1권의 실습 01~30·62에 이어 **31~61·63**을 다룬다. Module 02·03은 이번 범위에 포함하지 않는다.

지정 원전: https://docs.google.com/presentation/d/1o0H_2DDHBp8p2HvlSnEPbx6-jdURYzew

- [2권 작업 목차](editorial/volume02-plan.md)
- [1장 Windows 실습 환경과 로그 수집 DOCX](manuscript/volume02-chapter01.docx)
- [1장 원고 JSON](manuscript/volume02-chapter01.json)
- [2장 로그온 실패와 원격 접속 DOCX · 39쪽](manuscript/volume02-chapter02.docx)
- [3장 자격증명과 계정 권한의 변화 DOCX · 41쪽](manuscript/volume02-chapter03.docx)
- [4장 서비스와 작업을 이용한 지속화 DOCX · 36쪽](manuscript/volume02-chapter04.docx)
- [5장 PowerShell과 정상 프로그램 악용 DOCX · 36쪽](manuscript/volume02-chapter05.docx)
- [6장 자격증명 접근과 외부 통신 DOCX · 38쪽](manuscript/volume02-chapter06.docx)
- [7장 로그 삭제와 보호 기능의 대응 DOCX · 35쪽](manuscript/volume02-chapter07.docx)
- [8장 취약점과 보안 설정의 우선순위 DOCX · 34쪽](manuscript/volume02-chapter08.docx)
- [2장 복사용 입력 36개](examples/chapter02/README.md) · [3장 복사용 입력 33개](examples/chapter03/README.md)
- [2장 집필·검토 기록](editorial/chapter02-review.md) · [3장 집필·검토 기록](editorial/chapter03-review.md)
- [4장 복사용 입력 33개](examples/chapter04/README.md) · [5장 복사용 입력 30개](examples/chapter05/README.md)
- [4장 집필·검토 기록](editorial/chapter04-review.md) · [5장 집필·검토 기록](editorial/chapter05-review.md)
- [6장 복사용 입력 25개](examples/chapter06/README.md) · [6장 집필·검토 기록](editorial/chapter06-review.md)
- [7장 복사용 입력 26개](examples/chapter07/README.md) · [7장 집필·검토 기록](editorial/chapter07-review.md)
- [8장 복사용 입력 20개](examples/chapter08/README.md) · [8장 집필·검토 기록](editorial/chapter08-review.md)
- [1·2권 삽화 전체 점검](editorial/illustration-audit.md)
- [복사용 명령과 검색식](examples/chapter01/README.md)
- [출처와 검증 범위](editorial/chapter01-review.md)

현재는 **1~8장 초안**이다. 2장은 실습 31~34, 3장은 35~37·50, 4장은 39·40·44·63, 5장은 41·42·45·46, 6장은 43·47·48, 7장은 38·49, 8장은 51~53을 다룬다. 제한된 실습 입력, 원본 이벤트, Wazuh 검색·화면, 조사·대응과 원상복구를 확인했다. 4·5장은 서비스·작업·Run 등록과 문구 출력·파일 변환·모의 부모 프로그램을 관찰했다. 실제 악성코드·Office 매크로·자격증명 탈취를 실행한 결과로 표현하지 않는다. 상세 범위와 미실행 절차는 각 장 검토 기록을 따른다. 6장은 기존 LSASS 접근과 정상 HTTP·DNS 기록을 대조했다. LSASS 덤프·자격증명 추출·보호 해제는 원전 분석으로 한정했다. 7장은 로그 삭제의 관측 한계와 Defender 탐지·조치·현재 상태를 분석했다. 새 로그 삭제·보호 해제·EICAR 생성 없이 기존 기록 조회와 EVTX 사본 보존을 확인했다. 8장은 취약점 현재 상태·설치 패키지·제조사 공지와 SCA 검사식을 대조했다. 공격·패치·SSH/방화벽 변경 없이 조회와 보완 계획을 작성했다. 나머지 장은 작업 목차에 배분했다. 챕터별 DOCX를 제공하며 합본과 배포용 PDF는 만들지 않는다. REV01과 강의 저장소는 수정하지 않았다.

사용자 요청에 따라 1·2권 인물 삽화를 전부 점검해 반복 배치 15곳을 교체했다. 당시 27곳에 서로 다른 그림 27개를 사용했고, 4·5장에 새 그림 4개, 6·7·8장에 새 그림을 각각 2개 추가했다. 화풍을 유지하며 인물·장소·행동·소품을 달리했다. 팔·손 수와 문서·화면의 방향을 원본 및 실제 지면에서 확인했다. 생성 프롬프트와 출처는 editorial의 삽화 기록에 있다.

## 재생성

Python에 python-docx와 Pillow가 필요하다. tools/assets/bookk-B5.docx와 본문 지정 글꼴을 사용한다.

```powershell
python tools/create_chapter01.py
python tools/build_chapter01.py
python tools/create_chapter02.py
python tools/build_chapter02.py
python tools/create_chapter03.py
python tools/build_chapter03.py
python tools/create_chapter04.py
python tools/build_chapter04.py
python tools/create_chapter05.py
python tools/build_chapter05.py
python tools/create_chapter06.py
python tools/build_chapter06.py
python tools/create_chapter07.py
python tools/build_chapter07.py
python tools/create_chapter08.py
python tools/build_chapter08.py
```

조판 검사는 Windows Word에서 tools/render_word.ps1로 build 내부 PDF를 만든 뒤 tools/render_pages.py로 전체 페이지를 렌더한다. Python 렌더에는 pypdfium2·pypdf가 필요하다. PDF와 페이지 PNG는 검토용이며 배포하지 않는다.
