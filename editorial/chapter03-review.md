# 3장 집필·검토 기록 · 2026-11-03

## 범위와 원전

제목은 **자격증명과 계정 권한의 변화**다. 지정 Module 01 실습 35~37·50을 준비, 입력, 응답, Windows 원본, Wazuh 검색, 조사·대응, 원상복구로 재구성했다. 41쪽 DOCX, 복사용 입력 33개(명령 25·DQL 8), 실제 Wazuh 화면 7개, 관계 도식 4개, 인물 삽화 2개다. 합본·배포 PDF·REV01은 만들거나 수정하지 않았다.

- 원전: https://docs.google.com/presentation/d/1o0H_2DDHBp8p2HvlSnEPbx6-jdURYzew
- PPTX 726장, SHA256 `21c35b306bf7b48fd02e9fd81dfe9fdc97e370de6b610f5b3b3a0cc11daf0f03`.
- 실습 35: 슬라이드 순서 387~394. NTLM·NewCredentials.
- 실습 36: 395~402. 명시적 자격증명과 C$ 접근 거부.
- 실습 37: 403~411. 계정·그룹 변경.
- 실습 50: 527~535. 감사 정책과 특수 권한.
- kt66 기준: `63d4180b1d6866de986ef263a3bd831d6082b5d5`.

## 실제 수행 범위

준비된 KT66-WIN-01에 kt66 호스트를 경유한 SSH 관리자 PowerShell로 접속했다. 브라우저 콘솔을 통한 독자 입력과 저자의 접속 경로를 구분한다. 새 설치·해시 추출·실제 Pass-the-Hash·외부 호스트 이동·LSASS 덤프는 수행하지 않았다. Defender 실시간 보호와 변조 보호는 True를 유지했다.

저자용 연결·원본 수집 도구는 타임스탬프와 출력을 모으는 자동화다. 독자용 본문은 개별 명령과 GUI 검색을 유지했다. 계정 변경과 감사 정책 변경은 저자용 try/finally로 원상복구를 보장했다. 본문의 한 줄씩 실행 절차와 같은 실행 형태라고 주장하지 않는다. 기록은 `evidence/chapter03/2026-11-03/`에 있다.

| 입력 | 실제 관찰 | 원상복구 |
|---|---|---|
| victim 정상 암호로 127.0.0.1 IPC$ | 성공, 4624 번호 10627, 유형 3, NTLM/NtLmSsp | 해당 IPC$ 해제·빈 목록 |
| victim 정상 암호로 127.0.0.1 C$ | 오류 5 접근 거부, 4648 번호 10676와 4624 번호 10678 | 연결이 없어 삭제 생략 |
| LogonUserW, 유형 9·공급자 3 | True, 4624 번호 10712, 로컬 kt66student·외부 이름 fakeadmin/CORP | CloseHandle True |
| 비활성 book2_ch03 생성·관리자 그룹 추가 | 4720 10751, 4732 10755, SID 끝 1002 | 4733 10757, 4726 10759, 계정 부재·기존 구성원 둘 |
| 로그온 성공 감사 해제·즉시 활성화 | 4719 10862/10865, 원본 시각 간격 약 55ms | Success and Failure 재확인 |

초기 IPC$ 시험의 저자 명령에는 `/persistent:no`가 있었다. 기본 연결 기억 설정이 변경된 것을 확인하고 다음 단계에서 `/persistent:yes`로 사전 상태를 복원했다. 본문은 장치 문자 없는 IPC$ 연결에 불필요한 `/persistent:no`를 제외했다. 최종 출력은 “New connections will be remembered”, 빈 연결 목록이다. 옵션을 제거한 명령을 별도로 다시 실행했다고 주장하지 않는다.

계정 생성은 저자 도구에서 일회용 시험 문자열을 SecureString으로 변환했다. 계정은 처음부터 비활성이며 해당 자격증명으로 로그인하지 않았다. 본문은 암호를 파일에 쓰지 않도록 Read-Host -AsSecureString으로 받는다. 이 대화형 입력 자체는 SSH 자동 수집에서 실행하지 않았다. 계정 생성·SID 확인·그룹 추가·제거·계정 삭제 동작은 실제 수행했다.

C03-14의 C$ 삭제는 연결이 있을 때의 조건부 절차로 미실행이다. C03-11A는 최종적으로 -FilterXPath에서 EventRecordID를 직접 지정하고 ToXml로 읽어 10676 원본을 확인했다. 이전의 기간 조회 후 Where-Object 선택은 SSH 읽기 제한 90초 안에 완료되지 않아 본문에서 교체했다. C03-13의 grep·ls도 최종 읽기 확인을 마쳤다. `final.json`에 원본·설정·최종 계정/그룹/감사/서비스/보호 상태가 있다. 신규 설정 적용이나 보관 기능 활성화는 수행하지 않았다. PowerShell 입력은 정적 구문 검사와 실제 동작 기록을 나누어 확인한다.

## 원본·Wazuh 대조와 수정 근거

1. **NTLM과 Pass-the-Hash를 구분했다.** 정상 암호로 같은 NTLM 로그온을 만들었다. 유형 9 역시 해시 사용의 증명이 아니다. 원전의 미정의 `[K.A]` 호출을 완전한 Add-Type 정의와 CloseHandle 정리로 보완했다. 실제 logonProcessName은 Advapi, 인증 패키지는 Negotiate였다. seclogo 한 값만 필수 조건으로 두지 않는다.
2. **로컬·외부 계정을 구분했다.** 유형 9의 TargetUserName은 kt66student, TargetOutboundUserName은 fakeadmin, TargetOutboundDomainName은 CORP이다. 외부 자원의 인증 성공은 확인하지 않았다. 해당 세션 0x1e2a3b9에 4672 10713도 있으나 그것을 fakeadmin의 원격 권한 획득으로 해석하지 않는다.
3. **4648·4624·공유 권한을 구분했다.** C$ 오류 5와 네트워크 인증 성공은 모순이 아니다. 4648의 Subject는 kt66student, Target은 victim이다. TargetServerName이 KT66-WIN-01이어도 주소는 루프백이다. `NOT localhost` 조건은 횡적 이동의 충분조건이 아니다.
4. **경보 없음과 미수집을 구분했다.** 4648 10676은 archives.json과 wazuh-archives-*에 있고 alerts에는 없다. 보관 레코드에는 rule 필드가 없다. 미확인 “레벨 0 규칙”을 원인으로 쓰지 않는다. 현장 설정은 logall_json yes, log_alert_level 3, Filebeat archives enabled true였다.
5. **원본과 디코딩 필드 이름을 대조했다.** 4648의 원본 ProcessName은 `-`이나 Wazuh eventdata에는 필드가 생략됐다. 4732의 MemberName도 원본 `-`이고 화면에는 memberSid만 있다. 4719는 원본 AuditPolicyChanges 코드가 auditPolicyChangesId에, 해석한 문구가 auditPolicyChanges에 나타난다.
6. **계정·그룹·수행자를 구분했다.** 4720 targetSid와 4732 memberSid를 연결한다. 4732 targetSid는 그룹 SID S-1-5-32-544이다. 원전의 활성 backdoor 계정을 비활성 book2_ch03으로 바꾸어 계정·그룹 변경을 관찰했다. 4722 활성화와 도메인 글로벌 그룹 4728은 의미만 설명하며 재현을 주장하지 않는다.
7. **감사 방향과 권한 사용을 구분했다.** 4719의 %%8448/%%8449는 성공 감사 제거/추가이다. 4672의 SeDebugPrivilege는 새 세션에 할당된 권한이지 LSASS 덤프 성공이 아니다. 보호 수준과 실제 접근 결과가 따로 필요하다.
8. **식별 범위를 제한했다.** EventRecordID는 컴퓨터·채널과 함께 대조한다. Security의 589와 PowerShell 채널의 589를 혼동하지 않는다. LogonId는 같은 컴퓨터와 시간 구간에 제한한다. XML UTC 시각과 UI 한국 시각, Wazuh 수집 시각을 구분한다.

관찰된 규칙은 4624/NTLM 60106(3), 유형 9 67022(3), 4672 67028(3), 4720 60109(8), 4732·4733 60154(12), 4726 60111(8), 4719 60112(8)이다. 규칙의 동일성이나 MITRE 태그를 침해 사실·공격 성공으로 해석하지 않는다. 4672 10745의 수행자 세션 0x1e38ea7을 계정·그룹 변경과 연결했다.

## DQL와 화면

Discover에서 본문 DQL 8개를 입력했다. Last 24 hours 조회 당시 Q03-01/02/03/04/05/06/07/08 결과는 각각 **3·1·3·2·2·2·1·21건**이었다. Q03-03만 wazuh-archives-*이고 나머지는 wazuh-alerts-*이다. 범위에 이전 실습 기록도 들어 있으므로 건수를 이번 입력 수와 같다고 쓰지 않았다. `dql-ui.json`에 조회식·시간 범위·결과 UI 상태를 기록했다.

실제 Wazuh 단일 문서 화면을 CUA로 촬영했다. UI를 합성하거나 그림으로 대체하지 않았다. ntlm-fields 10627, type9-fields/type9-identity 10712, explicit-fields 10676, group-fields 10755, policy-fields 10862, privilege-fields 10745에 대응한다. 마지막 그림은 Message의 권한 목록을 펼쳐 다시 촬영했다. 본문 필드와 캡션, 원본 기록을 대조했다.

인물 삽화는 통신함 앞 조사자, 장비 보관실의 권한 검토 담당자로 달리 구성했다. 생성 도구는 built-in image_gen이며 프롬프트·생성 파일·해시는 illustration-prompts.json, illustration-refresh.json에 있다. 관계 도식은 tools/build_chapter03.py로 생성했다.

## 조판·검수

부크크 B5 원본 판형·여백을 상속했다. 본문 BookkMyungjo Light 10.5pt, 제목 BookkGothic Light, 코드 Consolas 10pt를 유지했다. 전체 41쪽을 렌더해 육안 검사했고 원본 XML 조회와 최종 화면 반영 후 달라진 21쪽을 다시 확인했다. 화면 7·35쪽은 개별 지면으로 가독성을 확인했다. 그림·표·코드·캡션의 잘림, 전체 URL 12개, 예제 파일 33개의 본문 일치를 검사했다. LibreOffice 실행 파일 부재로 이 턴의 packaged renderer가 동작하지 않아 저장소의 숨김 Word COM 렌더를 사용했다. PDF와 페이지 PNG는 build에만 두었다. 파일 해시와 검수 결과는 chapter03-qa.json에 기록한다.

공식 근거는 본문 참고자료의 Microsoft 이벤트 문서·LogonUserW·auditpol·New-LocalUser, Wazuh Event logging과 기준 kt66 코드를 사용했다. 강의 슬라이드의 공격·방어 학습 목표를 유지하되 위의 관찰 한계와 실행 차이를 저자 기록으로 남긴다.
