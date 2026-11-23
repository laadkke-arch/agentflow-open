"""Render the three required tables from sealed records and post-seal rows."""
from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parent


def jl(path):
    return [json.loads(s) for s in path.read_text().splitlines() if s.strip()]


def table(headers, rows):
    def cell(value):
        return str(value).replace("|", "\\|").replace("\n", " ")
    return "\n".join([
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
        *("| " + " | ".join(cell(c) for c in row) + " |" for row in rows),
    ]) + "\n"


def main():
    records = {(r["request_id"], r["mode"]): r for r in jl(ROOT / "records.jsonl")}
    sources = {r["source_id"]: r for r in jl(ROOT / "sources.jsonl")}
    reconciled = json.loads((ROOT / "evidence/reconciliation.json").read_text())
    with (ROOT / "judgments.csv").open(newline="") as handle:
        judgments = {(r["request_id"], r["method"]): r for r in csv.DictReader(handle)}
    cases = ("I1", "I2", "I3", "P1", "P2", "P3")

    def src(source_id, title=None, section=None):
        url = sources[source_id]['url']
        if section is not None:
            url = url.split('#')[0] + '#' + section
        return f"[{title or source_id}]({url})"

    def candidate(case, number, title=None):
        item = records[case, "A"]["record"]["candidates"][number - 1]
        if item is None:
            return "후보2 미확인"
        return f"[{title or (case + '-C' + str(number))}]({item['url']})"

    request_info = {
        "I1": ("#2225 · 현존 요청, 최초판 미복원", "한 text-box를 resize할 때 나머지 text-box와 원 참조 shape는 유지", "Spacebar stamp / Edit Duplicate; SVG2 text와 참조 shape 입력", "1.0.2+r75+1 / upstream 1.0.2 e86c870879", "배포판과 tag의 정확한 일치, 같은 SVG의 양쪽 resize 출력"),
        "I2": ("#2231 · 현존 요청, 최초판 미복원", "원본 path의 shape를 바꾸면 연결 path도 갱신; 기존 target ID 보존 의도는 공석", "ItemParam::linkitem(clipboard 버튼) / ObjectSet::cloneOriginalPathLPE(새 path 메뉴)", "1.0.2 / e86c870879", "기존 target 보존 필요, 두 경로의 같은 다음 shape 출력"),
        "I3": ("#2283 · 이동 전 inbox #4522 본문 사용; 최초판 미복원·오염 표시", "eraser Delete 뒤 요청한 원본/clone 생존 관계와 무충돌; 후속에서 요구가 좁아짐", "EraserTool Delete의 touched/selection 처리 / 후보2 null", "1.0.2+r75+1 / upstream 1.0.2 e86c870879", "같은 eraser 입력의 후보2; 원판 pair 출력; 후대 수정 문장 사전 노출"),
        "P1": ("#5406 · 현존 요청, 최초판 미복원", "GIF 프레임에 흰 자막 영역·검은 글씨를 더해 저장; 원 프레임색과 자막색 유지", "ImageOps.expand(P frame) / expand(frame.convert('RGB')); 같은 GIF frame", "8.2.0 / e0e353c0ef75", "완성 GIF 양쪽 결과와 수행판의 연결; index 보존은 요청되지 않음"),
        "P2": ("#5593 · 현존 요청, 최초판 미복원", "P 이미지를 변환한 직후 RGBA mode·투명 index0 의미 확인; 그 이후 조작은 요구 없음", "img.convert() / img.convert('RGBA'); P, RGB palette, transparency=0", "8.3.0 또는 8.3.1 / 8.3.0 51591a80a4e1", "원 PNG의 원 8.3.0 양호출 출력; 8.3.1 별도 검증"),
        "P3": ("#5595 · 현존 요청, 최초판 미복원", "p를 붙여 getpalette()[:len(p)] == p 확인; 8.3 새 RGBRGB 순서 선호", "ImagePalette 객체를 putpalette / raw p를 putpalette; P index1 이미지", "8.3.0+ / 8.3.0 51591a80a4e1", "모든 판의 호환 및 저장·변환 보존은 이번 목표 밖; 두 fresh image의 독립 실행 아님"),
    }
    table1 = []
    for case in cases:
        label, operation, calls, version, gap = request_info[case]
        request_url = records[case, "A"]["record"]["request_url"]
        if case == "I3":
            label += " · [사용 본문](https://gitlab.com/inkscape/inbox/-/issues/4522)"
        table1.append([
            f"{case} · [{label}]({request_url})" if case != "I3" else f"{case} · [#2283]({request_url}) · {label}",
            operation,
            f"{candidate(case, 1)} · {candidate(case, 2)} — {calls}",
            version, gap,
        ])

    a_reasons = {
        "I1": "원 요청에 이미 독립 resize와 stamp 실패가 있어 분리",
        "I2": "기존 target/새 target의 같은 요구 지원 미확인",
        "I3": "같은 입력의 후보2 없음",
        "P1": "두 절만으로 전체 caption/save 색 보존 미확인",
        "P2": "요청 자체가 RGBA를 명시하고 기본모드와 명시모드가 다름",
        "P3": "당시에는 이전판 호환과 새 순서 선호의 목적을 미결로 해석",
    }
    b_reasons = {
        "I1": "참조 shape 복사·재연결 차이를 추가; 분리 유지",
        "I2": "clipboard 원본 ID/기존 target과 메뉴의 새 target 명시; 다음 결과 공석",
        "I3": "touched/selection 대상·생존 요구를 적어도 후보2는 생기지 않음",
        "P1": "P 인덱스 대상과 RGB 값 대상으로 구분; 다음 저장 보존은 공석",
        "P2": "palette.mode와 transparency index0의 alpha 경로 명시; 이후 조작은 없음",
        "P3": "원 p·index1·8.3 순서로 범위를 제한; 원문 목적 재해석도 함께 발생",
    }
    post_cells = {
        "I1": f"원 영상은 stamp 실패만. {src('I-POST-001', '당시 설명')}·{src('I-POST-004', '참조 처리 수정')}은 분리 가설을 지지; 양쪽 resize 정답은 미확인",
        "I2": f"{src('I-POST-002', '1.0.2 버튼 재현')}은 문서 밖 clipboard group ID 연결 실패. {src('I-POST-005', 'MR2570')}은 후대 수정; 메뉴 성공을 대신하지 못함",
        "I3": f"{src('I-POST-003', '작성자 정정')}은 clone 미삭제를 selection 동작으로 수용. {src('I-POST-006', 'MR4079')}은 후대 crash 수정; 후보2 없음",
        "P1": f"{src('PIL-POST1', '작성자 후속')}이 expand 이전 RGB/RGBA 변환으로 해결됐다고 보고. 전체 두 출력·수행판의 충분성은 미확인",
        "P2": f"{src('PIL-POST2', '진단')}·{src('PIL-POST4', '수정 후 시험')}은 원 PNG·원 8.3.0의 같은 양호출 pair가 아님",
        "P3": f"{src('PIL-POST3', '두 호출 출력')}에서 8.3.0의 C1/C2 palette read는 p와 동일. [작성자 수용](https://github.com/python-pillow/Pillow/issues/5595#issuecomment-877853085). 제한범위 gold=묶음",
    }
    table2 = []
    for case in cases:
        ar, br = records[case, "A"], records[case, "B"]
        classification = "정답 결손: 오판 여부 미채점"
        if case == "P3":
            classification = "A 유보 / B 일치. 오병합·불필요한 분리 관측 없음"
        table2.append([
            case,
            f"{ar['judgment']} · {a_reasons[case]}",
            f"{br['judgment']} · {b_reasons[case]}",
            post_cells[case], classification, request_info[case][4],
        ])

    table3 = [
        ["I1 · 복제 text-box를 각각 resize", candidate("I1", 2, "Duplicate 참조 복사·재연결") + " 우선 후보", "원 shape-inside 참조를 따로 만드는 경로를 조사할 때; 1.0.2 코드 기반 분리 예측·사후 정답 미확인", "stamp의 공유 참조; LPE까지 일반화", "개별 편집 요구가 원문에 있어 재질문 없음. 사용자 배포판 pair 실행은 미확인"],
        ["I2 · 원본 수정이 연결 path에 반영", candidate("I2", 1, "기존 target 연결") + " + " + candidate("I2", 2, "새 LPE path 생성"), "기존 target 보존/새 target 허용을 구분. 1.0.2 버튼 실패와 후대 수정 시점을 표시", "clipboard에만 있는 group ID, 기존 target의 효과·ID가 필요한 입력", "기존 path의 ID·효과를 유지해야 하나요? 예→기존 target 경로와 수정 근거; 아니오→새 path 메뉴를 우선 후보로 제시"],
        ["I3 · eraser로 원본/clone 처리", candidate("I3", 1, "Eraser touched/selection 처리") + "; 후보2 미확인", "선택된 원본과 닿은 객체 집합을 구분하는 조사 링크", "후대 crash 수정을 원판의 완성 대체품으로 간주", "selection 조건은 작성자 후속에 있으므로 다시 묻지 않음. 같은 eraser 입력의 후보2부터 확보"],
        ["P1 · GIF에 자막을 더해 색 유지", candidate("P1", 2, "RGB 변환을 expand 앞에 둔 경로") + " + " + src("PIL-POST1", "작성자 해결 보고"), "8.2.0 원 사건의 해결 방향; 전체 GIF 저장 성공을 독립 검증한 추천은 아님", "expand 뒤 변환, 다른 palette·투명도·저장 옵션", "색 보존은 이미 요구됨. 질문 반복 대신 원 GIF·동일 수행판의 양쪽 결과 확인"],
        ["P2 · 변환 직후 RGBA가 필요", candidate("P2", 2, "명시 convert('RGBA')"), "원 8.3.0 공식 분기와 명시된 출력 mode 목적; 분리 예측·사후 정답 미확인", "자동 convert()의 RGB palette.mode, 다른 alpha 입력", "RGBA 조건이 원문에 있어 그대로 답함. 원 PNG pair 출력은 아직 미확인"],
        ["P3 · p 순서대로 palette를 부착·판독", candidate("P3", 2, "raw putpalette(p, rawmode='RGB')") + " 대표; 8.3에서는 " + candidate("P3", 1, "객체 경로") + "도 제한적 묶음", "같은 p·P index1·8.3.0·getpalette 관찰. raw 경로는 게시된 8.2 비교에서도 p 유지", "8.2 객체 palette 경로, 임의 저장/변환, 다른 rawmode", "새 순서 선호와 사후 raw 경로 수용이 있으므로 재질문 없음"],
        ["팔레트 재배열 뒤 원 번호로 선택", src("PIL-CE6", "remap 구현") + " + " + src("PIL-CE1", "index 변경 원 시험"), "원 번호가 label이면 대응표 보존. RGBA만 읽는 경우와 분리", "9.1.1 RGBA remap의 alpha 손실; 원 번호 0을 그대로 class로 사용", "번호 자체로 고르나요, RGBA 색만 쓰나요? 번호→원 번호/대응표 조건과 두 링크; 색→수정판 remap과 RGBA 비교 조건"],
        ["Calc · 값 고정 또는 다음 재계산", src("CD-C01", "Paste Special 값/수식", "L64-L97") + " + " + src("CD-C04", "재계산 회귀", "L10467-L10574"), "상수 snapshot과 수식·상대참조를 따로 보존", "첫 숫자가 0으로 같은 두 셀에 이후 다른 참조값 입력", "‘값 고정’이면 바로 답함. 복사만 명시하면 참조값 변경 후 다시 계산돼야 하는지 한 번 확인"],
        ["Arrow · dictionary의 논리값 또는 raw index", src("CD-A01", "명세", "L1022-L1075") + " + " + src("CD-A02", "Transpose 원 시험", "L1177-L1322"), "논리값 소비와 index 숫자 소비를 구분; identity map에서는 둘 다 유지 가능", "nonidentity map에서 이전 index로 행 선택; index type bytes 소비", "문자열만 같으면 충분한가요, 이전 번호도 필요한가요? 값→Transpose; 번호→원 index/map 보존 조건"],
    ]

    parts = ["# AF-RES-093 · 다음 조작을 더한 링크 판정 · PARTIAL\n"]
    parts += ["## 표 1. 요청·보존값·동일 후보\n", table(["요청·원문 판", "사용자가 할 다음 조작과 보존할 값", "후보 1·2 URL과 절", "사용자판·연구판", "빠진 조건"], table1)]
    parts += ["## 표 2. 사전 A/B와 봉인 후 원근거\n", table(["요청 ID", "A 판정·근거", "B 판정·추가 필드", "봉인 후 기대값과 주소", "오병합·불필요한 분리·유보", "미확인"], table2)]
    parts += ["## 표 3. 사용자 목적에 따라 반환할 링크\n", table(["사용자 목적", "반환할 대표 또는 두 링크", "적용 조건", "틀리는 입력", "한 번만 물을 질문 또는 그대로 답할 근거"], table3)]

    parts.append("""## 분모·결원·작성 비용

**연구 상태는 PARTIAL이다.** 고정 모집 30+30건에서 첫 적격 3+3건을 골랐고 6×2 사전 판정을 모두 봉인했다. 실제 후보 쌍은 5/6, 엄격한 사후 정답은 1/6이다. 나머지 5건을 성공·실패로 대체하지 않았다. 유일한 정답은 P3의 **주어진 p·P index1 이미지·Pillow 8.3.0·getpalette 관찰** 범위다. 같은 image에 차례로 palette를 부착한 유지관리자의 게시된 비교이며, 두 fresh image의 독립 실행이나 모든 후속 편집의 성공을 뜻하지 않는다. [판정 원장](judgments.csv) · [예측을 보지 않은 별도 검토](evidence/adjudication/ADJUDICATION.md).

오병합·불필요한 분리의 주 분모는 해당 gold가 있고 **확정 판정을 한 자리**다. 유보는 오류가 아니며 성공도 아니다. 분모 0은 산출 불가다.
""")
    metrics = reconciled["metrics"]
    score_rows = [
        ["신규 요청·사전 자리", "6건 / 6자리", "6건 / 6자리"],
        ["사전 묶음 / 분리 / 유보", "0/6 · 2/6 · 4/6", "1/6 · 2/6 · 3/6"],
        ["같은 목적·판의 사후 gold", "1/6 (묶음1·분리0)", "1/6 (묶음1·분리0)"],
        ["채점 가능한 확정 판정", "0/6 (gold 있는 P3도 유보)", "1/6"],
        ["오병합", "0/0 · 산출 불가", "0/0 · 산출 불가"],
        ["불필요한 분리", "0/0 · 산출 불가", "0/1"],
        ["전체 오판 / 채점 가능한 확정 판정", "0/0 · 산출 불가", "0/1"],
        ["gold 있는 행에서 유보", "1/1", "0/1"],
        ["전체 요청에서 유보", "4/6", "3/6"],
        ["정답 결손인 확정 판정", "2/6 (I1·P2)", "2/6 (I1·P2)"],
    ]
    parts.append(table(["집계", "A", "B"], score_rows))
    parts.append("""A/B 판정은 5/6에서 같고 P3 한 건만 유보→묶음이다. 이 변화는 이미 A에도 제공된 요청의 ‘새 순서 선호’를 다시 해석한 효과와 섞여 있다. P3 B의 다음 조작 필드도 첫 출력 이후의 독립 조작보다 palette 부착 단계에 가깝다. **추가 필드가 오병합을 줄였다는 효과 크기나 새 요청에서 필드가 필요한 빈도는 산출할 수 없다.** [Pillow 해석 한계](evidence/pillow/interpretation-limits.md).

P1의 원 작성자 질적 해결보고를 충분한 정답으로 허용하면 분리 gold 1건을 별도 추가할 수 있다. A/B 모두 그 행에서 유보했으므로 주 오류 분모는 바뀌지 않는다. I1·P2의 코드/유지관리자 설명을 원판의 양쪽 실행으로 대신 세지 않았다. I3의 사전 오염 행을 제외하는 민감도에서도 채점 가능 사건수는 1이며 원 모집 분모 6은 유지한다. [민감도·귀속](evidence/posthoc-summary.json).

### 실제 저장 바이트와 빠진 필드

바이트는 `record` payload를 공백 없는 JSON UTF-8로 직렬화한 실측이다. 공통 요청 원문, 후보 원문 cache, 판정·출처 metadata는 이 값에 포함하지 않는다. 따라서 전체 조사비용이나 사람의 읽기시간이 아니다. 두 조건에 같은 후보 절을 제공했으며 B 작성 중 추가 원문 network open은 0/6이다.
""")
    cost_rows = []
    for case in cases:
        a, b = records[case, "A"]["utf8_bytes"], records[case, "B"]["utf8_bytes"]
        missing = reconciled["extra_field_slots"]["by_case"][case]["missing"]
        cost_rows.append([case, a, b, b - a, "; ".join(missing) or "null 없음; 성공 관측이 모두 있다는 뜻은 아님", "0 / 0"])
    cost_rows.append(["합계 / 요청 분모", "4268 / 6", "7449 / 6", "+3181 (+74.5%)", "후보×3필드 36자리 중 text 채움25, null11", "0 / 0 (원문 재독은 별도)"])
    parts.append(table(["요청", "A bytes", "B bytes", "증가", "B에서 채우지 못한 구조상 필드", "A/B 작성 중 추가 자료 open"], cost_rows))
    parts.append("""Inkscape 요청 본문은 각 2회 모델에 노출됐고 Pillow는 각 1회였다. Inkscape A wrapper의 `request_read_count=1`은 논리적 본문 수를 잘못 표시한 것으로, 실제 노출 2회는 [read_budget.json](evidence/inkscape/read_budget.json)에 원값을 보존한 채 정정했다. B는 같은 원문 cache를 재독했다. 후보 탐색은 이 작성 비용 밖이며 고정 공식 자료 10개와 실제 읽기 영수증에 공개했다. P2의 이후 조작 null은 사용자 요구가 변환 직후 mode에서 끝나기 때문이고, 이를 억지로 채우거나 재질문할 이유가 없다.

### 자료 하한과 사건 계보
""")
    parts.append(table(["원자료 범주", "고유 자료 / 요구 하한", "의미와 제한"], [
        ["새 요청 본문", "6 / 6", "최초 작성 당시 revision은 여섯 건 모두 완전 복원하지 못함"],
        ["판이 고정된 공식 명령·API·구현", "10 / 6", "Inkscape7·Pillow3; 같은 Image.py의 판별 절·반복 판은 중복 산입 제외"],
        ["봉인 후 원 시험·수정·후속·영상", "16 / 8", "원자료 종류 하한은 충족하나 16개의 독립 gold 또는 성공 사례가 아님"],
        ["Calc·Arrow", "8 / 4", "Calc5·Arrow3; Calc의 정확한 두 paste 후 재계산 단일 시험은 미발견"],
        ["추가 반례", "9 / 별도", "신규 여섯 건 적중에 합치지 않음"],
        ["전체", "49 고유 1차 자료", "155 원장 행 중 나머지106은 검색·중복 재검토·접근 실패·교정·metadata 등 제외"],
    ]))
    parts.append("""원문 파일/명세/후속 저작 단위는 49개, 공유 저작 계보는 47개다. 직접 원문을 연 별개 이슈 사건은 **9개**(신규6, Inkscape #2389 및 Pillow #6263·#6349)다. Calc tdf116413은 원 회귀에서 번호를 확인했으며 원 사용자 thread는 열지 않았다. 원장의 event_id 26개에는 명세·구현·시험 family가 섞여 있어 26개의 독립 사용자 사건으로 해석하지 않는다. 요청 본문과 나중 후속 thread는 별도 1차 텍스트지만 같은 사건이며, 한 issue의 댓글 여러 개는 후속 자료 하나로 묶었다. 후보 구현·수정 PR·시험이 같은 프로젝트 저작군인 경우 별도 독립 확인자의 표로 세지 않았다. 유일한 gold도 유지관리자의 게시된 비교이며 외부 독립 실행은 0건이다. [출처 원장](sources.jsonl) · [재계산](evidence/reconciliation.json).

산입한 49개에는 직접 확인 UTC가 있다. 하한에서 제외한 탐색·metadata·중복 접근 31행은 정확한 개별 접근 초를 남기지 못해 시각 범위 또는 기록 시각 상한과 미확인 사유를 보존했다. 그 시각을 새로 지어내지 않았다.

## 모집·가림·버전의 실제 범위

Q1은 Inkscape 본 저장소의 `clone/duplicate/linked` title 검색과 Pillow의 `palette/indexed/transparency` title 검색을 2021–2025 생성 UTC로 고정했다. 서버 반환을 합치고 생성 UTC·숫자 ID로 정렬했다. Inkscape는 중복 사건 제거 전31행/후30사건, Pillow는 세 질의45행/중복제거41건 중 첫30건이다. 표본을 고른 뒤 후속 자료가 없다고 바꾸지 않았다. [frame.csv](frame.csv)에는 원순번·질의·중복/제외·선택·재열람 URL이 있다. Inkscape 선행 #2379·#3629는 이미 사용한 사건으로 표시했다. 두 프로젝트 모두 첫 세 모집 사건이 본문 적격이어서 뒤27건을 기능 부적격으로 추정하지 않고 미심사로 남겼다. Inkscape #2413은 생성 시각·제목이 같은 #2407의 중복 사건으로 제외했지만, 두 본문을 추가 대조하지 못한 중복 추정이다. 이 선택은 30건 경계에는 영향을 줄 수 있으나 앞3건 선정에는 영향을 주지 않는다.

GitLab은 duplicate 검색에 duplication이 잡히는 stemming을 사용한다. 이를 보고 literal 필터를 사후 추가하지 않았다. Inkscape inbox를 초기 탐색했으나 주 모집 범위는 본 저장소로 고정했으며 그 선택은 모집 모집단의 제한이다. I3의 현재 본문에 후대 수정 문장이 보인 뒤, 그 문장이 없는 이동 전 inbox #4522 본문을 사용했다. 노출을 없던 일로 만들지 않고 contaminated=true로 보존했다. [Inkscape PRESEAL](evidence/inkscape/PRESEAL.md) · [Pillow 모집](evidence/pillow/recruitment.md).

Q2의 후보는 실제 호출이 있는 기능 쌍이다. I1은 참조 text 복사, I2는 기존 LPE target 연결/새 target 생성, P1은 변환을 expand 앞에 넣은 조합, P2는 자동/명시 mode, P3는 객체/raw palette 부착이다. I2는 첫 객체의 identity가 다르고 P1은 P/RGB mode가 다르며 P2는 첫 mode부터 다르다. 여섯 사례 모두가 ‘첫 화면까지 같다고 검증된 쌍’은 아니다. I3에는 동일 eraser 입력의 후보2가 없다. 이 표본을 시각적으로 동일한 모든 링크 쌍의 대표 표본으로 해석하면 안 된다. 정확한 호출·입력·첫 출력은 [Inkscape 후보 지원](evidence/inkscape/candidate_support.json), [Pillow 후보](evidence/pillow/candidates.json)에 있다.

Q3–Q4에서는 프로젝트별 같은 작성자가 A를 먼저 고정한 뒤 B를 썼고, B 작성자는 A와 같은 후보 원문을 보았다. 원문의 최대 두 번 열람과 B 추가 원 URL 0회는 기록했지만 독립 판정자 무작위 비교가 아니다. I2 B 초기판에 후보 절 밖 callback 설명이 들어가 검토 중 제거했다. [원값·변경 시각·영향 행](evidence/inkscape/B_revision_log.json)과 초기 B를 보존했다. A는 바꾸지 않았다. scope는 원격 `b9f8780…`, 최종 12자리 사전 판정은 `3c50d0b…`에 봉인한 뒤 댓글·수정·원 시험을 열었다. [봉인 원장](evidence/preseal-summary.json).

Q5는 A/B 예측을 보지 않은 별도 검토 에이전트가 요청·후보와 사후 원자료를 대조했다. 수집자와 검토자는 제한판 P3만 채점 가능하다는 데 일치했다. 검토자가 처음 모든 버전 호환을 목적으로 넓게 읽었다가 사전 사용판·getpalette 기준을 재확인한 과정도 [review-note](evidence/adjudication/review-note.md)에 남겼다. 이는 외부 사람의 제품 사용시험이 아니다.

## 교정 입력 두 건 — 신규 적중과 분리

**CAL-089, 선행 원장 재열람 사실.** 기본 필터의 G/L 네 쌍은 같은 두 음을 바꾸고 8/8 메뉴 실행이 값을 바꿨다. Voice 1을 제외한 보조 대조에서는 G/L의 실제 선택이 모두 비고 V가 값을 바꾸지 않았는데 L만 파란 표시가 남았다. 시각적 선택색을 실제 다음 명령의 대상과 동일하게 읽으면 틀린다. 이 연구는 MuseScore를 다시 빌드하거나 그 네 쌍을 새 A/B 적중으로 세지 않았다. [고정 원장](https://github.com/laadkke-arch/agentflow-open/blob/4f7ace747bfc5313679b8023ce85b4e7cc3217f2/docs/workstreams/research/AF-RES-089/evidence/verify.json).

**CAL-091, 선행 원장 재열람 사실.** 같은 native bytes SHA-256 `8174134afb03872bd4495a9fb4507c2ae3c92b1f52cd673c9e9298db31669aaa`를 만든 두 원 입력은 원 Point인 행이 A/101 또는 B/null로 달랐다. 위치 선택 P는 둘 다 A/101이었다. 이미 잃은 원 타입을 새 설명 필드만으로 복원할 수 없다는 정보소실 경계다. 이번에는 재인코딩·재채점을 하지 않았다. [고정 동일 bytes 원장](https://github.com/laadkke-arch/agentflow-open/blob/952c81311dc7b5917fa04af6e4513dc5fd7020b0/docs/workstreams/research/AF-RES-091/evidence/auxiliary/type-alias.json) · [이번에 읽은 교정 값·지문](evidence/calibrations.json).

## Q6 · 반례를 찾은 결과와 세 관점
""")
    parts.append(table(["반례 축", "Inkscape에서 확인·미확인", "Pillow에서 확인·미확인", "링크 판정에 주는 제한"], [
        ["화면만 필요해 둘 다 충분", src("I-CE-001", "ObjectSetTest") + "는 type·개수를 assert. duplicate/clone의 같은 픽셀 gold는 탐색 범위에서 미발견", src("PIL-POST5", "투명 info→RGBA palette 시험") + "은 convertRGBA 결과 동일 assertion", "충분함은 실제 관측값별로 제한. type 동등을 화면 동등으로 바꾸지 않음"],
        ["같은 색/스타일, 이후 선택이 다름", src("I-CE-002", "SPUse unlink") + "와 원 시험은 SPUse→SPRect, 원본 연결 소실을 지지. 같은 픽셀과 실제 selected ID 로그는 미실시", src("PIL-CE1", "remap 시험") + "은 transparency index0→1. RGBA 전체 보존은 구현에 근거한 추론", "원본 탐색이나 숫자 label 소비는 별도 조건. 보기만 같다는 이유로 묶지 않음"],
        ["이름이 달라도 편집 결과가 같음", src("I-CE-001", "unlink/unlinkRecursive") + " 기본 사각형은 type·selection count와 다음 cloneOriginal assertion 동일. numeric width/fill 결과는 미확인", src("PIL-POST3", "객체/raw palette") + "는 8.3 동일 p 판독. 모든 후속 dirty/저장 pair는 아님", "다음 조작 필드를 채웠다고 자동 분리하지 않음. 확인한 후속 관측에서 같으면 대표 가능"],
        ["원 식별자가 이미 소실", "unlink 뒤 원 연결 attrs 제거는 코드 사실. 두 동일 원본의 역사 구분 불가 paired bytes는 미발견. " + src("I-CE-003", "#2389") + "는 새 연결용 ID 생성으로 해결 가능", src("PIL-CE2", "transparent colors equal 시험") + "은 투명 검정/흰색이 같은 P index. 출력만의 숨은 RGB 역복원 불가는 추론", "새 ID 생성과 과거 원본 복원은 다른 목적. 기록 필드는 소실된 원본을 만들어내지 않음"],
    ]))
    parts.append("""반례 탐색은 성공한 사례만 남기지 않았다. Inkscape에서는 rendering_tests 목록, cli_tests/testcases 두 페이지 110항목, ObjectSetTest 및 관계 구현을 읽었지만 대응 픽셀 gold와 역사 ID 동일 bytes pair를 찾지 못했다. Pillow에서는 선택 이슈의 후속, PR5594·5599·5606, #6263·#6349·PR6350, 고정 원 시험을 읽었다. 9.1.1 RGBA remap의 alpha 손실은 ‘팔레트와 index를 같이 바꾸면 어느 판에서나 같다’는 일반화를 반박한다. Inkscape #2225의 유지관리자도 다른 객체는 같을 것이라는 설명을 다음 날 LPE 예외로 정정했다. [Inkscape 반례/미발견 범위](evidence/inkscape/post/COUNTEREXAMPLES.md) · [Pillow 반례/미발견 범위](evidence/pillow/post/counterexamples.md).

생산자는 현재 색·형상을 만족하는 출력으로 충분하다고 볼 수 있다. 편집을 이어갈 사용자는 원본 연결, 원 번호, 다음 계산값이 필요할 수 있다. 링크 목록을 정리하는 사람은 그 목적이 원문에 이미 있는지 확인한 뒤 대표를 선택해야 한다. P2의 RGBA와 #6263의 원하는 index0/1은 이미 명시되어 있으므로 그 조건을 다시 물으면 불필요한 질문이다. I2의 기존 target ID와 일반 palette 재배열의 숫자 label 소비가 비어 있을 때만 표3의 한 질문이 유용하다. 이는 **설계 제안**이며 실제 독자에게 카드를 제시한 관측은 없다.

## Q7 · Calc와 Arrow로 옮겨 본 범위

**Calc, 원 시험 판독 사실.** 24.2.7.2의 CalcPasteOnly는 `=SUM(A2:A3)`를 D1에 값으로, E1에 수식으로 붙였을 때 두 값이 0임을 확인하고 E1 수식은 `=SUM(E2:E3)`라고 검사한다. 별도 tdf116413 회귀는 산술 붙여넣기 뒤 참조 A2를 1→2로 바꾸면 수식 값이 101→102로 바뀌고 상수는 유지되는지를 검사한다. 두 자료를 합쳐 얻는 ‘값 snapshot과 재계산 관계는 다르다’는 설명은 타당한 연구자 추론이지만, 동일 두 Paste 명령을 다음 재계산까지 비교한 단일 원 시험을 확보한 것은 아니다. ucalc_copypaste 10,772행, pasteSpecial 13/13 Python 시험, 관련 ucalc/ucalc_formula 범위를 검색하고 미발견으로 남겼다. [CD-C03](https://github.com/LibreOffice/core/blob/ee3885777aa7032db5a9b65deec9457448a91162/sc/qa/uitest/calc_tests/CalcPasteOnly.py#L17-L39) · [CD-C04](https://github.com/LibreOffice/core/blob/ee3885777aa7032db5a9b65deec9457448a91162/sc/qa/unit/ucalc_copypaste.cxx#L10467-L10574) · [탐색 범위](evidence/cross-domain/exact-regression-search.md).

**Arrow, 원 시험 판독 사실과 명세 적용 계산.** 18.1.0 TransposeBasic은 dictionary `[A,B,C]`, indices `[1,2,0,0]`을 `[Z,A,C,B]`, `[3,2,1,1]`로 옮긴다. 논리 문자열은 양쪽 `[B,C,A,A]`라는 명세 적용 계산이다. 예전 index0으로 고르면 앞에서는 행2·3, 뒤에서는 빈 집합이다. 이 술어 결과는 연구자가 원 벡터에 적용한 계산이며 실행 로그가 아니다. TransposeTrivial의 identity map `[0,1,2]`에서는 기존 index도 유지되어 불필요한 분리를 막는 대조가 된다. dictionary 중복값을 허용하므로 decode된 값만 남기면 원 slot의 유일 역복원이 일반적으로 불가능하다는 부분은 추론이다. [CD-A01 명세](https://arrow.apache.org/docs/18.1/format/Columnar.html#dictionary-encoded-layout) · [CD-A02 원 기대값](https://github.com/apache/arrow/blob/6a0414bd9a91e890ec6a45369bf61f405180628c/cpp/src/arrow/array/array_dict_test.cc#L1177-L1322).

옮길 수 있는 것은 ‘소비자가 읽을 값과 다음 조작을 명시한다’는 비교 원리다. Calc의 의존관계 자동 갱신을 Arrow dictionary나 Inkscape clone에 그대로 약속할 수 없고, Arrow 논리값 보존으로 UI 선택·Undo·역사 ID 보존을 증명할 수도 없다. 타 분야는 신규 정확도 분모에 넣지 않았다. [Q7 전체 대조·세 관점](evidence/cross-domain/cross-domain.md).

## 검산·보존·다음 사용

원 행 재계산은 [audit.py](audit.py), 당시 출력은 [reconciliation.json](evidence/reconciliation.json)이다. 6×2 자리, 후보2 결원, A/B 공통 URL·판·설명, B의 추가 세 필드, UTF-8 실측, 봉인 원본 hash, frame 30+30·선택3+3, 정답/오판 분모, 출처 중복을 대조했다. 모든 결과 파일은 지정 소유 경로 안에 있다. 결과 SHA의 실제 계약·공통 검사와 GitHub 원격 재열람의 대상·종료값은 마지막 단독 [HANDOFF.md](HANDOFF.md)에 기록한다. [재현 명령·입력](reproduce.md) · [Q1–Q7 자가검토](SELF_CHECK.md) · [실제 반환 카드](cards.md).

이 연구에서 Inkscape·Pillow·Calc·Arrow를 빌드하거나 원 시험을 실행하지 않았다. MuseScore 재빌드와 GeoParquet 재인코딩도 제외했다. 같은 사용자에게 실제로 링크를 보여 준 경험, 클릭 절약, 시간 절약, 실사용 성공률은 관측하지 않았다. 작은 선택지는 보존하되 모든 링크에 항상 세 필드를 붙이라는 제품 결정을 이 자료만으로 확정하지 않는다.

## 가장 중요한 불일치·약점 — 정확히 3건

| 틀릴 수 있는 주장 | 다음 조사 대상·입력·방법 | 판정을 바꿀 관측 |
|---|---|---|
| 1. I1·P2의 분리 advisory와 P3의 제한적 묶음이 같은 판의 독립 실행에서도 유지될 것이다. | I1 원 SVG와 배포판, P2 원 PNG/8.3.0, P3 같은 p의 fresh P images를 고정한다. 각 두 경로의 첫 출력과 같은 다음 resize/mode·alpha/getpalette를 각각 기록한다. P1은 원 GIF의 전체 caption/save pair를 추가한다. | I1/P2 두 경로가 필요한 결과를 모두 유지하면 기존 분리 예측이 불필요한 분리가 된다. P3 한 경로만 달라지면 범위 내 묶음이 오병합이다. 현재 gold1/6과 미채점5/6은 이런 관측 전에는 오류감소 추정에 부족하다. |
| 2. P3의 유보→묶음은 세 필드를 더한 효과다. | 예측에 노출되지 않은 작성자들에게 같은 요청·같은 두 절·동일 열람 예산을 제공하고 A/B를 순서 교차 또는 독립 배정한다. ‘현재판 palette 목표’와 ‘모든 판 호환’을 사전에 명시하고, B의 다음 조작을 진짜 첫 출력 이후 소비로 제한한다. | A만 다시 읽어도 같은 변화가 생기거나 B에만 새 의도 해석이 들어가면 필드 효과 주장은 기각한다. 추가 필드 때문에 정당한 묶음을 분리하는 행도 함께 센다. |
| 3. 확인한 소비값 구분을 화면·임의 편집·타 분야 재계산 전체로 일반화할 수 있다. | Calc의 C03 두 paste 뒤 D2/E2 변경·CalculateHard, Arrow 동일 배열의 값/indices 선택, Inkscape 단순 clone/unlink의 render·Select Original, Pillow RGBA remap의 판별 입력을 정확히 고정한다. 원 ID/원 RGB 소실에서는 원본·map 보유 여부도 기록한다. | 첫 값이 같아도 다음 값·선택이 다르거나, identity 대조에서 모든 요구가 같거나, 원본/map이 있어 역복원 가능하면 각각 일반화 범위·분리 필요·복구 불가 주장을 바꾼다. Calc exact pair·Inkscape 픽셀/역사 ID 대조 미발견을 성공으로 채우지 않는다. |
""")
    (ROOT / "RESULT.md").write_text("\n".join(parts))
    cards = ["# AF-RES-093 · 사용자에게 반환할 링크 카드\n", "각 행은 실제 링크와 한 줄 이유, 적용 조건이다. 실제 사용자에게 제시해 검증한 카드는 아니다.\n", table(["사용자 목적", "반환할 대표 또는 두 링크", "한 줄 이유·적용 조건", "틀리는 입력", "한 번만 물을 질문 또는 바로 답할 근거"], table3)]
    cards.append("\n대표 하나를 남기는 것은 명시된 목적의 결과가 대체 가능할 때만 허용한다. 이미 있는 원문 조건은 되묻지 않는다. 안내 예측과 별개로, 적격 후보가 없거나 같은 판의 양쪽 결과가 없으면 사후 정답 미확인을 표시한다. 세부 귀속과 미확인은 RESULT.md 표2 및 judgments.csv를 따른다.\n")
    (ROOT / "cards.md").write_text("\n".join(cards))
    assert (ROOT / "RESULT.md").read_text().find("## 표 1") < (ROOT / "RESULT.md").read_text().find("## 표 2") < (ROOT / "RESULT.md").read_text().find("## 표 3") < (ROOT / "RESULT.md").read_text().find("## 분모")
    print(json.dumps({"tables": [len(table1), len(table2), len(table3)], "result_bytes": (ROOT / "RESULT.md").stat().st_size, "cards_bytes": (ROOT / "cards.md").stat().st_size}))


if __name__ == "__main__":
    main()
