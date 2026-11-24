# 파일 링크와 경고를 반환하는 조건

## 이미 고정한 정확판을 재현할 때

`pytest==8.1.0`을 의도적으로 재현한다면 기존 파일의 버전·파일명·SHA-256을 설명에 유지한다. 인덱스가 이 파일을 제공하며 같은 해시와 Python/태그 조건을 만족할 때, pip 24.0 시험에서는 정확판을 선택했고 stderr에 철회 사유가 나왔다. [고정 파일과 지문](inputs.json) · [8.1.0 원 파일](https://files.pythonhosted.org/packages/5a/4a/3f626e3974bea1e6d471bd86f7965c67cd06d5770d1fec9aae445c44da7b/pytest-8.1.0-py3-none-any.whl) · [철회 사유](https://github.com/pytest-dev/pytest/issues/12069)

> pytest 8.1.0의 이 wheel은 철회 표시가 있습니다. 기존 환경을 재현하는 경우 파일명과 SHA-256을 대조하고, 영향을 받을 수 있는 예전 path hook 또는 플러그인을 확인하세요. 이 인덱스의 pip 24.0은 정확 핀을 선택하며 경고를 표시했습니다.

원사유가 제공되지 않으면 상태를 철회로 표시하고 사유는 미제공으로 둔다. 해당 링크를 누락한 미러에서는 같은 핀에 해가 없다. 이 경우 고정된 아티팩트의 신뢰할 수 있는 원출처와 해시를 조사할 수 있도록 링크 상태를 밝혀 둔다. 직접 URL 설치, lockfile 도구, 다른 소비자는 각자의 규칙·정책에 따른다. [빈 사유 검사](receipts/controls/pin-target-empty-r1/) · [링크 부재 검사](receipts/controls/pin-target-missing-r1/) · [설치기·미러 재량](https://packaging.python.org/en/latest/specifications/file-yanking/)

## 새 범위를 평가하거나 잠금을 갱신할 때

| 요청 범위 | 이 표본에서 첫 링크 | 동반 설명 |
| --- | --- | --- |
| `pytest>=8.0.2,<8.1.1` | [pytest 8.0.2](https://pypi.org/project/pytest/8.0.2/#files) | 8.1.0의 알려진 철회를 반영하면 8.0.2가 선택된다. 다음판을 쓰려면 상한 재평가가 필요하다. |
| `pytest>=8.0.2,<=8.1.1` 또는 의도적 `pytest==8.1.1` | [pytest 8.1.1](https://pypi.org/project/pytest/8.1.1/#files) | 포함 상한이라 8.1.1이 허용된다. 8.1.1은 두 path 관련 제거를 복원했으며 사설 API를 쓰는 조합은 개별 검증이 필요하다. |

새 범위의 해당 시행에서 stderr 선택 경고는 0이었다. 제품이 8.1.0을 제외한 이유를 보여줄 때에는 별도 출처와 관측 시점을 붙인다. 실제 적용에는 요청된 범위와 실제 인덱스의 후보, Python 태그, 의존 제약과 프로젝트 시험이 필요하다. 8.1.1 바깥의 공개 버전이나 전체 lock 생성에 대한 선택은 따로 검증한다. [16회 행렬](matrix.csv) · [pytest 8.1.1 변경기록](https://docs.pytest.org/en/8.1.x/changelog.html#pytest-8-1-1-2024-03-08)

## 인덱스 운영자와 출판 색인에 적용할 조건

파일 키는 프로젝트·버전·파일명·해시, 상태는 인덱스와 관측 UTC를 포함해 보존한다. 철회 철자와 원문 이유, 사유가 빈 표시, 후보 링크 부재를 각각 기록한다. 미러가 철회 파일을 노출하면 표시도 전달한다. 세션의 `unmarked`는 원인 분리를 위한 실험용 반전이다. [File Yanking · Mirrors](https://packaging.python.org/en/latest/specifications/file-yanking/#mirrors)

논문 이력이 목적이면 원 DOI와 업데이트 관계를 함께 연결한다. 새로운 근거를 추천하는 경우에는 공고의 종류와 적용 범위를 먼저 읽는다. 전체 철회 사례는 원 DOI에 공고를 붙여 이력을 보존하고, 새 근거 선택에서는 철회 상태를 명시해 보류할 수 있다. 정정 사례는 원문과 바뀐 부분의 정정 DOI를 함께 제공한다. [철회 원문](https://doi.org/10.1371/journal.pone.0208143) · [철회 공고](https://doi.org/10.1371/journal.pone.0322666) · [정정 공고](https://doi.org/10.1371/journal.pone.0313792)
