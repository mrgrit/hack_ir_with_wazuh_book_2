# 13장 복사용 입력

본문의 실행 위치·선행 조건을 읽고 한 블록씩 입력한다. 예시 주소·계정·시각·ID는 자신의 기록으로 바꾼다. 전체 파일을 일괄 실행하지 않는다.

hourly-risk.http는 D13-01·02를 합친 GET 요청이다. score-worked.csv의 A~E 및 hourly-worked.csv는 산식 확인용 가정값이다. 실제 IP·탐지 성능 측정값이 아니다. 빈 값은 미확인이며 0과 구분한다. rule-weight-worked.csv는 원전 인쇄 입력값의 재계산이다.

- [Q13-01.dql](Q13-01.dql) — Windows PC · Wazuh Discover · wazuh-alerts-* · DQL
- [Q13-02.dql](Q13-02.dql) — Windows PC · Wazuh Discover · wazuh-alerts-* · DQL
- [Q13-03.dql](Q13-03.dql) — Windows PC · Wazuh Discover · wazuh-alerts-* · DQL
- [D13-01.txt](D13-01.txt) — Windows PC · Wazuh · Indexer management → Dev Tools
- [D13-02.txt](D13-02.txt) — Windows PC · Wazuh · Indexer management → Dev Tools
- [Q13-04.dql](Q13-04.dql) — Windows PC · Wazuh Discover · wazuh-alerts-* · DQL

## 분석 보강 입력

기간·데이터 보기·ID는 본문의 절차와 맞춘다. 0건은 선택한 보존 범위의 결과다.

- [Q13-05.dql](Q13-05.dql) — Windows PC · Wazuh Discover · wazuh-alerts-* · DQL · 시간 점수의 구성 문서로 되돌아가기
- [Q13-06.dql](Q13-06.dql) — Windows PC · Wazuh Discover · wazuh-alerts-* · DQL · 시간 점수의 구성 문서로 되돌아가기
- [Q13-07.dql](Q13-07.dql) — Windows PC · Wazuh Discover · wazuh-alerts-* · DQL · 과거 조회 0건과 신규 주소 판정

- [observed-hour.http](observed-hour.http) — 보존된 실제 IP 사례의 완성 GET 요청. 합성 자료 요청과 별도로 사용한다. [입력 기록](analysis-inputs.json).
