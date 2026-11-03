"""Module01 실습57·58. 수집 상태와 자동 대응의 증거를 분리한다."""
from chapter_authoring import *
pages=[]
SIEM='kt66-siem 컨테이너 · root Bash'
BASTION='kt66-bastion 컨테이너 · root Bash'
def page(t,*b):pages.append({'title':t,'kind':'body','level':'section','break':False,'blocks':list(b)})
def dq(i,t,w,r):return query(i,t,w,r,index='wazuh-alerts-*')
def pic(n,c,w=127):return image('assets/screenshots/chapter10/'+n+'.png',c,w)
page('10장  수집 장애와 자동 대응',
 p('경보가 끊기면 공격이 멈춘 것인지 수집이 멈춘 것인지 먼저 구분한다. 자동 대응 기록이 생기면 명령을 전달한 대상과 실제로 바뀐 방화벽 상태를 확인한다. 두 확인을 마쳐야 관측 가능한 범위와 대응 결과를 기록할 수 있다.'),
 table(['실습','확인할 대상','완료 기준'],[['57','에이전트 단절·시작·중지','수집 공백과 원인 후보를 구분'],['58','자동 대응의 추가·해제','원인 경보·대상 IP·처리 이력을 연결']],[16,49,62]),
 p('기존 단절·차단 이력을 분석하고 현재 상태를 조회한다. 원전의 중지·접속 실험은 당시 기록으로 읽는다. 운영 중인 컨테이너를 멈추거나 인증 실패를 반복해서 새 경보를 만들 필요는 없다.'),
 image('assets/illustrations/chapter10/connectivity.png','그림 10-1  통신함의 장비 상태를 확인하는 담당자',66))
page('10.1  준비와 실행 위치',
 p('1권의 kt66 설치와 2권 1장의 수집 준비를 마친 환경에서 시작한다. Windows PC 브라우저로 https://192.168.0.107:5601에 접속한다. 로그인 뒤 **Overview → Active**에서 fw·bastion의 이름과 ID를 기록한다. 이번 등록값은 fw 003, bastion 001이다. ID는 환경마다 달라진다.'),
 p('Windows PC는 대시보드와 SSH 접속에 사용한다. kt66 Ubuntu VM은 Docker를 실행하는 호스트다. kt66-siem은 관리자 설정과 규칙을, kt66-bastion은 자동 대응 대상의 로그와 방화벽을 확인할 위치다.'),
 cmd('C10-01','ssh ccc@192.168.0.107','ssh는 원격 셸을 여는 도구다. 계정@주소를 지정하고 암호는 프롬프트에서 입력한다. 처음 접속하는 호스트의 지문은 VM의 값과 대조한다.','Ubuntu 프롬프트를 확인한다. 시간 초과는 VM·주소·통신 경로부터, 연결 거부는 SSH 서비스부터 점검한다.',where='Windows PC · PowerShell'),
 cmd('C10-02','sudo docker ps --format "{{.Names}}\\t{{.Status}}"','sudo는 관리자 권한으로 실행한다. docker ps는 실행 중인 컨테이너를 읽는다. --format은 출력 형식이며 Names·Status는 이름·상태, \\t는 탭이다.','kt66-siem·kt66-fw·kt66-bastion이 Up인지 기록한다. 목록에 없으면 docker ps -a로 중지된 항목도 확인한다.',where=HOST))
page('관리자 서버에서 연결 상태 확인',
 cmd('C10-03','sudo docker exec -it kt66-siem /bin/bash\nhostname','docker exec -it는 실행 중인 컨테이너에 표준입력과 대화형 터미널을 연결한다. /bin/bash는 셸 프로그램이며 hostname은 실행 위치의 이름을 출력한다.','kt66-siem 내부 셸에서 다음 명령을 실행한다. 끝나면 exit로 Ubuntu 호스트에 돌아온다.',where=HOST),
 cmd('C10-04','/var/ossec/bin/agent_control -l','agent_control은 관리자 서버에서 에이전트 정보를 조회·관리하는 도구다. 여기서는 목록 조회 옵션 -l만 사용한다.','fw와 bastion의 ID·이름·Active 여부를 기록한다. 연결 상태가 Active여도 특정 로그 파일이 수집되는지는 별도 확인한다.',where=SIEM),
 cmd('C10-05','less /var/ossec/etc/ossec.conf','less는 파일을 화면 단위로 읽는다. /agents_disconnection을 입력하고 Enter를 누른다. 슬래시(/)는 검색 시작, n은 다음 결과, q는 종료다.','global의 agents_disconnection_time과 agents_disconnection_alert_time을 찾는다. 이 환경은 60s와 0이다. 파일을 편집하지 않는다.',where=SIEM),
 p('keepalive는 에이전트가 연결을 알리는 주기적 통신이다. agents_disconnection_time은 마지막 keepalive 이후 단절로 간주할 시간을, agents_disconnection_alert_time은 단절 판단 뒤 경보까지의 추가 지연을 정한다. 수집·처리 지연도 있으므로 중지 버튼을 누른 시각에서 정확히 60초 뒤 경보가 표시된다고 계산하지 않는다.'))
page('10.2  실습 57 수집 공백을 찾는다',
 p('공격자는 관리자 권한으로 수집 서비스를 중지하거나 통신을 방해할 수 있다. 같은 공백이 계획된 재시작, VM 종료, 경로 장애에서도 발생한다. 공백은 조사할 사실이며 원인은 별도 증거로 결정한다.'),
 image('assets/figures/chapter10/collection.png','그림 10-2  연결 상태와 로그 수집 상태의 확인 지점'),
 table(['규칙','표시와 의미','함께 확인할 기록'],[['503','Agent started: 에이전트 시작','직전 중지·단절과 현재 수집'],['504','Agent disconnected: 통신 단절','VM·컨테이너·관리자 연결'],['506','Agent stopped: 중지 통지','서비스 종료·작업 승인 내역']],[17,55,55]),
 p('503은 시작을 뜻한다. 재시작 후에도 나타나지만 503 한 건만으로 재시작을 확정하지 않는다. 첫 연결에는 501이 나타날 수 있다. 비정상 종료나 통신 장애로 통지가 전달되지 않으면 506 대신 504만 관찰될 수 있다.'))
page('검색 기간과 표 열 구성',
 p('**Explore → Discover**에서 데이터 보기를 **wazuh-alerts-***, 언어를 **DQL**로 선택한다. 기존 고정 필터를 해제하고 상태 이력을 포함하는 기간을 선택한다. 이번 조회는 **Last 90 days**를 사용했다. 실제 조사에서는 공백 전후의 절대 시각을 기록한다. 화면 시간대는 KST다.'),
 dq('Q10-01','rule.id:(503 OR 504 OR 506)','괄호 안의 OR는 세 규칙 중 하나와 일치하는 경보를 찾는다. 콜론(:)은 필드 조건을 지정한다.','왼쪽 필드 목록에서 agent.name, rule.id, rule.description의 Add 버튼으로 열을 추가한다. Time을 오름차순으로 바꾸어 중지·단절·시작 순서를 읽는다.'),
 pic('agent-events','그림 10-3  에이전트 시작·중지·단절 이력'),
 p('조회한 환경에는 27건이 있었다. 최근 두 행은 kt66-host의 08:52:47 중지(506)와 08:52:48 시작(503)이다. 검색 건수와 에이전트는 실행 환경에 따라 달라진다. 각 행을 펼쳐 full_log의 대상과 agent.name이 일치하는지 확인한다.'))
page('원전의 fw 단절 사례',
 pic('source-disconnect','그림 10-4  fw와 bastion의 단절 및 fw 시작 기록'),
 p('원전에서는 kt66 Ubuntu 호스트에서 kt66-fw 컨테이너를 중지한 뒤 약 100초 후 시작했다. Docker 호스트에서 수행한 작업이지 별도 공격자 VM에서 로컬 컨테이너를 중지한 작업이 아니다. 이 절에서는 화면의 결과를 분석한다.'),
 p('10월 31일 19:26:17에 fw와 bastion의 504가 함께 있고, 19:27:01에는 fw의 503이 있다. fw는 통신 경로에도 관여하므로 여러 센서가 함께 단절될 수 있다. bastion의 504가 있다고 bastion 프로세스도 중지됐다고 단정하지 않는다.'),
 dq('Q10-02','agent.name:"fw" AND rule.id:(503 OR 504 OR 506)','AND는 같은 문서가 두 조건을 모두 만족하도록 한다. fw는 자신의 에이전트 이름으로 바꾼다.','첫 공백·마지막 정상 수집·복구 후 첫 로그의 시각을 기록한다. 기존 원전 자료가 없는 현재 인덱스에서 같은 4건을 기대하지 않는다.'),
 p('test*·lab*처럼 이름 접두어 전체를 제외하면 필요한 실습 센서까지 숨길 수 있다. 처음에는 전체를 확인하고, 승인된 제외 대상만 별도로 기록한다.'))
page('원인 조사와 실패 시 확인 순서',
 p('먼저 대시보드의 기간·필터·데이터 보기를 확인한다. 다음으로 다른 에이전트의 최근 로그를 비교한다. 모두 멈췄다면 관리자·인덱서·공통 경로를, 하나만 멈췄다면 해당 호스트의 전원·서비스·연결을 우선 확인한다.'),
 cmd('C10-06','tail -n 40 /var/ossec/logs/ossec.log','tail은 파일 끝을 읽는다. -n 40은 마지막 40줄이다. 관리자 서버의 최근 처리 오류를 확인한다.','연결·큐·인증 오류의 시각과 대상 ID를 기록한다. 오래된 장애는 less로 당시 구간을 확인한다. 최신 40줄에 없다는 이유만으로 오류가 없었다고 결론내리지 않는다.',where=SIEM),
 cmd('C10-07','exit\nsudo docker exec -it kt66-bastion /bin/bash\n/var/ossec/bin/wazuh-control status','exit는 컨테이너 셸을 끝낸다. Ubuntu 프롬프트에서 bastion 셸을 연다. wazuh-control status는 에이전트 구성 프로세스의 실행 상태를 읽는다.','wazuh-agentd·wazuh-logcollector·wazuh-execd 상태를 확인한다. 실행 상태와 오류 로그를 함께 읽고, 서비스를 일괄 재시작하기 전에 장애 시각을 보존한다.',where='kt66-siem에서 exit 후 kt66 Ubuntu VM, 이어 bastion'),
 p('중지 직전 sudo가 있었어도 명령 내용·계정·세션·승인 작업을 대조한다. 정상 유지보수도 sudo를 사용한다. 서비스 중지 명령과 실행 주체가 확인되면 고의 변경 가능성을 조사하되, 승인 여부까지 확인하여 악의적 행위와 구분한다.'))
page('실습 57의 복구 판정',
 table(['상황','다음 행동','복구 확인'],[['VM·컨테이너 중지','담당자가 승인된 시작 절차 수행','Up·Active와 새 로그'],['네트워크 단절','주소·경로·정책 변경 원인 복원','통신 회복과 수집 시각 갱신'],['수집 프로세스 오류','오류 원인을 보존하고 수정','프로세스·파일 읽기·새 이벤트'],['화면 조건 오류','기간·필터·데이터 보기 수정','같은 조건의 재검색']],[31,50,46]),
 p('완료 조건은 현재 Active, 필요한 수집 프로세스 실행, 해당 로그의 새 이벤트 도착이다. 시작 경보 한 건이나 페이지 새로고침만으로 끝내지 않는다. 장애 중 기록이 지연 수집되었는지, 영구 누락되었는지도 구분한다.'),
 p('원상복구는 변경한 대상에 한정한다. 이 절의 읽기 작업만 했다면 설정을 되돌릴 항목은 없다. 검색 필터와 기간을 원래 작업 조건으로 돌리고 셸을 종료한다. 원전처럼 fw를 중지한 별도 실습을 했다면 fw뿐 아니라 영향을 받은 bastion 등 모든 센서의 수집을 재확인한다.'))
page('10.3  실습 58 자동 대응의 구조',
 p('Active Response는 경보 조건을 만족할 때 정해진 프로그램을 실행하는 Wazuh 기능이다. firewall-drop은 지정한 출발지 IP의 통신을 방화벽 규칙으로 제한하는 대응 프로그램이다. 공격 시도의 탐지, 대응 명령, 실제 차단 결과는 각각 다른 증거다.'),
 image('assets/figures/chapter10/response.png','그림 10-5  원인 경보와 자동 대응 기록의 연결'),
 p('이 환경은 SSH 반복 인증 실패 규칙 5712·5763을 조건으로 firewall-drop을 호출한다. location이 local이면 경보를 발생시킨 에이전트에서 실행한다. 항상 관리자 서버에서 차단하는 설정이라는 뜻은 아니다. timeout 180은 해제 명령을 예약하는 180초 설정이다.'),
 p('원전에서는 차단 중 별도 공격자 VM의 bastion SSH 접속이 시간 초과했고 대상에서 IP 차단 규칙을 조회했다. 시간 초과는 경로·서비스 장애로도 생기므로 방화벽·원인 경보·접속 응답을 함께 보아야 한다.'))
page('자동 대응 설정을 읽는다',
 cmd('C10-08','exit\nsudo docker exec -it kt66-siem /bin/bash\nless /var/ossec/etc/ossec.conf','bastion에서 나와 관리자 컨테이너로 들어간다. less에서 /firewall-drop을 검색하고 n으로 다음 블록을 읽는다.','command 정의의 executable·timeout_allowed와 active-response 블록의 disabled·location·rules_id·timeout을 각각 기록한다.',where='kt66-bastion에서 exit 후 kt66 Ubuntu VM, 이어 siem'),
 code('<command>\n  <name>firewall-drop</name>\n  <executable>firewall-drop</executable>\n  <timeout_allowed>yes</timeout_allowed>\n</command>\n<active-response>\n  <disabled>no</disabled>\n  <command>firewall-drop</command>\n  <location>local</location>\n  <rules_id>5712,5763</rules_id>\n  <timeout>180</timeout>\n</active-response>'),
 p('위 블록은 확인할 구조다. command는 호출 이름과 실행 파일을 연결하고 timeout_allowed는 시간 만료 후 되돌리는 명령을 지원하게 한다. active-response의 disabled가 no여야 해당 대응이 활성화된다. 전역 white_list의 제외 주소와 호스트 이름 패턴도 함께 확인한다.'),
 p('공유 NAT 주소를 차단하면 같은 주소를 쓰는 정상 사용자도 영향을 받을 수 있다. 관리 접속 경로, 서비스 영향, 승인된 제외 대상, 해제 담당자를 정한 뒤 정책을 바꾼다. 오류를 피하려고 내부 대역 전체를 예외로 추가하는 방법은 사용하지 않는다.'))
page('대상 에이전트의 대응 로그',
 cmd('C10-09','exit\nsudo docker exec -it kt66-bastion /bin/bash\nless /var/ossec/logs/active-responses.log','관리자 셸을 끝내고 bastion에 들어간다. 대응 로그에서 /firewall-drop을 검색한다. n으로 같은 프로그램의 다음 줄을 읽는다.','add·check_keys·continue 또는 abort·delete와 오류를 구분한다. parameters.alert 안의 원인 경보 ID, data.srcip, agent.name을 기록한다.',where='kt66-siem에서 exit 후 kt66 Ubuntu VM, 이어 bastion'),
 p('이번에 보존된 기록은 11월 2일 20:31:37의 add와 20:34:38의 delete다. 원인 경보는 5763, 대상 에이전트는 bastion, IP는 192.168.0.108이다. 예약값은 180초지만 관찰된 로그 간격은 181초다. 처리 시각과 설정값을 그대로 구분해 적는다.'),
 table(['항목','뜻'],[['command: add','차단 추가 요청'],['check_keys','동일 대응 키의 중복 처리 확인'],['continue / abort','진행 또는 중단 결정'],['command: delete','해제 요청'],['parameters.alert.id','대응을 유발한 Wazuh 경보 ID']],[48,79]),
 p('로그에 add가 있어도 프로그램이 실제 규칙을 넣었는지는 아직 확인하지 않았다. 입력 JSON이 실행 전 기록될 수 있고 이후 오류도 있을 수 있다. delete도 같은 이유로 해제 완료와 구분한다.'))
page('Wazuh의 차단·해제 검색',
 dq('Q10-03','rule.id:(651 OR 652) OR rule.groups:active_response','규칙 651·652와 active_response 그룹을 함께 조회한다. 기존의 에이전트 필터를 해제하고 원인 경보 전후로 기간을 맞춘다.','각 행을 펼쳐 data.command와 data.parameters.alert의 내용을 확인한다. 651은 firewall-drop의 add, 652는 delete 입력을 분류한다.'),
 pic('active-response','그림 10-6  firewall-drop의 추가·해제 경보'),
 p('JSON 대응 로그는 ar_log_json 디코더로 해석한다. 650은 이 디코더를 받는 부모 규칙이고, 651·652는 parameters.program과 command를 검사하는 하위 규칙이다. 화면의 decoder.name, rule.id, 실행 프로그램 이름은 서로 다른 역할이다.'),
 p('원인 SSH 경보의 출발지는 data.srcip에 있지만 대응 경보는 원인 경보를 parameters.alert에 감싼다. 따라서 대응 대상 주소는 아래의 긴 경로로 검색한다.'))
page('대응 대상과 원인 경보를 연결한다',
 dq('Q10-04','rule.id:(651 OR 652) AND\ndata.parameters.alert.data.srcip:"192.168.0.108"','줄바꿈은 조건을 나누어 읽기 위한 것이다. 중첩된 alert의 data.srcip를 지정하여 실제 대응 대상 IP를 찾는다.','원인 경보의 id가 add와 delete에서 같은지, 대상 에이전트가 같은지 비교한다. 주소는 원문에서 확인한 값으로 바꾼다.'),
 dq('Q10-05','id:"1793619097.12602015"','자신의 대응 경보에 들어 있는 parameters.alert.id 값으로 바꾼다. 대응 로그 자체의 id와 혼동하지 않는다.','조회된 문서의 rule.id·full_log·계정·출발지·시각을 중첩된 원인 경보와 대조한다.'),
 p('이 기록에서는 중첩된 alert.rule.id가 5763이지만 위 ID의 인덱스 문서는 5760이다. 따라서 ID 조회만으로 원인 경보와 일치했다고 처리할 수 없다. 대응 로그의 원문을 보존하고 같은 시각·호스트·주소의 5763을 별도로 찾는다.'),
 dq('Q10-06','rule.id:5763 AND agent.name:"bastion" AND\ndata.srcip:"192.168.0.108"','기간을 대응 직전으로 좁히고 규칙·호스트·주소를 함께 지정한다.','이 환경의 5763 문서는 id가 1793619097.12600800이다. previous_output의 이전 실패와 full_log를 비교한다. 중첩 ID와의 불일치 원인은 별도 조사 항목으로 남긴다.'),
 p('대응 경보의 agent.name은 대응 로그를 수집한 에이전트다. parameters.alert.agent.name은 원인 경보의 에이전트다. local 설정에서는 보통 일치하지만 실행 위치를 바꾸면 달라질 수 있다. IP와 시각만으로 두 경보를 임의 연결하지 않는다.'),
 cmd('C10-10','iptables -S','iptables는 Linux 방화벽 규칙을 관리하는 도구다. -S는 현재 규칙을 명령 형식으로 출력하는 조회 옵션이다. bastion의 규칙을 읽으며 추가·삭제 옵션은 사용하지 않는다.','-s는 출발지, -j DROP은 해당 패킷을 버리는 대상 동작이다. 지금은 INPUT·FORWARD·OUTPUT의 ACCEPT 기본 정책만 있다. 과거 차단 당시의 규칙을 현재 출력으로 증명하지 않는다.',where=BASTION))
page('자동 대응이 보이지 않을 때',
 p('먼저 원인 규칙 5712·5763의 실제 발생 여부를 확인한다. 개별 실패 경보만 있는 경우 대응 조건을 만족하지 않을 수 있다. 다음으로 관리자 설정의 활성화·rules_id·white_list·location을 확인한다. 대상의 wazuh-execd 상태와 active-responses.log를 읽고 방화벽 도구·권한 오류를 찾는다.'),
 p('대상 로그에는 기록이 있으나 651·652가 없으면 에이전트 localfile의 /var/ossec/logs/active-responses.log 수집 설정, 관리자 디코더·규칙, 인덱스와 시간 범위를 순서대로 점검한다. 프로그램 문제와 로그 수집 문제를 분리한다.'),
 table(['증거','판정 가능한 범위'],[['651·add만 있음','대응 추가 입력이 기록됨'],['대상 IP DROP 규칙 있음','조회 시점에 해당 규칙 존재'],['허용된 접속 시험과 서비스 기록','해당 경로·시각의 통신 결과'],['652·delete와 규칙 소멸','해제 입력 및 현재 상태'],['규칙 없음·연결 실패','다른 차단·경로·서비스 원인 조사']],[48,79]),
 p('관측 결과를 “차단 명령 기록, 현재 규칙 없음, 과거 차단 효과는 당시 접속 기록과 대조 필요”처럼 나누어 쓴다. 로그 한 종류의 부재를 기능 전체의 실패로 바꾸어 적지 않는다.'))
page('실습 58의 원상복구와 종결',
 p('기존 대응을 조회한 경우 조회 조건을 되돌리고 셸을 종료한다. 별도로 승인된 차단 실습을 수행한 경우에는 예상 해제 시각 이후 delete·실제 규칙·정상 서비스 경로를 확인한다. 규칙이 남으면 원인과 소유자를 확인하고 해당 실습에서 추가된 정확한 규칙만 담당 절차로 제거한다. 전체 방화벽을 비우면 다른 보호 정책까지 없어지므로 복구 방법으로 삼지 않는다.'),
 cmd('C10-11','exit','exit는 현재 bastion 셸을 종료한다. Ubuntu 프롬프트에서 작업 종료 여부를 확인한다. SSH 연결까지 끝내려면 그 셸에서 exit를 한 번 더 입력한다.','조회 과정에서 변경한 설정·규칙이 없는지 기록한다. 수집·보호 상태는 실습 전후 동일해야 한다.',where=BASTION),
 p('실습 완료 기록에는 원인 경보 ID, 대상 에이전트와 IP, add·delete 시각, 실제 규칙 조회 시각, 서비스 확인 결과, 미확인 범위를 넣는다. 차단 동안의 활동을 조사할 때는 자동 대응이 통신을 바꾸었다는 사실도 시간선에 표시한다.'),
 h('확인 문제와 해설'),
 p('fw와 bastion이 같은 순간 504를 보이면 두 에이전트를 모두 재설치해야 하는가? 먼저 공통 경로와 fw 상태를 확인한다. 공유 경로 장애를 개별 설치 문제로 오인하면 복구가 늦어진다.'),
 p('651이 있고 3분 뒤 652가 있으면 공격 차단에 성공했는가? 추가·해제 입력의 이력은 확인했지만 방화벽 적용·경로·서비스 영향은 별도 근거가 필요하다. 원인 경보와 함께 조사한다.'))
page('참고자료',
 link('Module 01 — 실습 57·58, 슬라이드 583~601','https://docs.google.com/presentation/d/1o0H_2DDHBp8p2HvlSnEPbx6-jdURYzew'),
 link('Wazuh — global 설정','https://documentation.wazuh.com/current/user-manual/reference/ossec-conf/global.html'),
 link('Wazuh — Active Response 설정','https://documentation.wazuh.com/current/user-manual/reference/ossec-conf/active-response.html'),
 link('Wazuh 4.10.0 — 에이전트·자동 대응 규칙','https://github.com/wazuh/wazuh/blob/v4.10.0/ruleset/rules/0015-ossec_rules.xml'),
 link('kt66 — 기준 소스','https://github.com/mrgrit/kt66/tree/63d4180b1d6866de986ef263a3bd831d6082b5d5'))
pages[-1]['break']=True
save(10,'10장 수집 장애와 자동 대응',pages,'Module01 실습57·58. 기존 기록과 현재 읽기 조회를 구분. 신규 중지·차단·공격은 미실행. 상세 범위 editorial/chapter10-review.md.')
