# 4장 집필·검토 기록

2026-11-03. 「서비스와 작업을 이용한 지속화」. Module 01 실습 39·40·44·63을 장별 교정용 초안으로 작성했다. 2·3장 이후 5장까지 집필하라는 후속 요청을 적용했다. REV01·강의 저장소·1권은 수정하지 않았다.

## 출처와 대응

- 지정 원전: https://docs.google.com/presentation/d/1o0H_2DDHBp8p2HvlSnEPbx6-jdURYzew
- 캐시 PPTX 726쪽, SHA256 `21c35b306bf7b48fd02e9fd81dfe9fdc97e370de6b610f5b3b3a0cc11daf0f03`.
- 서비스 420~428쪽 → 4.2. 예약 작업 429~437쪽 → 4.3. Run 키 473~481쪽 → 4.4. osquery 627~628·636~644쪽 → 4.5 및 원상복구.
- 명령·결과 화면이 그림인 슬라이드는 원본 이미지를 열어 판독했다. 본문 UI 5개는 현재 실습망의 실제 Wazuh Discover에서 새로 확보했다. 원전 결과와 현재 결과를 동일 실행으로 합치지 않았다.
- Microsoft의 sc create, schtasks create, 4697·4698, Run/RunOnce, Sysmon, PsExec, 작업 스케줄러 반환 코드 문서와 osquery 설정·로깅, Wazuh osquery·이벤트 보관 문서를 대조했다. 전체 주소는 본문 참고자료에 수록했다.

## 실행·관찰 범위

kt66 VM의 Windows 게스트 KT66-WIN-01, Wazuh agent windows-user/005에서 사전 조회 후 고유 이름을 사용했다. 저자용 SSH·PowerShell 래퍼로 관찰했으며, 독자의 관리자 PowerShell 직접 입력과 전송 방식이 다르다. 최종 복사용 26개 명령은 Windows PowerShell 파서로 모두 구문 검사했다. 구문 검사 자체를 전 절차의 재실행으로 표현하지 않는다.

|대상|관찰|근거|
|---|---|---|
|서비스 book2_ch04_svc|없는 파일을 수동 시작 경로로 등록, qc/query, STOPPED|create.json, collect.json|
|System 7045|RecordId 416, imagePath, LocalSystem, rule 61138 level 5|원본과 관리자 archives/alerts|
|Security 4697|RecordId 11811, serviceFileName, subject kt66student, 아카이브에만 존재|collect.json, UI|
|예약 작업 book2_ch04_task|ONLOGON/SYSTEM, 고정 문구 출력, 수동 실행 1회|create.json|
|작업 완료|LastTaskResult 267009(0x41301 실행 중) 뒤 0|create/collect.json|
|Security 4698|RecordId 11818, rule 60228, taskContent·수행자|원본·UI|
|Run book2_ch04_run|HKCU 값 등록·재조회, 없는 실행 파일을 가리킴|create/collect.json|
|Sysmon 13|RecordId 8887, reg.exe, T1060,RunKey, rule 92302|원본·UI|
|osquery|startup_items·scheduled_tasks 직접 조회, 로컬 관리자 SID로 구성원 조회|collect.json|
|예약 osquery|두 added 행, rule 24010; 원상복구 뒤 두 removed 행|collect.json, dql-ui-checks.json|

Q04-01~07을 본문에 지정한 데이터 보기에서 실행했다. 서비스 1, 수행자 1, 작업 프로세스 1, 작업 생성 1, Run 변경 1, added 2, removed 2건을 확인했다. 건수는 이 관찰 시각의 값이며 독자의 고정 정답이 아니다. Q04-07은 아카이브에서도 별도 확인했다. UI에는 전송된 이벤트의 수집 시각이 표시되므로 원본 UTC와 구분했다.

## 교정한 해석

- 원전 evilsvc 생성 응답 1073은 기존 서비스 충돌이다. 새 설치 성공으로 쓰지 않았다.
- PsExec64.exe -s cmd /c whoami에는 원격 대상이 없다. 로컬 SYSTEM 문맥 요청과 정상 관리 도구의 사용을 설명하며 원격 이동·권한 상승 성공으로 단정하지 않았다. 이번 관찰에서는 PsExec를 실행하지 않았다.
- 서비스 등록·실행·현재 존재, 서비스 실행 계정·등록 수행자를 구분했다. 7045 imagePath와 4697 serviceFileName을 별도로 설명했다.
- 작업의 Command/Arguments만으로 실행 시점을 정하지 않는다. Triggers/Principals를 연결했다. 원전 minute와 본문 ONLOGON/수동 실행의 차이를 명시했다.
- Run 설정 이벤트는 다음 로그온에서의 실행 증명이 아니다. HKCU와 HKU의 사용자 SID 표현, Image/TargetObject/Details, Sysmon ruleName과 Wazuh rule.id를 구분했다.
- osquery 직접 SQL 출력과 예약 결과 수집을 구분했다. added/removed는 행 차이이며 객체 생성·삭제 시각 자체가 아니다. 초기 관찰·비교 상태 초기화·열 값 변경의 영향도 설명했다.
- 실제 eventdata 경로의 이중 역슬래시 표현을 확인했다. 원본 경로·JSON 표현·DQL 문법을 구분하여 일률적인 이스케이프 횟수를 주장하지 않았다.
- 사전 조회 중 추정했던 osquery 규칙 파일명 0240은 존재하지 않았다. 그 조회를 규칙 코드 검증으로 간주하지 않았다. rule 24010은 실제 수집 문서의 값이다.

## 원상복구와 한계

05:53 UTC에 이번 서비스·작업·Run 값만 제거했다. 서비스 1060, 작업·값 부재, 이후 직접 SQL 두 결과 []를 확인했다. WazuhSvc·Sysmon64·osqueryd Running, Defender 실시간 보호·변조 방지 True를 유지했다. 서비스 시작, Run 로그온 실행, 실제 악성 지속화·원격 침투·보호 해제는 수행하지 않았다.

실패 분기와 운영 대응 절차는 공식 동작 및 현재 환경을 바탕으로 작성했다. 모든 실패 분기를 재현하거나 다른 Windows 버전에서 시험한 것은 아니다. 저자 래퍼는 여러 독자 입력을 묶어 실행하므로 명령별 글자 단위 재현과 구분한다.

## 조판과 그림

부크크 B5 원본과 공통 조판기를 사용했다. DOCX 36쪽, 복사용 입력 33개(명령 26·DQL 7), 실제 화면 5, 관계 도식 4, 새 인물 삽화 2개다. 스크린샷 영역 지정 기능이 좌표를 무시한 초기 결과를 폐기하고 전체 UI 캡처에서 직사각형 영역만 잘라 교체했다. 문자·값을 합성하지 않았다. 좌표·해시는 chapter04-05-screenshots.json에 기록했다.

bundled render_docx.py는 LibreOffice soffice.exe 부재로 실패했다. 설치된 Word의 숨김 COM 렌더와 pypdfium2로 모든 페이지를 검사했다. 검사 PDF·PNG는 build에만 두며 배포하지 않는다. 구조·URL·예제·이미지 검사는 chapter04-qa.json에 기록했다.
