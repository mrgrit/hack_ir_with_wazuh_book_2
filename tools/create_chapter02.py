"""2장 원고·복사용 예제를 만든다. 실습 명령은 실행하지 않는다."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
pages=[]
def p(t):return {'type':'p','text':t}
def h(t):return {'type':'h','text':t}
def code(t):return {'type':'code','text':t}
def table(head,rows,widths):return {'type':'table','head':head,'rows':rows,'widths':widths,'keep':True}
def image(path,caption,width=127):return {'type':'image','path':path,'caption':caption,'width_mm':width}
def screen(name,caption):return image('assets/screenshots/chapter02/'+name+'.jpg',caption)
def fig(name,caption):return image('assets/figures/chapter02/'+name+'.png',caption)
def art(name,caption):return image('assets/illustrations/diversity/v2-c02-'+name+'.png',caption,62)
def cmd(cid,where,text,why,result):return {'type':'command','id':cid,'where':where,'text':text,'why':why,'result':result}
def query(qid,text,why,result):return {'type':'query','id':qid,'where':'Windows PC · Wazuh Discover · DQL','text':text,'why':why,'result':result}
def page(title,*blocks,br=False):pages.append({'title':title,'kind':'body','level':'section','break':br,'blocks':list(blocks)})
def link(title,url):return {'type':'link','text':title,'url':url}
WIN='Windows 실습 게스트 · 관리자 PowerShell'
HOST='kt66 Ubuntu VM · 터미널'
ATT='kt66-attacker 컨테이너 · Bash'
BASE='agent.name:"windows-user"\nAND data.win.system.channel:"Security"'

page('2장 로그온 실패와 원격 접속',
 p('같은 계정에 잘못된 암호가 반복되면 계정이 잠길 수 있다. 이후 올바른 암호로 접속했더라도 앞선 실패가 정상 사용자의 입력 실수였는지, 다른 사람이 계정을 시도했는지는 별도로 조사해야 한다. 입력한 자격증명, Windows의 판단, Wazuh의 경보를 시각 순서로 연결한다.'),
 fig('sequence','그림 2-1  로그온 실패·잠금·원격 접속의 조사 순서'),
 table(['실습','입력과 확인 대상'],[['31','victim에 틀린 암호 두 개 · 4625'],['32','존재하지 않는 이름 세 개 · 4625의 실패 사유'],['33','victim에 틀린 암호 다섯 개 · 잠금 상태와 4740'],['34','잠금 해제 후 정상 자격증명 · 4624와 유형 10']],[18,109]),
 p('1장의 Windows 수집 확인을 끝낸 환경에서 수행한다. 실습용 victim 계정과 kt66 내부 주소만 사용한다. 성공 기준은 각 입력을 해당 원본 이벤트와 Wazuh 경보에 연결하고, 마지막에 잠금과 접속 세션을 정리하는 것이다.'))

page('2.1  공격 입력과 조사 위치 구분하기',
 p('RDP(Remote Desktop Protocol)는 원격 Windows의 화면과 입력을 전달하는 프로토콜이다. 네트워크 수준 인증인 NLA는 원격 화면 세션을 본격적으로 사용하기 전에 자격증명을 검사한다. NLA 단계의 실패는 네트워크 로그온 유형 3으로 기록될 수 있다. 유형 10은 원격 대화형 로그온이다.'),
 fig('path','그림 2-2  RDP 요청과 Windows 이벤트의 수집 경로'),
 p('공격 입력은 kt66-attacker 컨테이너에서 10.20.70.10:3389로 보낸다. 이 주소는 kt66의 내부 Windows 접속 경로다. 별도의 공격자 VM 192.168.0.108과 구분한다. Windows 이벤트의 원본 주소는 이 환경에서 10.20.30.202로 나타났다.'),
 p('대상은 KT66-WIN-01이며 Wazuh 에이전트 이름은 windows-user이다. agent.ip의 172.30.70.2는 이벤트를 수집한 Windows 에이전트 주소다. 접속 출발지는 data.win.eventdata.ipAddress에서 읽는다. 두 주소를 바꾸어 해석하면 조사할 장비가 달라진다.'))

page('실습용 계정과 잠금 정책 확인',
 p('Windows 게스트의 브라우저 콘솔에 로그인하고 관리자 PowerShell을 연다. Get-LocalUser는 로컬 계정을 조회한다. Enabled는 사용 가능 상태이며, 암호 오류로 잠겼는지는 별도의 Lockout 속성으로 확인한다. CIM은 운영체제의 관리 정보를 조회하는 인터페이스다.'),
 cmd('C02-01',WIN,"Get-LocalUser -Name victim |\n  Format-List Name,Enabled\nGet-CimInstance Win32_UserAccount `\n  -Filter \"Name='victim' AND LocalAccount=True\" |\n  Format-List Name,Lockout",
     '-Name은 계정 이름을 지정한다. Get-CimInstance의 -Filter는 로컬 victim만 고르는 조건이다. 큰따옴표 안의 작은따옴표는 이름 문자열을 묶는다. 파이프(|) 뒤의 Format-List는 속성을 펼쳐 표시한다. 백틱(`)은 다음 줄로 명령을 잇는다.',
     'Name victim, Enabled True, Lockout False를 확인한다. 계정이 없으면 kt66의 Windows 준비 상태부터 확인한다. Lockout True이면 공격 입력을 멈추고 잠금 정책에 따라 해제된 뒤 다시 조회한다.'),
 cmd('C02-02',WIN,'net.exe accounts',
     'net.exe는 Windows의 계정·네트워크 관리 도구다. accounts만 입력하면 현재 계정 정책을 조회하며 값을 바꾸지 않는다.',
     '이 환경의 잠금 임계값은 5회, 잠금 기간과 잠금 카운터 관찰 기간은 각각 1분이다. 자신의 값을 기록한다. 정책이 다르면 다섯 번 입력으로 같은 결과가 나온다고 가정하지 않는다.'),
 p('kt66의 센서 준비 스크립트는 실습 계정과 잠금 정책을 마련한다. 상태 확인을 위해 설치 스크립트를 다시 실행하지 않는다. 운영 계정 대신 준비된 실습 계정을 사용하며, 여러 독자가 같은 victim을 동시에 시험하면 실패 횟수가 합쳐질 수 있다.'))

page('감사와 RDP 권한 확인',
 p('Security 기록을 만들려면 로그온의 성공·실패 감사가 필요하다. 계정 잠금에는 사용자 계정 관리의 성공 감사도 확인한다. auditpol.exe의 /get은 정책 조회이며, /subcategory는 하위 범주를 지정한다. 아래 GUID는 사용자 계정 관리 범주다.'),
 cmd('C02-03',WIN,"$accountAudit = '{0CCE9235-69AE-11D9-BED3-505054503030}'\nauditpol.exe /get /subcategory:$accountAudit\nGet-LocalGroupMember -SID 'S-1-5-32-555' |\n  Format-List Name",
     '$accountAudit에 범주의 식별 문자열을 저장한다. Get-LocalGroupMember는 로컬 그룹의 구성원을 조회한다. -SID의 값은 표시 언어와 무관하게 Remote Desktop Users 그룹을 지정한다.',
     '사용자 계정 관리에 성공 감사가 표시되는지, 원격 데스크톱 사용자 그룹에 KT66-WIN-01\\victim이 있는지 읽는다. 로그온 감사는 1장의 C01-06으로 확인한다.'),
 p('WazuhSvc와 Sysmon64가 실행 중이고 1장의 이벤트 대조가 성공했는지도 확인한다. 감사나 권한이 부족하면 해당 설정을 준비한 뒤 진행한다. 이번 절차에서는 잠금 임계값이나 Defender 보호 상태를 변경하지 않는다.'))

page('공격자 컨테이너와 도구 준비',
 p('kt66 Ubuntu VM의 터미널에서 Docker로 공격자 컨테이너에 들어간다. docker exec는 실행 중인 컨테이너에서 프로그램을 시작한다. -i는 입력을 유지하고 -t는 터미널을 할당한다. /bin/bash는 이후 명령을 해석할 셸이다.'),
 cmd('C02-04',HOST,'sudo docker exec -it kt66-attacker /bin/bash',
     'sudo는 Docker 명령을 관리자 권한으로 실행한다. 컨테이너 이름을 확인한 뒤 Bash에 들어간다.',
     '프롬프트가 컨테이너 안의 셸로 바뀐다. 아래의 hostname 결과도 attacker인지 확인한다.'),
 cmd('C02-05',ATT,'hostname\ncommand -v hydra xfreerdp xvfb-run timeout',
     'hostname은 현재 호스트 이름을 출력한다. command -v는 셸이 실행할 도구의 경로를 찾는다. 네 이름은 공백으로 구분한 개별 인수다.',
     '네 도구의 경로가 모두 출력되어야 한다. 이 환경에는 Hydra 9.2와 FreeRDP 2.6.1이 준비되어 있었다. 누락되면 외부 공격자 VM이 아닌 kt66-attacker에 들어왔는지 먼저 확인한다.'),
 p('Hydra는 계정과 암호 후보를 인증 서비스에 입력해 응답을 확인하는 도구다. xfreerdp는 Linux용 RDP 클라이언트다. xvfb-run은 실제 모니터 없이 그래픽 프로그램을 실행할 가상 화면을 마련한다. timeout은 지정 시간이 지나면 실행 중인 명령에 종료 신호를 보낸다. 역할이 서로 다르다.'))

page('실습 파일과 시각 마련하기',
 p('틀린 암호 목록과 가짜 이름 목록은 컨테이너의 전용 디렉터리에 둔다. ls는 파일 목록, -ld는 대상 디렉터리 자체의 상세 정보다. mkdir는 디렉터리를 만들고 cd는 현재 작업 위치를 바꾼다. pwd는 현재 위치를 출력한다.'),
 cmd('C02-06',ATT,'ls -ld /tmp/wazuh-book2-ch02',
     '파일을 만들기 전에 같은 이름의 디렉터리가 이미 있는지 읽는다.',
     '처음에는 No such file or directory가 정상이다. 이미 있으면 내용을 확인해 이전 실습 파일인지 판단하고, 다른 작업의 파일을 덮어쓰지 않는다.'),
 cmd('C02-07',ATT,'mkdir /tmp/wazuh-book2-ch02\ncd /tmp/wazuh-book2-ch02\npwd',
     '디렉터리가 없음을 확인한 경우에만 mkdir를 실행한다. 이미 이번 실습용으로 만든 디렉터리라면 cd부터 수행한다.',
     '/tmp/wazuh-book2-ch02가 출력된다. 이후 목록 파일은 이 위치에 저장한다.'),
 cmd('C02-08',WIN,'$start = Get-Date\n$start.ToString("o")',
     'Get-Date로 시작 시각을 $start에 보관한다. ToString("o")는 시각과 시간대가 포함된 문자열로 표시한다. 실습 31·32·33·34를 시작할 때마다 같은 PowerShell 창에서 다시 실행한다.',
     '이 시각 이후의 이벤트만 조회하는 기준을 얻는다. 각 실습의 종료 시각도 따로 적는다. PowerShell 창을 닫으면 변수는 사라지므로 다시 설정한다.'))

page('2.2  실습 31 · 잘못된 암호 입력',
 p('먼저 victim에 틀린 암호 두 개만 입력한다. 실패 사유가 암호 오류인지, 출발지가 공격자 컨테이너인지 확인한다. 입력 직전 Lockout False와 관찰 기간 동안 다른 실패가 없음을 확인한다.'),
 art('failure','그림 2-3  제한된 입력 목록과 인증 응답의 확인'),
 p('printf는 지정한 형식으로 문자열을 출력한다. 형식 %s는 문자열 하나, 역슬래시 엔(\\n)은 줄바꿈이다. 작은따옴표는 셸이 특수문자를 먼저 해석하지 않게 묶는다. >는 출력을 파일에 기록하며 기존 파일이 있으면 덮어쓴다.'),
 cmd('C02-09',ATT,"ls -l pw-two.txt\nprintf '%s\\n' Book2WrongA Book2WrongB > pw-two.txt\ncat pw-two.txt",
     'ls에서 파일이 없음을 확인한 뒤 printf를 실행한다. cat은 저장한 파일 내용을 읽는다. 두 단어는 이 실습에서 사용하는 잘못된 암호 후보다.',
     'Book2WrongA와 Book2WrongB가 한 줄씩 출력된다. 기존 파일이 있으면 먼저 내용을 읽고 이번 실습 파일인지 확인한다.'),
 cmd('C02-10',ATT,'hydra -l victim -P pw-two.txt -t 1 rdp://10.20.70.10',
     '기본 구문은 hydra 계정옵션 암호옵션 대상이다. 소문자 -l은 단일 계정, 대문자 -P는 암호 목록 파일이다. -t 1은 대상당 동시 작업을 하나로 제한한다. rdp:// 뒤는 실습 대상 주소이며 기본 포트는 3389다.',
     '두 후보를 처리한 뒤 0 valid password found가 출력됐다. 이 문장은 유효한 암호를 찾지 못했다는 도구의 보고다. Windows가 실제로 어떤 실패를 기록했는지는 다음 절에서 확인한다.'),
 p('Hydra의 RDP 모듈은 실행 시 experimental 경고를 표시했다. 도구의 출력 건수를 Windows 이벤트 수와 자동으로 같다고 두지 않는다. 연결 오류가 발생하면 목록을 늘리기 전에 대상 주소·RDP 서비스·계정 상태부터 확인한다.'))

page('Windows 원본에서 실패 사유 읽기',
 cmd('C02-11',WIN,"$filter = @{ LogName='Security'; Id=4625;\n  StartTime=$start }\n$event = Get-WinEvent -FilterHashtable $filter `\n  -MaxEvents 1\n$event | Format-List TimeCreated,Id,RecordId,Message\n$event.ToXml()",
     'Get-WinEvent는 이벤트를 조회한다. @{ }는 조건을 담는 해시 테이블이고 세미콜론은 항목을 구분한다. StartTime은 C02-08의 시작 시각, -MaxEvents 1은 최신 한 건이다. ToXml()은 같은 기록의 원본 필드를 표시한다.',
     'TargetUserName victim, Status 0xc000006d, SubStatus 0xc000006a, LogonType 3, IpAddress 10.20.30.202를 찾는다. 이 기록의 EventRecordID는 9978이었다. 자신의 번호와 시각을 기록한다.'),
 table(['항목','이번 기록의 해석'],[['Status 0xc000006d','로그온 실패의 일반 상태'],['SubStatus 0xc000006a','대상 계정의 암호가 맞지 않음'],['LogonType 3','네트워크 로그온 · SMB 전용 분류가 아님'],['AuthenticationPackageName NTLM','인증에 사용된 패키지'],['WorkstationName attacker','요청 과정에서 전달된 컴퓨터 이름']],[62,65]),
 p('0x는 16진수 표기다. Status와 SubStatus는 서로 다른 필드이며, 상세 이유가 항상 SubStatus에만 들어가는 것은 아니다. 기록 전체를 먼저 읽고 실제 코드가 있는 필드를 선택한다. 컴퓨터 이름은 주소·시각·계정과 대조할 단서이며 그 값 하나로 접속자를 확정하지 않는다.'))

page('Wazuh에서 같은 실패 찾기',
 p('Windows PC의 브라우저에서 https://192.168.0.107:5601에 로그인한다. 왼쪽 메뉴의 **Explore → Discover**로 들어가 데이터 보기를 **wazuh-alerts-***로 선택한다. 검색창 오른쪽이 **DQL**인지 확인한다. 시간 범위는 실습 시작과 종료를 포함하도록 정하고 검색을 실행한다.'),
 query('Q02-01',BASE+'\nAND data.win.system.eventID:"4625"\nAND data.win.eventdata.targetUserName:"victim"',
     '콜론(:)은 필드와 조건 값을 연결한다. 큰따옴표는 값을 묶고 AND는 모든 조건을 만족하는 기록을 고른다. 먼저 실패 전체를 읽은 뒤 이유 코드를 추가한다.',
     '실습 시간의 victim 실패를 찾는다. 결과 행 왼쪽 펼침 버튼으로 Table을 열어 계정·주소·실패 코드·기록 번호를 읽는다.'),
 query('Q02-02',BASE+'\nAND data.win.system.eventID:"4625"\nAND data.win.eventdata.targetUserName:"victim"\nAND (data.win.eventdata.status:"0xc000006a"\n  OR data.win.eventdata.subStatus:"0xc000006a")',
     'OR는 둘 중 하나를 만족하면 선택한다. 소괄호로 OR 묶음을 만들고 앞의 계정·이벤트 조건과 AND로 연결한다. 두 상태 필드 중 암호 오류 코드가 들어 있는 쪽을 찾는다.',
     '실습 31에서 두 기록이 대응했다. 실습 33까지 포함한 기간을 조회하면 이후의 암호 오류도 나타난다. 검색 결과 수는 선택한 시간과 조건의 기록 수다.'))

page('실패 경보의 필드 대조',
 p('결과의 **View single document**를 열면 한 경보의 필드를 이어 읽을 수 있다. Windows XML의 EventData 값은 Wazuh의 data.win.eventdata 아래에 표시된다. 원본과 같은 계정·코드·주소를 찾는다.'),
 screen('4625-detail','화면 2-1  victim 로그온 실패의 인증 패키지·주소·상태 코드'),
 p('이 경보의 rule.id는 60122이고 설명은 Logon Failure - Unknown user or bad password였다. 이 제목만으로 계정 부재와 암호 오류를 구분할 수 없으므로 Status·SubStatus를 읽는다. 필드 옆 기호와 관계없이 실패 이유는 해당 코드와 Windows 원본으로 판단한다.'))

page('개별 이벤트의 일치 확인',
 screen('4625-record','화면 2-2  실패 기록 9978의 계정·채널·컴퓨터·이벤트 번호'),
 p('EventID 4625는 사건 종류, EventRecordID 9978은 이 컴퓨터의 Security 채널에 저장된 개별 기록 번호다. 원본 시각은 2026-11-03T03:00:47.3683626Z이며, 화면의 Wazuh 시각은 한국 시각 12:00:47.982였다. 약 0.6초의 차이는 같은 이벤트를 다른 시점에 기록한 값이다.'),
 h('조사·대응'),
 p('같은 출발지에서 같은 계정의 암호 오류가 짧은 간격으로 반복되는지 본다. 사용자에게 암호 변경·입력 실수·저장된 자격증명 사용 여부를 확인한다. 출발지 장비의 소유자와 원격 접속 경로도 대조한다. 이후 성공 로그온이 있으면 해당 세션의 활동까지 조사 범위를 넓힌다.'),
 h('실패 시 확인과 원상복구'),
 p('원본이 없으면 시작 시각과 감사 정책, RDP 요청 도착 여부를 확인한다. 원본은 있고 경보가 없으면 에이전트 수집·매니저 규칙·Discover 데이터 보기와 기간을 차례로 확인한다. Hydra가 끝났는지 확인하고 victim의 Lockout을 다시 읽는다. 다음 실습 전에는 자신의 잠금 카운터 관찰 기간이 지나도록 기다린다. 목록 파일은 마지막 원상복구 절에서 정리한다.'))

page('2.3  실습 32 · 존재하지 않는 계정',
 p('계정 열거는 유효한 계정 이름을 알아내려는 행위다. 인증 응답과 실패 기록의 차이를 이용할 수 있다. 여기서는 실제로 없는 세 이름을 입력해 Windows가 계정 부재를 어떻게 기록하는지 확인한다.'),
 cmd('C02-12',WIN,"Get-LocalUser |\n  Where-Object Name -Like 'book2_missing_*' |\n  Select-Object Name",
     'Where-Object는 조건에 맞는 객체를 남긴다. -Like는 와일드카드 비교이고 별표(*)는 임의의 문자열이다. Select-Object는 출력할 Name 속성을 고른다.',
     '출력이 없어야 준비한 세 이름을 사용할 수 있다. 같은 이름이 있으면 해당 계정을 지우는 대신 충돌하지 않는 이름으로 목록과 검색식을 함께 바꾼다.'),
 p('Administrator와 Guest는 기본 제공 계정일 수 있다. 비활성 계정과 존재하지 않는 계정을 같은 사례로 섞지 않는다. C02-08로 이번 실습의 시작 시각을 다시 기록한다.'),
 cmd('C02-13',ATT,"ls -l users-three.txt\nprintf '%s\\n' book2_missing_a book2_missing_b \\\n  book2_missing_c > users-three.txt\ncat users-three.txt",
     '파일이 없음을 확인한 뒤 세 이름을 한 줄씩 저장한다. Bash에서 줄 끝의 역슬래시(\\)는 명령을 다음 줄로 잇는다. 역슬래시 뒤에 공백을 넣지 않는다.',
     '세 줄의 이름이 Windows에서 확인한 미존재 이름과 같아야 한다. 목록을 만들었다고 Windows 계정이 생성되지는 않는다.'),
 cmd('C02-14',ATT,'hydra -L users-three.txt -p Book2WrongA -t 1 \\\n  rdp://10.20.70.10',
     '대문자 -L은 계정 목록 파일이고 소문자 -p는 단일 암호다. 실습 31의 -l·-P와 입력 대상이 반대다. 세 계정에 같은 암호 하나를 입력한다.',
     '세 후보를 처리하고 0 valid password found가 출력됐다. Windows에서 C02-11을 다시 수행해 TargetUserName과 SubStatus를 읽는다.'))

page('계정 부재와 암호 오류 구분',
 query('Q02-03',BASE+'\nAND data.win.system.eventID:"4625"\nAND (data.win.eventdata.status:"0xc0000064"\n  OR data.win.eventdata.subStatus:"0xc0000064")',
     '0xc0000064는 지정한 계정이 없다는 상태 코드다. 시간 범위를 실습 32로 한정하고, 결과에서 세 이름과 출발지 주소를 대조한다.',
     'book2_missing_a·b·c의 세 기록이 나타났다. 최신 기록 10040은 book2_missing_c의 실패다. Status는 0xc000006d로 같지만 SubStatus는 실습 31의 6a와 다른 64였다.'),
 screen('missing-detail','화면 2-3  존재하지 않는 계정의 0xc0000064와 기록 번호 10040'),
 p('다른 이름이 연속해서 나타나는 패턴은 계정 이름 추측의 단서다. 그러나 오래된 계정으로 실행되는 예약 작업이나 장비 설정도 비슷한 실패를 만든다. 같은 출발지의 계정 이름 분포, 반복 간격, 정상 업무 시각을 함께 조사한다.'))

page('계정 열거의 조사와 원상복구',
 h('성공 기준과 결과가 다를 때'),
 p('세 미존재 이름, 출발지, 실습 시각이 원본과 Wazuh에서 대응하면 확인을 마친다. 0xc000006a가 나오면 이름의 존재 여부와 대상 컴퓨터를 다시 읽는다. 비활성·만료·로그온 제한 코드는 계정 부재와 따로 기록한다. 원본이 없으면 감사와 연결을, 경보만 없으면 수집과 검색을 확인한다.'),
 h('조사·대응'),
 p('유효한 계정으로 이어지는 성공 기록이 있는지 조사한다. 인증 오류의 세부 내용을 외부 응답에 과하게 노출하는 서비스인지도 점검한다. 비정상 출발지를 제한할 때는 공유 게이트웨이·정상 관리 장비 여부를 확인하고, 제한 후 정상 인증이 유지되는지 관찰한다.'),
 h('원상복구'),
 p('세 이름은 파일에만 기록했으므로 삭제할 Windows 계정이 없다. Hydra가 종료된 상태를 유지하고 마지막 절에서 users-three.txt를 제거한다. 이벤트 로그는 조사 근거로 보존한다.'))

page('2.4  실습 33 · 계정 잠금 확인',
 p('계정 잠금은 일정 조건의 인증 실패가 누적됐을 때 계정 사용을 제한하는 기능이다. 잠금으로 암호 추측을 줄일 수 있지만 정상 사용자의 업무도 중단될 수 있다. 실패 횟수, 잠금 기간, 발생 시각을 함께 기록한다.'),
 fig('lockout','그림 2-4  암호 오류·계정 잠금·잠금 기간 경과의 구분'),
 p('4740은 계정이 잠겼음을 알리는 Security 이벤트다. 도메인 컨트롤러뿐 아니라 로컬 계정을 관리하는 워크스테이션이나 멤버 서버에도 기록될 수 있다. 여기서는 KT66-WIN-01의 로컬 victim을 조사한다.'),
 p('C02-01·02로 Lockout False와 5회·1분·1분 정책을 확인한다. 이전 입력으로부터 관찰 기간이 충분히 지난 뒤 C02-08로 시작 시각을 새로 기록한다. 임계값이 다르면 자신의 실습 정책과 입력 수를 먼저 맞춘다.'))

page('잠금을 만드는 제한된 입력',
 cmd('C02-15',ATT,"ls -l pw-five.txt\nprintf '%s\\n' Book2Wrong1 Book2Wrong2 Book2Wrong3 \\\n  Book2Wrong4 Book2Wrong5 > pw-five.txt\ncat pw-five.txt",
     '이름이 같은 파일이 없음을 확인하고 틀린 암호 다섯 개를 저장한다. printf의 %s와 \\n이 각 후보를 별도 줄에 놓는다.',
     '다섯 줄을 읽고 자신의 계정 정책에 맞춘 목록인지 확인한다. 이 목록에는 정상 암호가 들어 있지 않다.'),
 cmd('C02-16',ATT,'hydra -l victim -P pw-five.txt -t 1 rdp://10.20.70.10',
     '같은 계정에 목록의 후보를 차례로 입력한다. -t 1은 동시성을 제한하며 전체 시도 횟수는 목록의 다섯 후보로 제한한다.',
     '입력이 끝나면 Windows에서 C02-01을 다시 실행한다. 이 환경에서는 Enabled True를 유지한 채 Lockout True가 됐다.'),
 cmd('C02-17',WIN,"$lockFilter = @{ LogName='Security'; Id=4740;\n  StartTime=$start }\n$lockEvent = Get-WinEvent `\n  -FilterHashtable $lockFilter -MaxEvents 1\n$lockEvent | Format-List TimeCreated,RecordId,Message\n$lockEvent.ToXml()",
     '$lockEvent에 이번 구간의 최신 잠금 기록을 보관한다. Message와 XML을 같은 이벤트에서 읽어 표시 이름과 원본 필드 이름을 연결한다.',
     '잠긴 계정 victim, 기록 번호 10103, 컴퓨터 KT66-WIN-01을 확인했다. 자신의 기록에서 잠금 대상과 시각이 일치해야 한다.'))

page('잠금 이벤트의 주체와 호출자',
 query('Q02-04',BASE+'\nAND data.win.system.eventID:"4740"\nAND data.win.eventdata.targetUserName:"victim"',
     '원본과 같은 계정의 잠금 이벤트를 찾는다. 행을 펼친 뒤 View single document에서 필드를 읽는다.',
     '기록 10103에 해당하는 경보를 찾았다. 4740에는 로그온 실패의 IpAddress가 없을 수 있으므로 인접한 4625와 함께 조사한다.'),
 screen('4740-detail','화면 2-4  로컬 victim의 잠금 대상과 이벤트 주체'),
 p('subjectUserName의 KT66-WIN-01$과 subjectUserSid S-1-5-18은 잠금을 처리한 시스템 문맥을 나타낸다. 이 값을 공격자 이름으로 적지 않는다. targetUserName victim이 잠긴 계정이다.'))

page('필드 이름만으로 호출자를 판단하지 않기',
 p('이 4740의 Windows 메시지는 Caller Computer Name을 attacker로 표시했다. 같은 이벤트 XML에서는 이 값이 TargetDomainName 요소에 들어 있었고 Wazuh는 data.win.eventdata.targetDomainName으로 표시했다. 따라서 이 기록의 attacker를 victim이 속한 도메인 이름으로 해석하면 안 된다.'),
 code('Message: Caller Computer Name = attacker\nXML: <Data Name="TargetDomainName">attacker</Data>\nWazuh: data.win.eventdata.targetDomainName'),
 p('이벤트마다 필드의 쓰임이 같다고 가정하지 않고 메시지·XML·수집 필드를 대조한다. 호출자 이름이 없거나 중계 장비를 가리키면 같은 계정의 앞선 4625에서 출발지 주소를 보완한다. 이름과 주소가 같더라도 NAT나 중계 경로가 있는지 확인한다.'),
 query('Q02-05',BASE+'\nAND data.win.system.eventID:"4625"\nAND data.win.eventdata.targetUserName:"victim"\nAND (data.win.eventdata.status:"0xc0000234"\n  OR data.win.eventdata.subStatus:"0xc0000234")',
     '0xc0000234는 잠긴 계정에 대한 로그온 실패를 찾는 조건이다. 이미 발생한 실패를 조사할 때 사용하며, 검색 결과를 만들기 위해 추가 실패를 반복할 필요는 없다.',
     '다섯 후보의 마지막 실패까지 0xc000006a였고 4740이 별도로 남았다. 이 검증 구간에서 위 검색은 0건이었다. 잠금 자체는 4740과 Lockout 상태로 확인한다.'),
 p('잠금 발생 이벤트와 잠긴 계정으로 다시 접속했다가 실패한 이벤트는 서로 다르다. 추가 입력 여부에 따라 후자의 기록이 없을 수 있다.'))

page('잠금의 대응과 원상복구',
 h('조사·대응'),
 p('잠금 직전 실패의 계정·주소·시각을 묶고 정상 사용자의 저장된 암호나 서비스 작업도 조사한다. 원인이 계속 남아 있으면 잠금을 풀어도 다시 잠길 수 있다. 업무 영향과 비정상 출발지를 확인한 뒤 접속 경로 제한과 계정 복구를 결정한다.'),
 h('원상복구'),
 p('Hydra 입력을 중지한 상태에서 정책의 잠금 기간이 지나기를 기다린다. 이 환경에서는 1분이 지난 후 C02-01의 Lockout이 False로 돌아왔다. Enabled True만 보고 해제됐다고 판단하지 않는다. 기간이 0으로 설정된 환경에서는 관리자 해제 절차가 필요하므로 이 실습의 자동 해제 결과를 적용하지 않는다.'),
 h('결과가 다를 때'),
 p('Lockout이 True인데 4740이 없으면 사용자 계정 관리 감사와 이벤트 발생 컴퓨터를 확인한다. 경보만 없으면 원본 기록 번호를 기준으로 수집 구간을 조사한다. 잠기지 않으면 실제 실패가 발생했는지, 관찰 기간과 임계값이 무엇인지 먼저 읽는다. 검증 없이 시도 수를 계속 늘리지 않는다.'),
 art('response','그림 2-5  잠금 시각과 정상 업무 기록의 대조'))

page('2.5  실습 34 · 원격 대화형 로그온',
 p('Lockout False인 victim의 정상 자격증명으로 RDP 인증을 수행한다. kt66 기준 준비 코드의 실습 암호는 Victim!2026이다. 자신의 실습 환경에서 바꿨다면 그 값을 사용한다. 실제 업무 계정의 암호를 예제 파일에 저장하지 않는다.'),
 p('이번 입력은 그래픽 환경이 없는 컨테이너에서 가상 화면을 사용하는 방식이다. 인증과 원격 로그온 이벤트를 조사하며, 독자의 Windows PC에 원격 데스크톱 화면이 표시되는 방식과 구분한다. 기존 Windows 사용자의 열린 작업은 유지한다.'),
 p('xvfb-run -a는 사용 가능한 가상 X 화면 번호를 골라 클라이언트를 실행한다. xfreerdp의 /v:는 서버, /u:는 사용자, /p:는 암호다. /cert:tofu는 처음 접속한 인증서를 저장하고 이후 다른 인증서가 나타나면 거부하는 방식이다. 첫 접속 대상의 진위는 별도로 확인해야 하므로 실습 VM과 주소를 먼저 대조한다.'),
 cmd('C02-18',ATT,'ls -l /root/.config/freerdp/known_hosts2',
     'FreeRDP가 기억한 인증서 목록 파일의 기존 유무를 확인한다. 이 경로는 현재 root 계정으로 들어간 컨테이너 기준이다.',
     '파일이 없다면 이번 접속에서 처음 만들어질 수 있다. 파일이 이미 있으면 다음 명령으로 별도 백업을 만든다.'),
 cmd('C02-19',ATT,'cp -p /root/.config/freerdp/known_hosts2 \\\n  /tmp/wazuh-book2-ch02/known_hosts2.before\nls -l /tmp/wazuh-book2-ch02/known_hosts2.before',
     'C02-18에서 파일이 있었고 백업 이름이 비어 있을 때만 실행한다. cp는 파일 복사, -p는 권한과 시각 등 속성을 보존한다.',
     '백업 파일이 생성됐는지 확인한다. 기존 목록이 없었다면 이 단계를 건너뛰고 파일이 없었다는 사실을 기록한다.'))

page('시간을 제한한 RDP 입력',
 p('C02-08로 이번 시작 시각을 다시 기록한다. timeout의 --signal=INT는 제한 시간이 지나면 인터럽트 신호를 보낸다. 25s는 25초다. 작은따옴표는 암호의 느낌표(!)가 Bash의 이력 확장 등으로 해석되지 않도록 묶는다.'),
 cmd('C02-20',ATT,"timeout --signal=INT 25s xvfb-run -a xfreerdp \\\n  /v:10.20.70.10 /u:victim /p:'Victim!2026' \\\n  /cert:tofu",
     'timeout이 xvfb-run과 그 안의 RDP 클라이언트 실행 시간을 제한한다. 실제 원격 로그온을 요청하므로 인증만 검사하는 +auth-only 옵션을 추가하지 않는다.',
     '클라이언트의 인증·연결 메시지를 읽는다. 25초 뒤 인터럽트 종료 메시지가 나올 수 있다. 시간 제한 종료 자체를 인증 실패로 해석하지 않고 Windows의 4624와 유형을 확인한다.'),
 p('현재 Windows에서 다른 사용자가 세션을 사용 중이면 세션 전환과 관련된 안내가 생길 수 있다. 이번 검증에서도 LOGON_MSG_BUMP_OPTIONS 메시지가 있었다. 원격 로그온 이벤트가 생성된 사실과 사용자가 원격 바탕 화면에서 실제 작업한 사실은 별도로 확인한다.'),
 cmd('C02-21',WIN,"$successFilter = @{ LogName='Security'; Id=4624;\n  StartTime=$start }\nGet-WinEvent -FilterHashtable $successFilter `\n  -MaxEvents 20 |\n  Format-List TimeCreated,RecordId,Message",
     '같은 시간대의 4624를 최신 20건까지 읽는다. 서비스와 관리 접속도 포함될 수 있으므로 메시지의 새 로그온 계정과 LogonType을 직접 확인한다.',
     'victim의 LogonType 10, IpAddress 10.20.30.202를 확인했다. 해당 기록 번호는 10207이다. 유형 3이나 서비스 로그온만으로 원격 대화형 로그온을 대신 판단하지 않는다.'))

page('Wazuh에서 원격 로그온 확인',
 query('Q02-06',BASE+'\nAND data.win.system.eventID:"4624"\nAND data.win.eventdata.logonType:"10"\nAND data.win.eventdata.targetUserName:"victim"\nAND data.win.eventdata.ipAddress:"10.20.30.202"',
     '성공 이벤트·원격 대화형 유형·계정·출발지 주소를 함께 제한한다. 다른 환경에서는 직접 관찰한 출발지 주소로 바꾼다.',
     '2026-11-03 12:09의 기록 10207에 해당하는 경보 한 건을 찾았다. 자신의 원본과 Wazuh의 계정·주소·유형·기록 번호가 같아야 한다.'),
 screen('4624-type','화면 2-5  원격 로그온의 출발지 주소와 유형 10'),
 p('루프백 주소 127.0.0.1과 미기록 값 -를 제외하는 검색은 공인 외부 IP만 고르는 조건이 아니다. 이 실습의 10.20.30.202도 사설 주소다. 출발지의 의미는 네트워크 구성과 주소 대역을 대조해 판단한다.'))

page('성공 로그온의 조사 범위',
 screen('4624-account','화면 2-6  성공 계정 victim과 원격 로그온 기록 10207'),
 p('이 기록의 targetLogonId는 0x1ca2207이었다. 같은 컴퓨터의 후속 활동과 로그오프를 연관시키는 단서로 사용할 수 있다. 계정 이름만 같다고 서로 다른 세션을 합치지 않는다. 이벤트 수와 사용자가 접속한 횟수도 자동으로 같다고 두지 않는다.'),
 h('조사·대응'),
 p('성공 직전의 암호 오류·계정 잠금, 사용자 승인 여부, 출발지 장비와 접속 시각을 대조한다. 승인되지 않은 성공이면 해당 세션의 프로세스·파일·계정 변경을 추가로 조사한다. 정상 관리 접속이면 변경 요청이나 작업 기록으로 근거를 남긴다. 성공 이벤트 자체만으로 침해를 확정하지 않는다.'),
 h('결과가 다를 때'),
 p('4625이면 상태 코드와 잠금·암호·로그온 권한을 확인한다. 4624의 유형 3만 있으면 인증 이후 원격 세션이 만들어졌는지 확인한다. 인증서 불일치가 나오면 대상 주소와 Windows 인증서를 대조하고, 캐시를 무조건 지우거나 검증을 끄는 방식으로 진행하지 않는다.'))

page('RDP 세션 원상복구',
 p('클라이언트 연결 종료와 Windows 세션의 로그오프는 다를 수 있다. quser.exe는 현재 Windows 사용자 세션을 조회한다. logoff.exe는 지정한 세션을 로그오프한다. 로그오프하면 그 세션의 프로그램이 종료되므로 이번 실습으로 생긴 victim 세션만 고른다.'),
 cmd('C02-22',WIN,'quser.exe',
     '사용자 이름·세션 ID·상태를 읽는다. 접속 전 목록과 비교해 이번 실습의 세션을 구분한다.',
     '이번 실행 뒤에는 기존 kt66student 콘솔 세션만 남았으므로 추가 로그오프가 필요 없었다. victim 세션이 남았다면 저장할 작업이 없는지 확인하고 다음 명령을 수행한다.'),
 cmd('C02-23',WIN,'logoff.exe <확인한_victim_세션_ID>\nquser.exe',
     '꺾쇠로 표시한 부분 전체를 C02-22에서 읽은 숫자로 바꾼다. 꺾쇠 자체는 입력하지 않는다. 다른 계정의 세션 ID를 넣지 않는다.',
     '선택한 victim 세션이 사라져야 한다. victim이 없으면 logoff를 실행하지 않는다. 마지막으로 C02-01에서 Enabled True와 Lockout False를 확인한다.'),
 p('이벤트 기록과 계정의 LastLogon은 관찰 이력으로 남는다. 원상복구를 위해 Security 로그를 지우거나 기록 시각을 되돌리지 않는다.'))

page('2.6  실패·잠금·성공을 시간순으로 연결',
 query('Q02-07',BASE+'\nAND data.win.eventdata.targetUserName:"victim"\nAND data.win.system.eventID:("4625" OR "4740" OR "4624")',
     '하나의 필드 뒤 소괄호 안에서 세 값을 OR로 묶는다. Discover 표에서 Time 열을 오름차순으로 정렬하고 사건 순서를 읽는다. systemTime도 펼쳐 원본 시각과 비교한다.',
     '실패·잠금·성공이 같은 컴퓨터와 계정에 연결되는지 읽는다. 같은 계정의 서비스 로그온 등 다른 유형은 구분한다.'),
 table(['관찰 시각 · 한국 시각','근거와 확인된 사실'],[['12:00:47','9976·9978 · victim 암호 오류 두 건'],['12:03:26~27','10036·10038·10040 · 세 미존재 이름'],['12:05:19~20','10096~10105 구간 · 암호 오류 다섯 건과 4740'],['12:09:19','10207 · victim 원격 대화형 로그온']],[48,79]),
 p('위 구간은 책의 서로 다른 입력을 차례로 수행한 기록이다. 실패 뒤 성공이 있다는 시간적 순서만으로 동일 공격자가 암호를 알아냈다고 주장하지 않는다. 실제로는 저자가 알고 있던 실습 암호를 마지막 입력에 사용했다. 조사 보고서에서도 확인된 사실과 원인에 관한 추정을 분리한다.'),
 fig('decision','그림 2-6  인증 관찰에서 대응 판단으로 이어지는 확인 항목'))

page('목록 파일과 인증서 캐시 원상복구',
 p('먼저 컨테이너의 현재 위치와 파일 목록을 확인한다. rm은 파일 제거, rmdir는 빈 디렉터리 제거 도구다. 이번 실습에서 만든 파일 이름을 하나씩 지정한다.'),
 cmd('C02-24',ATT,'pwd\nls -la /tmp/wazuh-book2-ch02\ncat /root/.config/freerdp/known_hosts2',
     '현재 위치가 실습 디렉터리인지 확인하고 삭제할 세 목록 파일을 읽는다. cat으로 저장된 인증서 목록이 어떤 대상의 기록인지 확인한다.',
     'pw-two.txt, users-three.txt, pw-five.txt를 확인한다. 기존 인증서 목록을 백업했다면 known_hosts2.before도 있다.'),
 cmd('C02-25',ATT,'cp -p known_hosts2.before \\\n  /root/.config/freerdp/known_hosts2\ncat /root/.config/freerdp/known_hosts2',
     '접속 전에 목록 파일이 있었고 C02-19의 백업이 확인된 경우에만 실행한다. 백업 내용으로 되돌린 뒤 결과를 읽는다.',
     '접속 전의 인증서 목록과 같아야 한다. 이전 파일이 없었다면 이 명령 대신 다음 문단의 조건을 적용한다.'),
 cmd('C02-25A',ATT,'rm /root/.config/freerdp/known_hosts2\nls -l /root/.config/freerdp/known_hosts2',
     '접속 전 known_hosts2가 없었고 지금도 이번 대상 10.20.70.10의 한 줄만 있을 때 그 새 파일을 제거한다. 다른 대상의 줄이 있으면 사전 기록과 대조한 뒤 해당 항목만 정리한다.',
     'No such file or directory로 제거 결과를 확인한다. 기존 파일을 복원한 경우에는 이 명령을 실행하지 않는다.'),
 cmd('C02-26',ATT,'rm pw-two.txt users-three.txt pw-five.txt\nls -la /tmp/wazuh-book2-ch02',
     '사전 목록에서 확인한 세 파일만 제거한다. 백업 파일이 남았다면 캐시 복원 확인 후 C02-26A를 실행한다.',
     '현재 디렉터리에 이번 실습 파일이 남지 않아야 한다. 다른 파일은 내용을 확인하기 전 제거하지 않는다.'),
 cmd('C02-26A',ATT,'ls -l known_hosts2.before\nrm known_hosts2.before\nls -l known_hosts2.before',
     'C02-25에서 기존 캐시의 복원을 확인했고 백업 파일이 남아 있을 때만 실행한다.',
     '백업 파일이 없어져야 한다. 처음부터 백업이 없었다면 이 명령을 건너뛴다.'),
 cmd('C02-27',ATT,'cd /tmp\nrmdir /tmp/wazuh-book2-ch02\nls -ld /tmp/wazuh-book2-ch02\nexit',
     'cd로 대상 밖으로 이동한다. rmdir는 비어 있을 때만 디렉터리를 제거한다. ls로 제거 결과를 읽고 exit로 컨테이너 셸을 끝낸다.',
     'No such file or directory를 확인한 뒤 kt66 호스트 프롬프트로 돌아온다. Windows의 센서와 보호 상태도 실습 전과 같은지 확인한다.'))

page('2.7  장 마무리',
 table(['판단할 질문','확인할 근거'],[['암호 오류인가, 없는 계정인가','4625의 Status·SubStatus와 계정 목록'],['계정이 실제로 잠겼는가','Lockout 속성과 4740의 대상'],['원격 대화형 로그온이 있었는가','4624의 유형 10·계정·출발지'],['그 접속은 승인됐는가','사용자·장비·업무 기록과 후속 활동'],['실습 상태로 돌아왔는가','잠금 해제·세션·목록 파일·센서 상태']],[55,72]),
 h('확인 문제'),
 p('① Enabled True인데 Lockout True인 계정은 어떤 상태인가? ② 4740의 subjectUserName이 컴퓨터 이름으로 나타날 때 누구를 공격자로 적어야 하는가? ③ 127.0.0.1을 제외한 주소가 모두 공인 외부 주소인가? ④ 4624 유형 10 한 건으로 원격 바탕 화면에서 특정 명령을 실행했다고 판단할 수 있는가?'),
 h('해설'),
 p('① 계정은 사용 가능하도록 설정되어 있으나 현재 인증 실패에 따른 잠금 상태다. ② 이벤트 주체와 접속 출발지를 구분하고 앞선 실패의 주소·이름·시각을 대조한다. 그 필드만으로 공격자를 정하지 않는다. ③ 사설 주소와 중계 주소도 포함되므로 네트워크 구성을 확인한다. ④ 원격 로그온의 단서이며 실제 명령 실행은 프로세스 등 별도 기록으로 확인한다.'))

page('참고자료',
 link('Module 01 · 실습 31~34 · 슬라이드 순서 349~386', 'https://docs.google.com/presentation/d/1o0H_2DDHBp8p2HvlSnEPbx6-jdURYzew'),
 link('kt66 Windows 센서 준비 코드 · 기준 커밋', 'https://github.com/mrgrit/kt66/blob/63d4180b1d6866de986ef263a3bd831d6082b5d5/endpoints/windows/oem/sensors.ps1'),
 link('Microsoft Learn · 이벤트 4625', 'https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4625'),
 link('Microsoft Learn · 이벤트 4740', 'https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4740'),br=True)
page('참고자료 계속',
 link('Microsoft Learn · 이벤트 4624', 'https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4624'),
 link('Hydra · 공식 저장소와 사용 설명', 'https://github.com/vanhauser-thc/thc-hydra'),
 link('FreeRDP · 공식 저장소 · 2.6.1', 'https://github.com/FreeRDP/FreeRDP/tree/2.6.1'),
 link('Microsoft Learn · logoff', 'https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/logoff'),br=True)

def main():
 data={'title':'로그온 실패와 원격 접속','series':'해킹·침해대응 실무 with Wazuh 2권','comments':'2026-11-03 초안. Module 01 실습 31~34. 제한된 입력 재현·원본 이벤트·Wazuh DQL·실제 화면 대조. 상세 범위는 editorial/chapter02-review.md.','pages':pages}
 (ROOT/'manuscript/volume02-chapter02.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 ex=ROOT/'examples/chapter02';ex.mkdir(parents=True,exist_ok=True);manifest=[]
 for pg in pages:
  for b in pg['blocks']:
   if b['type'] not in ('command','query'):continue
   name=b['id']+('.dql' if b['type']=='query' else '.txt');(ex/name).write_text(b['text']+'\n',encoding='utf8')
   manifest.append({'id':b['id'],'file':name,'where':b['where'],'section':pg['title'],'input':b['text']})
 (ex/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 (ex/'README.md').write_text('# 2장 복사용 예제\n\n본문의 선행 확인 뒤 한 명령씩 입력한다. 전체를 자동 실행하지 않는다.\n\n- C02-04: kt66 Ubuntu 호스트. 이후 ATT 표시는 컨테이너 안이다.\n- WIN 표시는 Windows 실습 게스트의 관리자 PowerShell이다.\n- C02-08의 $start는 각 실습 시작에 갱신한다. 같은 창에서 조회한다.\n- C02-19·23·25·25A·26A는 본문 조건에 해당할 때만 실행한다.\n- Q02는 Wazuh Discover DQL이다. 실습 시간 범위를 함께 맞춘다.\n- Victim!2026은 kt66 기준 코드의 공개 실습용 값이다. 개인 암호를 파일에 저장하지 않는다.\n\n'+ '\n'.join(f"- [{m['file']}]({m['file']}) — {m['where']}" for m in manifest)+'\n',encoding='utf8')
 (ex/'observation-template.md').write_text('# 2장 관찰 기록\n\n- 실습 번호와 시작·종료 시각/시간대:\n- 대상 컴퓨터와 계정, 출발지:\n- 잠금 정책과 사전 Lockout:\n- 입력 목록 수와 도구 응답:\n- 원본 채널·EventID·EventRecordID·시각:\n- Status·SubStatus·LogonType:\n- Wazuh 경보·원본과 일치한 값:\n- 확인된 사실과 추가 조사:\n- 잠금·세션·파일·보호 상태의 원상복구:\n',encoding='utf8')
 print(len(pages),'sections;',len(manifest),'examples')
if __name__=='__main__':main()
