# 2권 REV01 복사용 입력과 보존 기록

교정 원고는 [manuscript/REV01](../../manuscript/REV01/README.md)에 있다. 이 디렉터리의 입력은 해당 장의 선행 조건·실행 위치·확인 결과·원상복구와 함께 한 블록씩 사용한다.

- [전체 입력 색인](input-index.csv): 1~13장과 부록의 C·Q·D 입력 337개.
- [보존 기록](records/README.md): 출처·SHA-256·JSON 위치가 있는 로컬 필드 발췌본.
- [부록 입력](appendix/README.md): 로컬 자료 읽기 CA-01~CA-04와 기존 DQL.
- [ATT&CK 조사 범위](attack-coverage.csv): v16.1 기준 기법·증거·관측 한계.
- [탐지 개선 설계](detection-design.csv): 각 장의 가설·필드·정상 반례·검사 기록.

입력 파일은 실행 위치별로 분리되어 있다. `.txt`는 Bash·PowerShell 등을 본문과 대조하고, `.dql`은 Discover, `.http`는 Dev Tools에서 사용한다. 모든 파일을 일괄 실행하지 않는다.

이번 교정의 실제 실행 확인은 로컬 읽기 CA-01~CA-04와 발췌본 해시 검사다. 기존 공격·수집·규칙 적용을 다시 시험한 것으로 해석하지 않는다. 9장의 별도 로그 JSON과 90일 합성 원자료는 제공되지 않는다. 저장 화면·실제 보존 기록·가정값 계산을 구분한다.

로컬 검사:

```powershell
powershell -NoProfile -File tools/check_rev01_offline.ps1
```

검사는 저장소 파일을 읽고 기대 필드와 해시를 대조한다. VM·Wazuh에 접속하거나 설정을 바꾸지 않는다.
