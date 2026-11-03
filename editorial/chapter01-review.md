# 2권 1장 출처와 검증 기록

작성일: 2026-11-03. 상태: **챕터별 교정용 초안**. 이번 산출물은 작업 목차와 1장이다. 나머지 장의 집필 완료를 뜻하지 않는다.

## 범위와 원전

- 지정 슬라이드: https://docs.google.com/presentation/d/1o0H_2DDHBp8p2HvlSnEPbx6-jdURYzew
- 연결된 Google Drive에서 해당 PPTX를 읽었다. 수정 시각 2026-11-03T00:27:22.335Z, 18,389,162바이트, 726슬라이드.
- 내려받은 원전 SHA256: `21c35b306bf7b48fd02e9fd81dfe9fdc97e370de6b610f5b3b3a0cc11daf0f03`.
- 페이지는 PPTX 프레젠테이션 순서의 1부터 시작하는 번호다. Google Slides 내부 slide id와 혼동하지 않는다.
- 1장 기본 개념: 340~342쪽. 343~348쪽의 보호 기능 해제 절차는 이 장에 옮기지 않았다. 현재 상태를 읽고 유지하는 준비 장으로 구성했다.
- 실제 Security·Sysmon 원본과 Wazuh 경보는 가동 중인 사용자 실습 환경에서 읽었다. 스크린샷을 만들거나 UI를 도식으로 재현하지 않았다.
- 2권 실습 배분은 [작업 목차](volume02-plan.md)와 [대응표](module01-coverage.json)에 기록했다. 실습 31~61·63은 32개이며 1권의 62를 중복 수록하지 않는다. Module 02·03은 이번 범위가 아니다.

## 환경과 관찰

- kt66 Ubuntu VM: 192.168.0.107. 기준 커밋 `63d4180b1d6866de986ef263a3bd831d6082b5d5`. 원격 https://github.com/mrgrit/kt66 . 작업 전후 소스 상태는 읽기 확인했고 편집하지 않았다.
- Windows 컨테이너: kt66-windows-user. 콘솔: kt66-windows-console. Windows 게스트: KT66-WIN-01, Windows 11 Enterprise LTSC Evaluation, 10.0.26100 x64.
- Wazuh 에이전트: windows-user, ID 005, 매니저 목록에서 Active. Windows 게스트 IP 172.30.70.2와 컨테이너 측 10.20.70.10은 서로 다른 계층이다.
- WazuhSvc·Sysmon64·osqueryd는 Running/Automatic. Security·System·Sysmon Operational·PowerShell Operational 채널 활성화 확인.
- 로그온 감사는 Success and Failure. auditpol의 영문 출력에서 범주 표시 일부가 비어 보이는 문자 인코딩 문제가 있었지만 성공·실패 값과 반환 코드는 확인했다. 한글 범주명을 실제 출력으로 인용하지 않았다.
- Defender IsTamperProtected·RealTimeProtectionEnabled·BehaviorMonitorEnabled는 모두 True. 서비스·감사·보호 설정은 변경하지 않았다.
- 신규 설치, 보호 기능 해제, 서비스 재시작, 공격 입력, 이벤트 로그 삭제를 수행하지 않았다. 관리 접속과 조회 자체의 정상 로그는 추가될 수 있다.

## 명령별 확인 범위

| 대상 | 확인 방법 | 한계 |
|---|---|---|
| C01-01 | kt66 SSH에서 동일 docker ps 조회 | sudo 입력은 저자용 SSH 표준 입력으로 전달 |
| C01-02~13 | 게스트 OpenSSH에서 복사용 본문 명령 조회 | 새로운 SSH 프로세스마다 필요한 선행 변수를 재구성. UTF-8 출력 설정은 저자 세션에만 적용 |
| C01-14~15 | 매니저 컨테이너의 agent_control -l 직접 읽기 | 독자용 docker exec -it 진입·exit의 대화형 흐름은 이번에 UI 실행하지 않음 |
| Q01-01~04 | 실제 경보 JSON의 필드 이름·값과 검색 조건 대조 | **Discover에서 DQL 실행·화면 검증하지 않음** |
| Windows 설치 | 고정 커밋의 docs·install.ps1·sensors.ps1 대조 | 이번 작업에서 신규 설치를 검증하지 않음. 준비된 게스트를 선행 조건으로 둠 |

기록: [읽기 조회](evidence/chapter01/2026-11-03/windows-readonly.json), [복사용 명령 확인](evidence/chapter01/2026-11-03/copy-command-checks.json).

## 원본과 경보 대조

1. Security RecordId 9115: 이벤트 4624, KT66-WIN-01, kt66student, LogonType 8, ProcessName `C:\Program Files\OpenSSH\sshd.exe`. 원본 시각 2026-11-03T01:32:12.0920342Z. Wazuh timestamp 01:32:13.124+0000, 규칙 60200. 규칙 설명에 IIS가 있지만 원본 프로그램을 기준으로 해석했다. 유형 8만으로 네트워크 평문 전송이라고 설명하지 않았다.
2. Sysmon RecordId 6744: 이벤트 1, System.Execution.ProcessID 4440, EventData.ProcessId 8752. 관찰 대상 sdbinst.exe와 부모 svchost.exe. Wazuh 규칙 92058, 레벨 12. 생성 기록은 이번 저자 조회보다 앞선 기존 이벤트이며, 신규 공격 재현 또는 악성 확정 사례로 쓰지 않았다.
3. 두 기록은 Windows 원본 XML과 Wazuh 경보의 computer·channel·eventRecordID·systemTime·핵심 EventData를 대조했다. Wazuh JSON에서 경로 역슬래시가 중복 이스케이프된 표현과 원본 Windows 경로의 의미를 구분했다.

원본: [Security XML](evidence/chapter01/2026-11-03/security_xml.xml), [Sysmon XML](evidence/chapter01/2026-11-03/sysmon_xml.xml), [Wazuh 경보 발췌](evidence/chapter01/2026-11-03/wazuh-alert-excerpts.json). Wazuh 발췌에서는 반복되는 번역 메시지와 불필요한 최상위 필드를 제외했으며 사용한 필드 값은 유지했다.

## 코드와 설명의 차이

- 고정 커밋의 Windows 안내 문서에 에이전트 자동 설치·등록을 하지 않는다는 과거 설명이 남아 있지만 install.ps1은 sensors.ps1을 호출한다. 원고는 코드 호출과 실제 설치 상태를 기준으로 썼다.
- sensors.ps1에는 센서 설치뿐 아니라 추가 실습용 보안 설정도 있다. 상태 확인 목적으로 전체 스크립트 재실행을 유도하지 않았다.
- ossec.conf의 Security query는 여러 ID를 제외한다. 채널 등록을 모든 이벤트의 수집 성공으로 바꾸어 설명하지 않았다.
- 같은 파일에 osquery 기본 블록과 후속 추가 블록이 있으므로 첫 disabled 값만 보고 전체 상태를 단정하지 않았다. 예약 조회 검증은 지속화 장에 배정했다.
- 슬라이드의 “보호 기능이 막으면 로그 자체가 생기지 않는다”는 설명을 사용하지 않았다. 차단 전 활동과 보호 기능 기록은 별도로 확인한다.

## 공식 문서 대조

- Microsoft Get-WinEvent: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.diagnostics/get-winevent?view=powershell-5.1
- auditpol get: https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/auditpol-get
- 4624: https://learn.microsoft.com/windows/security/threat-protection/auditing/event-4624
- Sysmon: https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon
- Wazuh Windows 이벤트 수집: https://documentation.wazuh.com/current/user-manual/capabilities/log-data-collection/configuration.html
- 후속 2장의 4740 정정 근거: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4740

공식 문서는 2026-11-03 확인했다. 현재 공식 Sysmon 소개 페이지의 버전이 실습에 설치된 바이너리 버전과 같다고 가정하지 않았다.

## 그림과 지면 검토

- 부크크 B5 원본의 첫 구역·여백·테마를 상속했다. 본문 부크크 명조 Light 10.5pt, 제목 부크크 고딕 Light, 명령 Consolas 10pt. 글자 크기로 분량을 줄이지 않았다.
- 관계 도식 4개를 코드로 생성했고 인물 삽화 2개는 1권 자산을 재사용했다. 출처는 [자산 기록](asset-provenance.json) 참조.
- Chrome 화면을 읽으려던 Computer Use 호출이 자동 승인 검토에서 중단됐다. 이유는 Windows에서 현재 브라우저 URL을 충분히 확실하게 판별하지 못했기 때문이다. 이후 UI 조작·신규 UI 촬영은 수행하지 않았다. 다른 경로로 UI 제한을 우회하지 않았다.
- 신규 UI 화면은 본문에 포함하지 않았다. Windows 이벤트는 편집 가능한 XML·로그 값으로 제시했다. UI 단계 설명은 후속 화면 검수 대상이며, 신규 화면 촬영 완료로 표시하지 않는다.
- 기본 render_docx.py는 LibreOffice soffice.exe 부재로 실패했다. 설치된 Word의 COM ExportAsFixedFormat으로 임시 PDF를 생성하고 pypdfium2로 모든 페이지 PNG를 렌더했다.
- 1차 강제 쪽 나눔에서 생긴 단락 단독 페이지를 수정했다. 최종 조판은 30쪽이며 표·명령·도식·참고 URL을 전체 페이지에서 육안 확인했다. PDF와 PNG는 build 안의 검사 자료로만 둔다.
- 추후 교정: 신규 Windows 설치 및 브라우저 콘솔·Discover 조작의 실제 화면 검수. 이 항목은 이번 읽기 검증에 포함되지 않는다.
