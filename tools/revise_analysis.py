"""2026-11-04 분석 보강. 생성기와 현재 JSON에 같은 편집을 적용한다."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
REV='analysis-2026-11-04'
WIN='agent.name:"windows-user"'
SEC=WIN+'\nAND data.win.system.channel:"Security"'
SYS=WIN+'\nAND data.win.system.channel:\n "Microsoft-Windows-Sysmon/Operational"'
PS=WIN+'\nAND data.win.system.channel:\n "Microsoft-Windows-PowerShell/Operational"'
ARCH='wazuh-archives-*'; ALERT='wazuh-alerts-*'
NET='{af6e9a1f-8d82-6ae9-d106-000000000300}'
DNS='{af6e9a1f-8d8d-6ae9-d406-000000000300}'
SCRIPT='{af6e9a1f-780c-6ae9-7406-000000000300}'
def p(t):return {'type':'p','text':t}
def tb(rows,heads=('확인 대상','관찰과 판단'),widths=(34,93)):
 return {'type':'table','head':list(heads),'rows':rows,'widths':list(widths),'keep':True}
def q(i,t,why,result,index=ARCH):
 return {'type':'query','id':i,'where':'Windows PC · Wazuh Discover · '+index+' · DQL','text':t,'why':why,'result':result,'revision':REV}
def pg(t,*b):return {'title':t,'kind':'body','level':'section','break':False,'blocks':list(b),'revision':REV}
def screenshot(name,caption):return {'type':'image','path':'assets/screenshots/analysis-revision/'+name,'caption':caption,'width_mm':127}
def before(pages,anchor,*new):
 i=next(i for i,x in enumerate(pages) if x['title'].startswith(anchor));pages[i:i]=new
def replace_text(pages,old,new):
 for page in pages:
  for b in page['blocks']:
   for k in ('text','why','result'):
    if old in b.get(k,''):b[k]=b[k].replace(old,new)
def window(a,b):return f'\nAND timestamp >= "{a}"\nAND timestamp < "{b}"'
def revise(ch,pages):
 pages[:]=[x for x in pages if x.get('revision')!=REV]
 if ch==1:
  before(pages,'검색 결과가 없을 때',pg('같은 원본의 수집과 경보를 따로 확인하기',
   p('Q01-03의 Security RecordId 9115를 펼쳐 컴퓨터 KT66-WIN-01, 이벤트 4624, 원본 시각과 계정 kt66student를 대조한다. Wazuh의 rule.id는 60200이며 로그온 유형은 8이다. 이 결과는 해당 로그온 이벤트가 수집되어 경보로 저장되었다는 뜻이다. 암호 노출이나 비인가 접속의 판정은 인증 방식과 접속 프로그램을 더 조사해야 한다.'),
   p('3장에서 archives 저장과 색인 준비를 확인한 환경이라면 아래 검색으로 같은 원본의 보존 여부도 비교한다. 준비하지 않은 환경에서는 현재 alerts 대조까지 기록하고, archives 검색은 준비 후 수행한다.'),
   q('Q01-05',SEC+'\nAND data.win.system.computer:"KT66-WIN-01"\nAND data.win.system.eventID:"4624"\nAND data.win.system.eventRecordID:"9115"',
     '데이터 보기를 archives로 바꾸고 2026년 11월 3일을 포함한다. 기존 검색 필터를 해제한다. 자신의 기록 번호와 원본 시각으로 바꿀 때에도 채널 조건을 유지한다.',
     '보존 자료에서는 1건이다. alerts와 archives에 각각 있는 같은 원본을 두 번의 로그온으로 세지 않는다.'),
   p('두 데이터 보기에서 모두 찾으면 수집과 경보 저장을 확인한 것이다. archives에만 있으면 수집된 원본과 규칙·경보 저장 조건을 조사한다. 둘 다 없으면 Windows 원본 존재 여부부터 수집 경로를 확인한다. 원본이 없는 상태에서 중앙 수집 실패를 먼저 확정하지 않는다.')))
 elif ch==2:
  before(pages,'RDP 세션 원상복구',pg('로그온 뒤 같은 세션의 종료 확인',
   p('4624의 targetLogonId는 만들어진 로그온 세션을 식별한다. 예시의 10207번 기록에서는 0x1ca2207이다. 같은 컴퓨터의 짧은 시간 범위에서 수행 세션을 뜻하는 subjectLogonId와 대상 세션을 뜻하는 targetLogonId를 함께 찾는다.'),
   q('Q02-08',SEC+'\nAND data.win.system.computer:"KT66-WIN-01"\nAND (data.win.eventdata.subjectLogonId:"0x1ca2207"\n OR data.win.eventdata.targetLogonId:"0x1ca2207")'+window('2026-11-03T12:05:00+09:00','2026-11-03T12:20:00+09:00'),
     '시간 선택기도 이 구간을 포함한다. >=는 시작 포함, <는 끝 제외이며 +09:00은 KST다. OR로 두 필드 중 하나가 일치하는 문서를 찾는다.',
     'archives에서 4624·RecordId 10207과 4634·RecordId 10222를 찾는다. Time을 오름차순으로 정렬하고 각 문서의 systemTime·targetUserName·targetLogonId를 비교한다.'),
   p('이 사례는 victim의 원격 대화형 로그온과 같은 세션의 로그오프가 기록된 경우다. 4634는 해당 로그온 세션의 종료를 뒷받침한다. 다른 세션까지 모두 종료되었다는 뜻은 아니므로 다음 절의 현재 세션 조회도 수행한다.'),
   p('같은 주소의 앞선 실패와 이번 성공은 조사 후보로 연결한다. 암호 대입이 성공 원인이었는지는 승인된 시험 입력과 계정 사용 내역을 대조한다. 로그오프가 없으면 세션이 계속 열린 경우와 기록 부재를 구분하고 현재 세션·수집 범위를 확인한다.')))
 elif ch==3:
  before(pages,'계정 변경의 침해 판단',pg('만든 계정이 실제로 사용되었는지 확인',
   p('계정 생성과 관리자 그룹 편입은 권한 상태의 변화다. 그 계정으로 로그온했는지는 4624에서 별도로 확인한다. 이름이 재사용될 수 있으므로 4720의 targetSid를 4624의 targetUserSid와 비교한다. 4732에서는 같은 구성원을 memberSid로 표시한다.'),
   q('Q03-09',SEC+'\nAND data.win.system.eventID:"4624"\nAND data.win.eventdata.targetUserSid:\n "S-1-5-21-3937859836-2530084332-1215515481-1002"',
     '2026년 11월 3일의 생성·삭제 구간을 포함한다. SID 전체를 자신의 4720 기록 값으로 바꾼다. 계정 이름 조건과 대상 그룹 SID를 대신 넣지 않는다.',
     '보존 자료에서는 0건이다. 생성 때 Enabled=False였던 사실과 함께 기록하되, 검색 결과만으로 과거 모든 기간의 사용 부재를 증명하지 않는다.'),
   tb([['변경한 계정','book2_ch03, 끝자리 1002인 SID'],['변경 수행자','kt66student, subjectLogonId 0x1e38ea7'],['변경의 순서','4720 생성\n4732 편입\n4733 제거\n4726 삭제'],['사용 여부','대상 SID의 4624는 선택 범위에서 없음']]),
   p('완료 기록에는 비활성 계정의 생성·그룹 편입·제거·삭제와 사후 계정 부재를 적는다. 4672의 특수 권한은 변경 수행자의 세션에 부여된 것이므로 새 계정의 관리자 로그온으로 읽지 않는다. 비인가 변경이라면 수행자 세션과 변경 요청을 먼저 대조하고, 사용 흔적과 영향에 따라 계정 통제 범위를 결정한다.')))
 elif ch==4:
  before(pages,'4.5',pg('Run 값을 쓴 프로세스와 삭제 기록',
   p('Q04-05의 13번 이벤트에서 processGuid를 복사한다. 그 GUID는 레지스트리 값을 쓴 reg.exe의 것이다. 등록된 book2_ch04_missing.exe가 실행되었다는 식별자가 아니다.'),
   q('Q04-08',SYS+'\nAND data.win.system.eventID:(1 OR 13)\nAND data.win.eventdata.processGuid:\n "{af6e9a1f-765d-6ae9-4006-000000000300}"',
     '2026년 11월 3일 14:50~14:55 KST를 포함하여 생성과 값 설정을 함께 조회한다.',
     '8886번의 reg.exe 생성과 8887번의 SetValue가 나온다. PID 9140, 부모 powershell.exe, 계정 kt66student가 연결된다. commandLine의 /v 값 이름과 /d 등록 경로를 targetObject·details와 대조한다.'),
   q('Q04-09',SYS+'\nAND data.win.system.eventID:(12 OR 13)\nAND data.win.eventdata.targetObject:*book2_ch04_run',
     '생성 GUID 필터를 제거하고 같은 값 경로를 찾는다. 삭제는 별도로 실행한 reg.exe의 GUID를 가지므로 생성 GUID만 유지하면 누락된다.',
     '8887의 SetValue와 8935의 DeleteValue를 읽는다. 삭제 시각은 14:53:13 KST이며 생성 때와 GUID가 다르다.'),
   p('이 사례의 확인 범위는 Run 값 등록과 삭제다. 해당 경로의 파일은 준비하지 않았고 새 로그온으로 자동 실행도 시험하지 않았다. 지속화가 실제 실행되었다는 결론에는 별도의 프로세스 생성과 실행 결과가 필요하다.')),
   pg('세 가지 지속화 후보의 조사 결론',
   tb([['서비스','7045·4697로 등록과 수행자를 확인했다. STOPPED이고 대상 파일이 없어 실행 성공 근거는 없다.'],['예약 작업','4698의 작업 정의와 SYSTEM으로 실행한 PowerShell의 문구 출력을 연결했다. 예약 등록과 실제 실행을 구분한다.'],['Run 값','13의 값 설정을 1의 reg.exe 생성에 연결했다. 12의 DeleteValue와 현재 값 부재로 원상복구를 확인한다.'],['osquery','added·removed는 두 예약 조회 사이의 상태 변화다. 이벤트 시각과 동일한 생성·삭제 시각으로 치환하지 않는다.']]),
   p('의심 등록을 발견하면 등록 명령·경로·계정·시각을 보존하고 승인된 설치·관리 작업인지 확인한다. 파일을 조사하기 전에 실행해 보지 않는다. 미승인 실행과 영향이 확인되면 관련 서비스·작업·계정의 통제 범위를 정하고, 조치 후 현재 상태와 후속 이벤트를 다시 대조한다.')))
 elif ch==5:
  before(pages,'5.5',pg('4104를 실행 프로세스에 연결',
   p('Q05-03의 4104에는 processGuid가 없다. 이 PowerShell 채널에서 data.win.system.processID는 스크립트를 처리한 PowerShell 프로세스 PID이며 예시 값은 5228이다. Sysmon 채널의 System ProcessID는 Sysmon 공급자 프로세스이므로 같은 방식으로 연결하면 안 된다.'),
   q('Q05-12',SYS+'\nAND data.win.system.eventID:"1"\nAND data.win.eventdata.processId:"5228"'+window('2026-11-03T14:58:00+09:00','2026-11-03T15:00:00+09:00'),
     '같은 컴퓨터와 짧은 시각 범위에서 Sysmon eventdata.processId를 찾는다. 생성이 더 이르면 범위를 앞쪽으로 넓히고 종료·재사용 여부를 확인한다.',
     'RecordId 8995, GUID 끝부분 7406-000000000300을 찾는다. commandLine은 인코딩 입력이고 rule.id는 92057이다. 4104 RecordId 2530의 처리 코드와 대조한다.'),
   p('이 코드의 VirtualAlloc은 변수에 넣어 출력한 문자열이다. 92057은 인코딩된 PowerShell 실행을 분류한 경보이고, 4104 자체에는 같은 경보가 없다. 문자열 존재·프로세스 생성·실제 API 호출은 서로 다른 사실이다.')),
   pg('처리 코드 이후의 파일과 통신 조회',
   q('Q05-13',SYS+'\nAND data.win.system.eventID:(1 OR 3 OR 11 OR 22)\nAND (data.win.eventdata.processGuid:\n "'+SCRIPT+'"\n OR data.win.eventdata.parentProcessGuid:\n "'+SCRIPT+'")',
     '2026년 11월 3일 14:58~15:00 KST로 조회한다. processGuid는 해당 프로세스의 활동, parentProcessGuid는 직접 자식의 생성 후보를 찾는다. 손자 이하까지 자동으로 확장되는 검색은 아니다.',
     '각 문서의 이벤트 번호를 읽고 파일은 targetFilename, 연결은 destinationIp·destinationPort, 질의는 queryName을 기록한다. 자식이 발견되면 그 자식 GUID로 다시 조회한다.'),
   p('문구 출력 사례에서는 인코딩 실행과 처리 코드를 연결해 조사한다. 예상하지 않은 파일·자식·연결이 있으면 경로·내용·승인 작업을 더 확인한다. 단순히 출력 문자열이 의심 API 이름이라는 이유로 메모리 주입이 성공했다고 판정하지 않는다.'),
   p('파일·통신 이벤트가 없으면 해당 시각에 Sysmon 11·3·22가 수집되도록 설정되었는지 확인한다. 필터로 빠진 활동의 부재까지 증명할 수는 없다. 확인된 코드와 관측 가능 범위를 남긴 뒤 실습 파일의 원상복구 절차로 진행한다.')))
 elif ch==6:
  before(pages,'6.3',pg('ProcDump 사례와 osquery 접근의 비교',
   p('원전 실습 43은 ProcDump의 LSASS 접근을 분석한다. 현재 보존 자료에서 읽은 9407번은 osquery의 접근이다. 두 프로그램이 같은 targetImage와 넓은 권한을 보일 수 있으므로 접근 권한 하나로 덤프 성공을 판정하지 않는다.'),
   tb([['접근 주체','원전: procdump64.exe. 현재: 정해진 Program Files 경로의 osqueryd.exe.'],['실행 목적','원전 입력은 전체 메모리 덤프와 l.dmp 저장을 요청한다. 현재 생성 기록은 osquery.flags를 사용하는 수집 프로세스다.'],['추가 근거','명령·부모·계정·서명·설치 및 승인 내역을 확인한다. 덤프라면 실제 출력 파일·크기·시각·해시를 별도로 확인한다.'],['판정 한계','Sysmon 10은 접근 기록이다. 파일 작성·인증 자료 추출·다른 호스트의 인증 성공까지 대신 증명하지 않는다.']]),
   p('현재 예시에서는 Q06-03으로 1606번 생성 이벤트를 찾고 부모도 osqueryd.exe이며 SYSTEM으로 실행된 것을 확인한다. 서명 확인의 Valid와 Osquery Foundation, 버전 5.12.1.0을 준비된 수집 서비스와 대조한다. 승인된 osquery 수집 활동과 일치하는 접근으로 분류하되, 이름만 같은 다른 경로·해시까지 일괄 제외하지 않는다.'),
   p('의심 덤프가 발견되면 해당 프로세스·파일·LSASS 접근과 이후 인증 기록을 보존한다. 격리와 자격증명 교체는 노출된 계정·권한·후속 사용의 범위를 확인하여 결정한다. 원전의 보호 해제 설정을 운영 방어 절차로 적용하지 않는다.')),
   pg('수집된 원본과 저장된 경보의 직접 비교',
   p('같은 Sysmon 원본 여섯 건을 archives와 alerts에서 각각 찾는다. 먼저 아래 식을 archives에서 실행한 뒤 데이터 보기만 alerts로 바꾸어 같은 기간·조건을 유지한다. 두 데이터 보기의 결과를 합산하지 않는다.'),
   q('Q06-10',SYS+'\nAND data.win.system.eventRecordID:\n (9407 OR 9451 OR 9454 OR 9455 OR 9461 OR 9462)'+window('2026-11-03T16:00:00+09:00','2026-11-03T17:00:00+09:00'),
     '시간 선택기가 식의 구간을 포함하는지 확인한다. 컴퓨터·eventID·systemTime도 원본과 대조한다. 번호만으로 다른 채널의 문서와 연결하지 않는다.',
     '보존 자료에서 archives는 6건, alerts는 0건이다. LSASS 접근 1건, HTTP 연결 3건, DNS 질의 2건이 수집되었지만 같은 원본의 경보 문서는 찾지 못했다.'),
   screenshot('alerts-zero.jpg','화면 6-6  동일한 여섯 원본의 alerts 조회 결과'),
   p('이 환경은 logall_json=yes로 원본 JSON을 저장하고 log_alert_level=3으로 경보 저장 하한을 둔다. archives의 rule.id가 비었다는 사실만으로 정확히 어떤 규칙에서 제외되었는지는 알 수 없다. 규칙 조건·레벨·경보 억제와 색인 상태를 추가로 대조해야 한다.'),
   p('여섯 원본을 archives에서 찾았으므로 이 결과를 전체 수집 실패로 분류하지 않는다. 반대로 alerts 0건을 무해함의 증거로 삼지도 않는다. 다음 절에서는 같은 프로세스의 생성 경보와 통신 원본을 함께 읽는다.')))
  before(pages,'외부 연결 후보의 조사',pg('HTTP 연결을 생성 명령과 연결',
   q('Q06-11',SYS+'\nAND data.win.system.eventID:(1 OR 3 OR 11 OR 22)\nAND data.win.eventdata.processGuid:\n "'+NET+'"',
     '2026년 11월 3일 16:30 전후를 포함한다. 3번만 찾던 조건을 넓히고 Time을 오름차순으로 정렬한다. 각 문서를 펼쳐 utcTime과 부모·명령·대상을 비교한다.',
     '보존 자료는 5건이다. 9448은 생성, 9449는 파일 생성, 9451·9454·9455는 연결이다. 이 GUID의 DNS 22는 없다.'),
   screenshot('http-record-rule.jpg','화면 6-7  HTTP 프로세스의 원본 기록 번호와 경보 규칙'),
   tb([['9448 · 이벤트 1','PID 8080, 부모 powershell.exe, 계정 kt66student. rule.id 92057은 인코딩 실행에 해당한다.'],['9449 · 이벤트 11','Temp의 __PSScriptPolicyTest_로 시작하는 .ps1 파일, 규칙 92213. 경로·내용·생성 문맥으로 조사한다.'],['9451·9454·9455 · 이벤트 3','10.20.32.80:80으로 나간 TCP 연결. 같은 GUID, 서로 다른 출발지 포트이며 해당 원본의 rule.id는 없다.']]),
   p('생성 경보를 통신 탐지 경보로 바꾸어 읽지 않는다. 파일 생성 경보도 그 파일이 악성이라는 판정과 다르다. 예시의 전체 명령을 실행하지 않고 복원하면 내부 WAF에 세 번 요청하는 코드가 나온다. 입력에 IP를 직접 사용했으므로 이 요청을 example.com 질의와 연결할 근거가 없다.')),
   pg('HTTP 조사 결과와 후속 대응',
   p('확인한 동작은 승인된 내부 주소의 HTTP 요청 세 번, 응답 200과 본문 길이 23181, 같은 PID의 TCP 연결 세 건이다. 2.332초와 2.062초 간격은 이 짧은 관찰에서 계산한 두 값이다. 명령 제어 통신의 장기간 주기나 명령 수신을 입증한 결과는 아니다.'),
   p('다른 사례에서는 생성 명령의 URL·부모·계정과 연결 목적지를 확인하고 서버 접근 로그의 시각·요청 경로·응답을 대조한다. NAT로 출발지 주소가 달라지면 변환 경로를 확인한다. 목적지 호스트 이름 필드만으로 HTTP Host 헤더와 요청 도메인을 정하지 않는다.'),
   p('미승인 목적지, 의심 파일 유입, 후속 실행이나 명령 수신이 함께 관찰되면 해당 프로세스와 통신을 조사 대상으로 올린다. 승인된 점검이라면 작업 내역과 결과를 남긴다. 통신을 제한한 경우 정상 업무 경로와 차단 해제 결과도 확인한 뒤 종결한다.')))
  before(pages,'DNS 터널링 조사',pg('DNS 질의 프로세스와 후속 연결 조회',
   q('Q06-12',SYS+'\nAND data.win.system.eventID:(1 OR 3 OR 11 OR 22)\nAND data.win.eventdata.processGuid:\n "'+DNS+'"',
     '2026년 11월 3일 16:30 전후를 포함하여 DNS 프로세스의 생성과 후속 활동을 찾는다. 앞 절 HTTP의 GUID를 남겨 두지 않는다.',
     '9458 생성, 9459 파일 생성, 9461·9462 DNS 질의의 4건이다. PID 1540이며 HTTP 프로세스 PID 8080과 다르다.'),
   q('Q06-13',SYS+'\nAND data.win.system.eventID:"3"\nAND data.win.eventdata.processGuid:\n "'+DNS+'"\nAND data.win.eventdata.destinationIp:\n ("104.20.23.154" OR "172.66.147.243")',
     '성공한 질의의 queryResults에서 두 IPv4 주소를 읽어 목적지 조건으로 사용한다. 질의 시각부터 관찰 종료 시각까지를 선택한다. 자기 DNS 응답에 다른 주소가 있으면 그 값으로 바꾼다.',
     '이 예시의 16:30~16:35 KST 조회는 0건이다. 주소 반환은 확인했지만 같은 프로세스의 해당 주소 접속 기록은 찾지 못한 것으로 적는다.'),
   p('DNS 조회를 다른 프로세스가 담당하거나 프록시를 경유할 수 있다. 따라서 이 0건은 모든 프로세스의 통신 부재를 뜻하지 않는다. 필요하면 GUID 조건을 제거하고 같은 호스트·목적지·시각의 후보를 찾은 뒤 연결 근거를 다시 확인한다.')),
   pg('DNS 결과의 판정과 세 사례의 종결',
   p('example.com은 상태 0과 주소 응답을 보였다. book2-ch06.invalid는 상태 9003으로 이름을 찾지 못했다. 뒤 문서의 type: 6 응답 내용은 성공한 목적지 주소로 사용하지 않는다. 두 질의만으로 터널링·명령 수신·정보 반출을 판정할 근거는 없다.'),
   tb([['LSASS','osquery 서비스 문맥의 접근을 확인했다. 이 기록에 연결된 덤프 파일이나 인증 자료 추출은 확인하지 않았다.'],['HTTP','PID 8080의 생성과 내부 HTTP 연결 세 건을 연결했다. 생성 경보와 통신 원본을 구분했다.'],['DNS','PID 1540의 질의 두 건과 응답 상태를 확인했다. 반환 주소로의 후속 연결은 선택 범위에서 찾지 못했다.']]),
   p('세 사례는 서로 다른 프로세스의 관찰이다. 같은 날 수집되었다는 이유로 자격증명 탈취 후 외부 통신이라는 하나의 사건으로 합치지 않는다. 실제 사건의 시간선에는 GUID·계정·세션·호스트 이동 증거가 있는 연결만 넣는다.'),
   p('조사 기록에는 선택 기간·데이터 보기·원본 식별자·확인 동작·추가 자료를 남긴다. 현재 예시는 기존 보호 상태를 유지한 관찰과 승인된 통신이다. 실습 중 새로 바꾼 보호·연결·파일이 있으면 다음 절의 원상복구 대상을 개별 확인한다.')))
  replace_text(pages,'앞뒤의 Sysmon 1을 찾아','Q06-11·Q06-12와 같이 앞뒤의 Sysmon 1을 찾아')
 elif ch==7:
  before(pages,'7.5',pg('탐지와 조치를 연결한 조사 메모',
   p('현재 사례의 원본 1116과 1117은 같은 Detection ID를 가진다. Windows 원본에는 두 단계가 있고, 보존된 중앙 자료에는 1117만 있다. 따라서 “중앙에 탐지가 없었다”와 “Windows에서 탐지하지 않았다”를 구분한다.'),
   tb([['대상','C:\\Tools\\defender-off.ps1, Trojan:Win32/BatTamper.A'],['탐지','원본 Detection Time 2026-11-02 09:56:49.206Z'],['조치','1117의 action Name 격리, error Code 0x00000000, 추가 작업 없음'],['남은 조사','파일의 유입·실행 여부와 현재 보호 상태, 중앙 1116의 관측 공백']]),
   q('Q07-09',WIN+'\nAND data.win.system.channel:\n "Microsoft-Windows-Windows Defender/Operational"\nAND data.win.system.eventID:(1116 OR 1118 OR 1119)\nAND "data.win.eventdata.threat Name":\n "Trojan:Win32/BatTamper.A"'+window('2026-11-02T18:58:00+09:00','2026-11-04T00:00:00+09:00'),
     '조치 뒤 같은 위협명의 재탐지·조치 오류 후보를 archives에서 찾는다. 새 탐지는 Detection ID가 달라질 수 있으므로 앞선 탐지 ID 필터를 제거한다.',
     '보존 자료는 0건이다. 현재 파일·보호 상태와 원본 채널의 보존 범위를 함께 대조한다. 같은 이름의 다른 경로가 나오면 별도 탐지로 조사한다.'),
   p('종결 메모는 “해당 탐지의 격리 성공 기록 확인, 중앙 재탐지·오류 후보 없음, 현재 보호 상태 확인”처럼 범위를 적는다. 1116 중앙 부재의 원인은 수집 설정·시작·보존 자료가 더 필요하다. 탐지 파일이 실제 실행되었는지 확인하지 못했다면 그 항목을 남긴다.')))
 elif ch==8:
  before(pages,'보완 후 재확인',pg('취약점과 SCA의 종결 근거를 작성',
   q('Q08-10','vulnerability.id:"CVE-2025-54289"',
     'Inventory에서 확인한 CVE로 Discover의 취약점 상태 데이터 보기를 검색한다. agent.name 필터를 제거하여 다른 에이전트에도 같은 후보가 있는지 읽는다. 환경에 등록된 실제 상태 데이터 보기 이름을 사용한다.',
     '각 행의 agent.name·package.name·package.version과 설치 방식을 비교한다. 같은 CVE라도 호스트별 버전·노출·업무가 다르면 보완 순서를 따로 정한다.',index='wazuh-states-vulnerabilities-*'),
   tb([['LXD 후보','kt66-host의 snap LXD 5.0.11과 해당 CVE 문서를 대조했다. 현재 패키지를 갱신한 결과는 아니므로 수정 완료로 종결하지 않는다.'],['SSH 검사','28638의 failed와 sshd -T의 without-password를 대조했다. 정책이 요구하는 no와 달라 실패한 근거가 있다.'],['확인할 영향','LXD 접근 권한·업무 사용과 SSH의 root 공개키 사용·대체 관리 계정을 담당자에게 확인한다.']]),
   p('보완 담당자는 변경 전 버전·정책·실효 설정·검사 시각을 기록한다. 변경 후에는 같은 패키지와 검사 ID로 재수집 결과를 확인하고 새 스캔의 종료 시각을 남긴다. 과거 failed 경보가 검색되더라도 새 정책 결과가 Passed이고 실효 설정·정상 접속이 확인되면 과거 이력과 현재 상태를 나누어 보고한다.'),
   p('취약점 문서가 사라졌는데 패키지 목록과 최근 수집 시각도 비었다면 해결보다 수집 장애를 먼저 조사한다. 설정을 바꿀 수 없는 경우에는 예외 사유·보완 통제·담당자·만료일을 적고 재점검 날짜를 정한다.')))
 elif ch==9:
  before(pages,'판정과 대응 범위',pg('파일 이름과 원인 경보를 교차 확인',
   p('원전의 VirusTotal 화면에 표시된 파일은 /var/www/html/uploads/invoice.pdf.exe다. 선택 실습의 invoice-ch09.pdf.exe와 이름이 다르다. 원전 기록을 찾을 때에는 원전 경로를, 자기 실습에서는 실제 생성 경로를 사용한다.'),
   q('Q09-12','agent.name:"web" AND\n(syscheck.path:\n "/var/www/html/uploads/invoice.pdf.exe" OR\n data.virustotal.source.file:\n "/var/www/html/uploads/invoice.pdf.exe")',
     'alerts에서 원전 날짜를 포함하여 FIM과 VirusTotal 문서를 함께 찾는다. rule.id:87105 필터는 제거하여 원인 FIM 문서도 결과에 남긴다.',
     '현재 보존 인덱스에는 원전의 해당 양성 사례가 없다. 원전 화면의 positives 66과 현재 조회 0건을 같은 실행 결과로 기록하지 않는다.',index=ALERT),
   p('같은 경로가 검색되면 VirusTotal의 source.alert_id를 FIM의 id와, source.md5를 syscheck.md5_after와 비교한다. 경로만 같은 덮어쓰기 파일은 내용이 달라질 수 있다. 원인 FIM 문서를 못 찾으면 “조회 결과는 있으나 원인 FIM 미확인”으로 연결을 보류한다.'),
   tb([['동일 파일 후보','같은 에이전트·전체 경로·내용 해시·발생 순서'],['평판 결과','found·malicious·positives/total·scan_date로 보고서의 존재·판정·시점을 구분'],['로컬 검사','ClamAV의 경로·FOUND·시그니처와 검사 시각을 확인'],['실제 영향','프로세스 생성·웹 요청·권한 사용과 연결해야 실행·침해 범위를 판단']]),
   p('원전 양성 결과는 해시 보고서의 탐지와 로컬 EICAR 검사다. 실행 성공·자동 격리·호스트 전체 무결성까지 확인한 자료는 아니다. 현재 Rootcheck 권한 경보는 별도로 실제 권한과 승인 내역을 대조하고 파일 평판 사례에 자동으로 합치지 않는다.')))
 elif ch==10:
  before(pages,'자동 대응이 보이지',pg('대응 입력 한 쌍의 조사 결과',
   q('Q10-07','rule.id:(651 OR 652) AND\ndata.parameters.alert.id:"1793619097.12602015"',
     '2026년 11월 2일 20:25~20:40 KST로 조회한다. 원인 경보가 담긴 중첩 id를 검색한다. 최상위 id 조건과 구분한다.',
     'add와 delete 2건이다. 두 문서의 원인 경보·대상 bastion·IP·프로그램 firewall-drop이 같은지 대조한다.',index=ALERT),
   p('대상 로그의 add 20:31:37과 delete 20:34:38은 181초 차이다. 중앙 문서 timestamp는 20:31:37.189와 20:34:39.258로 약 182.069초 차이다. 예약값 180초, 프로그램 로그 시각, 중앙 저장 시각을 서로 치환하지 않는다.'),
   tb([['확인','같은 원인 정보를 가진 추가·해제 입력을 중앙에서 조회했다.'],['불일치','중첩 원인 ID를 직접 찾은 문서는 5760이고, 별도로 찾은 5763의 id는 다르다.'],['추가 증거','당시 방화벽 규칙·차단 중 접속 결과·해제 뒤 정상 경로가 실제 효과를 뒷받침한다.'],['종결 범위','현재 규칙 부재와 입력 이력을 기록한다. 과거 차단 효과와 ID 불일치는 별도 근거가 필요하다.']]),
   p('같은 IP에 대응이 여러 번 실행되면 가장 가까운 add·delete를 임의로 한 쌍으로 만들지 않는다. 원인 정보·대상·프로그램과 시각을 함께 대조한다. 해제가 없으면 예정 시각·실행 오류·남은 규칙을 확인하고 해당 대응의 정확한 변경만 원상복구한다.')))
 elif ch==11:
  before(pages,'저장한 검색',pg('고위험 경보에서 낮은 레벨의 원인으로',
   p('일일 고위험 목록에서 3장의 관리자 그룹 변경을 다시 조사해 본다. KT66-WIN-01의 4732·RecordId 10755는 규칙 60154, 레벨 12다. 경보 제목만 보고 새 계정이 관리자 권한으로 로그인했다고 결론내리지 않는다.'),
   q('Q11-10',SEC+'\nAND data.win.system.eventRecordID:"10755"',
     '2026년 11월 3일의 alerts에서 대상을 고른다. subjectLogonId 0x1e38ea7과 memberSid를 기록한다.',
     '수행자는 kt66student이고 구성원은 끝자리 1002인 SID다. 행위를 한 주체와 권한이 바뀐 계정을 구분한다.',index=ALERT),
   q('Q11-11',SEC+'\nAND (data.win.eventdata.subjectLogonId:"0x1e38ea7"\n OR data.win.eventdata.targetLogonId:"0x1e38ea7")\nAND data.win.system.eventID:\n (4624 OR 4672 OR 4720 OR 4732 OR 4733 OR 4726 OR 4634)'+window('2026-11-03T12:45:00+09:00','2026-11-03T12:50:00+09:00'),
     'archives로 바꾸고 레벨·MITRE 필터를 제거한다. 같은 수행자 세션의 시작·권한·변경·종료를 찾는다.',
     '10744 로그온, 10745 권한 부여, 10751 계정 생성, 10755 편입, 10757 제거, 10759 삭제, 10768 로그오프가 연결된다.'),
   p('높은 레벨의 두 그룹 변경만 남기면 수행자 로그온과 원상복구의 일부가 빠진다. 승인된 비활성 계정 시험이라는 작업 내역과 사후 계정 부재를 대조하면 이 사례의 분류 근거가 된다. 승인 내역이 없으면 수행자 세션과 새 계정 사용 여부를 우선 조사한다.')),
   pg('관제 인계 기록의 완성 예',
   tb([['대상과 시간','windows-user / KT66-WIN-01, 11월 3일 12:47 KST'],['최초 단서','60154·레벨 12, Security 4732 / 10755'],['확인한 연결','동일 수행 세션의 생성·편입·제거·삭제. 새 계정의 로그온과 구분.'],['판단','승인된 시험 내역과 일치하는 계정·그룹 변경. 현재 계정 부재를 원상복구 증거로 기록.'],['남길 한계','다른 세션·기간의 활동은 이번 조회 범위 밖. 같은 이름의 후속 경보는 SID부터 재대조.']]),
   p('담당자는 이 정도의 근거를 남겨 다음 근무자가 최초 경보에서 시간선까지 재조회할 수 있게 한다. 미확인 사건에는 확인할 자료·담당자·다음 점검 시각을 적는다. 높은 레벨이라는 이유만으로 차단하거나 낮은 레벨이라는 이유로 후속 근거를 버리지 않는다.')))
 elif ch==12:
  before(pages,'원상복구와 다음',pg('보존된 한 IP로 집계 결과까지 확인',
   p('90일 합성 자료가 준비되지 않은 환경에서는 보존된 실제 실습 기록으로 피벗과 집계의 연결을 확인한다. 아래 사례는 2026년 11월 2~3일의 192.168.0.108이다. 합성 자료의 다섯 IP 비교나 90일 평판·휴일 분석 결과를 대신하지 않는다.'),
   q('Q12-13','(data.srcip:"192.168.0.108" OR\n data.src_ip:"192.168.0.108")'+window('2026-11-02T00:00:00+09:00','2026-11-04T00:00:00+09:00'),
     'alerts에서 synthetic.flag:true 필터를 제거한다. 시간 선택기도 같은 두 날짜를 포함한다. data.srcip와 data.src_ip 중 하나가 해당 주소이면 문서를 선택한다.',
     '보존 자료에서 69건이다. 이 수는 두 출발지 필드에 해당 IP가 있는 경보 문서 수이며 요청 횟수나 실제 공격 횟수가 아니다.',index=ALERT),
   p('Dev Tools에서 examples/chapter12/observed-ip-profile.http를 연다. 앞 절 요청에서 synthetic.flag 조건을 제거하고 IP와 기간을 위 식에 맞춘 요청이다. size 0·track_total_hits와 응답 오류 점검은 그대로 적용한다.'),
   p('추가한 rules의 terms 집계는 rule.id별 문서 수를 최대 100개 버킷으로 보여 준다. 나머지 건수와 집계 오차가 0인지 확인한 뒤 버킷 수를 규칙 종류 수로 센다. level_5_or_higher의 filter는 rule.level이 5 이상인 문서만 별도로 세며 그 doc_count를 읽는다.'),
   tb([['전체와 높은 레벨','69건, 레벨 5 이상 47건, 최대 레벨 10'],['수집 에이전트','bastion 56, web 9, kt66-host 4'],['관찰 날짜','KST 2일. 자료가 존재한 날짜 수이며 지속 접속 시간은 아니다.'],['규칙 종류','15종. 전체 규칙 목록의 버킷 수와 나머지 건수 0을 대조한다.']]),
   p('agent.name은 수집 에이전트 이름이다. 이를 공격 대상 시스템 수와 자동으로 같게 두지 않는다. 자동 대응 로그가 다른 수집 위치에 있어도 중첩 원인 정보의 실제 대상은 bastion일 수 있다.')),
   pg('집계에서 원문과 시간 간격으로 돌아가기',
   q('Q12-14','agent.name:"bastion" AND rule.id:5760\nAND data.srcip:"192.168.0.108"'+window('2026-11-02T20:29:00+09:00','2026-11-02T20:31:00+09:00'),
     '같은 호스트와 개별 인증 실패 규칙으로 제한한 뒤 Time을 오름차순으로 정렬한다. 서로 다른 센서·원인 경보·대응 로그의 도착 간격을 한 연결 주기로 섞지 않는다.',
     '3건의 timestamp는 20:29:36.982, 20:29:59.002, 20:30:23.026 KST다. 차이는 22.020초와 24.024초다.',index=ALERT),
   p('여기서 계산한 것은 Wazuh 문서 timestamp 간격이다. 원본 인증 로그에는 초 단위 시각이 있으므로 실제 입력 간격을 조사할 때에는 원본 시각·PID·출발지 포트와 비교한다. 두 간격만으로 자동화 여부나 주기성을 확정하지 않는다.'),
   p('69건 안에는 인증 성공·실패·원인 경보·자동 대응 입력과 별도 웹 실습이 함께 있다. 높은 빈도 한 개로 하나의 침해사고를 구성하지 않는다. IP·호스트·계정·시각으로 원문을 나누고 직접 연결된 기록만 다음 장의 시간선에 넣는다.'),
   p('합성 자료의 비교표가 필요한 경우에는 이 사례와 별도 표로 유지한다. 자료가 없으면 해당 비교 항목을 미측정으로 두고, 실제 두 날짜의 수치에서 90일 장기 추세나 탐지 성능을 추정하지 않는다.')))
 elif ch==13:
  before(pages,'신규 IP와 반복',pg('시간 점수의 구성 문서로 되돌아가기',
   p('12장의 보존 IP 사례에서 KST 11월 2일 20시 구간은 49건이다. 이 구간의 레벨 제곱 합은 1228이다. 전체 환경의 가장 위험한 시간이라는 뜻은 아니며 선택한 IP 경보의 한 시간 집계다.'),
   q('Q13-05','(data.srcip:"192.168.0.108" OR\n data.src_ip:"192.168.0.108")'+window('2026-11-02T20:00:00+09:00','2026-11-02T21:00:00+09:00'),
     'alerts에서 합성 표시 필터를 제거하고 선택 기간을 맞춘다. 레벨 조건을 먼저 걸면 낮은 레벨의 성공·대응 입력이 빠지므로 전체 49건부터 읽는다.',
     '레벨 5는 32건, 8은 2건, 10은 3건, 3은 12건이다. 레벨 5 이상만 점수에 더하면 32×25 + 2×64 + 3×100 = 1228이다.',index=ALERT),
   p('집계 응답을 직접 확인할 때에는 examples/chapter13/observed-hour.http를 Dev Tools에서 연다. size 0과 시간·IP 필터, rule.level별 terms 집계가 들어 있다. 각 버킷의 key가 레벨이고 doc_count가 문서 수다. 응답의 전체 수·나머지 버킷·오류를 먼저 점검한 뒤 위 산식으로 계산한다.'),
   q('Q13-06','agent.name:"bastion"\nAND data.srcip:"192.168.0.108"\nAND rule.id:(5715 OR 5763)'+window('2026-11-02T20:00:00+09:00','2026-11-02T21:00:00+09:00'),
     '같은 시간대의 성공 로그온과 반복 실패 경보를 원문으로 읽는다. 사용자·PID·포트·시각·인증 방식을 대조한다.',
     '성공 10건과 반복 실패 경보 1건이다. 첫 성공 20:28은 20:31의 반복 실패보다 앞선다. 20:37 이후 성공은 승인된 실습 기록과 연결 근거를 추가 확인한다.',index=ALERT),
   p('성공이 같은 시간 구간에 있다는 이유로 암호 대입의 결과라고 판정하지 않는다. 10장의 대응 입력도 시간선에 나란히 두고 자동 대응이 통신에 영향을 줄 수 있었던 구간을 표시한다. 계정 승인·세션·실제 후속 활동이 확인되기 전에는 점수의 access 단계를 확정하지 않는다.')),
   pg('과거 조회 0건과 신규 주소 판정',
   q('Q13-07','(data.srcip:"192.168.0.108" OR\n data.src_ip:"192.168.0.108")'+window('2026-10-05T00:00:00+09:00','2026-11-02T00:00:00+09:00'),
     '이번 관찰 직전 4주에서 같은 주소를 찾는다. 시간 선택기도 4주 전체를 포함한다. synthetic.flag 조건이 붙어 있지 않은지 확인한다.',
     '현재 보존 자료는 이 범위에 0건이다. 그러나 현재 확인한 alerts 일자 인덱스는 11월 2·3일이므로 앞선 4주의 관측 완전성이 확보되지 않았다.',index=ALERT),
   p('따라서 이 사례의 신규 여부는 “기준 기간 자료 부족으로 판정 보류”다. 기준 기간에 자료가 없다는 상태와 자료가 충분한데 해당 주소가 없다는 상태는 다르다. 센서·보존 기간·수집 공백이 확인된 뒤에야 선택한 기준 기간의 신규 주소로 분류한다.'),
   p('점수 보고서에는 확인한 특성만 넣는다. 예를 들어 12장의 관찰 일수는 2일이고 국가·평판·90일 추세는 이 자료에서 확인하지 않았다. 미확인 항목을 0점으로 확정하기보다 확인된 점수와 미확인 범위를 함께 제시한다. 우선 확인할 항목은 성공 세션의 승인 여부와 후속 활동이다.')))
 elif ch=='appendix':
  before(pages,'H  원상복구',pg('G 보충  식별자 충돌과 조사 결론',
   p('Wazuh의 id는 원인 경보 연결에 사용하는 값이지만, 현재 자료에서도 서로 다른 Windows 원본이 같은 id를 가진 경우가 있다. 4장의 Sysmon 8886과 8887이 그 예다. id 검색 결과는 컴퓨터·채널·eventID·eventRecordID·systemTime 및 본문 필드로 다시 대조한다.'),
   p('인덱서에서 문서 한 건을 다시 찾을 때에는 _index와 _id를 함께 보존한다. 같은 Windows 원본이 alerts와 archives에 각각 있을 수 있으므로 인덱서 문서의 수와 원본 이벤트의 수를 구분한다. 원본 기록 번호도 채널 지우기·재생성 등으로 재사용될 수 있어 시간 범위가 필요하다.'),
   tb([['입력과 범위','6장, windows-user Sysmon, 11월 3일 16~17시 KST'],['원본 대조','10의 9407, 3의 9451·9454·9455, 22의 9461·9462'],['수집 판정','archives 6건. 해당 원본의 수집·보존 확인.'],['경보 판정','같은 조건 alerts 0건. 생성 경보는 다른 원본이므로 구분.'],['행위 판정','osquery 접근·내부 HTTP·DNS 질의는 각각 별도 GUID. 하나의 침해 체인으로 합치지 않음.'],['남은 확인','경보 제외의 상세 규칙 근거, 필요 시 원문·설정·저장 이력 추가 조사.']]),
   p('자료가 없는 항목은 미확인, 수집 범위가 부족한 항목은 판정 보류로 적는다. 조사 완료는 모든 값을 성공으로 표시하는 것이 아니라, 확인한 사실과 추가 조사 책임·기한을 구분해 다른 담당자가 이어갈 수 있게 남기는 것이다.')))
 refs={2:[('Microsoft Learn — 이벤트 4634와 로그온 세션의 종료','https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4634')],6:[('Wazuh — Event logging','https://documentation.wazuh.com/current/user-manual/manager/event-logging.html'),('Wazuh — Alerts 설정','https://documentation.wazuh.com/current/user-manual/reference/ossec-conf/alerts.html')]}
 if ch in refs:
  existing={b.get('url') for x in pages for b in x['blocks'] if b['type']=='link'}
  links=[{'type':'link','text':title,'url':url} for title,url in refs[ch] if url not in existing]
  if links:pages.append(pg('참고자료 보충',*links))
 return pages

def apply_existing():
 for ch in list(range(1,14))+['appendix']:
  stem='appendix' if ch=='appendix' else f'chapter{ch:02}'
  path=ROOT/f'manuscript/volume02-{stem}.json';data=json.loads(path.read_text(encoding='utf8'))
  revise(ch,data['pages'])
  note='2026-11-04 분석 보강. 범위·실측·미확인은 editorial/analysis-revision-review.md.'
  if note not in str(data.get('comments','')):data['comments']=str(data.get('comments',''))+' '+note
  path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
  dest=ROOT/'examples'/stem;manifest=[]
  for page in data['pages']:
   for b in page['blocks']:
    if b['type'] not in ('query','command'):continue
    name=b['id']+('.dql' if b['type']=='query' else '.txt')
    (dest/name).write_text(b['text']+'\n',encoding='utf8')
    manifest.append({'id':b['id'],'file':name,'where':b['where'],'section':page['title'],'input':b['text']})
  (dest/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
  readme=dest/'README.md'
  if readme.exists():
   text=readme.read_text(encoding='utf8')
   text=text.replace('Q03-03은 wazuh-archives-*, 나머지는 wazuh-alerts-*에서 사용한다.','Q03-03·Q03-09는 wazuh-archives-*, 나머지는 본문의 wazuh-alerts-*에서 사용한다.')
   missing=[m for m in manifest if '('+m['file']+')' not in text]
   if missing:
    text+='\n## 분석 보강 입력\n\n기간·데이터 보기·ID는 본문의 절차와 맞춘다.\n\n'
    text+='\n'.join(f"- [{m['file']}]({m['file']}) — {m['where']} · {m['section']}" for m in missing)+'\n'
   readme.write_text(text,encoding='utf8')
  print(stem,len(data['pages']),len(manifest))
 write_supplemental_inputs()

def write_supplemental_inputs():
 source=(ROOT/'examples/chapter12/ip-profile.http').read_text(encoding='utf8')
 observed=source.replace('    {"term": {"synthetic.flag": true}},\n','').replace('2026-08-01T00:00:00+09:00','2026-11-02T00:00:00+09:00').replace('2026-11-01T00:00:00+09:00','2026-11-04T00:00:00+09:00').replace('185.220.158.180','192.168.0.108')
 observed=observed.replace('"types_estimate": {"cardinality": {\n      "field": "rule.id"}},','"rules": {"terms": {\n      "field": "rule.id", "size": 100}},\n    "level_5_or_higher": {"filter": {\n      "range": {"rule.level": {"gte": 5}}}},')
 hour='''GET wazuh-alerts-*/_search
{
 "size": 0, "track_total_hits": true,
 "query": {"bool": {"filter": [
  {"range": {"timestamp": {
   "gte": "2026-11-02T20:00:00+09:00",
   "lt": "2026-11-02T21:00:00+09:00"
  }}},
  {"bool": {"minimum_should_match": 1,
   "should": [
    {"term": {"data.srcip": "192.168.0.108"}},
    {"term": {"data.src_ip": "192.168.0.108"}}
   ]}}
 ]}},
 "aggs": {"levels": {"terms": {
  "field": "rule.level", "size": 20
 }}}
}
'''
 for ch,name,body in [(12,'observed-ip-profile.http',observed),(13,'observed-hour.http',hour)]:
  dest=ROOT/f'examples/chapter{ch:02}'
  (dest/name).write_text(body,encoding='utf8')
  (dest/'analysis-inputs.json').write_text(json.dumps([{'file':name,'where':'Windows PC · Wazuh Dev Tools · GET 검색','scope':'보존된 실습 기록. 합성 데이터와 별도 모집단.','input':body}],ensure_ascii=False,indent=2)+'\n',encoding='utf8')
  readme=dest/'README.md'
  if readme.exists():
   text=readme.read_text(encoding='utf8')
   if '('+name+')' not in text:
    text+=f'\n- [{name}]({name}) — 보존된 실제 IP 사례의 완성 GET 요청. 합성 자료와 별도로 사용한다. [입력 기록](analysis-inputs.json).\n'
    readme.write_text(text,encoding='utf8')
if __name__=='__main__':apply_existing()
