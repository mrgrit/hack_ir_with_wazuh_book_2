# 12장 복사용 입력

본문의 실행 위치·선행 조건을 읽고 한 블록씩 입력한다. 예시 주소·계정·시각·ID는 자신의 기록으로 바꾼다. 전체 파일을 일괄 실행하지 않는다.

ip-profile.http는 D12-03·04를 합친 GET 요청이다. CSV는 빈 조사 양식이다. C12-02 파일 생성은 선택 절차이며 저자는 실행하지 않았다. 데이터가 없으면 강사에게 준비 범위를 확인한다.

- [C12-01.txt](C12-01.txt) — kt66 Ubuntu VM · 터미널
- [C12-02.txt](C12-02.txt) — kt66 Ubuntu VM · 터미널
- [C12-03.txt](C12-03.txt) — kt66 Ubuntu VM · 터미널
- [Q12-01.dql](Q12-01.dql) — Windows PC · Wazuh Discover · wazuh-alerts-* · DQL
- [Q12-02.dql](Q12-02.dql) — Windows PC · Wazuh Discover · wazuh-alerts-* · DQL
- [Q12-03.dql](Q12-03.dql) — Windows PC · Wazuh Discover · wazuh-alerts-* · DQL
- [Q12-04.dql](Q12-04.dql) — Windows PC · Wazuh Discover · wazuh-alerts-* · DQL
- [Q12-05.dql](Q12-05.dql) — Windows PC · Wazuh Discover · wazuh-alerts-* · DQL
- [Q12-06.dql](Q12-06.dql) — Windows PC · Wazuh Discover · wazuh-alerts-* · DQL
- [Q12-07.dql](Q12-07.dql) — Windows PC · Wazuh Discover · wazuh-alerts-* · DQL
- [Q12-08.dql](Q12-08.dql) — Windows PC · Wazuh Discover · wazuh-alerts-* · DQL
- [Q12-09.dql](Q12-09.dql) — Windows PC · Wazuh Discover · wazuh-alerts-* · DQL
- [Q12-10.dql](Q12-10.dql) — Windows PC · Wazuh Discover · wazuh-alerts-* · DQL
- [Q12-11.dql](Q12-11.dql) — Windows PC · Wazuh Discover · wazuh-alerts-* · DQL
- [Q12-12.dql](Q12-12.dql) — Windows PC · Wazuh Discover · wazuh-alerts-* · DQL
- [D12-01.txt](D12-01.txt) — Windows PC · Wazuh · Indexer management → Dev Tools
- [D12-02.txt](D12-02.txt) — Windows PC · Wazuh · Indexer management → Dev Tools
- [D12-03.txt](D12-03.txt) — Windows PC · Wazuh · Indexer management → Dev Tools
- [D12-04.txt](D12-04.txt) — Windows PC · Wazuh · Indexer management → Dev Tools
- [D12-05.txt](D12-05.txt) — Windows PC · Wazuh · Indexer management → Dev Tools

## 분석 보강 입력

기간·데이터 보기·ID는 본문의 절차와 맞춘다. 0건은 선택한 보존 범위의 결과다.

- [Q12-13.dql](Q12-13.dql) — Windows PC · Wazuh Discover · wazuh-alerts-* · DQL · 보존된 한 IP로 집계 결과까지 확인
- [Q12-14.dql](Q12-14.dql) — Windows PC · Wazuh Discover · wazuh-alerts-* · DQL · 집계에서 원문과 시간 간격으로 돌아가기

- [observed-ip-profile.http](observed-ip-profile.http) — 보존된 실제 IP 사례의 완성 GET 요청. 합성 자료 요청과 별도로 사용한다. [입력 기록](analysis-inputs.json).
