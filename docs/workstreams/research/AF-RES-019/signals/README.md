# 관측 원장과 고정 입력

- SIGNALS.csv는 80개 항목 × 4시점 × 13종이다. 빈 값마다 미확인 사유 코드가 있다. UTC 기준 날짜·로컬 수집 시각·원천도 함께 기록했다.
- DAYS.json.gz는 일별 값을 바뀐 날짜와 값으로 압축한다. 추적 데이터에는 프로젝트/항목 ID, 신호 ID, UTC 일수와 값만 들어 있다. 커미터 시각으로 이용 가능성을 대용한다.
- DETAILS.json은 Git 기본 HEAD, 경로·내용 해시·공지 단어, 라이선스/CLA 변경일, 태그와 레지스트리 응답 요약을 기록한다. 일부 README 및 매니페스트 상태는 고정한 스냅샷에서 다음 관측까지 보간했다. 고정판을 연 날짜와 처음 나타난 날짜를 구별한다.
- 현재 deprecated/yanked와 판 라이선스 표기는 레지스트리 응답 시점의 제한된 자료다. 날짜 있는 과거 표시 이력을 확보하지 못했으므로 그 두 시계열은 분석에서 미확인이다. 판 태그는 기본 브랜치 복제 뒤 공개 원격 전체 태그를 별도로 fetch했다. 과거 ref 삭제·후일 등록은 확인할 수 없다.
- partial clone Git pack과 후속 스냅샷 운송은 [수집 영수증](../results/collection-receipts.json)에 있다. 개인정보를 복제본 밖으로 내보내지 않았다.

실행 위치는 저장소 루트다.

```sh
p=docs/workstreams/research/AF-RES-019
python -B "$p/src/collect.py" --scratch /tmp/af-res-019-run --match --registry
python -B "$p/src/collect.py" --scratch /tmp/af-res-019-run --signals
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$p/src" python -m unittest discover -s "$p/tests" -v
```

현대 레지스트리와 기본 Git ref는 갱신될 수 있다. 고정 결과 재생은 분석 코드와 커밋된 압축 일별 입력을 사용한다.
