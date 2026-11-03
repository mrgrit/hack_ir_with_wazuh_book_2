"""2권 부록: 각 장과 Module01 pp722–726의 필드·검색·점검표."""
from chapter_authoring import *
pages=[]
def page(t,*b):pages.append({'title':t,'kind':'body','level':'section','break':False,'blocks':list(b)})
def dq(i,t,w,r):return query(i,t,w,r,index='wazuh-alerts-*')
page('부록  필드·검색·점검표',
 p('필드 이름을 찾을 때에는 원본 로그의 종류와 실행 위치부터 정한다. 이 부록은 각 장의 조사 대상을 빠르게 찾고 입력·응답·판단·원상복구를 기록하기 위한 참고표다. 명령 전체를 일괄 실행하지 않고 해당 장의 선행 조건과 함께 사용한다.'),
 table(['장','조사 대상','Module 01 실습'],[['1','Windows 수집 준비','환경·채널·원본 대조'],['2','로그온 실패·잠금·RDP','31~34'],['3','자격증명·계정·권한','35~37, 50'],['4','서비스·작업·Run·osquery','39, 40, 44, 63'],['5','PowerShell·정상 프로그램 악용','41, 42, 45, 46'],['6','LSASS 접근·외부 통신','43, 47, 48'],['7','로그 삭제·Defender','38, 49'],['8','취약점·SCA','51~53'],['9','Rootcheck·파일 판정','54~56'],['10','단절·자동 대응','57, 58'],['11','Suricata·MITRE·일일 관제','59~61'],['12·13','장기 집계·시간선·평가','후반 분석 자료']],[16,67,44]),
 p('1권은 실습 01~30·62, 2권은 31~61·63으로 총 32개 실습을 다룬다. 후반 장기 분석도 Module 01 자료다. Module 02·03의 실습을 포함한 것으로 계산하지 않는다.'))
page('A  실행 위치와 주소',
 table(['위치','대상과 용도'],[['Windows PC','브라우저, SSH 클라이언트, DOCX 검토'],['kt66 Ubuntu VM','192.168.0.107 · Docker 호스트'],['별도 공격자 VM','192.168.0.108 · 앞 장의 제한된 요청 실습'],['kt66-siem','Wazuh 관리자 설정·디코더·규칙'],['kt66-wazuh-indexer','검색 인덱스·집계'],['kt66-bastion / web / ips','각 컨테이너의 원본·에이전트 로그'],['Windows 실습 게스트','KT66-WIN-01 · windows-user 에이전트']],[47,80]),
 p('주소는 이번 환경의 예시다. 별도 공격자 VM과 kt66 내부 attacker 컨테이너를 구분한다. 2권의 일부 Windows 네트워크 기록에는 NAT·라우팅으로 10.20.30.202가 보인다. 브라우저가 사용하는 VM 주소와 이벤트에 기록된 출발지는 관측 지점에 따라 다를 수 있다.'),
 p('Wazuh 대시보드는 HTTPS 5601이다. Windows PC에서 VM 주소로 접속한다. 에이전트 ID는 등록 순서에 따라 달라지므로 각 장의 예시 번호를 외워 대상 선택에 사용하지 않는다. 컴퓨터·채널·ID·이름을 현재 목록과 대조한다.'),
 p('컨테이너에서는 sudo docker exec -it 이름 /bin/bash로 연 대화형 셸을 사용한다. 작업 후 exit로 호스트에 돌아온다. 같은 /var/ossec 경로라도 관리자와 에이전트에서 내용과 역할이 다르다.'))
page('B  이벤트 번호와 식별자',
 table(['필드','뜻'],[['data.win.system.eventID','Windows 공급자·채널의 사건 종류'],['data.win.system.eventRecordID','해당 컴퓨터·채널의 개별 기록 번호'],['data.win.system.systemTime','Windows 원본 이벤트 시각'],['timestamp','Wazuh 문서의 시각'],['rule.id / rule.level','Wazuh 규칙 번호 / 경보 우선순위'],['id','Wazuh 경보 식별값'],['_index / _id','인덱스와 저장 문서 식별자'],['rule.mitre.id','ATT&CK 기법 식별자']],[62,65]),
 p('서로 다른 채널의 EventID 1은 다른 의미일 수 있다. EventRecordID도 채널·컴퓨터와 함께 보존한다. 원본 시각, 수집 시각, 화면의 시간대를 대조하면 지연·시간대 차이를 사건 순서로 오인하는 일을 줄일 수 있다.'),
 p('Windows 대상 계정은 targetUserName, 행위 주체는 subjectUserName인 경우가 많지만 이벤트마다 메시지와 XML을 읽는다. 4740처럼 화면 메시지와 XML 요소의 해석에 주의가 필요한 사례는 2장의 원본 대조를 따른다.'))
page('Windows 인증·계정 이벤트 찾아보기',
 table(['채널·번호','관찰 내용','관련 장'],[['Security 4625','로그온 실패·Status/SubStatus','2'],['Security 4740','계정 잠금·대상 계정','2'],['Security 4624','로그온 성공·유형·계정·주소','2·3'],['Security 4648','명시적 자격증명 사용','3'],['Security 4720','계정 생성','3'],['Security 4732 / 4728','로컬 / 글로벌 그룹 구성원 추가','3'],['Security 4719','시스템 감사 정책 변경','3'],['Security 4688','프로세스 생성·명령줄','1·5']],[47,61,19]),
 p('4624의 유형 3은 네트워크, 10은 원격 대화형, 9는 NewCredentials 로그온이다. NTLM 또는 유형 9만으로 Pass-the-Hash를 확정하지 않는다. 정상 자격증명 사용과 실제 해시 사용을 구분한다.'),
 p('권한·계정 변경은 등록 사실과 승인 여부, 후속 사용을 함께 확인한다. 계정 이름만으로 계정 소유자가 실제 명령을 수행했다고 단정하지 않는다.'))
page('프로세스·지속화·보호 이벤트 찾아보기',
 table(['채널·번호','관찰 내용','관련 장'],[['System 7045 / Security 4697','서비스 등록','4'],['Security 4698','예약 작업 생성','4'],['Sysmon 1','프로세스 생성·부모·명령줄','5'],['Sysmon 3 / 22','네트워크 연결 / DNS 질의','6'],['Sysmon 10','다른 프로세스 접근','6'],['Sysmon 13','레지스트리 값 설정','4'],['PowerShell Operational 4104','스크립트 블록 내용','5'],['Security 1102 / System 104','로그 삭제 관련 이벤트','7'],['Defender Operational 1116 / 1117','악성 요소 탐지 / 조치','7'],['Defender Operational 5007','설정 변경','7']],[60,50,17]),
 p('표의 Sysmon 채널은 Microsoft-Windows-Sysmon/Operational, PowerShell은 Microsoft-Windows-PowerShell/Operational, Defender는 Microsoft-Windows-Windows Defender/Operational이다. 짧은 표기만 보고 Security 채널에서 해당 번호를 찾지 않는다.'),
 p('LSASS 접근은 접근 권한과 프로세스 관계를 확인하는 단서다. 덤프 파일 생성·자격증명 탈취와 구분한다. 1117도 조치 메시지와 오류·현재 상태를 확인해야 한다. 탐지·차단·격리·복구를 한 단어로 합치지 않는다.'))
page('C  위협 묶음별 표 열',
 table(['종류','우선 추가할 필드'],[['공통','timestamp · agent.name · rule.id\nrule.level · rule.description'],['웹','data.srcip · data.protocol\ndata.url · data.id'],['Linux 인증','data.srcip · data.srcuser · data.dstuser\npredecoder.hostname · full_log'],['Windows','data.win.system.eventID\ndata.win.eventdata.targetUserName\ndata.win.eventdata.ipAddress'],['프로세스','data.win.eventdata.image\ndata.win.eventdata.commandLine\ndata.win.eventdata.parentImage'],['Suricata','data.src_ip · data.dest_ip\ndata.alert.signature · data.alert.action'],['파일','syscheck.path · syscheck.event\nsyscheck.sha256_after']],[31,96]),
 p('한 표에 모든 필드를 넣으면 가로 폭만 넓어진다. 기본 목록에서 시간·대상·설명을 읽고 행을 펼쳐 원문 필드를 확인한다. 필요한 묶음의 열을 추가한 뒤 저장 검색으로 보존한다. 값이 비어 있으면 필드가 없는 문서인지 다른 필드 이름을 쓰는지 원본을 읽는다.'))
page('출발지와 자동 대응 필드',
 table(['문서 종류','주소 필드'],[['웹·SSH 등','data.srcip'],['Suricata','data.src_ip / data.dest_ip'],['Windows 인증','data.win.eventdata.ipAddress'],['firewall-drop 대응 JSON','data.parameters.alert.data.srcip'],['에이전트 자체 주소','agent.ip']],[49,78]),
 p('agent.ip를 통신 출발지로 대신 사용하지 않는다. 자동 대응 경보에는 원인 경보가 parameters.alert 안에 들어 있다. 바깥 id와 안쪽 parameters.alert.id를 구분하고 규칙·원문·대상·시각까지 대조한다. 10장처럼 중첩된 ID와 인덱스 문서가 일치하지 않는 사례도 조사 기록에 남긴다.'),
 dq('QA-01','data.srcip:"192.168.0.108" OR\ndata.src_ip:"192.168.0.108" OR\ndata.win.eventdata.ipAddress:"192.168.0.108"','한 주소를 여러 로그 종류의 출발지 필드에서 찾는다. 주소는 원문에서 읽은 값으로 바꾼다.','원본 시각·관측 지점·NAT를 대조한다. 같은 IP라는 이유만으로 같은 사람이나 세션으로 귀속하지 않는다.'))
page('D  DQL 기본형',
 table(['표현','사용 목적'],[['필드:값','해당 필드의 값 검색'],['"공백 있는 값"','여러 단어를 한 값으로 지정'],['A AND B','두 조건을 모두 만족'],['A OR B','둘 중 하나 이상 만족'],['NOT A','A 조건에 해당하는 문서 제외'],['(A OR B) AND C','추가 조건의 적용 범위를 고정'],['필드:*','필드에 값이 있는 문서'],['rule.level >= 8','숫자 레벨의 범위 조건']],[58,69]),
 p('keyword는 전체 값을 기준으로, text는 분석기를 거친 토큰을 기준으로 검색한다. 실제 자료형·분석기는 인덱스 매핑에서 확인한다. rule.level은 숫자, timestamp는 날짜처럼 같은 이름 영역에서도 타입이 다를 수 있다. full_log의 모든 기호가 무조건 무시된다고 가정하지 않는다.'),
 p('범위 검색은 숫자뿐 아니라 날짜에도 사용한다. 문자열의 범위는 숫자 크기 비교와 다를 수 있으므로 EventID·HTTP 상태처럼 코드인 값은 명시적으로 나열한다. 앞쪽 별표 검색은 비용이 커질 수 있어 기간·호스트를 먼저 좁힌다.'))
page('검색 예와 오류 점검',
 dq('QA-02','agent.name:"windows-user" AND\ndata.win.system.channel:"Security" AND\ndata.win.system.eventID:("4624" OR "4625")','대상 에이전트·채널·사건 종류를 함께 지정한다.','성공과 실패를 계정·유형·시각으로 비교한다. rule.id 4624를 찾는 검색과 다르다.'),
 dq('QA-03','rule.id:(503 OR 504 OR 506 OR 651 OR 652)','에이전트 상태와 자동 대응 이력을 함께 살핀다.','대상·시각·원인 경보를 구분한다. 상태 경보와 차단 효과를 같은 결과로 해석하지 않는다.'),
 dq('QA-04','synthetic.flag:true AND\n(data.srcip:"185.220.158.180" OR\n data.src_ip:"185.220.158.180")','합성 조건을 두 출발지 필드 전체에 적용한다.','12장의 기간·데이터 준비 상태를 먼저 확인한다. 교육용 주소와 평판을 실제 위협 정보로 사용하지 않는다.'),
 p('구문 오류이면 괄호·따옴표·필드명을 먼저 읽는다. 정상 응답의 0건이면 기간·고정 필터·인덱스·원본 존재·수집 상태 순서로 확인한다. 원하는 결과가 나올 때까지 임의로 조건을 제거한 검색은 원래 질문의 답과 구분하여 기록한다.'))
page('E  로그·설정 위치',
 table(['실행 위치','경로와 용도'],[['Linux 에이전트','/var/ossec/etc/ossec.conf\n수집·검사 설정'],['Linux 에이전트·관리자 각각','/var/ossec/logs/ossec.log\n자체 실행·오류 기록'],['자동 대응 대상 에이전트','/var/ossec/logs/active-responses.log\n대응 입력·실행 기록'],['kt66-ips','/var/log/suricata/eve.json\n네트워크 원본 이벤트'],['kt66-siem','/var/ossec/ruleset/rules\n기본 규칙'],['kt66-siem','/var/ossec/etc/rules\n로컬 규칙'],['kt66-siem','/var/ossec/etc/decoders\n로컬 디코더']],[48,79]),
 p('기본 규칙·디코더를 읽을 때에는 설치 버전과 부모·하위 관계를 함께 기록한다. decoder.name은 파싱 정의, predecoder.program_name은 원본 헤더에서 읽은 프로그램 이름, rule.id는 탐지 분류다. 문자열이 같아도 역할이 다르다.'),
 p('취약점 현재 상태, SCA 결과, 경보 이력은 다른 데이터일 수 있다. 현재 상태 화면의 0건과 alerts 검색의 0건을 같은 의미로 기록하지 않는다. 8·9장의 기능별 점검 순서를 따른다.'))
page('F  수집 장애 점검표',
 image('assets/figures/appendix/check-path.png','그림 A-1  원본부터 대시보드까지의 장애 확인 순서'),
 table(['확인 지점','질문'],[['원본','해당 컴퓨터·채널·파일에 기록이 있는가'],['생성 정책','감사·Sysmon·Script Block 필터가 맞는가'],['에이전트','실행·연결·localfile·읽기 권한이 맞는가'],['관리자','디코더·규칙·저장 기준·큐 오류는 없는가'],['인덱서','적재 오류·자료형 충돌·보존 만료는 없는가'],['화면','데이터 보기·기간·시간대·필터가 맞는가']],[30,97]),
 p('각 지점의 확인 시각과 근거를 남긴다. 관리자와 에이전트가 Active라고 특정 채널 수집까지 정상인 것은 아니다. 원본이 없을 때 수집기를 재설치하는 식으로 다음 단계부터 고치지 않는다.'))
page('G  조사 기록 양식',
 p('아래 항목을 복사하여 사건마다 작성한다. examples/appendix/investigation-template.md에 같은 양식이 있다. 다른 담당자가 같은 조건으로 검색하고 원문을 찾을 수 있을 정도로 구체적으로 적는다.'),
 table(['항목','작성할 값'],[['조사 범위','시작·끝·시간대, 대상·계정, 데이터 보기'],['입력·응답','실행 위치, 입력, 결과 코드·본문·상태'],['원본 식별','컴퓨터·채널·EventID·RecordID 또는 파일·시각'],['수집 식별','agent·rule·경보 id·인덱스·문서 ID'],['연결 근거','IP·PID·GUID·세션·TTY·계정·시간차'],['확인 사실','기록으로 입증한 동작과 영향'],['미확인 가설','추가 자료·반증 가능성·수집 공백'],['조치','담당자·승인 범위·기한·영향'],['검증·종결','재조회·서비스·보호 상태·원상복구']],[31,96]),
 p('기존 캡처와 현재 조회, 예상 결과와 실행 결과를 구분한다. 캡처의 규칙 설명만 전사하지 않고 핵심 필드가 원문의 어떤 내용인지 연결한다. 조사 결과를 “성공” 하나로 축약하지 않는다.'))
page('H  원상복구 점검표',
 table(['대상','사전·사후 비교'],[['계정·그룹','활성·잠금·구성원·임시 계정'],['서비스·작업','이름·경로·실행 계정·시작 유형·실행 결과'],['파일·레지스트리','정확한 경로·값·해시·기존 객체'],['보호 기능','정책·실시간 보호·감사·센서 상태'],['방화벽·자동 대응','추가한 규칙·만료·해제·정상 경로'],['관제 화면','필터·기간·자신의 저장 검색'],['합성 자료','원본 파일·실행 식별자·보존·정리 범위']],[44,83]),
 p('실습 전에 있던 객체와 이번에 만든 객체를 나누어 기록한다. 원상복구는 이번 변경의 정확한 대상에 적용한다. 이벤트 로그 전체 삭제, 방화벽 전체 초기화, synthetic.flag:true 전체 일괄 삭제를 일반 정리 방법으로 사용하지 않는다.'),
 p('완료 조건은 변경 대상의 사후 상태, 서비스 접근, 보호·수집 상태의 확인이다. 실패하면 남은 변경과 영향, 추가 담당자를 기록한다. 읽기 조회만 했다면 설정 복구를 위한 불필요한 재시작이나 초기화를 하지 않는다.'))
page('I  예제 파일과 재검토',
 p('examples/chapter01부터 chapter13까지 각 장의 복사용 입력과 manifest.json이 있다. C는 셸·PowerShell 명령, Q는 DQL, 후반 D는 Dev Tools 입력이다. 12·13장의 나뉜 DSL은 ip-profile.http와 hourly-risk.http 완성본을 사용한다. 전체 예제 파일을 한꺼번에 실행하지 않는다.'),
 p('원고의 명령 번호와 실행 위치를 먼저 확인한다. 예시 주소·계정·GUID·시각은 자신의 기록에서 읽은 값으로 바꾼다. 실패 결과가 나오면 다음 명령으로 넘어가기 전에 선행 조건과 실패 시 확인 절차를 수행한다.'),
 p('각 장의 검증·촬영 범위는 저장소 editorial의 chapterNN-review.md에 있다. 초안 전체를 교정할 때에는 문장뿐 아니라 표·캡션·복사용 파일·현재 상태와 원전의 구분을 함께 확인한다. 장별 DOCX를 교정본의 단위로 유지한다.'))
page('참고자료',
 link('2권 집필 저장소','https://github.com/mrgrit/hack_ir_with_wazuh_book_2'),
 link('Module 01 — 필드·검색 팁, 슬라이드 722~726','https://docs.google.com/presentation/d/1o0H_2DDHBp8p2HvlSnEPbx6-jdURYzew'),
 link('Microsoft Learn — Sysmon','https://learn.microsoft.com/sysinternals/downloads/sysmon'),
 link('OpenSearch — DQL','https://docs.opensearch.org/2.13/dashboards/dql/'),
 link('OpenSearch — Field capabilities','https://docs.opensearch.org/latest/api-reference/search-apis/field-caps/'))
pages[-1]['break']=True
from revise_analysis import revise
revise('appendix',pages)
data={'title':'부록 필드·검색·점검표','series':'해킹·침해대응 실무 with Wazuh 2권','comments':'각 장 및 Module01 pp722~726 대응 부록. 검증 범위 editorial/appendix-review.md 및 editorial/analysis-revision-review.md.','pages':pages}
(ROOT/'manuscript/volume02-appendix.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
dest=ROOT/'examples/appendix';dest.mkdir(parents=True,exist_ok=True);manifest=[]
for pg in pages:
 for b in pg['blocks']:
  if b['type']=='query':
   name=b['id']+'.dql';(dest/name).write_text(b['text']+'\n',encoding='utf8')
   manifest.append({'id':b['id'],'file':name,'where':b['where'],'section':pg['title'],'input':b['text']})
(dest/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('appendix',len(pages),'sections',len(manifest),'inputs')
