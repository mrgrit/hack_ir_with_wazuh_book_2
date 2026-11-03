# 5장 집필·검토 기록

2026-11-03. 「PowerShell과 정상 프로그램 악용」. Module 01 실습 41·42·45·46, 슬라이드 438~460·482~498을 구성했다. 원전 주소와 SHA256은 chapter04-review.md 및 module01-coverage.json과 같다. Module 02·03을 추가하지 않았다.

## 구성과 공식 근거

실습 41은 UTF-16LE/Base64 명령 입력·복원과 다운로드 응답 해석, 42는 4104의 코드·분할 기록·프로세스 연결, 45는 certutil과 정상 도구의 인자·파일 결과, 46은 모의 Office 이름의 부모·자식 관계로 구성했다. 준비·입력·응답·수집·검색·조사·대응·원상복구를 연결했다.

Microsoft Windows PowerShell 5.1의 about_PowerShell_exe, about_Logging, 실행 정책, Sysmon, certutil, regsvr32, AMSI, ProcessStartInfo.UseShellExecute, Defender 이벤트 문서를 확인했다. PowerShell 7 문서의 설정을 5.1의 검증 근거로 대체하지 않았다. kt66 기준 커밋의 Windows 센서 준비 코드도 대조했다. 전체 URL은 본문에 인쇄했다.

## 실제 관찰과 입력의 차이

Windows 게스트 KT66-WIN-01/windows-user에서 다음 무해한 동작을 관찰했다. 저자용 SSH 전송은 EncodedCommand 래퍼를 사용하므로 저자가 만든 부모 명령도 검색 결과에 나타난다. 본문은 독자의 관리자 PowerShell 직접 입력 순서로 제공한다. 최종 19개 명령은 게스트의 PowerShell 파서로 전부 검사했으며 오류가 없었다. 명령별 문구·줄 나눔과 저자 관찰 스크립트가 완전히 같다는 뜻은 아니다.

|대상|실제 결과와 식별자|
|---|---|
|인코딩 문구|book2-ch05-encoded 출력, Sysmon 1/8952, rule 92057|
|복원된 코드 4104|RecordId 2473, ScriptBlockId c6b05be4-bfdb-4ae4-b16c-ebcbd0c7d19b|
|문자열 VirtualAlloc|book2-ch05-scriptblock VirtualAlloc 출력, 4104/2530, ScriptBlockId 5b40f8dd-b7da-4b25-932a-8b50a8b9a59e, processID 5228|
|certutil -decode|Sysmon 1/8957, rule 92073, p.txt 15바이트·내용 book2-ch05-file|
|p.txt SHA256|DBF99CE9604DA7C47846FC02E9C91517341E3DF600631388B936A360FDB79171|
|모의 WINWORD.EXE|C# 소스 컴파일 4096바이트·NotSigned, Sysmon 1/8961|
|자식 cmd.exe|book2-ch05-child 출력, Sysmon 1/8962, rule 92052, 부모 GUID 끝 6a06과 연결|

첫 저자 시도에서는 block.ps1을 -File로 실행했으나 게스트 실행 정책 때문에 UnauthorizedAccess로 실패했다. 이를 성공으로 처리하지 않고 현재 PowerShell에서 -Command { ... }를 전달하는 본문 C05-09로 바꾸어 확인했다. 정책을 변경하거나 Bypass로 우회하지 않았다. scriptblock-correction.json에 수정 후 실제 결과를 남겼다. 준비의 Undefined 범위 목록은 유효 실행 정책이 무제한이라는 뜻이 아니다.

## DQL 검증

Q05-01~11을 실제 Discover에서 실행했다. 고유 인코딩 입력·블록 ID·certutil·모의 부모/자식 검색으로 해당 이벤트를 확인했다. 넓은 PowerShell 탐색 Q05-02는 142건으로 저자 관리 명령을 포함한다. 첫 즉시 조회가 직전 결과를 보여 준 것을 발견해 완료된 결과를 다시 판독했다. 결과 증거는 dql-ui-checks.json에 있다.

Q05-07의 최근 24시간 결과 1건은 **전날 2026-11-02 18:57 KST의 기존 Defender 기록**이다. 이번 certutil의 차단 증거가 아니다. Q05-11의 정상 도구 8건 역시 해당 기간의 기존 실행을 포함하며 7종 도구를 모두 새로 실행했다는 뜻이 아니다. 원본 시각·파일·프로세스를 일치시키는 판정 기준을 본문에 유지했다.

## 원전 교정과 실행하지 않은 범위

- Base64는 인코딩이다. UTF-16LE PowerShell 입력과 ASCII 파일 내용의 바이트 해석을 구분했다.
- 원전의 DownloadString 응답 404는 요청 파일을 받지 못한 결과다. IEX가 명령줄에 있다는 이유로 다운로드 코드 실행 성공으로 쓰지 않았다. 해당 URL 요청·다운로드·원격 코드 실행은 이번에 재현하지 않았다.
- 원전의 큰따옴표 안 $api가 부모에서 먼저 확장되는 문제를 고쳤다. 4104의 VirtualAlloc 문자열은 API 호출·메모리 인젝션·AMSI 우회 성공이 아니다.
- 4104는 모든 실행 결과나 최종 값의 완전한 추적기가 아니다. ScriptBlockId, messageNumber/messageTotal, processID와 Sysmon processGuid의 역할을 구분했다.
- certutil의 파일 복원과 파일 실행을 분리했다. 원전 Defender 탐지를 모든 certutil 명령의 결과로 일반화하거나 Sysmon 1의 대체라고 설명하지 않았다.
- 원전 WINWORD.EXE도 모의 컴파일 프로그램이다. 본문에서 실제 Office·문서·매크로 실행으로 바꾸어 쓰지 않았다. 파일 이름·서명·경로·제품·부모 GUID와 문서 출처를 구분했다.
- 실제 악성코드, 자격증명 탈취, 인젝션, 매크로, 보호 해제, 실제 공격용 LOLBin 명령을 실행하지 않았다. 나머지 도구는 정상 기능과 인자를 읽는 탐색 범위로 설명했다.

## 원상복구와 산출물

저자가 만든 block.ps1·p.b64·p.txt·w.cs·WINWORD.EXE 다섯 파일을 사전 확인한 고정 경로로 각각 제거했다. 본문의 수정 절차는 block.ps1을 만들지 않으므로 네 파일이다. 빈 전용 폴더의 제거와 Test-Path False, 센서 Running, Defender 보호 True, 실행 정책 불변을 확인했다. 추가 구문 검사는 문자열 파싱만 수행하며 실습 객체를 다시 만들지 않았다.

DOCX 36쪽, 복사용 입력 30개(명령 19·DQL 11), 실제 화면 4, 도식 4, 새 삽화 2개다. 원본 UI 전체 화면에서 필요한 영역만 잘랐고 긴 commandLine은 실제 값 영역을 캡처했다. 합성 UI는 없다. 렌더러의 LibreOffice 부재와 Word 대체 경로는 4장과 같다. 최종 페이지·URL·미디어·예제 검사는 chapter05-qa.json에 기록했다. 모든 실패 분기나 다른 OS 버전에서의 동작까지 실행 검증한 것은 아니다.
