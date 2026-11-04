# 3장 복사용 입력

본문의 사전 확인과 함께 한 블록씩 사용한다. 전체를 자동 실행하지 않는다.

- WIN: Windows 실습 게스트 관리자 PowerShell. HOST: kt66 Ubuntu VM. SIEM: 진입한 kt66-siem Bash.
- C03-03을 각 실습 시작에 갱신한다. 같은 창의 변수와 생성 객체를 유지한다.
- C03-08을 정의한 뒤 C03-09를 실행하고 핸들을 닫는다. 외부 인증을 수행하지 않는다.
- C03-14 삭제는 이번 실습 연결이 있을 때만 수행한다.
- C03-15에서 계정 부재와 사전 구성원을 확인한 뒤 생성한다. C03-18·19로 원상복구한다.
- C03-22는 사전 Success and Failure인 실습 게스트에서만 수행하고 즉시 원상복구한다.
- Q03-03·Q03-09는 wazuh-archives-*, 나머지는 본문의 wazuh-alerts-*에서 사용한다. 번호·SID·로그온 ID는 자신의 기록으로 바꾼다.

- [C03-01.txt](C03-01.txt) — Windows 실습 게스트 · 관리자 PowerShell
- [C03-02.txt](C03-02.txt) — Windows 실습 게스트 · 관리자 PowerShell
- [C03-03.txt](C03-03.txt) — Windows 실습 게스트 · 관리자 PowerShell
- [C03-04.txt](C03-04.txt) — Windows 실습 게스트 · 관리자 PowerShell
- [C03-05.txt](C03-05.txt) — Windows 실습 게스트 · 관리자 PowerShell
- [C03-06.txt](C03-06.txt) — Windows 실습 게스트 · 관리자 PowerShell
- [Q03-01.dql](Q03-01.dql) — Windows PC · Wazuh Discover · DQL
- [C03-07.txt](C03-07.txt) — Windows 실습 게스트 · 관리자 PowerShell
- [C03-08.txt](C03-08.txt) — Windows 실습 게스트 · 관리자 PowerShell
- [C03-09.txt](C03-09.txt) — Windows 실습 게스트 · 관리자 PowerShell
- [Q03-02.dql](Q03-02.dql) — Windows PC · Wazuh Discover · DQL
- [C03-10.txt](C03-10.txt) — Windows 실습 게스트 · 관리자 PowerShell
- [C03-11.txt](C03-11.txt) — Windows 실습 게스트 · 관리자 PowerShell
- [C03-11A.txt](C03-11A.txt) — Windows 실습 게스트 · 관리자 PowerShell
- [C03-12.txt](C03-12.txt) — kt66 Ubuntu VM · 터미널
- [C03-13.txt](C03-13.txt) — kt66-siem 컨테이너 · Bash
- [Q03-03.dql](Q03-03.dql) — Windows PC · Wazuh Discover · DQL
- [C03-14.txt](C03-14.txt) — Windows 실습 게스트 · 관리자 PowerShell
- [C03-15.txt](C03-15.txt) — Windows 실습 게스트 · 관리자 PowerShell
- [C03-16.txt](C03-16.txt) — Windows 실습 게스트 · 관리자 PowerShell
- [C03-17.txt](C03-17.txt) — Windows 실습 게스트 · 관리자 PowerShell
- [C03-18.txt](C03-18.txt) — Windows 실습 게스트 · 관리자 PowerShell
- [C03-19.txt](C03-19.txt) — Windows 실습 게스트 · 관리자 PowerShell
- [C03-20.txt](C03-20.txt) — Windows 실습 게스트 · 관리자 PowerShell
- [Q03-04.dql](Q03-04.dql) — Windows PC · Wazuh Discover · DQL
- [Q03-05.dql](Q03-05.dql) — Windows PC · Wazuh Discover · DQL
- [C03-21.txt](C03-21.txt) — Windows 실습 게스트 · 관리자 PowerShell
- [C03-22.txt](C03-22.txt) — Windows 실습 게스트 · 관리자 PowerShell
- [C03-23.txt](C03-23.txt) — Windows 실습 게스트 · 관리자 PowerShell
- [Q03-06.dql](Q03-06.dql) — Windows PC · Wazuh Discover · DQL
- [C03-24.txt](C03-24.txt) — Windows 실습 게스트 · 관리자 PowerShell
- [Q03-07.dql](Q03-07.dql) — Windows PC · Wazuh Discover · DQL
- [Q03-08.dql](Q03-08.dql) — Windows PC · Wazuh Discover · DQL

## 분석 보강 입력

기간·데이터 보기·ID는 본문의 절차와 맞춘다. 0건은 선택한 보존 범위의 결과다.

- [Q03-09.dql](Q03-09.dql) — Windows PC · Wazuh Discover · wazuh-archives-* · DQL · 만든 계정이 실제로 사용되었는지 확인
