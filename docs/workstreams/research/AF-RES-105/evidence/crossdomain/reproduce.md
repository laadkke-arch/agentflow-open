# 교차 분야 읽기 재현

작업 디렉터리는 저장소 루트다. 원문 본문은 무시되는 `.cache/crossdomain/`에 있으며, 커밋되는 영수증은 `evidence/crossdomain/acquisition.jsonl`, 판독은 `original-examples.json`과 `findings.md`다. 공개 출처 22개에 대해 원문 URL과 SHA256을 보존했다. 공개 GitHub API 이슈 응답은 수정될 수 있으므로 현재 재조회가 기존 SHA256과 같을 것을 가정하지 않는다.

## 버전 핀 확인

```sh
git ls-remote https://github.com/LibreOffice/help.git 'refs/tags/libreoffice-24.2.0.3' 'refs/tags/libreoffice-24.2.0.3^{}'
git ls-remote https://github.com/LibreOffice/core.git 'refs/tags/libreoffice-24.2.0.3' 'refs/tags/libreoffice-24.2.0.3^{}'
git ls-remote https://github.com/audacity/audacity.git 'refs/tags/Audacity-3.6.4' 'refs/tags/Audacity-3.6.4^{}'
git ls-remote https://github.com/audacity/audacity-manual.git 'refs/tags/v3.6.4'
```

태그와 commit의 대응은 `pins.json`을 대조한다. LibreOffice annotated tag에서는 tag object와 `^{}` commit을 구분한다.

## 원문 재조회 — 파일과 같은 저작 수 구분

아래 명령은 네 필수 저작의 고정 소스/공개 사건을 다시 열고 새 영수증을 남긴다. 이미 있던 원문이 바뀌면 과거 판독을 고치지 말고 새로운 파일 ID로 저장한다. 따라서 재조회 ID에는 `RECHECK-`를 붙인다.

```sh
python -B - <<'PY'
from pathlib import Path
import json,sys
sys.path.insert(0,'docs/workstreams/research/AF-RES-105/evidence/crossdomain')
from read_source import read
root=Path('docs/workstreams/research/AF-RES-105/evidence/crossdomain')
for line in (root/'sources-part.jsonl').read_text().splitlines():
    row=json.loads(line)
    if row['count_unique_primary']:
        body,receipt=read('RECHECK-'+row['source_id'],row['acquisition_url'])
        print(row['source_id'],receipt.get('status'),receipt.get('sha256'),
              receipt.get('sha256')==row['acquisition_sha256'])
PY
```

필수 네 자료는 `CD-CALC-MAN`, `CD-CALC-FORMULA`, `CD-AUD-ENVELOPE-364`, `CD-AUD-ISSUE2371`이다. 이슈 첨부 이미지도 `original-examples.json`에 적힌 URL로 다시 열어야 그림 판독을 재현할 수 있다. 이미지 세 장은 Audacity 사건 한 건이며 자료 수를 세 번 늘리지 않는다.

## 필수량 재집계

```sh
python -B - <<'PY'
from pathlib import Path
import json,collections
p=Path('docs/workstreams/research/AF-RES-105/evidence/crossdomain/sources-part.jsonl')
r=[json.loads(x) for x in p.read_text().splitlines()]
a=[x for x in r if x['count_unique_primary']]
print('records',len(r),'admitted',len(a),'unique_work_lineages',len({x['same_work_lineage'] for x in a}))
print(collections.Counter(x['minimum_slot'] for x in a))
PY
```

관측된 재집계는 기록22, 필수 산입4, 산입 저작 계보4다. 이 숫자는 이 연구 전체의 출처 수와 별도이며, Q1/Q4 사용자 사건이나 학습/채택 분자에 더하지 않는다.

## 앱 실행과 예상 출력의 경계

- LibreOffice `testFormulaRefUpdate`의 원 코드 입력·단언을 읽었다. 로컬 C++ 시험 실행은 **미실시**다. 실행이 필요한 다음 검토자는 정확히 24.2.0.3 core의 기존 build/test 환경에서 이 시험을 실행하고 빌드 commit과 종료값을 별도로 보존해야 한다. 이 조사에는 그 빌드 환경이나 통과 영수증이 없다.
- Audacity 원 예제는 보고자 판3.1.3이다. 재현 입력은 30초 tone, 10–20초 envelope 최저 구간, Allow Clipping을 켠 +50 dB Amplify 3회다. 대조 경로는 동일 envelope 이후 10–20초에 Ctrl+L을 먼저 적용하고 같은 Amplify 3회다. 원 tone 주파수·정확한 envelope 값이 없어 동일 입력 복원은 **미확인**이다. 숫자 잔여 진폭이나 최신 버전 재현을 주장하려면 새로 고정한 입력 파일과 raw sample 측정을 별도 사건으로 남겨야 한다.
- #5099 재현 입력은 3.3.3 Windows, envelope가 있는 압축된 stereo clip, 그 clip 선택, Clip Fix다. 원 오디오 파일과 매개변수는 미확인이므로 이 자료만으로 동일 실행을 복원할 수 없다.
- 이 미실시는 직접 읽은 공식 계약/상류 예상값/작성자 보고를 비교하는 본문의 결론을 실행 결과로 확대하지 않게 하는 제한이다. 원 작성자의 실행이나 새 지식 습득을 확인했다는 뜻이 아니다.
