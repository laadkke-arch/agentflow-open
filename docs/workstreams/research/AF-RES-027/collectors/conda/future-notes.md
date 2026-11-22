# conda-forge A 후속 조사 인계 메모

## 실행과 원장

- A 전체 원격 봉인: `1714a55a529c7da42596ac0779d398f3aacf97c3`. 후속 조사 시작:2026-11-22T05:06:31Z.
- 원문 열람 구간:2026-11-22T05:06:31Z–05:27:00Z. 이후는 정리·검산이다. 사람의 해석 시간을 따로 측정한 것은 아니다.
- frozen historical/frame/sources/search-log/historical-seal 파일은 수정하지 않았다. 후속 결과로 사례를 교체하지 않았다.
- upstream.json, chains.json, verdicts.json은 각각 A-C01~06의6행. future-sources.json은 C-F01~71이다.
- future-api-receipts.json에는6개 공식 Anaconda release 응답의 artifact별 upload_time·플랫폼·의존성·조회 UTC·응답 해시가 있다. setuptools44의 플랫폼별 조회는 C-F66에 남겼다.
- 같은 편집의 여러 렌더링·release metadata·창 말 대조는 보수적으로 최소수에서 제외했다. 미래 원장만으로 상류/후속 최소수는 충분하지만 독립 사건 수와 다르다.

## 여섯 참조

| 참조 | 관측된 결과 | 한계 |
| --- | --- | --- |
| A-C01 Dask→Python3.6 | AppVeyor 경로가 Actions의 환경3.6으로 이어진다. 365일 창 말에도3.6. 그 뒤2021-03-09에>=3.7 지원정책으로 바꾼다. | 소스 목적 유지이며 과거 시험 성공은 미확인. 버전 핀을 역사 재현 의도로 올리지 않는다. |
| A-C02 JupyterLab→Sphinx | conda→pip→conda로 이동하면서>=1.8 유지.2.4 recipe는 Python3.5와 문서 entrypoint 유지. | 창 말만 보면 중간 이행을 놓친다. RTD 실제 배포·테마 조합 성공은 미확인. |
| A-C03 Napari→setuptools | Python3 CI의 도구가 pip/tox 이행에도 남는다.45의Python2 배제는 원래 Python3.6/3.7 목적과 다르다. | 일반적인 호환성 파괴를 선택 소비자의 실패로 전이하지 않는다. 최초 후계44와45 비교를 구별한다. |
| A-C04 Pandas→NumPy | 같은 환경의 문서 빌드가1.19/Matplotlib 경고로 실패했다는 직접 보고 후<1.19 pin. rc0·안정판에 포함되고 이후 unpin. | 정확 실패 artifact·CI 로그·문서 서버 배포·효과 미확인. 모든 NumPy 사용의 실패가 아니다. |
| A-C05 scikit-image→SciPy | scipy/scipy-tests 출력이 T0 전에 공존했고 ndimage 출력 유지. 후속1.11.2 하한은 새 sparse-array 사용 PR에 속한다. | 옛 Gaussian 호출 실패 미확인. 다른 기능의 하한 변경으로 지연을 계산하지 않는다. |
| A-C06 Spyder→applaunchservices | 누락 의존성 수정 뒤 conda.txt→main.yml→macos.yml을 거쳐0.3 하한으로 올려v5.3.2에 포함한다. | 최초 실패는 상류 수정 전이다. 옛>=0.1.7도0.3을 허용하므로 하한 수정일이 모든 사용자 정상화일은 아니다. 계보가 겹친다. |

소스상 목적 유지3행, 특정 용도 부적합의 직접 보고2행, 보류1행이다. 실제 실행을 통과한 참조 수는 **미확인**이다. 이 실행에서 환경을 설치하거나 시험하지 않았다. 실제 오추천 피해는 전부 미확인이다. Spyder의 개발자 실행 오류·plugin 검사 실패 보고를 특정 옛 참조가 초래한 오추천 피해로 확대하지 않는다.

## Pandas 목적과 날짜 보강

A-C04 최초 봉인은 개발환경/NumPy 의존성 목적이었다. 봉인 뒤 **같은2019 SHA**에서 문서 용도까지 연결했다(C-F53; C-S04/C-S13 보강).

- .github/workflows/ci.yml L9–10: ENV_FILE=environment.yml.
- 같은 파일 L99–111: Ubuntu web_and_docs가 ci/setup_env.sh를 호출.
- ci/setup_env.sh L94–104: 그 ENV_FILE로 conda 환경 생성·활성화.
- CI L118–121: doc/make.py --warnings-are-errors.
- contributing.rst L474–485: 위 개발환경을 요구하고 python make.py html 및 출력 경로를 명시.
- pin 직전 parent5e45f4에도 같은 환경→문서 경로가 유지된다(C-F54).

선정 목적에 대한 원문 추가 확인이며 봉인 파일을 바꾸지 않았다. NumPy recipe bot commit은2020-06-20, PR 병합은07-16 17:13:54, 보존된 Linux CPython 초기 artifact 업로드는17:23:43.986–17:26:43.103, Pandas 보고는21:32:11, pin은22:43:07이다. 제안 날짜를 시행일로 쓰면 약26일을 잘못 더한다.

실패 binary가 특정되지 않아 엄격한 upstream→consumer 지연 집계에 넣지 않는다. **조건부 metadata 간격**은 해당 세 Linux CPython artifact 중 하나였을 때5.2733–5.3231시간이다. consumer commit→source release는 rc0까지76,027초, 첫 안정판까지1,004,454초로 확인된다. 실제 rendered docs 배포는 미확인이다.

Matplotlib PR17289의 선제 적응은2020-05-22 병합되어 NumPy conda 배포보다 앞선다(C-F64). 이 중간 의존성의 source 수정과 소비자가 쓸 수 있는 release 공급은 다른 시점이다. 별도 A 소비자나 분자로 더하지 않는다.

## Spyder의 순서와 계보

C-F28의2022-04-29 실행 오류는0.3의5월 배포보다 앞선다. 상류가 새로 깨뜨린 사건이 아니라 기존 누락 의존성 문제의 수정 전파다. consumer commit은07-03 19:56:02,5.x 병합은07-04 18:52:59, source release5.3.2는07-13 19:55:59이다. commit→source release는863,997초다.

상류 maintainer impact27은 Spyder5.3.2 기여자이기도 하다. 같은 계보의 이슈·댓글을 독립 관측으로 중복 세지 않는다. 저장소 수와 독립 작성자 수를 구별한다. 선택한 옛 줄의 작성자 동일성까지 증명된 것은 아니므로 독립 소비자 산입을 보류한다.

Dask 선택 줄 생성자는 TomAugspurger이며 확인한 Python recipe/ABI 저자와 다르다(C-F61). Jupyter의>=1.8 생성자는 ian-r-rose로 Sphinx recipe 저자와 다르다(C-F62). 이는 특정 편집 쌍의 차이이며 모든 작성자·조직의 독립성 증명이 아니다.

## 실행·배포와 가벼운 기록의 경계

Pandas 실패 전후 SHA의 현재 GitHub check/status API에서 보존된 결과0개를 받았다(C-F55). 당시 시험0회·실패0회를 뜻하지 않는다. recipe test/pip check와 CI YAML은 지시 원문이며 성공 영수증이 아니다. source release의 수정 파일 포함은 확인했지만 바이너리 설치·문서 배포·사용자 성공은 별도다.

이 묶음의 엄격한 ‘같은 실제 artifact/기능 노출→실패→수정 효과’ 완전 체인은0건이다. 날짜는 역할별로 보존했다. 시작점 미확인을 우측 검열로 위장하지 않았고, 무정정 사건·새 기능·노출 미확인을 나눴다.

verdicts의 L1 주소, L2 기능·판·목적, L3 당시 원문·시점·관계 비교는 전체 자료를 본 같은 연구자의 구조적 점검이다. 독립 맹검 실험이 아니다. Python3 Napari에 Python2 배제 문제가 적용되지 않음을 판단할 때는 기대 범위와 recipe가 충분하다. 반면 Spyder 옛 경로 삭제가 미수정인지 판단하려면 경로 이력이 필요하다.

실제 재열람 횟수·사람의 해석 시간·운영 비용은 측정하지 않았고 추정하지 않았다. 원장 내 서로 다른 URL·고정 commit 수만 계산했다.

## 다음 최소 입력

1. Pandas:2020-07-16 web_and_docs의 conda list --explicit 또는 lock, 첫 post-pin 성공 및 문서 업로드 receipt. 현재 공개 check/status로 복원 실패했다.
2. Spyder: 실패 macOS의 CPU/Python3.10 artifact 목록,0.3 뒤 실제 실행,5.3.2 첫 conda/installer 배포 및 의존성 metadata. source release만으로 효과를 확정하지 않는다.
3. SciPy: 옛 Gaussian 용도와 일치하는 고정판 시험 또는 옛 소비자가 이미 새 sparse-array 기능을 요구했다는 원문. 없으면2024 하한 변경의 달력 차이를 지연으로 쓰지 않는다.

재현 입력은 future-search-log.jsonl의 공개 API URL과 future-sources.json의 고정 GitHub URL이다. 환경 재실행에는 정확 artifact 입력이 먼저 필요하며, 이를 임의 최신 버전으로 대체하면 이 조사 질문의 검사가 아니다.
