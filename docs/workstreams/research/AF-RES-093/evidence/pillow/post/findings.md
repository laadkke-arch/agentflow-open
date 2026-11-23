# Pillow 봉인 후 대조

사전 봉인 원격 SHA는 `3c50d0bd1d8f3659d86f8cf45fe233595c3d2592`다. 이후에만 원 issue comments, 수정 PR, 원 시험을 열었다. A/B 기록과 후보 URL은 수정하지 않았다. 아래 기대값은 출판자가 남긴 보고/코드/시험에서 읽었으며 이 세션이 Pillow를 실행해 만든 결과가 아니다.

| 요청 | 봉인 후 직접 근거 | 두 선택지·판 일치 감사 | 엄격 채점 |
|---|---|---|---|
| P1 #5406 | [원 작성자 후속](https://github.com/python-pillow/Pillow/issues/5406#issuecomment-820672806) PIL-POST1: RGB/RGBA 변환을 expand **전**에 하면 해결된다고 보고 | 원본문의 P-frame expand 실패와 후속 convert-before-expand 해결은 같은 사건. 전체 caption/draw/save 결과와 수행판의 양후보 대조는 후속에 충분히 명시되지 않음 | 미확인. 작성자 질적 해결보고를 허용하는 민감도에서는 gold=분리1건을 추가할 수 있으나 A/B 둘다 유보라 오류감소는 없음 |
| P2 #5593 | [유지관리자 설명](https://github.com/python-pillow/Pillow/issues/5593#issuecomment-876192273), [5594](https://github.com/python-pillow/Pillow/pull/5594), [원시험](https://github.com/python-pillow/Pillow/blob/fdfa9e8521a0b9436a6324f652c323a2e3a0b21e/Tests/test_image_convert.py#L41-L52), [5606](https://github.com/python-pillow/Pillow/pull/5606) | 자동mode 회귀는 설명됨. fixed test의 hopper/transparency0과 explicitRGBA test의 hopper/transparency128은 다른 입력이고 PR head는 수정후판 | 미확인. Image.py의 같은 분기로 독립 정답을 만들어 채점하지 않음 |
| P3 #5595 | [유지관리자의 두 호출·두 판 출력](https://github.com/python-pillow/Pillow/issues/5595#issuecomment-877558030), [작성자 수용](https://github.com/python-pillow/Pillow/issues/5595#issuecomment-877853085) PIL-POST3 | 원 p, P index1 이미지, object palette/direct array 두 경로가8.3.0에서 같은 palette read를 반환.8.2.0에서는 object 경로만 달라짐 | 8.3.0의 새RGB순서 목적에서 묶음. A=유보, B=묶음. 단, B 변화에는 원문의 목적 재해석이 섞임 |

P3의 원 작성자는 후속에서8.2 호환성도 원한다고 더 명확히 말했다. 최종 링크 반환은 direct `putpalette(p)`를 대표로 삼으면8.2.0/8.3.0에 게시된 결과가 같다. 이 후속 조건을 봉인된 B에 소급해 넣지 않았다.

엄격 Pillow 집계는 신규 3건 중 정답 가능 1건, 불가능 2건이다. SCOPE의 주 분모는 해당 gold이면서 확정 판정을 한 자리다. gold 분리가 0건이므로 오병합률은 A/B 모두 **산출 불가(0/0)**. 불필요한 분리는 A **산출 불가(0/0)**, B **0/1**이다. 보조로 모든 gold 묶음 자리를 분모로 쓰면 A/B 모두 0/1이지만, A는 그 1건을 유보했으므로 이를 맞힌 것으로 세지 않는다. gold 가능 1건에서 A 유보 1/1, B 맞는 묶음 1/1이다. 전체 3건의 A 유보 2/3, B 유보 1/3을 별도로 표시한다. 전체 오류율은 A의 채점 가능한 확정 판정이 없어 산출 불가(0/0), B는 0/1이다. 이는 사용자 성과나 추가 필드의 인과효과를 측정한 수치가 아니다.

## 출처 계보

PIL-POST1/2/3은 각각 한 issue의 후속 댓글 전체를 한 출처로 묶었다. 여러 댓글로 외부 고유 수를 늘리지 않는다. 요청 본문과 같은 사건이므로 사건수에서도 증가하지 않는다. PR5594와 그 convert 시험은5593 계보, PR5599와 putpalette/GIF 시험은5595 계보다. 후보문서와 같은 Image.py 계열 또는 파생 diff의 일치는 독립 재현으로 세지 않는다. Q6의 6349,6263 및11.3.0시험은 신규3건 적중 분모 밖이다.
