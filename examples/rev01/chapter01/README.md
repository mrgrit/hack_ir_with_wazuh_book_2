# 1장 복사용 예제

본문 순서에 맞춰 각 파일의 명령을 한 줄 또는 한 명령 블록씩 입력한다. 전체 실습을 자동 실행하는 스크립트가 아니다. 실행 위치와 선행 변수는 본문에서 먼저 확인한다.

- C01-01·14: kt66 Ubuntu VM.
- C01-15: C01-14로 들어간 kt66-siem 컨테이너. exit로 나온다.
- 나머지 C01: Windows **실습 게스트**의 관리자 PowerShell. 독자의 Windows PC와 구분한다.
- C01-09는 C01-08의 $event, C01-11은 C01-10의 $processEvent, C01-13은 C01-12의 $agentDir를 같은 창에서 사용한다.
- Q01: Wazuh Discover의 DQL 검색창. 명령 셸에서 실행하지 않는다.
- Q01-03의 기록 번호·컴퓨터 이름은 자신의 관찰 값으로 바꾼다. 검색 기간도 맞춘다.

| 파일 | 실행 위치 |
|---|---|
| [C01-01.txt](C01-01.txt) | kt66 Ubuntu VM의 터미널 |
| [C01-02.txt](C01-02.txt) | Windows 실습 게스트의 관리자 PowerShell |
| [C01-03.txt](C01-03.txt) | Windows 실습 게스트의 관리자 PowerShell |
| [C01-04.txt](C01-04.txt) | Windows 실습 게스트의 관리자 PowerShell |
| [C01-05.txt](C01-05.txt) | Windows 실습 게스트의 관리자 PowerShell |
| [C01-06.txt](C01-06.txt) | Windows 실습 게스트의 관리자 PowerShell |
| [C01-07.txt](C01-07.txt) | Windows 실습 게스트의 관리자 PowerShell |
| [C01-08.txt](C01-08.txt) | Windows 실습 게스트의 관리자 PowerShell |
| [C01-09.txt](C01-09.txt) | Windows 실습 게스트의 관리자 PowerShell |
| [C01-10.txt](C01-10.txt) | Windows 실습 게스트의 관리자 PowerShell |
| [C01-11.txt](C01-11.txt) | Windows 실습 게스트의 관리자 PowerShell |
| [C01-12.txt](C01-12.txt) | Windows 실습 게스트의 관리자 PowerShell |
| [C01-13.txt](C01-13.txt) | Windows 실습 게스트의 관리자 PowerShell |
| [C01-14.txt](C01-14.txt) | kt66 Ubuntu VM의 터미널 |
| [C01-15.txt](C01-15.txt) | kt66-siem 컨테이너의 Bash |
| [Q01-01.dql](Q01-01.dql) | Windows PC의 Wazuh Discover 검색창 |
| [Q01-02.dql](Q01-02.dql) | Windows PC의 Wazuh Discover 검색창 |
| [Q01-03.dql](Q01-03.dql) | Windows PC의 Wazuh Discover 검색창 |
| [Q01-04.dql](Q01-04.dql) | Windows PC의 Wazuh Discover 검색창 |

REV01의 검증 범위는 [저자용 기록](../../../editorial/REV01/review.md)을 참조한다. 기존 시험 이력과 이번 교정의 정적 검사를 구분한다.

## 분석 보강 입력

기간·데이터 보기·ID는 본문의 절차와 맞춘다. 0건은 선택한 보존 범위의 결과다.

- [Q01-05.dql](Q01-05.dql) — Windows PC · Wazuh Discover · wazuh-archives-* · DQL · 같은 원본의 수집과 경보를 따로 확인하기
