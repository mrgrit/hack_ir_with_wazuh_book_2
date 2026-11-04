# 2장 복사용 예제

본문의 선행 확인 뒤 한 명령씩 입력한다. 전체를 자동 실행하지 않는다.

- C02-04: kt66 Ubuntu 호스트. 이후 ATT 표시는 컨테이너 안이다.
- WIN 표시는 Windows 실습 게스트의 관리자 PowerShell이다.
- C02-08의 $start는 각 실습 시작에 갱신한다. 같은 창에서 조회한다.
- C02-19·23·25·25A·26A는 본문 조건에 해당할 때만 실행한다.
- Q02는 Wazuh Discover DQL이다. 실습 시간 범위를 함께 맞춘다.
- Victim!2026은 kt66 기준 코드의 공개 실습용 값이다. 개인 암호를 파일에 저장하지 않는다.

- [C02-01.txt](C02-01.txt) — Windows 실습 게스트 · 관리자 PowerShell
- [C02-02.txt](C02-02.txt) — Windows 실습 게스트 · 관리자 PowerShell
- [C02-03.txt](C02-03.txt) — Windows 실습 게스트 · 관리자 PowerShell
- [C02-04.txt](C02-04.txt) — kt66 Ubuntu VM · 터미널
- [C02-05.txt](C02-05.txt) — kt66-attacker 컨테이너 · Bash
- [C02-06.txt](C02-06.txt) — kt66-attacker 컨테이너 · Bash
- [C02-07.txt](C02-07.txt) — kt66-attacker 컨테이너 · Bash
- [C02-08.txt](C02-08.txt) — Windows 실습 게스트 · 관리자 PowerShell
- [C02-09.txt](C02-09.txt) — kt66-attacker 컨테이너 · Bash
- [C02-10.txt](C02-10.txt) — kt66-attacker 컨테이너 · Bash
- [C02-11.txt](C02-11.txt) — Windows 실습 게스트 · 관리자 PowerShell
- [Q02-01.dql](Q02-01.dql) — Windows PC · Wazuh Discover · DQL
- [Q02-02.dql](Q02-02.dql) — Windows PC · Wazuh Discover · DQL
- [C02-12.txt](C02-12.txt) — Windows 실습 게스트 · 관리자 PowerShell
- [C02-13.txt](C02-13.txt) — kt66-attacker 컨테이너 · Bash
- [C02-14.txt](C02-14.txt) — kt66-attacker 컨테이너 · Bash
- [Q02-03.dql](Q02-03.dql) — Windows PC · Wazuh Discover · DQL
- [C02-15.txt](C02-15.txt) — kt66-attacker 컨테이너 · Bash
- [C02-16.txt](C02-16.txt) — kt66-attacker 컨테이너 · Bash
- [C02-17.txt](C02-17.txt) — Windows 실습 게스트 · 관리자 PowerShell
- [Q02-04.dql](Q02-04.dql) — Windows PC · Wazuh Discover · DQL
- [Q02-05.dql](Q02-05.dql) — Windows PC · Wazuh Discover · DQL
- [C02-18.txt](C02-18.txt) — kt66-attacker 컨테이너 · Bash
- [C02-19.txt](C02-19.txt) — kt66-attacker 컨테이너 · Bash
- [C02-20.txt](C02-20.txt) — kt66-attacker 컨테이너 · Bash
- [C02-21.txt](C02-21.txt) — Windows 실습 게스트 · 관리자 PowerShell
- [Q02-06.dql](Q02-06.dql) — Windows PC · Wazuh Discover · DQL
- [C02-22.txt](C02-22.txt) — Windows 실습 게스트 · 관리자 PowerShell
- [C02-23.txt](C02-23.txt) — Windows 실습 게스트 · 관리자 PowerShell
- [Q02-07.dql](Q02-07.dql) — Windows PC · Wazuh Discover · DQL
- [C02-24.txt](C02-24.txt) — kt66-attacker 컨테이너 · Bash
- [C02-25.txt](C02-25.txt) — kt66-attacker 컨테이너 · Bash
- [C02-25A.txt](C02-25A.txt) — kt66-attacker 컨테이너 · Bash
- [C02-26.txt](C02-26.txt) — kt66-attacker 컨테이너 · Bash
- [C02-26A.txt](C02-26A.txt) — kt66-attacker 컨테이너 · Bash
- [C02-27.txt](C02-27.txt) — kt66-attacker 컨테이너 · Bash

## 분석 보강 입력

기간·데이터 보기·ID는 본문의 절차와 맞춘다. 0건은 선택한 보존 범위의 결과다.

- [Q02-08.dql](Q02-08.dql) — Windows PC · Wazuh Discover · wazuh-archives-* · DQL · 로그온 뒤 같은 세션의 종료 확인
