# 2권 REV01 교정본

1~13장과 부록·참고문헌을 순차 교정했다. 장별 DOCX 15개, 현재 Word 렌더 기준 합계 **492쪽**이다. 합본은 만들지 않았다. 쪽수는 설치 글꼴·Word 버전에 따라 달라질 수 있다.

| 문서 | 쪽 | 편집 원본 |
|---|---:|---|
| [1장 · Windows 실습 환경과 로그 수집](volume02-chapter01.docx) | 33 | [JSON](volume02-chapter01.json) |
| [2장 · 로그온 실패와 원격 접속](volume02-chapter02.docx) | 40 | [JSON](volume02-chapter02.json) |
| [3장 · 자격증명과 계정 권한의 변화](volume02-chapter03.docx) | 41 | [JSON](volume02-chapter03.json) |
| [4장 · 서비스와 작업을 이용한 지속화](volume02-chapter04.docx) | 38 | [JSON](volume02-chapter04.json) |
| [5장 · PowerShell과 정상 프로그램 악용](volume02-chapter05.docx) | 36 | [JSON](volume02-chapter05.json) |
| [6장 자격증명 접근과 외부 통신](volume02-chapter06.docx) | 45 | [JSON](volume02-chapter06.json) |
| [7장 로그 삭제와 보호 기능의 대응](volume02-chapter07.docx) | 35 | [JSON](volume02-chapter07.json) |
| [8장 · 취약점과 보안 설정의 우선순위](volume02-chapter08.docx) | 36 | [JSON](volume02-chapter08.json) |
| [9장 호스트 이상과 파일 판정](volume02-chapter09.docx) | 41 | [JSON](volume02-chapter09.json) |
| [10장 수집 장애와 자동 대응](volume02-chapter10.docx) | 22 | [JSON](volume02-chapter10.json) |
| [11장 네트워크 경보와 일일 관제](volume02-chapter11.docx) | 22 | [JSON](volume02-chapter11.json) |
| [12장 장기 로그의 피벗과 집계](volume02-chapter12.docx) | 29 | [JSON](volume02-chapter12.json) |
| [13장 시간 흐름과 위험도 평가](volume02-chapter13.docx) | 25 | [JSON](volume02-chapter13.json) |
| [부록 필드·검색·점검표](volume02-appendix.docx) | 37 | [JSON](volume02-appendix.json) |
| [참고문헌](volume02-references.docx) | 12 | [JSON](volume02-references.json) |

원본은 이 디렉터리의 **JSON**이다. DOCX에서 검토한 수정은 JSON에도 반영한 뒤 재생성한다. 원래 `manuscript/volume02-*.json`과 이 교정본을 혼용하지 않는다.

- [복사용 입력 337개·보존 기록](../../examples/rev01/README.md)
- [교정 내용과 검증 한계](../../editorial/REV01/review.md)
- [장별 산출물 해시·쪽수](../../editorial/REV01/output-manifest.json)
- [전체 조판 검사](../../editorial/REV01/visual-review.json)

재생성에는 Python의 python-docx·Pillow와 부크크 명조 Light·부크크 고딕 Light·Consolas가 필요하다. 고정된 부크크 B5 원본과 REV01 자산을 사용한다.

```powershell
python tools/build_rev01.py
python tools/check_rev01.py
powershell -NoProfile -File tools/check_rev01_offline.ps1
```

Windows Word를 설치한 저자 환경에서는 다음 명령으로 임시 렌더를 검사한다. pypdfium2와 pypdf가 필요하다. `build`의 PDF·PNG는 검토용이며 배포하지 않는다.

```powershell
powershell -NoProfile -File tools/render_rev01.ps1
python tools/check_rev01_render.py
python tools/check_rev01_text.py
```

최초 이관용 prepare·polish·package 도구를 다시 실행하면 후속 수동 교정이 유지되지 않는다. 일반 수정은 최종 JSON → build_rev01.py 순서로 진행한다.
