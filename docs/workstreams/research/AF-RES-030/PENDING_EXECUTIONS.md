# 미실시 실행과 첫 재개 입력

본 조사의 집계·봉인·경로·수용 조건 검사는 `evidence/validation.json` 및 session 검사 영수증에 기록한다. 아래 제품 실행은 **미실시**이며, 기술적 실행 성공이나 요청자 행동의 증거로 사용하지 않았다. 공개 원문에 있는 당사자의 실행 보고와 조사자의 새 재현은 다른 증거다.

## 현재 실행환경 확인

실제 셸에서 `importlib.metadata.version`과 `shutil.which`로 읽은 환경은 Python3.12.14, NumPy2.3.5, Matplotlib3.10.8, pandas2.2.3, Seaborn0.13.2였다. xarray/rioxarray/DuckDB/Cartopy/pytest와 Docker는 설치되어 있지 않았다. LaTeX/xeLaTeX/ffmpeg는 실행파일이 존재하지만 역사판과 GUI 환경은 일치하지 않는다. 따라서 현재 패키지의 출력을2023/2024의 해당 사용자 실행으로 바꾸지 않았다. 원 실데이터와 macOS GUI도 없다. 환경 확인 영수증은 `evidence/execution-environment.json`이다.

역사판 실행이 필요할 때 아래의 고정 Python 환경을 새로 준비한다. 명령은 저장소 루트에서 실행하며 작업 경로는 모두 본 소유 경로다. `runs/`·`inputs/`는 재개 담당자가 만든 실행 입력/출력이고 이번 결과에는 존재한다고 가정하지 않는다. 입력 파일이 없으면 임의 값을 채워 성공으로 세지 말고 중단 이유를 실행 영수증에 남긴다. 네트워크 설치와 아래 명령은 이번에 실행하지 않았다.

## 1. 가장 먼저 확인할 자료: X04의 전체목표

- 사건: <https://github.com/pydata/xarray/issues/7411#issuecomment-1372480571>
- 필요한 원입력: 당시 GeoTIFF 전체 세트, glob이 반환한 경로목록, 목표 CRS/transform/nodata/bounds/좌표값, 실제 xarray/rioxarray/intake 판. 현재 스레드에는 이 전부를 검증할 출력이 없다.
- 공급자 제한근거: <https://github.com/corteva/rioxarray/blob/0.13.3/setup.cfg>의 backend 등록. 이 판이 작성자 실제 설치판이었다는 보장은 없다.
- 먼저 `inputs/X04-files.txt`에 실제 경로를 한 줄씩 고정하고 `inputs/X04-expected.json`에 요청자가 원하는 metadata 기준을 고정한다. 원입력이 없으므로 아래는 **입력 확보 후 실행할 검사 형태**다. 독립 실행이 성공해도 당시 요청자의 실행으로 소급하지 않는다.

```bash
python3.10 -m venv docs/workstreams/research/AF-RES-030/runs/x04-env
docs/workstreams/research/AF-RES-030/runs/x04-env/bin/python -m pip install 'numpy<2' 'xarray==2022.12.0' 'rioxarray==0.13.3' dask
docs/workstreams/research/AF-RES-030/runs/x04-env/bin/python docs/workstreams/research/AF-RES-030/inputs/X04-check.py
```

`X04-check.py`는 다음 데이터를 저장하고 expected와 항목별 비교하도록 작성한다. 설치판 가정은 실제 작성자 판이 확인되면 그 판으로 교체하고 교체 이유를 기록한다.

```python
import json
from pathlib import Path
import xarray as xr
import rioxarray
p = Path('docs/workstreams/research/AF-RES-030')
files = (p / 'inputs/X04-files.txt').read_text().splitlines()
assert files, '원 파일목록 없음'
ds = xr.open_mfdataset(files, engine='rasterio')
observed = {'sizes': dict(ds.sizes), 'crs': str(ds.rio.crs),
            'transform': list(ds.rio.transform()), 'bounds': list(ds.rio.bounds())}
(p / 'runs/X04-observed.json').write_text(json.dumps(observed, indent=2))
expected = json.loads((p / 'inputs/X04-expected.json').read_text())
for key, value in expected.items():
    assert observed[key] == value, (key, observed[key], value)
```

이 코드는 기본 공간 속성만 검사하는 **연구자 작성·미검사 초안**이다. nodata/좌표/변수별 encoding과 intake 전달까지는 별도 검사가 필요하며, 위 코드가 원목표 전부를 승인하지 않는다.

## 2. M07: 공식 setter 존재와 실제 레이아웃

정확한 명령과 합성6-label 입력 코드 전체는 `streams/matplotlib/pending-checks.md`의 첫 절에 있다. Matplotlib3.8.4/Seaborn0.13.2에서 기존 legend의 `set(ncols=3)`와 `move_legend(...,ncols=3)`를 비교한다. 현재3.10.8 결과로 역사판을 대신하지 않는다. 실행 출력 이미지·실제 package판·코드해시·종료코드와 `_ncols`/pack된 열 수를 함께 남긴다. 합성 입력의 성공으로 원작성자의100개 scientific-name 데이터 성공을 채우지 않는다.

## 3. D08: frame과 함수 설명의 범위

- 최초/성공/정정 원문: <https://github.com/duckdb/duckdb/issues/12804#issuecomment-2203075138>, <https://github.com/duckdb/duckdb/issues/12804#issuecomment-2203153988>, <https://github.com/duckdb/duckdb/issues/12804#issuecomment-2203186542>.
- 명시판: DuckDB1.0.0. 원 테이블·query를 `inputs/D08-original.sql`에 보존하고 해시를 기록한다. 실제 root와 다르면 합성 입력으로 분리한다.

```bash
python3.10 -m venv docs/workstreams/research/AF-RES-030/runs/duckdb100
docs/workstreams/research/AF-RES-030/runs/duckdb100/bin/python -m pip install 'duckdb==1.0.0'
docs/workstreams/research/AF-RES-030/runs/duckdb100/bin/python docs/workstreams/research/AF-RES-030/inputs/D08-check.py
```

동일 함수를 유지한 채 frame만 바꾸는 최소 합성 입력은 아래와 같다. 이 코드는 alias 자체에 대한 지원자의 첫 설명을 검증하는 전체 실험이 아니며, 원 실제 데이터와도 별도다.

```python
import duckdb
c = duckdb.connect()
sql = '''WITH t(k, status) AS (VALUES (1,'a'), (2,'b'), (3,'c'))
SELECT k,
 last_value(status) OVER (ORDER BY k) AS default_frame,
 last_value(status) OVER (ORDER BY k ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS full_frame
FROM t ORDER BY k'''
print(duckdb.__version__)
print(c.execute(sql).fetchall())
```

peer ties/NULL/partition이 있으면 추가 입력을 별도로 고정해야 한다. 원작성자 동일입력 성공은 공개 댓글의 보고 수준으로만 유지한다.

## 4. DB04: quoted null의 당시판과 후발 수정판

원입력 주소는 <https://github.com/duckdb/duckdb/issues/6943#issuecomment-1493302942>이다. original unquoted 예와 수정 quoted 예를 서로 다른 입력 파일로 보존한다. 동일 parser 옵션/nullstr/열형을 유지한0.7.1 실행과 공급자 고정 수정판 `bd98353fbf2356853ad5603c9a9b51f0ea870cb8`을 비교해야 한다. 두 판을 혼합하지 않는다.

```bash
python3.10 -m venv docs/workstreams/research/AF-RES-030/runs/duckdb071
docs/workstreams/research/AF-RES-030/runs/duckdb071/bin/python -m pip install 'duckdb==0.7.1'
docs/workstreams/research/AF-RES-030/runs/duckdb071/bin/python docs/workstreams/research/AF-RES-030/inputs/DB04-check.py
```

`DB04-check.py`의 입력은 원 댓글 CSV bytes와 원 옵션을 그대로 사용해야 한다. 다음 공식 테스트는 후발 공급자 기대값 확인 입력이며 실행했다는 영수증이 없다: <https://github.com/duckdb/duckdb/blob/bd98353fbf2356853ad5603c9a9b51f0ea870cb8/test/sql/copy/csv/parallel/test_parallel_csv.test>. 수정판 소스 빌드/해당판의 공식 test runner 명령은 재개 환경에서 저장소 build 지침을 확인한 뒤 고정해야 하므로 여기서 실행 가능하다고 꾸미지 않는다. 최초 목표값 공개는 이미 직접답으로 확인됐지만 원작성자 수정판 사용은 이 검사로 대체할 수 없다.

## 5. 그 밖의 재개 자료와 실행 입력

| 사례 | 첫 자료와 필요한 입력 | 실행 명령·판 또는 실행 불가능 이유 |
| --- | --- | --- |
| M01 | [원 root](https://github.com/matplotlib/matplotlib/issues/24865) 원판 코드와 `-W always` 설정; NumPy1.24.0/Matplotlib3.6.2 | 해당 역사환경에서 `python -W always inputs/M01-repro.py`; 경고옵션을 고정한 판 비교와 판을 고정한 경고옵션 비교를 나눔. 원 요청자 실행은 미확인. |
| M03 | [cache 삭제 보고](https://github.com/matplotlib/matplotlib/issues/24872#issuecomment-1370892263), 실제font 경로/권한/cache,3.6.2 | 같은 환경의 별도 새 Python 프로세스2회로 `python inputs/M03-findfont.py`; 현재세션 성공과 재시작 영속성을 구분. 실제font 미공개라 미실시. |
| M05 | [PGF 입력](https://github.com/matplotlib/matplotlib/issues/28496),3.8.4와 당시TeX/PGF판, 원 기대 그림 | `python inputs/M05-pgf.py`; xlim/hatch/clip 조합의PDF·PNG와 기대 그림 비교. 당시TeX판/원인 미확인. |
| M08 | [실패 축소입력](https://github.com/matplotlib/matplotlib/issues/28513#issuecomment-2211433918), macOS14.5/Python3.12.3/Matplotlib3.9.1 | 실제 macOS에서 `python inputs/M08-macosx-only.py`와 원 혼합입력을 반복close 비교. Linux환경은 원 GUI를 실행할 수 없음. |
| MB09 | [새환경 실행](https://github.com/matplotlib/matplotlib/issues/25612#issuecomment-1496211688), 옛/새conda의 executable·import경로·package판 | 두 환경에서 `python -c 'import sys,matplotlib,cartopy; print(sys.executable,matplotlib.__file__,matplotlib.__version__,cartopy.__file__,cartopy.__version__)'`. 옛환경 없음. |
| X02 | [후발 오류요청](https://github.com/pydata/xarray/issues/7408#issuecomment-1369974685), 실제S3+moto fixture와오류 | `pytest inputs/test_X02_same_fixture.py -vv`; 오류를 아직 제시하지 않은 원작성자의 입력을 대체하지 않음. 최초오류요청 revision도 필요. |
| XB13 | [실패원파일](https://github.com/pydata/xarray/issues/7754#issuecomment-1509390748), 실제 local파일·Python/engine판 | 당시환경에서 `python inputs/XB13-open-original.py`; 다른 파일 성공으로 대체 금지. 원파일 bytes 미확보. |
| D02 | [BufferManager 지정판](https://github.com/duckdb/duckdb/blob/662041e2b43283bfcfeed984af7c3eaa85fb4996/src/storage/buffer_manager.cpp), 원 동시query workload·메모리한계 | 단일/다중query interleaving을 고정한실행 harness가 필요. 입력/실행가능 harness 미공개라 명령을 지어낼 수 없음. 첫 재개는 [명시 논거 답](https://github.com/duckdb/duckdb/issues/5818#issuecomment-1374537619)에 연결된 공개 workload/결정 기록 탐색. |
| D05 | [시간대 질문](https://github.com/duckdb/duckdb/issues/12784#issuecomment-2200636928), 원 query와 같은 연결 설정 | 원 연결에서 `SELECT current_setting('TimeZone');` 및 원 timestamp+interval query. 실제zone값 없음. [수정판](https://github.com/duckdb/duckdb/commit/3098c5a5e1c810294bb5b1407420f08ca1a87a94)은 공급자의 Kolkata 재현이며 사용자입력 대체 금지. |
| DB07 | [원 dplyr 예](https://github.com/duckdb/duckdb/issues/6947#issuecomment-1493849083), 실제client 변경과 원입력순서열 | R환경에서 `Rscript inputs/DB07-original.R`; 입력에 순서키를 먼저 붙인 뒤 최종ORDERBY한 결과와 기대행순서를 비교. 원client 변경커밋/환경 미확보. |

임의 합성실행으로 사람의 회상·수락·다음 선택을 확인할 수는 없다. 요청자 연락·새 질문 실험은 수행하지 않았으며 재개 절차에도 포함하지 않는다. 연구자의 코드 실행을 추가할 때마다 고정판·입력해시·명령·종료코드·출력을 별도 커밋하고, 당사자 원문에 의존하는 분자와 분리한다.
