# 9장 집필·검토 기록

2026-11-03. 「호스트 이상과 파일 판정」. Module 01 실습 54~56, 슬라이드 558~582를 40쪽으로 구성했다. 명령 17개·DQL 11개, 실제 화면 5개·흐름도 3개·인물 삽화 2개다. 기존 1~8장, REV01과 강의 저장소는 변경하지 않았다. 챕터별 DOCX를 제공하며 합본과 배포용 PDF를 만들지 않았다.

## 원전과 적용 범위

원전: https://docs.google.com/presentation/d/1o0H_2DDHBp8p2HvlSnEPbx6-jdURYzew

Drive 메타데이터에서 지정 자료는 Module01_Wazuh_위협탐지_DQL.pptx, 18,389,162바이트, 수정 시각 2026-11-03T00:27:22.335Z임을 재확인했다. 726쪽 캐시의 SHA256은 `21c35b306bf7b48fd02e9fd81dfe9fdc97e370de6b610f5b3b3a0cc11daf0f03`이다. 실습 54는 558~564쪽, 55는 565~574쪽, 56은 575~582쪽이다. 해당 텍스트와 내장 이미지 14개를 조사했다. 583쪽 이후는 다음 장 범위다.

현재 kt66 기준 커밋은 `63d4180b1d6866de986ef263a3bd831d6082b5d5`이며 작업 트리는 깨끗했다. 원전의 공격 개념은 은닉과 파일 위장·유입으로 소개하고 방어 관찰에 연결했다. 실제 루트킷 설치·외부 침투·악성코드 실행을 추가하지 않았다. 원전의 파일 생성은 kt66 호스트에서 들어간 web 컨테이너의 시험이다. HTTP 업로드 성공을 증명하는 사례로 바꾸지 않았다.

공식 Wazuh Rootcheck·VirusTotal·ClamAV 문서와 현재 설치된 4.10 규칙·연동 스크립트, ClamAV 1.5.4 clamdscan 매뉴얼, EICAR 공식 안내와 VirusTotal 공개 API 안내를 대조했다. 본문에 전체 URL 10개를 인쇄했다. EICAR 안내 직접 열기는 시간 초과였으나 공식 검색 결과의 표준 시험 파일·68바이트 설명을 확인했다. EICAR 파일 자체는 다운로드하지 않았다. ClamAV 매뉴얼 RETURN CODES의 0·1·2 및 --fdpass의 로컬 소켓 조건을 확인했다.

## 현재 관찰과 기존 결과

|대상|현재 읽기 관찰 또는 원전 결과|
|---|---|
|kt66|Ubuntu VM 192.168.0.107, web 컨테이너 hostname web|
|Wazuh|관리자 4.10.0, web/002 4.10.1, kt66-host/006 4.10.0. 원전 web ID는 013|
|Rootcheck|enabled, frequency 43200초. web 검사 시작·종료 05:54:11~05:54:24 및 17:54:25~17:54:38|
|현재 권한|/var/log/kt66-cmd.log, -rw-rw-rw-, 666 root:root|
|Rootcheck UI|Last 24 hours 전체 32건, web 2건, 해당 경로 2건. 모두 두 검사 시점의 쓰기 권한 경보|
|관리자 연동|ossec.conf에 VirusTotal integration 없음. 현재 7일 VirusTotal 경보 0건|
|원전 VirusTotal|2026-10-31 19:12:55.178 invoice.pdf.exe 87105·positives 66. 19:08:32.412 /usr/bin/clamdscan 87104·positives 0|
|FIM|web의 /var/www 실시간 감시와 frequency 300, 전용 ClamAV 로그 localfile/syslog 수집|
|ClamAV 프로세스|감시 스크립트 PID 587, clamd PID 591. 로컬 소켓 존재. VERSION 비활성 경고와 로컬 clamdscan 1.5.4|
|ClamAV 로그/DB|kt66-clamav.log 53바이트의 시작 줄 하나, kt66-seen 0바이트. main·daily·bytecode DB 파일 존재. DB 최신성을 단정하지 않음|
|ClamAV 설정|LogSyslog false, /var/log/clamav/clamav.log, MaxFileSize 25M·MaxScanSize 100M|
|현재 업로드 경로|기존 book07-shell.php 61바이트. 이번 invoice-ch09.pdf.exe 없음. 기존 파일을 변경하지 않음|
|원전 ClamAV|원문 19:13:09 Eicar-Test-Signature FOUND, Wazuh 19:13:11.371 규칙 52502. data.url·extra_data 빈 값|
|종료 상태|clamd와 Wazuh 수집 프로세스 실행, 여섯 에이전트 Active. 대상 권한·전용 로그·seen 관찰값 유지|

현재 Rootcheck 문서 id는 `1793696066.21559233`과 `1793652852.15871877`이다. 2건을 두 파일·두 침해로 세지 않았다. 원전 204건도 당시 검색 결과이며 현재 건수와 섞지 않았다. 원전의 VirusTotal·ClamAV 결과는 같은 경로·시간대의 사례지만 두 화면만으로 파일 바이트 동일성을 증명하지 못한다.

## 해석과 절차 교정

|혼동 또는 오류|본문 처리|
|---|---|
|루트킷을 커널 방식에만 한정|사용자 영역과 커널 영역을 구분하고 Rootcheck의 파일·권한·프로세스·포트 조사 소개|
|ps와 /proc만 비교한다고 단순화|여러 시스템 호출·관찰 방법의 불일치 검사로 설명|
|Rootcheck 510=루트킷 확정|509 부모·510 일반 이상·521 은닉 의심을 구분, 그룹 검색과 실제 권한 대조|
|경로가 uploads이면 HTTP 업로드 공격|원전의 컨테이너 파일 생성과 웹 유입·실행 증거를 구분|
|echo의 EICAR 자리표시자와 68바이트 주장|자리표시자를 실행 입력으로 복제하지 않음. 공식 다운로드를 독자 선택 절차로 기술하고 미실행 명시|
|FIM 파일 추가=악성 판정|554/550과 경로·md5_after·id 확인 후 별도 VirusTotal 결과 연결|
|VirusTotal 연동=파일 내용 업로드|설치된 virustotal.py의 md5_after 기반 기존 보고서 조회와 별도 파일 업로드 구분|
|두 검색 결과=악성 두 건|87105 탐지 한 건과 87104 탐지 0 한 건을 분리|
|positives 수치 비교·malicious 확률|keyword 매핑 가능성과 malicious 0/1 파생 의미 설명, 후보는 87105로 검색|
|조회 오류를 web에만 검색|이 버전 오류 이벤트는 원래 agent 인수를 전달하지 않는 경로가 있어 먼저 전체 범위 조회|
|미등록·0건·한도·시간 초과=안전|87101~87106 상태와 다음 확인을 분리|
|clamd[PID]=항상 백신 데몬 PID|kt66 감시 스크립트의 $$ 태그와 실제 데몬 PID 구분|
|ClamAV 빈 data.url=파일 정보 없음|full_log와 부모 clamd·하위 clamd-found 정규표현식의 괄호 속 해시 조건 대조|
|검사 루프가 정확히 20초마다 실행|검사 완료 뒤 sleep 20, 검사 시간·중복 억제·오류 출력 제외 설명|
|FOUND=격리/삭제/실행/침해 성공|탐지·조치·실행 증거를 별도 기록하고 종료 코드 0/1/2 구분|
|.env 키를 비우면 연동 제거|90-virustotal.sh의 빈 키 조기 종료를 확인, 실제 integration 블록과 이전 설정 대조|

규칙·디코더는 kt66-siem의 `0015-ossec_rules.xml`, `0490-virustotal_rules.xml`, `0320-clam_av_rules.xml`, `0075-clamav_decoders.xml`을 실제 경로에서 읽었다. 고정 kt66의 `web/kt66-clamav.sh`, `web/wazuh-agent.conf.append`, `siem/90-virustotal.sh`, `docker-compose.yaml`, `.env.example`도 대조했다. 이들은 읽기만 수행했다.

## 검증 범위와 한계

DQL 11개를 CUA 브라우저 UI에서 입력·조회했다. Q09-01~03은 Last 24 hours, 나머지는 Last 7 days다. 순서대로 32·2·2·0·0·0·0·0·0·0·0건이었다. 구문 오류는 없었다. 상세 식·기간·건수는 chapter09-query-ui.json에 있다. 0건은 구문 수용과 현재 빈 결과만 확인한 것이며 EICAR 양성 경로의 종단 검증이 아니다. Overview의 Active 버튼으로 목록에 진입하여 web·kt66-host의 실제 연결 상태도 확인했다.

현재 상태 조회는 SSH 저자 래퍼를 이용했다. 독자용 sudo·대화형 컨테이너 진입과 저자용 -S·일회성 읽기를 구분한다. C09-04·05·06·08·13·17은 최종 입력과 대응하여 읽기 실행했다. C09-08의 grep 종료 상태 1은 이름 줄이 없는 현재 상태이고 stderr는 비었다. C09-13의 VERSION 경고는 로컬 버전만 출력됨을 나타내며 본문에 반영했다. C09-02의 docker ps 서식과 hostname도 확인했다. C09-03·15의 대상 파일 내용은 읽었지만 less의 모든 대화형 키는 재현하지 않았다. C09-07·09의 셸 이동은 독자 절차이며 SSH 래퍼는 해당 컨테이너를 직접 지정했다.

명령 17개를 bash -n으로 구문 검사했고, Windows 명령 C09-01은 PowerShell 파서로 별도 확인했다. SSH 연결은 실제 사용했으나 Windows ssh.exe의 최초 신뢰 확인 화면을 다시 만들지 않았다. C09-10~12·14·16은 독자 선택 절차다. 새 파일 준비·EICAR 다운로드·직접 백신 검사·파일 삭제를 실행하지 않았으며 해당 정상 응답은 예상 결과로 썼다. VirusTotal 키 입력·활성화·외부 해시 조회, 보호 해제·자동 대응·환경 초기화·서비스 재시작·로그 삭제를 수행하지 않았다. 읽기 명령이 남기는 접속·감사 기록은 지우지 않았다.

API 키를 보유하지 않은 현재 환경에서는 원전 분석을 완료 경로로 제공했다. 연동 활성화는 별도 관리 준비 조건으로 설명했으며 적용·원상복구를 검증했다고 주장하지 않는다. 모든 실패 분기·재처리·오탐·실제 사고의 증거 수집을 실행 검증한 것은 아니다.

## 증거와 시도 중 오류

`evidence/chapter09/2026-11-03/`의 preflight.json은 환경·원본 설정, config-rules.json은 설치 규칙·연동, source-selected.json은 고정 코드, research-extra.json과 wiring.json은 연동 전달·수집 연결, final-read.json은 최종 입력 구문·읽기·종료 상태다. 인증을 위한 로컬 래퍼와 원본 UI·슬라이드 추출물은 ignored build에 두고 커밋하지 않는다.

초기 preflight의 추정 rootcheck 규칙 glob은 일치하지 않아 실제 `0015-ossec_rules.xml` 경로로 바로잡았다. 한 SSH 명령 안의 두 번째 sudo에는 암호 표준입력이 남지 않아 실패했으며 이후 각각 분리하여 읽었다. 추정했던 kt66-eicar.ndb와 로컬 man 문서는 없었다. DB 파일을 만들지 않았고 공식 ClamAV 버전별 문서로 대조했다. 연구용 grep의 불일치와 command -v nano의 미설치 종료 상태도 성공으로 바꾸지 않았다. web에서 설치되지 않은 file·nano를 독자 명령에 쓰지 않았다. 기존 오류 기록은 보존했다.

## 화면·삽화·조판

화면 9-1·9-2는 2026-11-03 현재 Rootcheck 경보에서 자른 실제 UI다. 화면 9-3~9-5는 원전 571·572·580쪽의 2026-10-31 VirusTotal·ClamAV 사례다. 직사각형 자르기 외에 값을 덮어쓰거나 UI를 그리지 않았다. 자산·원본 해시·자르기 영역은 chapter09-screenshot-provenance.json에 기록했다. 본문도 현재 ID/시각과 원전 ID/시각을 구분한다.

새 삽화는 장비실의 중년 여성과 증거 보관 공간의 안경 쓴 남성이다. 장소·인물·복장·행동·소품을 구분했다. 이미지 원본을 한 장씩 열어 두 팔·두 손·두 다리, 어깨·팔꿈치·손목 연결, 고정 선반과 평평한 종이, 카운터와 봉투의 접촉·무게 지지, 한 장면의 시점을 확인했다. 원본 생성물의 바이트를 변경하지 않고 복사했다. 프롬프트·원본 파일과 검수는 chapter09-illustrations.json에 있다.

부크크 B5 base의 첫 구역 판형·여백·테마를 보존했다. 본문 부크크 명조 Light 10.5pt, 제목 부크크 고딕 Light, 명령 Consolas 10pt다. 초기 39쪽을 각각 확인한 뒤 긴 grep을 짧은 고정 문자열 검색으로 교정하고 실제 읽기 실행했다. Docker의 탭 표기를 리터럴 \\t로 정리했으며 필드 나열과 PID·시그니처 정의, 메뉴·규칙 파일 위치를 보완했다. ClamAV 흐름도의 세로 간격을 줄이고 글자 크기는 유지했다.

최종 40쪽을 개별 육안 확인했다. 삽화 실제 배치, 명령·표·캡션·URL 전체 문자와 본문 판면을 대조했다. 내장 그림 해시·종횡비·복사용 입력 일치와 폰트·판형 검사는 chapter09-qa.json에 있다. 숨김 Word COM으로 임시 PDF를 내보내고 pypdfium2로 렌더했다. 번들 soffice.exe가 없는 환경의 기존 검증 절차다. PDF·페이지 PNG는 build 내부 조판 검사에만 사용한다.
