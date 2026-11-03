"""Module01 실습59~61. 네트워크 경보·ATT&CK·일일 관제."""
from chapter_authoring import *
pages=[]
IPS='kt66-ips 컨테이너 · root Bash'
SIEM='kt66-siem 컨테이너 · root Bash'
def page(t,*b):pages.append({'title':t,'kind':'body','level':'section','break':False,'blocks':list(b)})
def dq(i,t,w,r):return query(i,t,w,r,index='wazuh-alerts-*')
def pic(n,c):return image('assets/screenshots/chapter11/'+n+'.png',c)
page('11장  네트워크 경보와 일일 관제',
 p('네트워크 센서는 요청과 패킷의 특징을, 호스트 로그는 로그인·프로세스·파일의 변화를 보여준다. 한쪽의 경보를 발견하면 같은 시각과 대상을 다른 기록에서 찾아 실제 영향을 확인한다. 매일 확인할 경보도 이 기준으로 분류한다.'),
 table(['실습','주제','남길 결과'],[['59','Suricata 네트워크 경보','관측 지점과 호스트 기록의 연결'],['60','MITRE ATT&CK 분류','전술·기법과 실제 증거의 구분'],['61','일일 고위험 경보','담당자·기한·다음 조치가 있는 기록']],[16,48,63]),
 image('assets/illustrations/chapter11/daily-review.png','그림 11-1  사무실에서 일일 관제 보고서를 검토하는 담당자',75))
page('11.1  실습 59 센서의 역할부터 확인한다',
 p('Suricata는 네트워크 트래픽을 분석하여 규칙과 일치하는 특징을 기록하는 엔진이다. 트래픽을 관찰하는 IDS 방식과 전달 경로에서 패킷을 차단하는 IPS 방식이 있다. 프로그램이 경로에 있다는 사실, 규칙의 동작, 실제 실행 모드는 각각 확인해야 한다.'),
 p('이 실습의 kt66-ips는 컨테이너 이름이다. 확인한 Suricata 6.0.4는 -i eth2 -i eth0으로 인터페이스를 읽고, 로컬 규칙은 alert 동작을 사용한다. 현재 설정에서 Suricata의 인라인 차단이 동작한다고 전제하지 않는다. 컨테이너의 별도 nftables 필터 동작과 Suricata 경보를 구분한다.'),
 image('assets/figures/chapter11/sensors.png','그림 11-2  네트워크 관측과 호스트 수집의 연결'),
 p('Wazuh의 ips 에이전트는 /var/log/suricata/eve.json을 읽는다. EVE는 Suricata가 JSON으로 내보내는 이벤트 형식이다. alert 외에도 flow·HTTP·DNS·TLS 등 여러 종류가 있을 수 있다. 모든 EVE 줄이 침해 경보인 것은 아니다.'))
page('준비와 프로세스 확인',
 p('Windows PC에서 Wazuh에 로그인하고 **Overview → Active**에서 ips와 web의 이름·ID를 기록한다. 이번 환경은 ips 004, web 002다. kt66 Ubuntu VM의 터미널로 접속한 다음 아래 순서로 컨테이너에 들어간다. 설치와 등록을 마친 환경을 사용하며 Suricata를 중복 설치하지 않는다.'),
 cmd('C11-01','sudo docker ps --format "{{.Names}}\\t{{.Status}}"\nsudo docker exec -it kt66-ips /bin/bash\nhostname','docker ps는 상태를 조회한다. --format의 Names·Status는 이름·상태, \\t는 탭이다. exec -it는 대화형 Bash 셸을 열며 hostname으로 위치를 확인한다.','kt66-ips가 Up이고 셸의 호스트 이름이 ips인지 확인한다. 종료는 exit다.',where=HOST),
 cmd('C11-02',"suricata -V\npgrep -a -f '^suricata '",'suricata -V는 설치 버전을 출력한다. pgrep은 프로세스를 찾는 도구다. -a는 인수까지 출력하고 -f는 전체 명령줄에서 검색한다. 작은따옴표는 검색식을 셸 해석 없이 전달하며 ^는 줄 시작이다. suricata 뒤 공백까지 일치시킨다. 실행 중 프로세스의 짧은 이름은 Suricata-Main일 수 있다.','버전과 -i·-c·-l·--runmode 값을 기록한다. 이 환경의 -c는 설정 파일, -l은 로그 디렉터리, --runmode autofp는 처리 스레드 방식이며 IPS 차단 스위치가 아니다.',where=IPS),
 p('프로세스가 없으면 컨테이너 상태·시작 로그·설정 오류를 확인한다. 이미 실행 중인 엔진 옆에 두 번째 프로세스를 띄워 오류를 가리지 않는다.'))
page('규칙과 수집 파일을 확인한다',
 cmd('C11-03','less /etc/suricata/rules/local.rules','less는 파일을 화면 단위로 읽는다. 위·아래 키로 이동하고 q로 끝낸다. 규칙 첫 단어와 msg·sid를 대조한다.','로컬 규칙의 첫 동작이 alert인지 확인한다. SQLi·XSS·스캐너 문자열·경로 순회·SYN 반복을 찾는 규칙은 시그니처 일치의 근거이지 성공 판정이 아니다.',where=IPS),
 p('sid는 Suricata 규칙 식별자다. Wazuh rule.id와 다른 번호 체계다. 규칙의 threshold는 특정 기간의 반복 조건을 나타낸다. 이 환경의 SYN 규칙은 같은 출발지에서 10초 동안 30회 조건을 사용한다. 패킷 손실·관측 인터페이스·트래픽 방향에 따라 결과가 달라질 수 있다.'),
 cmd('C11-04','tail -n 2 /var/log/suricata/eve.json\nless /var/ossec/etc/ossec.conf','tail -n 2는 파일의 마지막 두 줄을 읽는다. 다음 less 화면에서 /eve.json을 검색하고 n으로 중복 정의 여부까지 확인한다. 슬래시(/)는 검색 시작이다.','EVE의 timestamp·event_type을 읽고 localfile의 location과 log_format json을 확인한다. 같은 파일을 중복 수집하는 설정이 있으면 건수 해석 전에 검토 대상으로 기록한다.',where=IPS),
 p('파일의 최근 줄이 flow·tls라면 정상적인 다른 종류의 이벤트일 수 있다. alert가 없다고 엔진이 멈췄다고 단정하지 않는다. 프로세스·파일 갱신·경보 조건을 나누어 확인한다.'))
page('Wazuh에서 Suricata를 찾는다',
 p('**Explore → Discover**에서 **wazuh-alerts-***와 **DQL**을 선택한다. 기존 필터를 해제하고 실습 시각이 포함된 기간을 설정한다. 먼저 전체 Suricata 그룹을 찾고, 이후 필요한 조건을 더한다.'),
 dq('Q11-01','rule.groups:suricata','suricata 그룹으로 분류된 경보를 조회한다.','Time·agent.name·rule.id·rule.description을 표 열로 추가한다. 행을 펼쳐 data.event_type과 data.alert.signature를 읽는다.'),
 pic('suricata-current','그림 11-3  Suricata 경보 검색'),
 p('결과가 비면 같은 기간의 EVE alert 존재 여부부터 확인한다. 파일에는 있지만 Wazuh에 없으면 localfile·에이전트 연결·디코더·규칙·인덱싱 순서로 점검한다. 현재 검색의 빈 결과를 원전의 탐지 화면으로 대체해 성공으로 기록하지 않는다.'),
 cmd('C11-05','exit\nsudo docker exec -it kt66-siem /bin/bash\nless /var/ossec/ruleset/rules/0475-suricata_rules.xml','ips 셸에서 나와 관리자 서버로 들어간다. Suricata 규칙 파일을 읽는다.','86600은 JSON의 event_type 분류를 받는 부모이며, 86601은 alert를 처리한다. 설치된 86601 레벨은 3이다. 후반 합성 자료에 지정된 레벨과 같다고 가정하지 않는다.',where='kt66-ips에서 exit 후 kt66 Ubuntu VM, 이어 siem'))
page('원전의 탐지 결과를 해석한다',
 p('원전은 별도 공격자 VM에서 nmap 탐색과 스캐너를 흉내 낸 User-Agent의 웹 요청을 보냈다. nmap은 포트와 서비스 상태를 조사하는 도구이고 User-Agent는 요청 프로그램이 보내는 문자열이다. 문자열은 임의로 바꿀 수 있으므로 해당 도구를 실제 사용했다는 증거와 구분한다.'),
 pic('source-signature','그림 11-4  Suricata의 규칙별 네트워크 경보'),
 pic('source-action','그림 11-5  Suricata의 출발지·목적지와 allowed 동작'),
 p('원전 두 행의 출발지는 192.168.0.202, 목적지는 10.20.32.80, alert.action은 allowed다. 이 값은 해당 경보에 기록된 동작이다. 요청이 애플리케이션에서 성공했는지, 파일이나 데이터가 바뀌었는지는 웹 응답과 호스트 증거로 확인한다.'),
 p('data.alert.severity는 Suricata 규칙의 우선순위이며 보통 작은 수가 더 높은 심각도를 뜻한다. Wazuh rule.level은 큰 수를 높은 우선순위로 사용하는 별도 값이다. severity 3을 rule.level 3과 같은 등급으로 읽지 않는다.'))
page('추가 필터와 누락 점검',
 dq('Q11-02','rule.groups:suricata AND\nNOT data.alert.category:"Not Suspicious Traffic"','NOT은 해당 분류와 일치하는 문서를 제외한다. 공백이 있는 값은 큰따옴표로 묶는다.','제외 전후 건수와 제외된 시그니처를 비교한다. category 필드가 없는 경보는 이 NOT 조건을 통과할 수 있다.'),
 dq('Q11-03','rule.groups:suricata AND\nNOT data.alert.category:*','별표(*)를 값 자리에 쓰면 필드 존재를 검색한다. NOT과 결합하여 category가 없는 항목을 확인한다.','필드 누락과 “정상 분류”를 구분한다. 누락이 많으면 원본 EVE와 수집·파싱 구조를 확인한다.'),
 dq('Q11-04','rule.groups:suricata AND\ndata.alert.action:blocked','blocked로 기록된 Suricata 경보를 찾는다.','일치하면 실제 실행 모드·규칙 동작·해당 패킷의 처리 근거를 확인한다. 0건은 차단할 트래픽 부재와 관찰 모드를 구분하여 해석한다.'),
 p('alert.action이 allowed인 경보도 위험한 요청일 수 있다. blocked인 경보도 다른 경로나 후속 요청까지 막았다는 뜻은 아니다. 경보 하나의 동작을 시스템 전체의 결과로 확대하지 않는다.'))
page('네트워크와 호스트 기록을 연결한다',
 dq('Q11-05','data.src_ip:"192.168.0.108" OR\ndata.srcip:"192.168.0.108"','Suricata 출발지 src_ip와 웹·SSH 로그의 srcip를 OR로 묶는다. 주소는 실제 경보에서 읽은 값으로 바꾼다.','같은 시각의 ips·web·bastion 기록을 비교한다. 출발지 주소만 같다는 이유로 모든 행을 같은 요청으로 연결하지 않는다.'),
 table(['연결할 값','대조할 이유'],[['원본 시각·시간대','수집 지연과 순서 오해 방지'],['출발지·목적지 IP와 포트','같은 통신 후보 구분'],['프로토콜·URL·메서드','같은 웹 요청인지 확인'],['flow_id와 센서','동일 Suricata 흐름 내부 연결'],['호스트·프로세스·파일','실제 실행·변경의 후속 근거']],[45,82]),
 p('agent.ip는 Wazuh 에이전트의 주소다. 네트워크 이벤트의 목적지 data.dest_ip와 다를 수 있다. NAT나 프록시가 있으면 원래 주소와 변환된 주소, 관측 지점을 적는다. flow_id는 해당 센서의 EVE 흐름을 묶는 값이며 모든 장비를 관통하는 공통 요청 ID가 아니다.'),
 p('조사 기록에는 “요청 패턴 탐지”, “HTTP 응답”, “호스트 후속 활동”을 각각 적는다. 시간·대상이 맞지 않으면 연결을 보류하고 별도 후보로 남긴다.'))
page('실습 59의 대응과 원상복구',
 p('대상 서비스의 중요도와 실제 영향을 확인한 다음 대응을 정한다. 요청만 탐지되었다면 승인된 스캐너·운영 점검 여부를 확인한다. 비인가 실행이나 파일 변경이 연결되면 자산 담당자와 격리 범위·증거 보존·서비스 복구 순서를 정한다. IP 한 개의 평판만으로 전체 서비스 접근을 차단하지 않는다.'),
 p('읽기 조회의 완료 조건은 센서 실행 모드, EVE 수집 경로, 규칙 식별자, 요청과 호스트의 연결 근거를 기록하는 것이다. 원상복구는 변경한 검색 필터·기간을 되돌리고 관리자 컨테이너에서 exit로 나오는 것이다. 이번 조회에서는 센서 규칙·방화벽·서비스 설정을 바꿀 항목이 없다.'),
 p('별도 승인된 탐색 실습을 수행했다면 생성한 요청의 시각·출발지·대상을 기록하고 발생한 경보를 교육 활동으로 식별한다. 경보를 없애기 위해 센서 로그나 인덱스를 지우지 않는다.'))
page('11.2  실습 60 ATT&CK로 조사 범위를 정한다',
 p('MITRE ATT&CK는 공격자의 행동을 전술과 기법으로 분류한 지식 체계다. 전술은 행동의 목적, 기법은 그 목적을 달성하는 방법을 나타낸다. Wazuh 규칙의 매핑은 탐지 내용을 이 분류와 연결한다.'),
 p('ATT&CK 전술 목록은 사건마다 반드시 같은 순서로 진행하는 절차가 아니다. 한 이벤트에 여러 전술이 붙거나 어떤 경보에는 태그가 없을 수 있다. 태그가 있다는 사실은 실제 공격 성공이나 특정 공격자 집단의 행위를 입증하지 않는다.'),
 dq('Q11-06','rule.mitre.tactic:("Privilege Escalation" OR\n"Credential Access" OR "Persistence" OR\n"Defense Evasion") AND rule.level >= 8','괄호는 네 전술을 하나의 조건으로 묶는다. >=는 8 이상이다. 레벨은 조사 우선순위 필터로 사용한다.','전술·기법 ID·규칙 설명·호스트를 대조한다. 전체 침해 이력이 아니라 선택한 전술과 레벨의 부분집합임을 기록한다.'),
 pic('mitre-current','그림 11-6  전술과 규칙 레벨을 결합한 검색'))
page('MITRE 화면과 원문 경보의 왕복',
 p('메뉴의 **Threat intelligence → MITRE ATT&CK**를 열어 관심 기법을 찾는다. 기법의 설명과 대응 경보를 읽고 Discover에서 원문을 펼친다. rule.mitre.id는 T로 시작하는 기법 번호이고 Windows EventID나 Wazuh rule.id와 다른 번호다.'),
 p('예를 들어 수집 중지 경보에 T1562.001이 연결되어 있으면 보안 도구 중지 가능성을 조사한다. 그러나 10장의 504는 통신 장애에서도 발생한다. 태그를 결론으로 쓰지 말고 서비스·계정·변경 승인을 확인하는 질문으로 바꾼다.'),
 dq('Q11-07','rule.mitre.id:"T1562.001"','선택한 기법 ID를 정확히 조회한다. 앞서 사용한 레벨 필터를 제거한다.','레벨 3인 504·506 같은 상태 경보도 읽는다. 레벨 8 이상 검색에서 빠졌던 원인·복구 이력을 보완한다.'),
 dq('Q11-08','rule.level >= 8 AND NOT rule.mitre.id:*','높은 레벨이지만 MITRE 기법 필드가 없는 문서를 찾는다.','태그 없는 중요 경보를 별도 조사 목록에 남긴다. 매핑이 없다는 사실은 공격과 무관하다는 뜻이 아니다.'),
 p('전술별 집계에서 같은 경보가 두 전술에 포함될 수 있다. 전술 막대의 합을 고유 사건 수로 적지 않는다. 중복을 제거할 때에는 원본 문서의 인덱스·문서 ID 또는 보존한 경보 식별자를 사용한다.'))
page('실습 60의 판단 기록',
 table(['관찰','추가 확인','결론 예'],[['Credential Access 태그','인증 패키지·접근 권한·성공 여부','자격증명 접근 후보, 성공 미확인'],['Persistence 태그','생성 객체·실행·승인 작업','등록 사실 확인, 악성 여부 조사'],['Defense Evasion 태그','중지·삭제 원인과 수집 공백','탐지 공백 확인, 원인 미확정']],[35,50,42]),
 p('선행 조건은 해당 기간에 경보가 있고 규칙 매핑을 읽을 수 있는 것이다. 결과가 없으면 기간·필터를 확인하고 레벨 조건을 제거한 뒤 기법 필드 존재 여부를 확인한다. 특정 ATT&CK 이름만 반복 검색하여 원문 증거를 대신하지 않는다.'),
 p('완료 조건은 관심 기법 한 건을 원문 이벤트와 연결하고, 확인된 사실과 미확인 가설을 분리한 조사 메모다. 원상복구는 검색 필터·기간을 되돌리는 것이며 규칙의 태그나 레벨을 변경하지 않는다.'))
page('11.3  실습 61 일일 관제의 시작',
 p('매일 정해진 시각에 같은 시간대를 확인하면 누락된 검토 구간을 줄일 수 있다. 예를 들어 KST 전일 00:00:00부터 당일 00:00:00 직전까지를 기준 구간으로 삼고, 마지막 검토 종료 시각과 지연 도착 경보를 별도로 기록한다.'),
 image('assets/figures/chapter11/daily.png','그림 11-7  수집 상태와 경보 검토를 함께 수행하는 일일 관제'),
 p('먼저 연결 단절·수집 지연을 확인한다. 다음으로 고위험 경보를 선별하고, 해당 호스트의 낮은 레벨 전후 기록까지 확장한다. 취약점·SCA·Rootcheck 상태는 별도 작업 목록에서 추적한다. 발생 경보와 현재 노출 상태를 한 건수로 합치지 않는다.'),
 dq('Q11-09','rule.level >= 12 AND NOT\nrule.groups:(sca OR vulnerability-detector OR rootcheck)','레벨 12 이상에서 세 상태 점검 그룹을 제외한 관제 출발점이다. 제외된 그룹도 별도 목록에서 계속 검토한다.','Time·agent.name·rule.id·rule.description을 읽고 각 행을 펼친다. 출발지 필드가 없는 경보도 목록에 남긴다.'))
page('고위험 목록을 조사 항목으로 바꾼다',
 pic('daily-current','그림 11-8  일일 고위험 경보 검색'),
 p('첫 경보에서 자산·계정·프로세스·명령·대상 파일·네트워크 주소 중 실제 존재하는 값을 적는다. 같은 규칙이 반복되더라도 요청과 계정이 다르면 별도 후보가 될 수 있다. 동일 원본의 중복 수집과 새로운 반복 행위도 구분한다.'),
 table(['기록','필수 내용'],[['조회 범위','시작·끝 시각, KST, 데이터 보기·검색식'],['대상','에이전트, 원본 컴퓨터, 계정·프로세스'],['증거','원본 시각, EventID·경보 ID, 경로·해시'],['판단','확인 사실, 승인 작업, 미확인 영향'],['후속 조치','담당자, 기한, 보존·확인할 자료'],['상태','신규·조사 중·조치 중·종결과 근거']],[31,96]),
 p('“고위험 10건”만 적으면 다음 담당자가 무엇을 해야 할지 알기 어렵다. 자산별로 가장 먼저 확인할 행동을 하나씩 지정한다. 이미 조치한 사건이면 중복 발생인지 재발인지 판단할 근거를 남긴다.'))
page('저장한 검색과 자동 알림을 구분한다',
 p('Discover의 **Save**를 누르고 “V2 일일 고위험 검토”처럼 용도를 알 수 있는 이름을 입력한다. 저장한 검색은 조회 조건과 열 구성을 다시 여는 기능이다. 시간 범위 저장 여부를 확인하여 오래된 절대 기간을 매일 재사용하지 않게 한다. 저장 후 **Open**에서 다시 열어 조건을 확인한다.'),
 p('예약 실행과 알림 전송은 별도 기능이다. 저장 검색 자체가 주기적으로 담당자에게 알림을 보내지는 않는다. 예약 관제에는 실행 주기·조회 창·중복 처리·수신 대상·실패 감시를 별도로 설계한다. 실제 통지 수신과 재시도 정책을 확인한 뒤 운영한다.'),
 p('지연 도착을 고려하여 조회 구간을 조금 겹치면 같은 경보를 다시 만날 수 있다. 인덱스와 문서 ID를 함께 보존하여 중복 검토를 식별하고, 새로 도착한 경보는 원본 시각과 최초 검토 시각을 구분한다. 첫 500개 화면만 보고 전체 검토를 끝내지 않는다.'),
 p('실습용으로 새 저장 검색을 만들었다면 이름·소유자·용도를 기록한다. 원상복구가 필요할 때에는 자신의 실습용 저장 검색만 대시보드 관리 화면에서 확인하여 정리한다. 원본 경보 인덱스와 다른 사람의 저장 객체는 정리 대상에 포함하지 않는다.'))
page('관제 마감과 다음 분석',
 p('완료 조건은 조회 구간의 수집 상태 확인, 고위험 후보의 증거와 담당자 지정, 제외한 상태 점검 목록의 추적이다. 검색 0건이어도 수집 공백이 있으면 “특이 사항 없음”으로 마감하지 않는다. 수집이 정상이고 검토 범위에서 해당 조건의 경보가 없었다고 기록한다.'),
 p('단기 관제는 즉시 확인할 대상을 찾고, 장기 분석은 반복·분산·시간대의 변화를 찾는다. 다음 장에서는 같은 출발지와 여러 센서의 필드를 연결하고, 집계 분모와 누락을 확인하여 장기 조사 목록을 만든다.'),
 h('확인 문제와 해설'),
 p('allowed와 HTTP 200이 함께 있으면 침투 성공인가? 엔진의 해당 동작과 HTTP 응답을 확인한 것이다. 권한 획득·데이터 접근·프로세스 실행 같은 목적 달성의 증거가 더 필요하다.'),
 p('레벨 12 이상만 보면 충분한가? 중지·시작, 정상처럼 보이는 로그인 성공, sudo 등 낮은 레벨의 원인·후속 기록이 빠질 수 있다. 후보를 찾은 뒤 호스트·계정·시각으로 확장한다.'))
page('참고자료',
 link('Module 01 — 실습 59~61, 슬라이드 602~626','https://docs.google.com/presentation/d/1o0H_2DDHBp8p2HvlSnEPbx6-jdURYzew'),
 link('Suricata 6.0.4 — EVE JSON','https://docs.suricata.io/en/suricata-6.0.4/output/eve/eve-json-output.html'),
 link('Suricata 6.0.4 — 인라인 모드','https://docs.suricata.io/en/suricata-6.0.4/setting-up-ipsinline-for-linux.html'),
 link('Wazuh 4.10.0 — Suricata 규칙','https://github.com/wazuh/wazuh/blob/v4.10.0/ruleset/rules/0475-suricata_rules.xml'),
 link('MITRE ATT&CK — Enterprise tactics','https://attack.mitre.org/tactics/enterprise/'),
 link('OpenSearch — Dashboards Query Language','https://docs.opensearch.org/2.13/dashboards/dql/'))
for pg in pages:
 for b in pg['blocks']:
  if b['type']=='image' and any(n in b['path'] for n in ('mitre-current','daily-current')):b['width_mm']=90
save(11,'11장 네트워크 경보와 일일 관제',pages,'Module01 실습59~61. 현재 읽기 조회와 원전 탐지 기록을 구분. 신규 공격·방화벽 변경·알림 전송 미실행. editorial/chapter11-review.md 참조.')
