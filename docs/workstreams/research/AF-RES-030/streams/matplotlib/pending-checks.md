# 미실행 기술 검사 입력

이 연구는 공개 대화의 관측이다. 아래 검사는 원작성자의 선택·실행을 대신하지 않으며 완료했다고 보고하지 않는다. 당시 OS GUI, PGF/TeX 또는 Cartopy 전체 환경은 준비하지 않았다.

## M07: 문서의 setter와 실제 legend 배치

목적: Matplotlib3.8.4에서 기존 `Legend.set(ncols=3)`가 열 배치를 바꾸는지, Seaborn0.13.2의 `move_legend` 재생성과 어떻게 다른지 기술적으로 확인. 작성자의 실데이터가 없으므로6개 label의 합성 입력만 사용한다. 아래는 **미실행** 명령이다.

```bash
cd docs/workstreams/research/AF-RES-030/streams/matplotlib
python3.11 -m venv cache/legend-venv
cache/legend-venv/bin/python -m pip install 'numpy<2' 'matplotlib==3.8.4' 'seaborn==0.13.2'
MPLBACKEND=Agg cache/legend-venv/bin/python cache/legend_check.py
```

`cache/legend_check.py` 입력:

```python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

fig, axes = plt.subplots(1, 3, figsize=(12, 4))
for ax in axes:
    for i in range(6):
        ax.plot([0, 1], [i, i + 1], label=f'category-{i}')
    ax.legend(ncols=1, loc='upper left')
axes[0].set_title('existing one column')
axes[1].get_legend().set(ncols=3)
axes[1].set_title('existing legend setter')
sns.move_legend(axes[2], 'upper left', ncols=3)
axes[2].set_title('recreated legend')
fig.savefig('cache/legend_check.png')
print({'matplotlib': matplotlib.__version__, 'seaborn': sns.__version__})
for ax in axes:
    legend = ax.get_legend()
    print(legend._ncols, len(legend._legend_handle_box.get_children()))
```

확인할 것: 각 출력 이미지의 실제 열 수와 `_ncols`/pack된 column 수를 함께 비교한다. 내부 attribute 접근은 관측 검사 목적이며 제품용 API로 추천하지 않는다. 모든 결과에 Python/package 실제판·코드해시·종료코드·이미지를 붙여야 한다.

## M01·M05·M08·MB09

- M01: root24865의 정확한 원판 코드, Matplotlib3.6.2와NumPy1.24.0, `python -W always repro.py`. NumPy판 답과 경고설정 보충의 기여를 분리하려면 경고옵션을 고정한 비교가 먼저 필요하다.
- M05: root28496의 `fill_between`/`hatch`/`xlim(0,8)` 코드, Matplotlib3.8.4와pgf/TeX 실제판, `python repro.py`; 정상기대 그림을 출력파일과 비교한다. root후속이 없으므로 이 실행으로 사용자 성공을 채우지 않는다.
- M08: root28513 및 댓글2211433918의 코드, macOS14.5·Python3.12.3·Matplotlib3.9.1. 먼저 Tk를 제거한 macosx-only 입력을 별도로 고정하고 `python repro_macosx_only.py`로 반복 close 결과를 기록한다. 연구 Linux환경에서 원래 macOS GUI를 실행한 적 없다.
- MB09: 이전환경과새환경 각각에서 `python -c 'import sys,matplotlib,cartopy; print(sys.executable); print(matplotlib.__version__,matplotlib.__file__); print(cartopy.__version__,cartopy.__file__)'`. 이전환경이 공개되어 있지 않으므로 현재 상태에서는 미실행이며 새환경성공이 이전환경원인을 확정하지 않는다.
