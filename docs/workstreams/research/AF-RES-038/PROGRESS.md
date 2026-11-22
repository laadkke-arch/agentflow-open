# AF-RES-038 커밋·검증 진행표

| 묶음 | 원격 SHA | 확인 |
| --- | --- | --- |
| ① 표집·종점·사전 합격 기준 | `7b977101c53730a5d6f5028a4ac540e045a6f84e` | GitHub ref 갱신 및 고정 SHA의 SCOPE 재독. 로컬 동일 tree 확인 후 remote commit으로 동기화. |
| ② 최초판·대안·참가자 자료 | `dfe65f444631d22e952d8c2d198767939ea6dd9d` | 원장106행/산입34개, 후보40행, 실제 참가자20파일. B/C11개 URL/순서/판 일치, 인증 없는 HTTP200 11/11. 별도 기대 판독 전 자료 고정. |
| ③a 채점 전 기대·가림 입력 봉인 | `a9589eb1ed899da83230e5c6a3ffa30123b7d5f2` | 루브릭12행, 예시12개/36셀, 익명 입력 해시4fbf39de… 고정 후 별도 문맥 판독 요청. 작성자 기존 N08 R2 이견도 봉인. |
| ③b 최초 판독·이견·명료화 입력 | `cbf1c3b4a81799370e440b055b03001c4a2e66fe` | 전체12/12 일치, 요구셀35/36. N08 R2의 partial/fail/pass를 보존하고 명료화 입력 고정. 원판 재독·보수적33원문·상태12예시·전송 줄바꿈 정정 기록. |
| ③c 대상 재독·결측 의미 검토 | `a0c1179453c3dd80bbb3ea75fb6b73d47a0a0734` | 같은 AI의 N08 3예시 재독, R2 한 셀만pass→fail. 별도 측정 문맥의 상태12개 판독과 규칙 출력 비교. 사람0·미실시 API 재현 명령 전달. |

최초 배정 통합은 `de544231bc72fa6f2ddb3e91f9c0e8d16a0d1f62`다. 요청된 `python -B -m workbench.session start af-res-038 --allow docs/workstreams/research/AF-RES-038/ --output docs/workstreams/research/AF-RES-038/manifest.json --dependency work/research-af-res-021=29049a5f15b6ef7cd7431f59a059598db6f5d857 --dependency work/research-af-res-034=f6dc9b8873b049f1eb4f8977ce3408ed057df1f7 --fetch`는 종료0, freshness_at_start=remote_checked였다. 원격 읽기는 공개 Git으로 성공했지만 셸 push는 자격증명 부재로 종료128이었다. 인증된 GitHub 연결로 정상 tree·commit·조건부 ref 갱신을 사용했다. 권한·계정·브랜치 보호를 변경하지 않았다.

세 조사 갈래(pandas / NumPy / 디자인·교육 방법)를 분담하고 root가 통합한다. 분담은 같은 모델 계열 AI 작업이며 외부 사람 독립 검토가 아니다. 별도 문맥 판독은 작성자료를 고정한 뒤 별도로 실시하고 실제 입력·판독·불일치를 보존한다.
