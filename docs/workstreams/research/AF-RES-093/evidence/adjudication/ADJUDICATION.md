# AF-RES-093 독립 사후 판정 감사

기록: 2026-11-23 18:11:39 UTC. 사전 A/B 원격 봉인 SHA: `3c50d0bd1d8f3659d86f8cf45fe233595c3d2592`.

## 결과와 분모

선정 요청 6건을 모두 분모에 남겼다. 같은 판·입력·실제 관찰 목표에서 두 후보를 대조할 수 있는 제한범위 gold는 P3 한 건이다. I3의 두 번째 후보 결손을 사후 보충하지 않았다.

| 요청 | true pair label | strict scorable | 핵심 범위 또는 결손 |
| --- | --- | --- | --- |
| I1 / Inkscape2225 | 유보 | false | stamp 실패 보고와 shape-inside 차이 설명은 있지만 원1.0.2의 양 후보 resize 결과 비교가 없다. |
| I2 / Inkscape2231 | 유보 | false | C1은 exact1.0.2에서 재현되나 C2의 동판 성공 관측이 없다. 이후 C1 수정판을 C2 성공으로 바꾸지 않는다. |
| I3 / Inkscape2283 | 유보 | false | 봉인 입력의 candidate2=null. selection 변화와 후대 수정 주장을 후보로 추가하지 않는다. |
| P1 / Pillow5406 | 유보 | false | OP의 before-expand RGB 해결 보고는 보고형 분리를 지지한다. 두 결과의 판·입력 동일성 및 최종 결과 비교는 추정이 남는다. |
| P2 / Pillow5593 | 유보 | false | 원 implicit convert 실패는 지지된다. 이후 수정판 hopper 회귀시험은 원 PNG·원판의 C2 결과가 아니다. |
| P3 / Pillow5595 | 묶음 | true | 명시8.3.0·같은 p·P index1 image·getpalette assertion에 한정한다. |

이 1/6은 제한범위 정답을 구성할 수 있었던 요청 수이다. 오류 감소율, 일반적 실패 빈도, 전체 사용자 작업의 성공률로 해석하지 않는다. A/B 예측을 열지 않았으므로 이 검토자는 예측 정오를 채점하지 않았다.

## P3를 채점할 수 있는 이유와 한계

[maintainer 비교](https://github.com/python-pillow/Pillow/issues/5595#issuecomment-877558030)는 동일한 p와 P image에서 ImagePalette 객체를 설치한 결과와 배열을 직접 설치한 결과를 명시8.3.0에서 각각 제시한다. 두 결과는 원 본문의 getpalette assertion에 필요한 p와 같다. [원 작성자 수용](https://github.com/python-pillow/Pillow/issues/5595#issuecomment-877853085)은 직접 배열 전달이 목적에 맞는다고 확인한다.

댓글의 putpalette(p)는 rawmode를 생략한다. [고정8.3.0 signature](https://github.com/python-pillow/Pillow/blob/51591a80a4e14543ea8cbe93026db5e79354b8c4/src/PIL/Image.py#L1749-L1776)를 열어 기본값 RGB와 봉인 C2의 대응을 확인했다. 이 코드 확인은 별도 결과 시험으로 세지 않는다.

radarhere는 비교 게시자이며 관련 변경을 설명하고 후속 PR5599/PR5594를 작성했다. 따라서 이것은 **maintainer가 게시한 paired test**와 **별도 OP 수용**이며, 구현 저자에게서 독립된 외부 실행이나 제3자 CI 재현이라고 부르지 않는다. 동일 저작군의 문서·코드·PR를 여러 독립 검증으로 늘리지 않는다.

8.2.0 출력 보존, 모든 설치판의 호환, 임의 팔레트, 후속 GIF 저장·색 변환은 이 gold 밖이다. 그 넓은 목적은 유보한다. 명시8.3.0 목표에 모든판 호환을 자동으로 추가하지 않은 이유와 재판정 과정은 [review-note.md](review-note.md)에 기록했다.

## 보고형 근거와 제외 근거

P1의 [OP 후속](https://github.com/python-pillow/Pillow/issues/5406#issuecomment-820672806)은 정확히 RGB 변환을 expand 이전으로 옮기는 방법을 지지한다. 숫자 픽셀 artifact가 없다는 이유만으로 탈락시킨 것은 아니다. 같은8.2.0·같은 원 GIF와 설정의 나란한 최종 결과를 확보하지 못했고, 후속이 판을 재명시하지 않아 strict gold는 유보했다. 보고형 분리는 판단 파일에 남겼다.

P2의 [PR5594](https://github.com/python-pillow/Pillow/pull/5594)는 이후 수정 코드에서 별도 hopper 입력의 implicit convert를 검사한다. 원8.3.0 PNG의 explicit RGBA 결과를 대신하지 않는다. I2 역시 후대 C1 수정 확인을 원판 C2 확인으로 대체하지 않았다. I3의 초기 trunk-fixed 주장은 원 작성자의 재시험 및 maintainer 정정과 함께 보존했다.

## 파일과 열람 기록

- [pair-adjudication.jsonl](pair-adjudication.jsonl): 6행 truth. 후보마다 원근거 URL·판·입력·expected·관측 종류·누락·최소 추가 관측을 기록한다.
- [source-open-log.jsonl](source-open-log.jsonl): 실제 직접 열람 50개 resource/event 기록. 모든 행은 category=independent_recheck, counted=false이다. collection과 note 하위 사건은 중복 계수하지 않는다.
- [adjudicator-provenance.json](adjudicator-provenance.json), [input-hashes.json](input-hashes.json): 허용 입력·봉인·미열람 경계·입력 해시.
- receipts/: 원문 대신 URL, 시각, 저자/사건 metadata, 지문, 짧은 요약을 보존한다. 원문 전문은 삭제했고 ledger의 snapshot_retained=false와 reopen_url을 따라 재열람한다. HTTP 원bytes 지문과 parsed response 지문은 혼동하지 않도록 범위를 적었다.

GitLab /notes API의 401 세 건과 초기 웹 추출 실패를 그대로 남겼다. 공개 discussions.json을 직접 열어 후속을 읽었다. 추가 외부 조사나 새 실행은 하지 않았으며, commit/push는 수행하지 않았다.

