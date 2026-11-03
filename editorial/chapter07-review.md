# 7장 집필·검토 기록

2026-11-03. 「로그 삭제와 보호 기능의 대응」. Module 01 실습 38·49, 슬라이드 412~419·517~526을 35쪽으로 구성했다. 본문 입력은 명령 18개와 DQL 8개다. 기존 1~6장, REV01, 강의 저장소는 변경하지 않았다. 합본과 배포용 PDF는 만들지 않았다.

## 원전과 근거

원전: https://docs.google.com/presentation/d/1o0H_2DDHBp8p2HvlSnEPbx6-jdURYzew

Drive 제목은 Module01_Wazuh_위협탐지_DQL.pptx, 크기는 18389162바이트, 수정 시각은 2026-11-03T00:27:22.335Z다. 캐시 SHA256은 `21c35b306bf7b48fd02e9fd81dfe9fdc97e370de6b610f5b3b3a0cc11daf0f03`이다. 해당 구간 텍스트와 내장 이미지 9개를 개별 확인했다. 원전의 터미널 모양 입력 자료는 새 실행 증거로 취급하지 않았다.

Microsoft의 1102 XML, wevtutil, Windows Event Forwarding, Get-WinEvent 5.1, Defender 이벤트·오류 문서와 MSFT_MpThreatDetection을 대조했다. Wazuh Defender 수집 문서에서 공백이 있는 필드 이름을 확인했다. EICAR 공식 검색 결과에서 핵심 68바이트·허용 후행 공백을 포함한 최대 128바이트 조건을 확인했다. EICAR 페이지 직접 열기는 시간 초과였으며 테스트 파일은 다운로드하지 않았다. 전체 참고 URL 10개는 본문에 인쇄했다.

kt66 기준 커밋은 `63d4180b1d6866de986ef263a3bd831d6082b5d5`다. sensors.ps1의 Defender eventchannel 등록과 현재 ossec.conf를 대조했다. 준비 스크립트의 보호 설정 변경 부분은 실행하지 않았다. 현재 설치된 Wazuh 4.10.0의 0610-win-ms_logs_rules.xml과 0600-win-wdefender_rules.xml도 읽어 부모·하위 규칙과 설명 템플릿을 확인했다.

## 실제 관찰과 실행 범위

kt66 VM 192.168.0.107 안의 기존 Windows 게스트 KT66-WIN-01, 에이전트 windows-user/005를 사용했다. 게스트의 인터페이스 주소는 172.30.70.2다. 저자용 SSH 연결은 kt66을 경유한 10.20.70.10 전달 주소를 사용했다. Windows 11 Enterprise LTSC Evaluation 10.0.26100, Windows PowerShell 5.1.26100.1591이었다.

|대상|관찰 결과|
|---|---|
|시작·종료 상태|EventLog·WazuhSvc·WinDefend·Sysmon64 모두 Running. 실시간 보호·변조 방지 True|
|채널|Security·System·Defender 모두 활성화, Circular. 최대 크기 20·20·16 MiB|
|수집 설정|Security query는 1102를 제외하지 않음. System·Defender에는 별도 query 없음|
|삭제 이벤트|보존된 원본에서 Eventlog 공급자의 Security 1102·System 104 없음. 중앙 조회도 일치 문서 없음|
|기존 탐지|Defender 1116, RecordId 46, 2026-11-02T09:56:49.2293663Z|
|기존 조치|Defender 1117, RecordId 47, 2026-11-02T09:57:12.6035151Z|
|사건 연결|두 기록의 Detection ID `{EBD2A2EF-E4E2-4682-9CF7-79EEF7D28939}` 일치. Detection Time 09:56:49.206Z|
|대상|Trojan:Win32/BatTamper.A, Threat ID 2147818424, file:_C:\Tools\defender-off.ps1, 관련 PowerShell 경로|
|조치·상태|action Name 격리, action ID 2, error Code 0x00000000, 추가 조치 없음. Get-MpThreat의 IsActive·DidThreatExecute False, 해당 Get-MpThreatDetection의 ActionSuccess True|
|중앙 문서|보존 archives와 alerts에 1117 한 건, 1116은 찾지 못함. timestamp 2026-11-02T09:57:14.288Z, rule.id 62124, level 3. 누락 원인은 미확인|
|보호 변경|원본 5000·5001 없음. 중앙에는 5007 기록 존재. 현재 보호 True와 과거 이벤트의 보존 여부는 별개|

`evidence/chapter07/2026-11-03/`에 증거를 저장했다. preflight.json은 환경·기존 이벤트, archives-complete.json은 보존 중앙 자료, rules-complete.json은 설치 규칙·버전, export.json은 세 EVTX 생성·해시·재조회, reader-readonly.json은 최종 읽기 명령, cleanup.json은 저자 임시 산출물 정리와 종료 상태다.

최종 읽기 명령 C07-01~06·12~18을 저자 래퍼 안에서 실행했다. C07-04·05·06·17은 NoMatchingEventsFound였으며 권한 오류가 아니다. 1102의 ToXml 결과는 없으므로 그 경로를 현재 환경에서 검증한 것으로 표현하지 않았다. C07-07~11과 같은 사전 경로 확인·생성·epl·해시·사본 재조회는 export.json의 저자 절차로 확인했다. 독자 명령 전체와 모든 실패 분기를 그대로 반복한 검증은 아니다. 본문 명령 18개는 PowerShell 구문 분석에서 오류가 없었다.

저자 수집은 SSH의 PowerShell EncodedCommand 래퍼를 사용했다. 이 래퍼 때문에 생기는 프로세스 명령줄은 독자의 콘솔 직접 입력과 다르다. 공격자 VM 작업, 신규 설치, 로그 삭제, 서비스 중지, 보호 해제, 새 EICAR 생성, 격리 파일 복원·실행은 수행하지 않았다.

## 원전의 해석 교정

|원전의 문제 또는 혼동 지점|본문 처리|
|---|---|
|삭제 이벤트는 반드시 남고 중앙에 이전 이벤트가 모두 보존된다는 표현|생성·필터·전송·보존·조회 조건을 구분. 삭제·덮어쓰기·수집 장애에 따른 관측 한계 설명|
|1102·104 번호만으로 판정|공급자·저장 채널을 함께 제한. 104의 저장 채널과 LogFileCleared 대상 채널 구분|
|eventdata.subjectUserName 빈 열|1102 원본은 UserData/LogFileCleared 구조. 빈 표시를 익명 수행자로 바꾸지 않음|
|clientProcessId 4516|프로세스 번호로 읽고 같은 호스트·시각·세션·승인 작업을 추가 대조|
|wevtutil cl 두 명령의 세미콜론|순차 구분자이며 성공 조건이 아님. 기본 /bu 백업 없음. 분석용 입력으로만 보존|
|실습 49의 설명 3건과 화면 23 hits 불일치|건수를 완료 기준으로 삼지 않음. EICAR·Ceprolad·DumpLsass·5001을 단일 실행의 결과로 합치지 않음|
|Set-Content 뒤 True 표시|기본 출력으로 해석하지 않음. 파일 작성·차단·격리 기록으로 판단. 본문 문자열은 두 부분을 +로 연결하며 68바이트 일치 확인|
|Defender 필드명|실제 detection ID·threat Name·process Name·action Name·error Code의 공백·대소문자 보존|
|1116·1117의 의미|탐지와 조치 분리. Allow·조치 없음은 격리·제거와 다름. 오류·추가 작업·현재 잔존 상태 확인|
|1118·1119|비치명적 오류와 치명적 오류를 구분|
|5001|실시간 보호 비활성화 관측이며 공격자 귀속은 아님. 5000·5007·현재 상태 대조|
|위험도와 설명의 빈 괄호|Defender 심각도·Windows 수준·Wazuh level은 별도 체계. 규칙 62124는 processName을 참조하지만 실제 process Name에 값이 있어 설명만 비는 사례 설명|
|사본과 원상복구|EVTX 내보내기는 원본 삭제 복구와 다름. 해시 일치는 수집 이전의 완전성·진위를 보장하지 않음|

## 검색과 화면

최종 DQL 8개를 Discover UI에서 Last 7 days로 조회했다. Q07-01 0건, Q07-02 archives 34건, Q07-03~06 각각 1건, Q07-07 0건, Q07-08 257건이었다. Q07-03은 archives에서도 1건을 확인했다. 수치는 검토 시점 관찰값이며 재현 목표가 아니다. Q07-02에는 정상 epl 등도 포함될 수 있다.

필드의 공백을 역슬래시로 이스케이프한 초기 식은 이 DQL 파서에서 실패했다. 필드 이름 전체를 큰따옴표로 묶는 최종 Q07-05·06은 각각 한 건을 찾았다. 쿼리 원문·데이터 보기·건수는 chapter07-query-ui.json에 있다.

화면은 원전 417·418쪽 두 장과 현재 Wazuh의 기존 1117 문서 네 장이다. 채널·기록 번호·탐지 ID를 먼저 대조한 뒤 실제 필드를 촬영했다. 직사각형 자르기만 적용했고 UI를 재구성하거나 값을 덮어쓰지 않았다. 원본 경로·해시·자르기 좌표는 chapter07-screenshot-provenance.json에 있다. 전체 원본은 내부 build 자료다.

## 조판·삽화 검수

Bookk B5 원본 첫 구역의 판형·여백·테마를 유지했다. 본문·제목·명령 글꼴과 검정 표 테두리는 이전 장의 조판 체계를 사용했다. 관계 도식 4개, 실제 화면 6개, 새 인물 삽화 2개를 삽입했다. 보존 흐름도의 마지막 상자는 ‘인덱스와 검색’으로 명시해 Windows에서 내보내는 EVTX 사본과 혼동하지 않게 했다.

새 삽화는 보관실에서 닫힌 케이스를 드는 남성과 보호 조치를 확인하는 중년 여성이다. 원본을 개별 열어 두 팔·두 손·두 다리, 손의 연결, 물체의 무게 지지, 노트북 화면 방향과 책상·의자 배치를 확인했다. 문서와 화면을 독자에게 보이기 위해 비틀지 않았다. 최종 내장 자산의 해시·종횡비와 실제 배치 2·30쪽을 확인했다. 원본 생성물은 수정 없이 복사했으며 프롬프트는 chapter07-illustration-prompts.json에 있다.

초기 35쪽을 모두 개별 확인했다. 흐름도·단위 정의·PID 표현·규칙 파일 위치를 수정하고 최종 렌더와 비교해 변경된 3·5·6·12·27·28·29·30쪽을 다시 확인했다. 나머지 27쪽은 최초 검수 이미지와 해시가 같다. 참고 URL의 전체 문자열, 캡션과 그림의 연결, 명령 줄 나눔과 판면을 점검했다. Word COM 숨김 렌더와 pypdfium2를 사용했으며 PDF·PNG는 내부 build에만 둔다. 최종 결과와 해시는 chapter07-qa.json에 기록한다.

## 시도 중 오류와 원상복구

archives.json의 초기 읽기는 UTF-8 해석 오류가 났다. archives-complete.json에서 .json/.json.gz를 구분해 다시 조회했다. rules.json은 규칙을 읽은 뒤 존재하지 않는 ossec-init.conf 조회에서 실패했다. rules-complete.json에서는 wazuh-control info로 버전을 확인했다. 최초 실패 기록도 보존해 성공 범위를 과장하지 않았다.

저자 검증용 `C:\Users\kt66student\Documents\book2-ch07-20261103-173702`에는 새 EVTX 세 개만 만들었다. 종료 때 정확한 절대 경로·상위 경로·파일 목록·생성 당시 SHA-256을 확인하고 그 세 파일과 빈 폴더만 삭제했다. 원래 Windows 채널과 격리 이력은 변경하지 않았다. 종료 시 폴더 부재, 네 서비스 Running, 실시간 보호·변조 방지 True를 재확인했다. 독자는 본문 안내대로 필요한 조사 사본과 해시를 보존한다.
