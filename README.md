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
- [9장 호스트 이상과 파일 판정 DOCX · 40쪽](manuscript/volume02-chapter09.docx)
- [10장 수집 장애와 자동 대응 DOCX · 19쪽](manuscript/volume02-chapter10.docx)
- [11장 네트워크 경보와 일일 관제 DOCX · 18쪽](manuscript/volume02-chapter11.docx)
- [12장 장기 로그의 피벗과 집계 DOCX · 25쪽](manuscript/volume02-chapter12.docx)
- [13장 시간 흐름과 위험도 평가 DOCX · 21쪽](manuscript/volume02-chapter13.docx)
- [부록 필드·검색·조사 점검표 DOCX · 17쪽](manuscript/volume02-appendix.docx)
- [10장 입력 17개](examples/chapter10/README.md) · [11장 입력 14개](examples/chapter11/README.md)
- [12장 입력 20개·IP 비교표](examples/chapter12/README.md) · [13장 입력 6개·계산 연습](examples/chapter13/README.md)
- [부록 검색 4개·조사 양식](examples/appendix/README.md) · [10~13장·부록 집필과 검토 기록](editorial/remaining-review.md)
- [2장 복사용 입력 36개](examples/chapter02/README.md) · [3장 복사용 입력 33개](examples/chapter03/README.md)
- [2장 집필·검토 기록](editorial/chapter02-review.md) · [3장 집필·검토 기록](editorial/chapter03-review.md)
- [4장 복사용 입력 33개](examples/chapter04/README.md) · [5장 복사용 입력 30개](examples/chapter05/README.md)
- [4장 집필·검토 기록](editorial/chapter04-review.md) · [5장 집필·검토 기록](editorial/chapter05-review.md)
- [6장 복사용 입력 25개](examples/chapter06/README.md) · [6장 집필·검토 기록](editorial/chapter06-review.md)
- [7장 복사용 입력 26개](examples/chapter07/README.md) · [7장 집필·검토 기록](editorial/chapter07-review.md)
- [8장 복사용 입력 20개](examples/chapter08/README.md) · [8장 집필·검토 기록](editorial/chapter08-review.md)
- [9장 복사용 입력 28개](examples/chapter09/README.md) · [9장 집필·검토 기록](editorial/chapter09-review.md)
- [1·2권 삽화 전체 점검](editorial/illustration-audit.md)
- [복사용 명령과 검색식](examples/chapter01/README.md)
- [출처와 검증 범위](editorial/chapter01-review.md)

현재는 **13장과 부록의 초안**을 갖추었다. 챕터별 교정과 출판 검토는 별도로 진행한다. 2장은 실습 31~34, 3장은 35~37·50, 4장은 39·40·44·63, 5장은 41·42·45·46, 6장은 43·47·48, 7장은 38·49, 8장은 51~53, 9장은 54~56을 다룬다. 제한된 실습 입력, 원본 이벤트, Wazuh 검색·화면, 조사·대응과 원상복구를 확인했다. 4·5장은 서비스·작업·Run 등록과 문구 출력·파일 변환·모의 부모 프로그램을 관찰했다. 실제 악성코드·Office 매크로·자격증명 탈취를 실행한 결과로 표현하지 않는다. 상세 범위와 미실행 절차는 각 장 검토 기록을 따른다. 6장은 기존 LSASS 접근과 정상 HTTP·DNS 기록을 대조했다. LSASS 덤프·자격증명 추출·보호 해제는 원전 분석으로 한정했다. 7장은 로그 삭제의 관측 한계와 Defender 탐지·조치·현재 상태를 분석했다. 새 로그 삭제·보호 해제·EICAR 생성 없이 기존 기록 조회와 EVTX 사본 보존을 확인했다. 8장은 취약점 현재 상태·설치 패키지·제조사 공지와 SCA 검사식을 대조했다. 공격·패치·SSH/방화벽 변경 없이 조회와 보완 계획을 작성했다. 9장은 Rootcheck 권한 경보와 VirusTotal·ClamAV의 파일 판정을 연결했다. 현재 상태·검색을 확인하고 원전의 탐지 사례와 구분했다. 새 공격·EICAR 생성·검사·삭제·VirusTotal 활성화·외부 조회는 수행하지 않았다. 10·11장은 실습 57~61의 수집 장애·자동 대응·Suricata·MITRE·일일 관제를 다룬다. 12·13장과 부록은 같은 Module 01 후반부의 장기 로그·집계·위험도·점검표다. 새 공격·수집 중지·설정 변경·합성 자료 적재 없이 기존 기록과 읽기 검색을 확인했다. 10~13장과 부록은 합계 100쪽, 복사용 입력 61개이며 현재 없는 합성 자료는 원전 결과·가정값 연습과 구분한다. 챕터별 DOCX를 제공하며 합본과 배포용 PDF는 만들지 않는다. REV01과 강의 저장소는 수정하지 않았다.

사용자 요청에 따라 1·2권 인물 삽화를 전부 점검해 반복 배치 15곳을 교체했다. 당시 27곳에 서로 다른 그림 27개를 사용했고, 4·5장에 새 그림 4개, 6·7·8·9장에 새 그림을 각각 2개 추가했다. 화풍을 유지하며 인물·장소·행동·소품을 달리했다. 팔·손 수와 문서·화면의 방향을 원본 및 실제 지면에서 확인했다. 10~13장에는 새 그림 네 개를 추가했으며 세 개는 사무실의 기록·분석·회의 장면이다. 11장의 몸통·다리 연결이 어색한 최초 생성본은 교정본으로 교체했다. 생성 프롬프트와 출처는 editorial의 삽화 기록에 있다.

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
python tools/create_chapter09.py
python tools/build_chapter09.py
python tools/create_chapter10.py
python tools/create_chapter11.py
python tools/create_chapter12.py
python tools/create_chapter13.py
python tools/create_appendix.py
python tools/complete_remaining_examples.py
python tools/build_remaining.py
```

조판 검사는 Windows Word에서 tools/render_word.ps1로 build 내부 PDF를 만든 뒤 tools/render_pages.py로 전체 페이지를 렌더한다. Python 렌더에는 pypdfium2·pypdf가 필요하다. PDF와 페이지 PNG는 검토용이며 배포하지 않는다.
