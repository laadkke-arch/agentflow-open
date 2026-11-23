"""Render the fixed tables and validate the research evidence before publication."""

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence"
FIRST = "| 분야·run ID·조건 | 발행판·파일 URL·해시 | 실제 열린 경로·행·필드 | 출력 셀·원값·보고값 | 독립 정답·검증 위치 | 경로/내용/결과 기여 | 미확인 |"
SECOND = "| 같은 run ID·기록 방식 | 물은 사실 | 사전 규칙의 판정 | 검증된 정답 | 거짓 양성·거짓 음성·보류·일치 | 추가 필드·바이트 | 근거 주소·행 | 한계 |"
END = "| 불일치 또는 약점 | 영향받는 결론 | 근거 주소·행 | 다음 최소 조사 | 판정이 바뀌는 조건 |"
AXES = ["A", "K", "R", "I"]
CONDITIONS = {1: "원본", 2: "복사", 3: "헤더", 4: "경계"}
TRI_ABBREV = {"확인": "확", "반증": "반", "미확인": "미"}
SENSE = {"거짓 양성": "FP", "거짓 음성": "FN", "보류": "보류", "일치": "일치"}


def csv_rows(name):
    with (ROOT / name).open(newline="") as f:
        return list(csv.DictReader(f))


def lines_by_id(name, key):
    return {entry[key]: (line, entry) for line, entry in enumerate(csv_rows(name), 2)}


def json_lines(name, key):
    rows = (ROOT / name).read_text().splitlines()
    return {entry[key]: (line, entry) for line, entry in enumerate(map(json.loads, rows), 1)}


def row(*fields):
    return "| " + " | ".join(str(value).replace("|", r"\|") for value in fields) + " |"


def separator(header):
    return row(*(["---"] * (header.count("|") - 1)))


def ref(path, n, label):
    return f"[{label}]({path}#L{n})"


def src(sources, id, label=None):
    return f"[{label or id}]({sources[id][1]['url']})"


def load_tables():
    truth = lines_by_id("truth.csv", "run_id")
    runs = json_lines("runs.jsonl", "run_id")
    packets = lines_by_id("packets.csv", "packet_id")
    decisions = lines_by_id("decisions.csv", "decision_id")
    independent = json_lines("evidence/truth-verification.jsonl", "run_id")
    sources = json_lines("sources.jsonl", "id")
    return truth, runs, packets, decisions, independent, sources


def packet_counts(decisions):
    results = defaultdict(Counter)
    for line, decision in decisions.values():
        profile = decision["mode"]
        results[(profile, "strict")][decision["primary_outcome"]] += 1
        results[(profile, "shortcut")][decision["shortcut_outcome"]] += 1
    return results


def validation(truth, runs, packets, decisions, independent, sources):
    tests = {}

    def check(name, condition):
        tests[name] = bool(condition)
        if not condition:
            raise AssertionError(name)

    panel_ids = set(truth)
    check("main_slots", len(truth) == 16 == len(independent) and set(independent) == panel_ids)
    check("design_factorization", Counter((r["domain"], r["condition"]) for _, r in truth.values())
          == Counter({(domain, str(i)): 2 for domain in ("S", "T") for i in range(1, 5)}))
    check("observed_main", {r["run_id"] for _, r in runs.values() if r["truth_id"]} == panel_ids)
    check("all_exit_codes", len(runs) == 59 and all(r["exit_code"] == 0 for _, r in runs.values()))
    check("zero_network_and_fixture_mmap", all(not r["os"]["network_calls"]
          and all(p["mmap_calls"] == 0 for p in r["os"]["by_path"].values()) for _, r in runs.values()))
    for run_id, (_, sealed) in truth.items():
        real = independent[run_id][1]["facts"]
        check(f"truth_{run_id}", all(real[k] == sealed[k] for k in real))
        run = runs[run_id][1]
        os_paths = run["os"]["by_path"]
        opened = run["receipt"]["opens"]
        check(f"io_{run_id}", set(os_paths) == {o["path"] for o in opened}
              and all(os_paths[o["path"]]["read_bytes"] == o["bytes"] for o in opened))
        for p in ("SEL", "NON"):
            child = runs[run_id + "-" + p][1]
            check(f"pair_{run_id}_{p}", child["parent_run_id"] == run_id and
                  len([k for k, v in run["visible"].items() if v != child["visible"][k]]) == 1)
        observed = {}
        for mode, extra in [("P0", 2), ("P1", 4), ("P2", 7)]:
            packet = packets[f"PK-{run_id}-{mode}"][1]
            visible = json.loads(packet["fields_json"])
            check(f"packet_{run_id}_{mode}", int(packet["bytes"]) == len(packet["fields_json"].encode())
                  and int(packet["added_field_count"]) == extra
                  and int(packet["field_count"]) == len(visible)
                  and all(visible.get(k) == v for k, v in observed.items()))
            observed = visible
            for axis in AXES:
                d = decisions[f"D-{run_id}-{mode}-{axis}"][1]
                check(f"decision_{run_id}_{mode}_{axis}", d["truth_id"] == sealed["truth_id"]
                      and d["packet_id"] == packet["packet_id"] and d["fact"] == axis
                      and d["measured_truth_denominator"] == "1")
    check("packet_and_decision_denominators", len(packets) == 48 and len(decisions) == 192)
    actual = packet_counts(decisions)
    check("strict_totals", [actual[(mode, "strict")] for mode in ("P0", "P1", "P2")]
          == [{"보류": 64}, {"보류": 48, "일치": 16}, {"일치": 64}])
    check("shortcut_totals", [actual[(mode, "shortcut")] for mode in ("P0", "P1", "P2")]
          == [{"거짓 양성": 28, "일치": 36}, {"거짓 양성": 16, "거짓 음성": 4, "일치": 44}, {"일치": 64}])
    counted = [source for _, source in sources.values() if source["counts"]]
    check("source_identity_unique", len({record["work_id"] for record in counted}) == len(counted))
    check("source_allocations", all(record["status"] == "direct" for record in counted) and
          Counter(x["allocation"] for x in counted) == {
              "통계-발행": 5, "통계-정의·검증": 4, "교통-발행": 4, "교통-정의·검증": 5, "계보·빌드": 8})
    check("sources_not_search_snippets", all(record.get("locator") and record.get("confirmed")
          and record.get("confirmed_utc") and record.get("limits") for record in counted))
    check("failures_excluded", sum(r["status"] == "failed" for _, r in sources.values()) == 10 and
          all(not r["counts"] for _, r in sources.values() if r["status"] == "failed"))
    repeat = json.loads((EVIDENCE / "repeat-check.json").read_text())
    check("second_panel", repeat["normalized_runs_equal"] == 59 and len(repeat["byte_equal_reports_sha256"]) == 5)
    return tests


def first_table(truth, runs, indie):
    out = [FIRST, separator(FIRST)]
    for rid, (_, sealed) in truth.items():
        ln, r = runs[rid]
        iln, checked = indie[rid]
        target = r["target"]
        receipt, output, facts = r["receipt"], r["receipt"]["output"], checked["facts"]
        domain = r["domain"]
        title = f"{'통계' if domain == 'S' else '교통'} {ref('runs.jsonl', ln, rid)} C{r['condition']} {CONDITIONS[r['condition']]}"
        edition = f"[{r['edition'][:8]}]({r['publisher_url']}) D {r['distribution_sha256'][:12]}… F {r['publisher_file_sha256'][:12]}…"
        if r["condition"] == 3:
            edition += f" · probe {r['visible'][target['path']]['sha256'][:12]}…"
        if domain == "S":
            opened = "statistics.csv 386행 BX·BK 값, 진단일 키 스캔"
            extra = output["contributors"][0]["fields"]
            cell = f"{output['id']} · {extra['BX_CASE_COUNT']}+{extra['BK_CASE_COUNT']} = {output['raw']}명 → {output['report']}명"
            limitation = "관측 범위 밖 I/O·후일 확정값"
        else:
            opened = "routes 6행 route_id, calendar 2·3행 서비스·요일·기간, calendar_dates 2행 날짜·예외, trips 9–12행 trip_id·direction_id"
            if r["condition"] == 4:
                opened += " · AAMV2(10행) 제외"
            cell = f"{output['id']} · AAMV1/3 · {output['raw']}→{output['report']} trip ID"
            limitation = "실 운행·독립 발행 feed_version"
        probe = [o for o in receipt["opens"] if o["mode"] == "header"]
        if probe:
            opened = f"{probe[0]['path']} 헤더 {probe[0]['bytes']} B · " + opened
        if r["condition"] == 2:
            opened += f" · {target['path']} 열기 관측 0"
        verified = f"{ref('evidence/truth-verification.jsonl', iln, sealed['truth_id'])} · {'B-S 386행/별도 CSV' if domain == 'S' else 'B-T ZIP/별도 txt'} · SQL·strace"
        use = " / ".join("참" if facts[item] == "yes" else "거짓"
                         for item in ("path_open", "same_content_used", "reported_effect"))
        out.append(row(title, edition, opened, cell, verified, use, limitation))
    return out


def second_table(truth, packets, decisions):
    out = [SECOND, separator(SECOND)]
    for rid in truth:
        for mode in ("P0", "P1", "P2"):
            pid = f"PK-{rid}-{mode}"
            pline, packet = packets[pid]
            ids = [f"D-{rid}-{mode}-{axis}" for axis in AXES]
            votes = [decisions[id][1] for id in ids]
            ordered = lambda field: "·".join(TRI_ABBREV[value[field]] for value in votes)
            primary = Counter(value["primary_outcome"] for value in votes)
            shortcut = Counter(value["shortcut_outcome"] for value in votes)

            def fmt(count):
                return " ".join(f"{SENSE[label]}{count[label]}" for label in SENSE if count[label])

            outcome = fmt(primary)
            if mode != "P2":
                outcome += f" / 지름길 {fmt(shortcut)}"
            storage = f"+{packet['added_field_count']} 필드 +{packet['added_bytes']} B / {packet['bytes']} B"
            lo, hi = decisions[ids[0]][0], decisions[ids[-1]][0]
            evidence = (f"{ref('packets.csv', pline, pid)} · "
                        f"{ref('decisions.csv', lo, f'D-{rid}-{mode} {lo}–{hi}행')}")
            limit = {"P0": "주소와 의도", "P1": "발행 객체 바이트 대조", "P2": "통제 자식의 명시적 조회 범위"}[mode]
            out.append(row(f"{rid} {mode}", "A/K/R/I", ordered("primary_verdict"), ordered("verified_truth"),
                           outcome, storage, evidence, limit))
    return out


def limitations():
    return [
        END, separator(END),
        row("계측 대상 또는 수집 범위의 표시가 잘못되면 P2에도 오판이 생긴다",
            "P2 64/64와 로컬 미사용 근거를 운영 분석에 적용하는 범위",
            "[T1-1 누락 감도](evidence/receipt-sensitivity.json) · [PROV Usage](https://www.w3.org/TR/prov-dm/#term-Usage)",
            "캐시·네이티브 로더가 있는 별도 산출에서 외부 추적과 영수증을 대조",
            "수집 누락이 검출되면 해당 사용 판정을 보류한다. 독립 추적으로 닫힌 경로만 확인 범위에 둔다"),
        row("국소 교란에서 보고값이 같을 수 있으며 T-C4의 단일 ID 교체는 stop_times를 갱신하지 않는다",
            "읽기·입력 기여·보고 감도를 더 큰 변형과 전 피드 적합성에 적용하는 범위",
            "[S4/T4 짝](evidence/pairs.csv) · [X03/X04](evidence/contrasts.md)",
            "참조를 보존하는 보류 행의 비키 선택값 하나와 각 반올림 경계에서 독립 변형",
            "같은 변환의 유효 입력에서 달라지는 결과가 관측되면 그 변형의 R을 바꾼다"),
        row("GTFS의 2016/2026 저장소판은 같은 예제 ZIP을 재포함한다",
            "실제 운영 사업자의 독립 개정판에 대한 감도",
            "[T-A-EDITION](runs.jsonl) · [MBTA 발행 원목록](https://cdn.mbta.com/archive/archived_feeds.txt)",
            "같은 서비스일을 포함하며 게시 시각이 보존된 사업자 ZIP 두 개의 원본 확보",
            "양쪽 원본과 동일 노선·서비스일·방향을 확인하면 운영 개정판을 별도 결과로 추가한다"),
    ]


def result_text(tables, sources):
    short = lambda id: src(sources, id)
    return "\n".join(tables[0] + [""] + tables[1] + [""]) + f"""
두 표의 주 실행은 **관측 16/16**이다. 두 번째 표는 **관측 48/48 구성**, 구성별 4사실로 **192/192 판정**이다. A는 대상 경로 열기, K는 대상 행·필드 조회, R은 사전 지정한 변경에 대한 보고값 변화, I는 지목한 발행 멤버의 전체 바이트 동일성이다. 순서는 A/K/R/I이며 확·반·미는 확인·반증·미확인이다. 표 1의 세 판단은 경로 열기·산식에 들어간 동일 내용·국소 보고 감도 순서다. D는 배포 단위, F는 발행 파일/멤버의 SHA256 접두사다. 전체 해시와 후보 경로의 해시를 함께 확인할 수 있다. [입력 원장](evidence/inputs.json) · [주 실행 원장](runs.jsonl)

## Q1. 발행판과 선택 필드

**확인.** NYC DOHMH는 Git 커밋으로 발행 스냅샷을 고정한다. D는 루트 Git 트리의 raw manifest 바이트, F는 공식 CSV 전체다. 원본 행 키는 진단일 `03/19/2021`이고 두 측정은 Bronx와 Brooklyn의 일별 확진자 수다. 보고일과 기준일을 따로 둔다. 사전 68행에서 INCOMPLETE는 표시용 보조 열로 정의된다. 합과 100명 단위 반올림은 이번 통제 산식이다. {short('S01')} · {short('S03')} · {short('S10')}

GTFS 예제의 D는 ZIP 전체, F는 정확한 ZIP 멤버 `trips.txt`다. `routes.route_id=AAMV`를 `trips.route_id`와 조인하고 날짜별 활성 `service_id`와 상대 방향 0을 고른다. 기준일은 `America/Los_Angeles`의 2007-01-06이다. 예제 ZIP의 서비스 범위는 2007-01-01~2010-12-31이고 `feed_info.txt`는 없다. Cairo 예제는 `feed_version=0.5`와 서비스 시작·끝을 별도로 선언한다. MBTA도 아카이브의 효력일과 버전 이름을 별도 열로 둔다. {short('T01')} · {short('T03')} · {short('T02')} · {short('T10')}

| 이름이나 값이 같은 경우 | 확인한 차이 | 근거 |
| --- | --- | --- |
| 같은 노선명 Airport - Amargosa Valley | 방향 0의 AAMV1·AAMV3과 방향 1의 AAMV2·AAMV4 | {short('T01')} routes 6행, trips 9–12행 |
| 같은 지역 Bronx | 누적 CASE_COUNT 134314명과 CASE_RATE 9470.69명/10만 명 | {short('S05')} 2행 · {short('S11')} 117–136행 |
| 같은 값 228 | Bronx 일별 확진 건수 2021-03-14, 2021-03-20 | {short('S01')} 381·387행 |

## Q2. 실행이 본 것과 읽은 것

**확인.** 파일은 준비 단계에서 해시와 후보 목록을 만들었다. 각 새 분석 자식은 해당 local fixture에만 접근했다. GTFS 11개 멤버 중 `routes.txt`, `calendar.txt`, `calendar_dates.txt`, `trips.txt` 네 개가 주 변환에 들어갔다. `agency.txt`의 시간대와 `frequencies.txt`가 AAMV에 적용되지 않는 사실은 발행물 확인 단계에서 읽었다. 출발 횟수로 확장한 결과나 실제 운행을 추론하려면 별도 근거가 필요하다. {short('T01')} · {short('T10')} · [입력 목록과 의존](evidence/inputs.json)

**확인.** 애플리케이션 I/O 이벤트와 Linux `strace -yy`의 fixture 경로가 일치했다. C3의 probe는 통계 1377 B, 교통 74 B까지만 읽었다. 날짜/노선 후보의 바이트 파싱, 논리 필드 명시 조회, 산식에 반영된 키를 각각 남겼다. 선행 취득·캐시 읽기, 선택되지 않은 라이브러리 경로, 이 자식 외부의 프로세스와 기존 공개 소비자의 실행은 **미확인**이다. [X01–X04](evidence/contrasts.md) · [실행 영수증](evidence/execution.json)

## Q3. 정답의 독립성

**확인.** 구조 정답 `truth.csv`를 먼저 고정했다. 실행 전 원표에서 AWK가 별도 공개 표현으로 읽은 469와 831을 손으로 합해 1300을 고정했다. GTFS는 `unzip -p`와 번호화한 원표에서 1월 6일 토요일, `WE`, AAMV1·AAMV3을 대조해 2를 고정했다. 코드 실행에서도 별도 plain-line 입력·SQLite 조인으로 원값·보고값을 검산했다. 운영체제로 후보 경로를 확인했고 정확한 한 행의 사전 참조를 가로채는 별도 진단 자식으로 키 조회를 대조했다. 양성 8회는 조회 위치를 발견했고 음성 8회는 같은 조회로 들어가지 않았다. 32개 한 셀 짝의 값·관계가 봉인값과 맞았다. 별도 파일 표현은 같은 발행자 계보여서 독립 생산 관측은 **미확인**이다. {short('S14')} · {short('T01b')} · [사전 기준선](evidence/baseline.json) · [정답 검증 행](evidence/truth-verification.jsonl) · [짝 원장](evidence/pairs.csv)

## Q4. 기록 방식별 판정과 오판

| 방식 | 주 규칙 일치 / 정답 관측 | 주 규칙 거짓 양성·거짓 음성·보류 | 지름길 일치·거짓 양성·거짓 음성 / 64 | 구성당 추가 필드 | 총 JSON B / 전 단계 추가 B |
| --- | --- | --- | --- | --- | --- |
| P0 | 관측 0 / 64 | 관측 0 · 관측 0 · 64 | 36 · 28 · 관측 0 | 2 | 3520 / +3520 |
| P1 | 16 / 64 | 관측 0 · 관측 0 · 48 | 44 · 16 · 4 | 4 | 8624 / +5104 |
| P2 | 64 / 64 | 관측 0 · 관측 0 · 관측 0 | 64 · 관측 0 · 관측 0 | 7 | 38088 / +29464 |

**확인.** P1은 I에서만 16사실을 풀었다. 그중 12개는 같은 바이트, 4개는 변형 probe였다. P2는 A/K/R의 48사실을 더 풀었다. P1 동일성을 사용에 복사하면 C2의 A/K/R에서 12 거짓 양성, C4의 R에서 4 거짓 양성, C3의 A에서 4 거짓 음성이 나왔다. 주소·목적만 긍정하는 P0 지름길은 28 거짓 양성이었다. 조건부 확정판정의 오판율은 P0에서 분모 0이므로 **해당 없음**이다. 192사실에 검증된 정답이 있었고 미확인 정답은 **관측 0**이었다. 이 점수는 사전 규칙의 대조이며 사람의 판독 시험은 **미실시**다. [공개 구성](packets.csv) · [사실별 판정](decisions.csv)

## Q5. 같은 바이트와 경로 미사용

**확인.** C2 네 실행의 extra는 main과 전체 SHA256이 일치했다. extra 경로 열기는 **관측 0**, main의 같은 내용이 산식에 들어간 것은 4/4, extra의 지정 변경에 따른 보고값 변화는 **관측 0**이었다. C3에서는 probe가 실제 열렸고 내용 해시는 달랐으며 데이터 값을 조회하지 않았다. S4는 산식에 들었고 원합은 바뀌었다. T4의 AAMV2는 명시적으로 읽은 뒤 방향에서 버렸다. 파일이 열렸다는 한 문장으로는 네 상태를 구별할 수 없다. {short('P01')} · [X01–X04](evidence/contrasts.md)

## Q6. 같은 보고값과 다른 계보

| 통제 또는 공식 판 대조 | 원값 → 보고값, 기여 집합 | 확인 상태 |
| --- | --- | --- |
| S4의 선택값 469→470, 동일한 보고 구간 | 1300→1300 vs 1301→1300명. BX·BK 두 필드 유지 | 통제 두 짝에서 확인 |
| S-A-MISS, BX 값만 공란 | 1300→1300 vs 831→800명. 유효 2→1 | 통제 양성 확인 |
| NYC 3/24판→3/25판, 같은 3/19 진단일 | 469+831=1300→1300 vs 483+848=1331→1300명 | 두 공식판 확인 |
| NYC 3/20판→3/24판, 최근 공통 3/17 진단일 | 107+260=367→400 vs 485+897=1382→1400명. 3/20판의 3/19 값은 미확인 | 두 공식판과 결측 확인 |
| T-A-DIR, 01-06 방향만 0→1 | 원값/보고값 2→2 유지. AAMV1/3→AAMV2/4 | 통제 다른 계보 확인 |
| T-A-SAME와 T-A-DATE, 서비스일만 변경 | 01-07은 2와 같은 행. 01-08은 평일이라 WE가 비활성이고 관측 0 | 통제 음성·양성 확인 |
| T-A-EXCEPTION 및 비교 | 06-04 AB 방향 0은 FULLW 제거로 관측 0. 06-05는 AB1 1 | 발행된 예외 적용 확인 |
| T-A-EDITION 2016→2026 저장소판 | 서비스 구간·ZIP과 11개 멤버·AAMV1/3·보고값 2 동일 | 별도 개정 feed_version 미확인 |

자료의 기준일과 발행일, 더 작은 원값과 보고 단위를 함께 붙여야 같은 숫자를 올바르게 비교할 수 있다. Eurostat의 2024-12 유로지역 실업률 6.3%→6.2%는 별도 공식 보도표의 개정이다. 두 형식의 통계 원 API 파일은 실행 환경에서 미확인으로 유지했다. {short('S01a')} · {short('S01')} · {short('S01b')} · {short('S04')} · {short('S06')} · {short('T01a')} · [대조 원장](evidence/contrasts.md)

## Q7. 목적별 최소 기록과 비용

| 목적 | 조건부 제안 | 확인 범위와 남는 항목 |
| --- | --- | --- |
| 분석 재현자 | 같은 run·출력 ID, 발행판과 실제 경로 입력 해시, 변환·키·단위·결측 규칙을 보존한다. 미사용을 주장하려면 독립적으로 확인한 계측 범위가 필요하다. | P2로 48/48 A/K/R을 판정했다. T1-1의 사용 항목이 빠지면 보류하며, 완전하다고 잘못 표시하면 A/K/R에 거짓 음성 3건이 생긴다. [누락 감도](evidence/receipt-sensitivity.json) |
| 현재 자료 재사용자 | 주소와 목적에서 출발해, 현행 판·기준일·단위·정정 사유를 확인한다. 선택 셀을 계산해야 할 때 변환을 더 조회한다. | P1의 16 I는 당시 바이트 귀속 판단이다. 현행 판의 적합성은 발행자의 정정 정책이 필요하다. {short('S03')} · {short('T14')} |
| 원자료 발행자 | 판 목록·배포와 멤버 식별·효력 범위·정오를 우선 제공한다. 소비자가 사용을 보고할 때 공동 입력·결과 식별자로 연결한다. | 보관된 판은 나중에 교체될 수 있다. 공개 배포 목록의 일치와 소비 실행의 열기·필드 기여를 각각 확인한다. {short('T02')} · {short('T05')} |

**확인.** P0→P1은 구성당 319 B를 추가해 I 16개를 해결했다. P1→P2는 구성당 평균 1841.5 B를 추가해 A/K/R 48개를 해결했다. P2 합계는 38088 B, 구성별 1187~3606 B다. 측정값은 공개 canonical UTF-8 JSON이며 별도 strace·사전 기준·서명·보관본 및 판독 노동의 비용은 **미확인**이다. [바이트 원장](packets.csv) · [수용 원장](evidence/acceptance-evidence.json)

**다른 분야 직접 대조.** PyPI의 urllib3 2.5.0 wheel은 실제 129795 B를 해시해 publish 영수증의 SHA256과 맞췄다. predicate가 null이므로 확인되는 주장은 발행자와 파일이다. npm의 @sigstore/verify 2.1.1은 실제 15807 B tar의 SHA512와 두 발행·빌드 statement의 subject가 일치한다. 빌드 영수증에는 invocation과 Git 소스 한 건이 있고, 같은 커밋의 workflow는 npm ci를 명세한다. 어떤 로컬 패키지 파일이 산출물에 기여했는지는 두 자료로 확인되지 않았다. Debian의 Installed-Build-Depends는 정확 버전의 설치 환경과 후보 대안까지 담고, SLSA의 resolvedDependencies 완전성은 best effort다. 두 실제 영수증의 서명 신뢰 사슬 검증은 **미실시**다. {short('P05')} · {short('P06')} · {short('P07')} · {short('P02')} · {short('P03')} · [원문 디코딩과 산출 해시](evidence/attestation-check.json)

**의존 작업 배경.** AF-RES-047은 기존 소비자 우선 6건에서 발행판 4, 특정판 사용 선언 1, 원 실행의 외부 입력 연결 0, 선택 필드 독립 검증 0이었다. 실행 기록 우선 2건의 외부 입력 연결은 1, 선택 필드 독립 검증은 0이었다. 이번 16개 새 통제 실행과 분모를 합치지 않았다. [047 당시 인계](https://github.com/laadkke-arch/agentflow-open/blob/a6ef2b0bcb6412d9e6fa7a9eb59b5e863c621ff0/docs/workstreams/research/AF-RES-047/HANDOFF.md)

직접 열람 기록은 42행이다. 독립 배당으로 인정한 고유 원문은 **26/22**이며 통계 발행 5/4, 통계 정의·검증 4/4, 교통 발행 4/4, 교통 정의·검증 5/4, 계보·빌드 8/6이다. 같은 저작의 판·표현·문서가 원자료를 인용한 관계는 소급 연결했다. 실패는 10행이고 배당에서 제외했다. [직접 열람과 실패 원장](sources.jsonl)

""" + "\n".join(limitations()) + "\n"


def acceptance(table1, table2, tests, sources):
    counts = Counter(r["allocation"] for _, r in sources.values() if r["counts"])
    items = []

    def item(id, status, num, denom, unit, evidence, reason=None):
        items.append({"id": id, "status": status, "numerator": num, "denominator": denom,
                      "unit": unit, "evidence": evidence, "unmet_reason": reason})
    item("sources_unique", "충족", sum(counts.values()), 22, "credited distinct primary works", ["sources.jsonl"])
    for kind, required in [("통계-발행", 4), ("통계-정의·검증", 4), ("교통-발행", 4),
                           ("교통-정의·검증", 4), ("계보·빌드", 6)]:
        item(kind, "충족", counts[kind], required, "credited distinct works",
             [f"sources.jsonl:{line} {id}" for id, (line, source) in sources.items()
              if source["counts"] and source["allocation"] == kind])
    item("frozen_order", "충족", 2, 2, "pre-observation commits",
         ["30f92ecc300b0579b6aa37f2147d14ad180c4355 SCOPE/truth",
          "4fdcb35b9134f41a59fef08fd8dabe5d8b875d76 inputs, baseline and sources"])
    item("main_panel", "충족", len(table1) - 2, 16, "main executions", ["RESULT.md:1–18", "runs.jsonl"])
    item("packet_comparisons", "충족", len(table2) - 2, 48, "run-mode configurations",
         ["RESULT.md:20–69", "packets.csv:2–49"])
    item("facts_against_verified_truth", "충족", 192, 192, "verified decisions",
         ["decisions.csv:2–193", "evidence/truth-verification.jsonl:1–16"])
    item("controls_identical_unopened_and_header_only", "충족", 8, 8, "C2+C3 main executions",
         ["RESULT.md table 1 C2/C3", "evidence/contrasts.md X01–X02", "runs.jsonl os.by_path"])
    item("truth_lookup_diagnostics", "충족", 16, 16, "separate trapped/negative probes",
         ["runs.jsonl independent.field_trap"])
    item("independent_numbers", "충족", 16, 16, "main numerical checks",
         ["evidence/baseline.json B-S/B-T", "runs.jsonl independent", "independent.py"])
    item("paired_perturbations", "충족", 32, 32, "one-cell variants", ["evidence/pairs.csv:2–33"])
    item("supplemental", "충족", 11, 11, "sensitivity runs outside main", ["runs.jsonl:49–59", "RESULT.md Q6"])
    item("publisher_same_reference_dates", "충족", 2, 2, "domains with publisher snapshot pairs",
         ["evidence/inputs.json", "S-A-NEXT in runs.jsonl", "T-A-EDITION: two Git snapshots of the same ZIP"])
    item("independently_changed_transit_feed_release", "미확인", 0, 1, "changed actual official feed with same service date",
         ["evidence/contrasts.md X07", "sources.jsonl T02/T14/F06"],
         "Identical example ZIP at two Git pins. A matching original agency pair was outside the analyzed main sample.")
    item("attestations", "충족", 2, 2, "published receipts with actual artifact hash match",
         ["evidence/attestation-check.json", "sources.jsonl P05/P06"])
    item("cold_repeat", "충족", 59, 59, "run rows rechecked with new processes",
         ["evidence/repeat-check.json excluding timestamps only"])
    item("questions", "충족", 7, 7, "Q1–Q7 answers and contrary evidence", ["SELF_CHECK.md:3–11", "RESULT.md Q1–Q7"])
    item("limits_final", "충족", 3, 3, "closing weakness rows", ["RESULT.md last table"])
    item("fixed_result_remote_reread", "후속 영수증 예정", None, 2, "files at committed RESULT SHA",
         ["evidence/final-check.json"], "Runs after the result commit.")
    item("workbench_check_fetch", "후속 영수증 예정", None, 1, "actual command exit status",
         ["evidence/final-check.json"], "Runs after the result commit.")
    return {"task_id": "AF-RES-051", "panel_units": {"main": 16, "packet_views": 48, "fact_predictions": 192},
            "structural_checks_passed": len(tests), "criteria": items}


def main():
    truth, runs, packets, decisions, indie, sources = load_tables()
    tests = validation(truth, runs, packets, decisions, indie, sources)
    table1 = first_table(truth, runs, indie)
    table2 = second_table(truth, packets, decisions)
    assert len(table1) == 18 and len(table2) == 50 and len(limitations()) == 5
    report = result_text((table1, table2), sources)
    assert report.startswith(FIRST) and report.rstrip().endswith(limitations()[-1])
    (ROOT / "RESULT.md").write_text(report, encoding="utf-8")
    verdict = acceptance(table1, table2, tests, sources)
    (EVIDENCE / "acceptance-evidence.json").write_text(json.dumps(verdict, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(tests)} evidence checks passed; main/packet/fact shapes 16/48/192.")


if __name__ == "__main__":
    main()
