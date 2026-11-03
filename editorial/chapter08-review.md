# 8장 집필·검토 기록

2026-11-03. 「취약점과 보안 설정의 우선순위」. Module 01 실습 51~53, 슬라이드 538~557을 34쪽으로 구성했다. 복사용 입력은 명령 11개·DQL 9개다. 기존 1~7장·REV01·강의 저장소는 변경하지 않았다. 합본과 배포용 PDF는 만들지 않았다.

## 원전과 범위

원전: https://docs.google.com/presentation/d/1o0H_2DDHBp8p2HvlSnEPbx6-jdURYzew

Drive의 Module01_Wazuh_위협탐지_DQL.pptx는 18,389,162바이트, 수정 시각 2026-11-03T00:27:22.335Z다. 재확인한 메타데이터와 기존 캐시가 일치했다. 캐시 SHA256은 `21c35b306bf7b48fd02e9fd81dfe9fdc97e370de6b610f5b3b3a0cc11daf0f03`이다. 538~540쪽 공통 메뉴, 541~545쪽 실습 51, 546~550쪽 실습 52, 551~557쪽 실습 53의 텍스트와 내장 이미지 11개를 각각 확인했다.

원전의 공격 단계 표기는 이 구간에서 취약점 조회와 SCA 점검을 가리킨다. 새 악용 실습을 추가하지 않았다. 실제 후보 LXD의 공격 전제 조건, xz 영향 버전, SSH 설정 위험을 방어 확인 절차와 연결했다. 패치·서비스 재시작·SSH/방화벽 변경은 보완 계획과 완료 기준으로 기술하고 실행한 결과로 표현하지 않았다.

Wazuh 공식 취약점/SCA 문서, Ubuntu의 CVE-2024-3094 공지와 Jammy sshd_config 설명, Canonical LXD 공식 보안 공지, FIRST CVSS 문서를 대조했다. 본문 참고자료에 전체 URL 11개를 인쇄했다. Wazuh current 문서의 신규 옵션을 4.10 설정에 그대로 복사하지 않았다. 버전별 초기 동기화·자료 갱신·경보 생성 조건 차이는 현재 상태와 경보 이력의 구분으로 설명했다.

NVD 페이지 직접 열기는 읽을 수 있는 본문을 반환하지 않았다. 본문의 NVD 8.1·3.1·High는 실제 Wazuh 문서에서 관찰한 값으로만 제시했다. Canonical 공지는 6.8·3.1·Moderate와 수정/지원 계열을 확인했다. CISA KEV 직접 열기는 403이었으며 특정 CVE의 KEV 등재 여부를 주장하거나 본문 근거로 쓰지 않았다.

## 현재 환경과 관찰

kt66 기준 커밋은 `63d4180b1d6866de986ef263a3bd831d6082b5d5`다. 현재 Ubuntu VM 192.168.0.107의 hostname은 ccc, 에이전트는 kt66-host/006이다. Wazuh 관리자와 대상 에이전트는 4.10.0, 운영체제는 Ubuntu 22.04.5 LTS, 실행 커널은 5.15.0-202-generic이다. Windows 게스트 windows-user/005는 보조 정책 비교만 했다.

|대상|관찰 결과|
|---|---|
|준비/종료|wazuh-agent와 ssh 모두 active. 패키지·보안 설정·서비스 상태 변경 없음|
|호스트 Syscollector|disabled no, packages yes, interval 1h, scan_on_start yes|
|호스트 SCA|enabled yes, interval 12h, scan_on_start yes|
|관리자 취약점 기능|enabled yes, index-status yes, feed-update-interval 60m. 인덱서 연결 설정 존재|
|전체 Critical/High|3,603 취약점 문서|
|kt66-host Critical/High|1,039 취약점 문서|
|OpenSSH/xz/Log4j 이름 후보|취약점 문서 0건|
|Ubuntu 설치 패키지|xz-utils·liblzma5 5.2.5-2ubuntu1.2; openssh-client/server 1:8.9p1-3ubuntu0.18; amd64|
|APT 캐시|xz-utils·openssh-server의 Installed=Candidate. apt update는 실행하지 않음|
|LXD|snap 5.0.11-e42d773, revision 41283, 5.0/stable 계열. CVE-2025-54289 1건|
|xz CVE|CVE-2024-3094 Inventory 0건. Ubuntu 공식 공지의 22.04 영향 없음과 대조|
|Ubuntu SCA|cis_ubuntu22-04, Benchmark v1.0.0, 80 Passed/101 Failed/1 NA, 182개, 44%|
|Windows SCA|cis_win11_enterprise, Benchmark v3.0.0, 114 Passed/359 Failed/9 NA. 정책 설명의 비영어 OS 검사 한계 확인|
|체크 28638|Failed. condition all. sshd -T 출력 조건과 주 설정 파일 정규표현식 조건|
|실제 SSH 값|permitrootlogin without-password, pubkeyauthentication yes, passwordauthentication yes, permitemptypasswords no|
|체크 28634|Failed. 현재 /etc/ssh/sshd_config는 644 root:root; 정책은 0600 및 root 소유·그룹 조건|
|SSH 문법|sshd -t 오류 없음, 종료 상태 0. Include 지시문은 주 파일 12행|

증거는 `evidence/chapter08/2026-11-03/`에 둔다. preflight.json은 환경, inventory-sca.json은 관리자 DB의 읽기 전용 상태, details.json은 상세 정책·실효 SSH 설정, reader-checks.json은 독자 입력에 대응하는 읽기, installed-rules.json은 현재 0520 규칙 파일, final-read.json은 최종 구문 검사·수정 명령·종료 상태다. SQLite는 mode=ro로 열었고 저자 자료 대조용이며 독자의 GUI 절차를 대체하지 않는다. DB 항목별 scan_time/scan_id는 변경 없이 유지될 수 있어 최신 전체 검사 시각으로 해석하지 않았다.

## 원전 해석 교정

|혼동 지점|본문 처리|
|---|---|
|Inventory와 최근 24시간 경보의 혼용|현재 상태와 경보 이력 분리. 실제 4.10 Inventory에는 일반 시간 선택기가 없음을 확인|
|data.vulnerability 경보 필드를 현재 상태 검색에 사용|Inventory vulnerability.id/severity와 경보 data.vulnerability.cve/severity 구분. 현재 설치 규칙 파일 경로 명시|
|첫 검사·자료 갱신은 항상 동일한 경보 생성|버전·동기화·패키지 변경·자료 갱신 조건 차이 명시. 0건 경보와 현재 항목의 공존 설명|
|패키지 이름 식을 특정 CVE 조회로 명명|이름 후보 검색과 vulnerability.id 정확한 식별자 검색을 별도 제시|
|0건이면 패키지를 보유하지 않음|실제 xz/OpenSSH 설치와 0건을 대조. 수집 누락·이름·배포판 영향 범위 점검|
|상태 건수=호스트 수/고유 CVE 수|호스트·패키지·CVE 조합의 문서 수로 해석|
|점수 하나로 처리 순서 확정|평가 출처·버전·영향 조건·접근 범위·업무 중요도·작업 가능성 연결|
|제조사 5.0 Ignored를 패치 완료로 해석|미수정/정책 판단과 수정 계열을 구분하고 지원·갱신 계획으로 기록|
|SCA 제목 식=모든 실패 목록|영어 키워드 부분집합·기간·경보 생성 조건 명시. 현재 정책 목록과 대조|
|반복 SCA 행=서로 다른 문제|에이전트·정책·체크 ID·시각·문서 식별자로 구분|
|SSH root Failed=root 비밀번호 허용|without-password/prohibit-password와 no, 일반 passwordauthentication 설정을 구분|
|remediation 복사 즉시 적용|Include·Match·실효 설정·대체 관리 경로·문법·기능 확인과 원상복구 준비|
|MITRE 태그=공격 발생|설정 위험 분류와 실제 인증·프로세스·통신 증거 구분|

## 명령·검색·화면 검증

최종 DQL 9개를 UI에서 실행했다. 본문 순서로 번호를 정리했으며 식 자체는 동일하다. Q08-01 3603, Q08-02 1039, Q08-03 1, Q08-04 0, Q08-05 0, Q08-06 0, Q08-07 147, Q08-08 22, Q08-09 1건이다. Inventory는 현재 상태, Discover는 Last 1 week를 사용했다. 최초 날짜 입력에서 Last 17 days가 된 것을 확인하고 1 week로 바로잡은 뒤 최종 값을 기록했다. 취약점 경보 0건도 정정한 기간으로 다시 확인했다. 조건·건수는 chapter08-query-ui.json에 있다.

Ubuntu 명령은 SSH 저자 래퍼에서 읽기 전용으로 실행했다. sudo 인증 전달 때문에 -S를 사용하는 저자 형식과 독자 콘솔 입력을 구분한다. C08-02·04~10의 값은 확인했으며, 최종 C08-05·07·10·11은 줄 연결을 포함한 입력을 다시 읽기 실행했다. C08-03의 less는 설치 경로와 동일 설정 파일의 내용을 확인했으나 독자의 대화형 검색 키 전체를 재현하지 않았다. C08-01은 실제 SSH 라이브러리 연결과 Windows PowerShell 구문 검사로 확인했고, Windows ssh.exe의 첫 호스트 키 등록 화면을 새로 촬영하지 않았다. 전 명령은 bash -n으로도 구문 확인했으며 C08-01은 실제 실행 셸의 PowerShell 검사 기록을 별도로 남겼다. 모든 실패 분기나 패치·설정 반영 후 동작을 검증한 것은 아니다.

화면 5개는 현재 Wazuh 4.10의 실제 UI다. 원본에서 직사각형 자르기만 했고 값을 덮어쓰거나 UI를 그리지 않았다. chapter08-screenshot-provenance.json에 원본 경로·SHA256·자르기 영역을 기록했다. 원본 화면·슬라이드 추출물·렌더는 내부 build에 둔다. 재생성 도구는 커밋된 화면 자산을 사용하므로 내부 캡처가 없어도 DOCX를 다시 만들 수 있다.

## 시도 중 오류와 미실행 범위

inventory-sca.json의 초기 host-syscollector-sca 명령은 sudo 표준입력과 Python here-document가 충돌하여 인증 오류를 냈다. details.json의 Python -c 방식으로 같은 설정을 읽어 성공했다. 잘못된 암호 시도에 해당하는 초기 오류 기록도 보존했다. 계정 암호·권한을 변경하지 않았다.

reader-checks.json에서 추정한 0475 규칙 파일 경로는 존재하지 않았다. rules-path.json에서 실제 0520-vulnerability-detector_rules.xml을 찾고 installed-rules.json에 읽은 내용을 보존했다. 파이프의 마지막 명령 상태만으로 앞선 grep의 실패를 성공으로 판단하지 않았다.

공격자 VM 접속·취약점 악용·문제 버전 설치·패키지 갱신·SCA 정책 변경·SSH/방화벽 설정 변경·서비스 재시작·보호 해제·로그 삭제를 수행하지 않았다. 읽기 명령 자체가 만드는 접속·감사 기록은 삭제하지 않았다. 종료 시 두 서비스 active, SSH 실효 값과 파일 권한이 시작 관찰과 같음을 확인했다.

## 조판과 삽화 검수

부크크 B5 원본 첫 구역의 판형·여백·테마를 보존했다. 본문 부크크 명조 Light 10.5pt, 제목 부크크 고딕 Light, 명령 Consolas 10pt다. 화면 5개·관계 도식 3개·새 삽화 2개를 배치했다. 삽화는 통신함 앞 태블릿을 든 여성과 정비 작업장의 중년 남성으로 장소·인물·소품·행동을 구분했다.

원본 두 이미지를 개별 확인하여 두 팔·두 손·두 다리의 연결, 한 손의 태블릿 지지, 사용자 쪽 화면 방향, 타워·손·정비대의 접촉과 지지를 점검했다. 문서·화면을 독자 쪽으로 비틀지 않았다. 최종 내장 해시·종횡비와 실제 1·30쪽 배치를 대조했다. 원본 생성물은 바이트 변경 없이 복사했다.

초기 34쪽 전부를 개별 육안 확인했다. 긴 grep 정규표현식은 따옴표 문자열과 줄 연결로 나누고 실제 실행을 확인했다. 검색식 번호·규칙 파일 위치·시간대 표기를 교정했다. 최종 변경 페이지 9·11·12·13·14·15·17·18·20·21·23·24쪽을 다시 확인하고 나머지 22쪽은 이미지 해시 일치로 대조했다. 전체 URL 문자열, 그림·캡션 연결, 명령 줄바꿈·표·판면을 확인했다.

조판 검사는 숨김 Word COM PDF 내보내기와 pypdfium2를 사용한다. 번들 기본 렌더러의 soffice.exe가 없어 기존 장에서 검증된 Windows Word 절차를 사용했다. PDF·페이지 PNG는 내부 검토용이다. 최종 해시와 확인 항목은 chapter08-qa.json에 기록한다.
