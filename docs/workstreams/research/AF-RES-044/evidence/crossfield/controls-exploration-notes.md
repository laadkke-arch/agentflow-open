# 보강 후보 독립 탐색 기록

이 기록은 자연 8요구를 보지 않고 진행한 보강 후보 탐색이다. 공식 HTTPX/Requests, Pillow/PIL, psycopg 계열에서 시작했고, 처음 지시에서 허용한 pandas/NumPy/Matplotlib 비교 문서로 확장했다. 탐색 중 해법 설명을 읽은 사실을 숨기지 않는다. 이 후보들은 해법 발견률의 표본이 아니다.

## 선정과 탈락

| 원문 | 확인 범위와 결정 | 남은 한계 |
| --- | --- | --- |
| [HTTPX Requests compatibility](https://www.python-httpx.org/compatibility/) | 전체 본문 최초 여섯 href의 전역 순번 74–79. 앞의 HTTPX 문서 셋 뒤 Requests 문서가 실제 네 번째에 위치. 부모 작업에서 C1로 채택. | 링크 목적은 각각 다르다. 같은 프로젝트라는 이유만으로 같은 호출 계약이라고 말할 수 없다. C1의 최종 판정은 부모 원장에 둔다. |
| [pandas 현재 ecosystem](https://pandas.pydata.org/community/ecosystem.html) | Plotting backends의 최초 링크는 자체 절, matplotlib, hvPlot이므로 요청한 세 개의 선행 같은 상류 구조에 맞지 않는다. | 현재판을 과거판의 href 원천으로 쓰지 않았다. |
| [pandas 2.0.3 ecosystem](https://pandas.pydata.org/pandas-docs/version/2.0/ecosystem.html#visualization) | 발행된 Visualization 절의 실제 첫 여섯 링크를 C2로 봉인. 원 HTML 해시와 42–47의 DOM 순번 보존. | 절 대표 하나가 하위 설명도 포함하므로 중복 제거의 이득이 없을 수 있는 양성 대조다. 단순히 별도 제품 링크가 뒤에 있다는 이유로 가려진 대안이라고 판정하지 않는다. |
| [Matplotlib 3.4.3 third-party packages](https://matplotlib.org/3.4.3/thirdpartypackages/index.html) | Mapping toolkits와 declarative libraries의 실제 링크/제목 순서를 확인. | 문서 발행자, 자기 앵커, 설명 대상 프로젝트가 서로 다르다. 세 개를 같은 상류로 묶으려고 목록 중간부터 자르는 보강은 만들지 않았다. |
| Pillow, psycopg, NumPy beginner, Requests 직접 HTTP 시도 | 접근 실패는 URL·오류·첫 재개 URL과 함께 별도 원장에 기록. | 실패 및 링크 구조만 파싱한 페이지는 최소 읽기 수에서 제외. |
| [Requests advanced](https://requests.readthedocs.io/en/latest/user/advanced/#blocking-or-non-blocking), [NumPy interoperability](https://numpy.org/doc/stable/user/basics.interoperability.html) | 웹 도구로 원문을 열어 일반 Requests의 blocking 특성과 변환/dispatch의 차이를 읽음. | C2 채택 후 추가 통제군으로 발전시키지 않았다. 원 HTML 기반 여섯 링크를 봉인하지 않았으므로 탐색 메모이며 산입하지 않는다. |

## C2 인계

`control-C2.json`은 원요구, 원 HTML 해시, 여섯 raw href, 각 후보의 실제 HTTP 도착, 발행자 식별 링크, 판독 창과 확인 내용을 담는다. `controls-exploration-c2-access.json`은 후보별 접근 메타데이터이고 `controls-exploration-sources.jsonl`은 독립 원문 5개와 반복 fragment·탈락/실패 기록을 구분한다. 원 HTML 전체는 저장하지 않았다.

고정 요구의 visualization/plotting은 표 꾸미기도 허용한다. 따라서 Styler를 차트가 아니라는 이유로 오답 처리하면 사후 요구 변경이다. 언어 조건을 빠뜨린 가까운 오답은 같은 허용 절 안에서 R용으로 명시된 ggplot2다. Altair 홈페이지와 Bokeh 홈페이지의 도착 창은 Python 시각화를 말하지만 tabular/DataFrame 입력을 명시하지 않으므로 그 창 하나의 근거와 다른 풀 문서의 보완 근거를 분리했다.

반환 후보 여섯 개와 문서가 설명하는 대안 수는 다르다. 첫 후보의 Visualization 절에는 10개의 적격 이름 후보와 Python 언어 명시가 부족한 IPython Vega·qtpandas가 있다. Bokeh, plotnine 등은 해당 절 전체의 pandas-compatible 진술을 사용하며, backend 예제는 Python pandas 문맥을 사용한다. 이것은 독립 렌더러 10개나 현재 실행 호환성을 검증했다는 뜻이 아니다.

세 번째 후보의 `#visualization`은 h1 시작점이므로 허용 창 전체가 4,949어절이다. 처음 추출 출력에서 후반이 잘려 앞의 pandas wrapper 설명만 보고 Matplotlib을 구성품으로만 분류했다. 남은 창을 읽자 **Plotting directly with Matplotlib**(웹 원문 972–993행)이 Series·DataFrame의 Matplotlib 직접 전달과 `plt.plot` 예제를 명시했다. 원요구·href·판독 경계는 그대로 두고 별도 Matplotlib 대안을 추가하여 원풀 분모를 **11**로 고쳤다. 초기 파일은 `controls-exploration-C2-before-fullwindow.json`, 변경 이유와 영향 슬롯은 최종 JSON의 `source_coverage_revisions`에 보존했다. 같은 파이프라인을 두 번 센 것이 아니라 별도로 기술된 직접 인터페이스를 확인한 보정이다. 뒤의 Plotting backends 절까지 읽었으며, 그 부분의 Bokeh/Altair/hvplot은 앞서 포함된 이름이고 `backend.module`은 실제 구현이 아닌 예시 자리다.

따라서 첫 후보가 이미 제공하는 10개에 대해서는 새로 되살릴 대안이 없지만, 세 번째 후보를 가리면 Matplotlib 직접 사용의 추가 근거가 사라질 수 있다. 전체 방식별 이득·손실이 모두 0이라고 미리 결론 내리지 않는다. 이 반례가 최종 그룹 계산에서 어떻게 나타나는지는 부모 작업이 같은 입력으로 판정한다.

이 보조 작업에서는 A/B/C 그룹을 계산하거나 실제 사람의 클릭을 관측하지 않았다. 여섯 실제 URL 도착과 허용 범위 의미 판독만 제공했고, 부모 작업이 같은 풀로 반환 및 두 클릭 경로를 계산한다.
