# 6장 집필·검토 기록

2026-11-03. 「자격증명 접근과 외부 통신」. Module 01 실습 43·47·48, 슬라이드 461~472·499~516을 구성했다. 기존 1~5장 원고·예제·자산은 변경하지 않는다. 합본·배포용 PDF·REV01·강의 저장소를 만들거나 수정하지 않는다.

## 원전과 근거

원전: https://docs.google.com/presentation/d/1o0H_2DDHBp8p2HvlSnEPbx6-jdURYzew

Drive 메타데이터의 제목은 Module01_Wazuh_위협탐지_DQL.pptx, 크기는 18389162바이트, 수정 시각은 2026-11-03T00:27:22.335Z였다. 캐시 SHA256은 `21c35b306bf7b48fd02e9fd81dfe9fdc97e370de6b610f5b3b3a0cc11daf0f03`이다. 텍스트와 해당 구간의 내장 이미지 14개를 읽었다. 터미널 모양으로 구성한 원전 입력 화면을 새로운 실행 증거로 취급하지 않았다. 원전의 7·1·3 hits와 현재 관찰을 분리했다.

Microsoft Sysmon·ProcDump·Process Security and Access Rights·추가 LSA 보호·Credential Guard 구성과 확인·Windows PowerShell 5.1 Invoke-WebRequest·Resolve-DnsName·Windows DNS 오류 문서를 대조했다. IANA 사설 주소와 RFC 6761·7686으로 주소 및 특별 용도 이름을 확인했다. 전체 URL 13개는 본문에 인쇄한다. kt66 기준은 `63d4180b1d6866de986ef263a3bd831d6082b5d5`이며 Windows 안내와 sensors.ps1 캐시를 대조했다.

## 실제 관찰

kt66 VM 192.168.0.107의 기존 Windows 게스트 KT66-WIN-01, Wazuh 에이전트 windows-user/005를 사용했다. 게스트 주소는 172.30.70.2, 기본 게이트웨이·DNS 설정은 172.30.70.1이었다. 새 설치나 공격자 VM 작업은 수행하지 않았다.

|대상|관찰 결과|
|---|---|
|센서|WazuhSvc·Sysmon64·osqueryd Running. Sysmon 15.22. `Sysmon64.exe -c`로 현재 적용 설정을 읽음|
|보호 상태|Defender RealTimeProtectionEnabled·IsTamperProtected True. 기존 RunAsPPL·RunAsPPLBoot 0. DeviceGuard VBS 상태 0, 기능 목록 0|
|LSASS 접근|Sysmon 10/9407. osqueryd PID 5156 → lsass PID 916. GrantedAccess 0x1fffff. 원본과 Wazuh 필드 일치|
|osquery 파일|Authenticode Valid, Osquery Foundation, 제품 osquery, 버전 5.12.1.0. 이름·서명만으로 모든 행위를 정상으로 확정하지 않음|
|HTTP|PowerShell PID 8080. 내부 WAF `http://10.20.32.80/?book=book2-ch06`에 GET 3회. 상태 200·최종 URI 동일·RawContentLength 23181|
|연결|Sysmon 3/9451·9454·9455. 같은 processGuid, tcp/initiated true, 목적지 10.20.32.80:80, 출발지 포트 57522·57523·57524|
|DNS|별도 PowerShell PID 1540. example.com의 A 조회는 주소 2개·상태 0. book2-ch06.invalid는 이름 부재·상태 9003|
|DNS 이벤트|Sysmon 22/9461·9462. 두 기록의 processGuid 일치. 실패 응답 queryResults에는 `type: 6 a.root-servers.net;`가 존재|
|Wazuh 경보|위 10·3·22 문서에는 rule.id 없음. 저자용 EncodedCommand 래퍼의 프로세스 생성 이벤트에는 92057이 존재하며 통신 자체의 경보와 구분|

증거는 `evidence/chapter06/2026-11-03/`의 preflight·observe·collect·final-state·sysmon-current.json에 있다. 저자용 SSH 전송은 PowerShell EncodedCommand 래퍼를 사용했다. 이 방식 때문에 생긴 부모 명령줄은 독자의 콘솔 직접 입력과 다르다. 본문은 관리자 PowerShell에서 한 블록씩 수행하는 순서이며, 출력 서식·변수 이름·줄 나눔이 저자 수집 스크립트와 완전히 같은 것은 아니다. final-state의 서비스 JSON 숫자 4는 Running이다.

구형 Wininit 12 두 건의 시각은 2026-11-02 09:28·09:30 UTC였고, 마지막 부팅은 같은 날 10:55:37.500 UTC였다. 이를 현재 부팅의 LSA 보호 증거로 사용하지 않았다. 현재 보호의 확정 여부와 레지스트리 값·Defender·Credential Guard를 분리했다. 초기 SSH 출력 일부의 한국어 인코딩 손상과 Sysmon UTF-16 NUL은 원본 그대로 보존하고, 영문 필드와 XML 및 숫자 값으로 대조했다.

## DQL과 입력 검토

Q06-01~09를 실제 Discover, wazuh-archives-*, Last 24 hours에서 실행했다. 완료된 결과를 판독했으며 즉시 응답에 남은 이전 검색 결과를 검증값으로 사용하지 않았다. 상세 식·건수는 chapter06-query-ui.json에 있다. 넓은 LSASS 후보는 5529건, 원본 9407은 1건, osquery 생성 GUID는 1건, 내부 HTTP 대상·GUID·프로그램 후보는 각각 3건, DNS 두 식은 각각 1건, 원전 서비스 도메인 식은 0건이었다. 건수는 조회 시각과 데이터 보존·반복에 따라 달라진다.

최종 본문 명령 16개는 Windows PowerShell 파서로 검사했으며 구문 오류가 없었다. 이 검사는 입력 문자열의 구문 검사이며 모든 실패 분기와 전체 최종 절차를 다시 실행했다는 뜻이 아니다. C06-10의 본문 확인은 독자가 응답 내용을 읽는 절차이며, 저자 증거에 보관한 HTTP 값은 코드·최종 URI·내용 크기다. source-analysis의 ProcDump·원전 HTTP·원전 DNS 입력은 분석용이며 실행 예제 목록에서 분리했다.

## 원전 교정

- Windows 입력의 실행 위치를 게스트로 명시했다. 원전의 공격자 VM 표기를 Linux 실행 위치로 옮기지 않았다.
- LSASS에 평문 암호가 항상 존재한다고 설명하지 않는다. 메모리 접근·덤프 파일·인증 자료 해석·인증 악용을 분리했다.
- 새 LSASS 덤프, Mimikatz, 자격증명 추출, Pass-the-Hash, PPL·Credential Guard·Defender 해제는 실행하지 않았다. 원전의 해제 명령은 준비 단계로 제공하지 않는다.
- PPL 차단을 모든 이벤트 10의 부재로 일반화하지 않았다. 제품 차단 단계·로그 수집 조건을 조사하게 했다.
- 권한은 비트마스크다. 0x1010·0x1410·0x1fffff를 덤프 성공의 판정식으로 쓰지 않는다. UNKNOWN callTrace를 코드 주입 증명으로 바꾸지 않는다.
- 정상 프로그램 이름의 포괄 제외를 제거했다. 경로·서명·해시·승인된 작업과 후속 결과를 조사한다.
- HTTP 요청 수와 TCP 연결 수, 응답 뒤 대기와 정확한 주기, 내부 WAF와 외부 C2를 구분했다. 짧은 반복만으로 비컨을 확정하지 않는다.
- 원전의 172.16.* 제외는 전체 172.16/12 범위가 아니다. 전체 사설 범위를 설명하고 프로그램 후보를 모아 조직 주소 목록으로 분류하도록 했다. IPv6·특수 주소·NAT·프록시를 누락한 인터넷 판정식을 만들지 않았다.
- DNS 질의·성공 응답·접속·터널링·자료 유출을 분리했다. 9003과 SOA 결과를 A 주소나 실제 접속으로 읽지 않는다.
- ngrok·DuckDNS·Pastebin의 용도를 구분하고 정확한 도메인 경계를 사용했다. 광범위한 부분 문자열·최상위 도메인·.onion 조회를 단독 악성 판정으로 쓰지 않았다.
- sourceProcessGUID·targetProcessGUID와 processGuid의 필드 표기, PID 재사용, 서로 다른 세 프로세스를 명시했다.

## 원상복구와 그림

조회와 소량의 정상 HTTP·DNS 요청만 수행했다. 새 파일·서비스·작업·보호 정책을 만들지 않았다. 센서와 보호 상태는 사전 값과 같았다. 원래 있던 파일·이벤트·DNS 캐시를 삭제하지 않았다.

실제 UI 화면 5개는 원본 화면의 직사각형 영역만 잘랐다. 첫 조판에서 툴팁이 필드를 가린 4개를 발견해 UI에서 툴팁을 해제한 뒤 다시 촬영했다. 좌표와 원본·자산 해시는 chapter06-screenshot-provenance.json에 있다. 조작한 UI 도식은 없다. 관계 도식 5개와 생성 삽화 2개를 사용한다.

여성 삽화는 사용자의 팔·손·거치대 교정과 최종 요청에 따라 닫힌 노트북을 한 손으로 드는 자세로 바꾸었다. 사용자가 “ㅇㅋ 됐다”로 승인한 `exec-c08458b6-aeeb-40e6-a3dc-209feff48050.png`를 그대로 복사했다. 이전 선반·카트 후보는 모두 제외했다. 다른 삽화는 장비 보관실에서 평평한 노트와 컴퓨터를 비교하는 남성이다. 양팔·손, 문서 방향, 화면 뒷면, 지지 구조, 투명 배경과 실제 지면을 확인했다. 프롬프트와 승인 이력은 삽화 JSON에 보관한다.

## 조판 검토

DOCX 38쪽. 복사용 입력 25개(명령 16·DQL 9), 화면 5·도식 5·삽화 2다. 부크크 B5 원본의 첫 구역 판형·여백·테마를 유지했다. bundled render_docx.py는 soffice.exe 부재로 실패하여 기존 hidden Word COM PDF 내보내기와 pypdfium2 렌더를 사용했다. 기존 임시 PDF 덮어쓰기 실패 뒤 새 파일을 사용했으며 최종 렌더는 chapter06-final2.pdf다. PDF·페이지 PNG는 build의 내부 검토용이다.

초기 38쪽을 모두 개별 확인했다. 툴팁·개념도 화살표·긴 명령 속성 나열·용어 정의를 수정하고 명령·DQL 줄 나눔과 제목 스타일을 정리했다. 최종 렌더를 이전 이미지 해시와 비교해 변경된 28쪽을 다시 개별 확인했다. 나머지 10쪽은 최초 검수 지면과 이미지 해시가 같았다. 전체 URL 13개, 입력 25개, 내장 그림 12개, 판형·여백·테마를 대조했다. 최종 해시·URL·미디어·파서·판면 확인 결과는 chapter06-qa.json에 기록했다. 재현하지 않은 공격의 성공이나 다른 OS·네트워크의 모든 분기까지 검증한 것으로 표시하지 않는다.
