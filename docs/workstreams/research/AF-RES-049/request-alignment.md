# 요구 원문과 고정 코드 대응

GitHub에 현재 보이는 첫 본문은 최초 가용 본문으로 사용했다. #13600은 제목을 입력한 직후 전송됐고 작성자가 뒤이어 보고서를 채웠다. #13522의 생성 순간 본문은 확정할 수 없다. 다음의 GitHub 행은 2026-11-23 열람 시점의 렌더링 행이다. [#13600 보고서 완성 댓글](https://github.com/matplotlib/matplotlib/issues/13600#issuecomment-470135635) · [#13522](https://github.com/matplotlib/matplotlib/issues/13522)

| 행과 출처 | 작성자 요구·조건 | AF-RES-045 및 이번 고정 입력 |
| --- | --- | --- |
| M03 #13600 L154–155, L174 | 10×10 배열, factor .01 및 .001. 난수 사용 없음 | requests L4와 predictions L6–7의 같은 배열. 이번 판별 입력은 두 factor. 본문 L190의 .1 그림은 역사 근거로 보존 |
| M03 L157–164 | 5×4인치, DPI 100, 위 제목, 오른쪽 폭 5%와 pad 10%, `imshow` | 같은 fixture. `make_axes_locatable`로 붙인 축을 `fig.colorbar`에 넘김 |
| M03 L165–170 | `text(.5,.5)`, 수평·수직 가운데, 회전 90°, 같은 rect와 PNG | 원문은 기본 데이터 transform B. A만 조언에서 나온 `cb.ax.transAxes`를 추가. 출력 경로만 새 실행 ID로 지정 |
| M03 L171–207 | 색 막대 안의 정중앙이 목적. .01과 .1로 예시, .001은 경고와 예외 기록 | 045가 중앙의 관측 단위를 axes 비율로 명시. 실제 x/y limits와 단계별 표시 좌표·PNG를 이번에 계측 |
| M03 L217–223 및 댓글 470153183/470159527 | Windows 10, 3.0.2, TkAgg, Python 3.7.2, NumPy 판 미기재. 작성자가 좌표 조언 수락 | Linux x86_64/Agg, 3.6.8/1.16.6, 글꼴 및 의존판을 고정. 수락에는 factor별 좌표·PNG 재시험 로그가 없음 |
| M02 #13522 L149–161 | 원 caption 순서, palette, 10개 점, 10점/계열, 원본은 20계열에 10/30 제시. seed 없음 | requests L3, predictions L4–5의 10/30. 045 probe의 `random.Random(45045)`를 사용. 원 순서·색·정수 범위 고정 |
| M02 L164–189 | 10×3인치, 폭 비 5:1:5, 좌측 scatter·우측 lines와 고정 y limits | 같은 fixture, DPI 100과 새 figure는 연구자 설정. 현재 figure 재사용을 분리 |
| M02 L191–202 | 중앙 axes 범례 제목·loc 0·frameon False·spine/tick 숨김·tight_layout·show | A 유지, B만 `set_in_layout(False)`, C는 범례 artist만 생략. Agg PNG로 교체, bbox_inches 기본. 각 항목 수의 세 조작은 같은 데이터 |
| M02 L203–206 | 10개 정상, 30개 layout 실패 보고. 글꼴 크기 고정, 범례가 넘으면 자르되 데이터 축 축소 방지 | 글꼴을 수치로 고정하는 DejaVu Sans 10pt, 동수 C, bbox/라벨별 픽셀 비교는 연구자 설정. 20개는 역사 보고로 유지 |
| M02 L208–220 및 댓글 467476150/470121184 | Windows 10 x64, 32비트 Python 3.7, 3.0.2/TkAgg. 수락 댓글은 동작 보고. 최초 가용 본문에 PNG 첨부 없음 | Linux/Agg와 명시된 폰트·PNG는 신규. 원 작성자의 bbox, 동일 seed, 판독 가능한 계열 이름 수는 미확인 |

원문 주소와 첨부 시도는 [I01–I04 및 부속 행](sources.jsonl#L1)에 있다. 045의 [requests.csv L3–4](https://github.com/laadkke-arch/agentflow-open/blob/29c5da579b7a29118f31541092e6a51f3d77219d/docs/workstreams/research/AF-RES-045/requests.csv#L3), [predictions.csv L4–7](https://github.com/laadkke-arch/agentflow-open/blob/29c5da579b7a29118f31541092e6a51f3d77219d/docs/workstreams/research/AF-RES-045/predictions.csv#L4) 및 [REPRODUCE.md](https://github.com/laadkke-arch/agentflow-open/blob/29c5da579b7a29118f31541092e6a51f3d77219d/docs/workstreams/research/AF-RES-045/evidence/reproduction/REPRODUCE.md)에 대응한다.
