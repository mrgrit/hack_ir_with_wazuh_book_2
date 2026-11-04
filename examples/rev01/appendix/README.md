# 부록 복사용 입력

CA-01~04는 저장소 루트에서 실행하는 로컬 PowerShell 읽기다. QA-01~04는 Wazuh Discover의 DQL이다. investigation-template.md는 조사 기록 양식이다. 예시 주소·기간·계정은 자신의 원문에서 확인한다.

- [CA-01.txt](CA-01.txt) — 보존 자료 목록
- [CA-02.txt](CA-02.txt) — SHA-256 대조
- [CA-03.txt](CA-03.txt) — 1장의 경보 제목과 원본 로그온 필드
- [CA-04.txt](CA-04.txt) — 6장의 archives 6건·alerts 0건

부록 J를 먼저 읽고 CA-01부터 같은 PowerShell 창에서 순서대로 실행한다. 로컬 자료는 [records](../records/README.md)에 있다.

## 분석 보강 입력

기간·데이터 보기·ID는 본문의 절차와 맞춘다. 0건은 선택한 보존 범위의 결과다.

- [QA-01.dql](QA-01.dql) — Windows PC · Wazuh Discover · wazuh-alerts-* · DQL · 출발지와 자동 대응 필드
- [QA-02.dql](QA-02.dql) — Windows PC · Wazuh Discover · wazuh-alerts-* · DQL · 검색 예와 오류 점검
- [QA-03.dql](QA-03.dql) — Windows PC · Wazuh Discover · wazuh-alerts-* · DQL · 검색 예와 오류 점검
- [QA-04.dql](QA-04.dql) — Windows PC · Wazuh Discover · wazuh-alerts-* · DQL · 검색 예와 오류 점검

식별자 충돌과 6장 조사표의 완성 예시는 부록 G 보충을 따른다. 이번 보강의 새 부록 검색식은 없다.
