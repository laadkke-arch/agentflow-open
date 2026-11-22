#!/usr/bin/env python3
"""Render the required Korean research report from the audited local ledgers."""
import csv
import json
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
D = [json.loads(line) for line in (BASE / "decisions.jsonl").read_text().splitlines()]
S = {row["source_id"]: row for row in json.loads((BASE / "sources.json").read_text())}
ST = json.loads((BASE / "evidence/statistics.json").read_text())
C = list(csv.DictReader((BASE / "costs.csv").open()))
BY = {row["id"]: row for row in D}
CC = defaultdict(list)
for row in C:
    CC[row["case_id"]].append(row)


def cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def table(headers, rows):
    return "\n".join(["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"] +
                     ["| " + " | ".join(cell(value) for value in row) + " |" for row in rows]) + "\n"


def link(label, url):
    return f"[{label}]({url})" if url else label


def source(source_id, location=True):
    row = S[source_id]
    return link(source_id, row["url"]) + (" — " + row["location"] if location else "")


def date(record):
    if record.get("date_range"):
        interval = record["date_range"]
        if isinstance(interval, dict):
            start, end = interval.get("start", "미확인"), interval.get("end", "미확인")
        elif isinstance(interval, list) and len(interval) >= 2:
            start, end = interval[0], interval[1]
        else:
            start, end = record.get("date") or "미확인", str(interval)
        display = str(start) if start == end else f"{start}~{end}"
        return f"{display} ({record.get('precision', 'range')})"
    return f"{record.get('date') or '미확인'} ({record.get('precision', 'unknown')})"


kind = {"explicit_unaware": "명시 미인지", "first_introduction": "대화에서 소개", "known_reassessment": "기지 재평가",
        "known_rejected": "기지 거절", "mere_mention": "언급", "unknown": "인지 미확인"}
outcome = {"retained": "유지", "replaced": "대체", "partial_adoption": "일부 채택", "trial_reverted": "시험 후 철회", "change_unconfirmed": "변경/시행 미확인"}
rows1 = []
for row in D:
    options = []
    for option in row["alternatives"]:
        state = {"yes": "조건 확인", "no": "당시 조건 불충족/후발", "unknown": "미확인"}.get(option["available_at_decision"], option["available_at_decision"])
        options.append(link(option["name"] + " " + str(option.get("version", "")), option.get("url")) + f" [{state}]: " + option.get("condition", "") +
                       ("; " + option["availability_timeline_note"] if option.get("availability_timeline_note") else ""))
    aware = []
    for a in row["awareness"]:
        aware.append(link(a["actor"] + "(" + a["role"] + ")", a["url"]) + " " + kind.get(a["kind"], a["kind"]) + ": " + a["summary"] + "; " + date(a))
    audit = row.get("initial_awareness_audit")
    if audit:
        aware.append("초기 표적 인지=" + ("기지" if audit["baseline_known"] is True else "미확인") + "; 생애 최초일 미확인")
    rows1.append([
        row["sample"] + "·" + row["id"],
        link(row["title"], row["original_url"]) + "; " + row["need"]["text"] + "; 필요 기록 " + date(row["need"]) +
        ("; 구체 공개 제안 " + date(row["proposal"]) + " " + link("제안 원문", row["proposal"].get("url")) if row.get("proposal") else ""),
        "; ".join(options), "; ".join(aware),
        row["initial_choice"] + " → " + row["final_choice"] + " [" + outcome[row["outcome"]] + "]; " +
        link("후속", row["implementation"].get("url")) + " " + date(row["implementation"]) + "; " + row["implementation"].get("summary", ""),
        "; ".join(row["competing_explanations"]),
        "; ".join(row["unknowns"]) + "; 최소 추가 입력: " + row["minimum_next_record"]
    ])

rows2 = [
    ["A·F1 보존 ADR/RFC", "상한 전9 검토·관리절차1 탈락·8 채택; 이후28 보류", "공개 필요/제안일8; 발견 양성으로 승격0", "표적 결정자0; A06 초기 최종기능 인지 불명", "기지 제약 교정+시행 A01 1", "초기 기지6/8; 공개 API 거절·내부 재사용 A07은 후속 확인", "A06 최종 AAD 기능1; 초기 필요 자체도 불명", "초기인지2(A06,A07), 시행1(A04)", "보존 문서 선택8; 조직 전체 제안의 분모 아님"],
    ["A·F2 Apache 제안/메일", "9 검토·FLIP32를A12와 중복1·8 채택", "공개 제안/원장 생성8; 발견 승격0", "표적 해법 미인지0; 요구 미고려 A09는 별도", "기지 검토/설계변경이 있으나 엄격 발견사슬0", "초기 기지7/8; A09도 후속에서 RocksDB 거절", "A09·A15에 후발 보조기능2; 초기 표적 전체를 후발로 바꾸지 않음", "초기인지1(A09); 최초 공개코드8", "동결 page-created 순서의8; 메일 전체 모집단 아님"],
    ["A·F3 조직 RFC PR", "11 검토·오탈자/관리3 탈락·8 채택", "초안 author timestamp와 PR 생성8; 발견 승격0", "결정자0; 리뷰어만1(A21)", "기지 명세 제약 교정+시행 A19 1", "초기 기지8/8; Criterion(A20)·write_bytes(A22) 이미 검토", "새기능 후발 A18,A20,A21,A22 4; 각각 기존 대안은 별도", "시행3(A17,A22,A24); 사적 최초필요8", "첫 연속 적격8; 기각·미실행 포함"],
    ["A 합계", "29 검토·5 제외(중복1 포함)·24 채택; 보류28", "공개날짜24; 미인지 양성 대체0", "표적 결정자0/24; 리뷰어1 별도", "엄격 미인지 인과0/24; 기지 제약 교정2/24", "초기 표적 기지21/24; 거절·부분 재사용은 표1", "최종 표적의 후발 조건 A06을 미확인 범위에서 분리", "초기인지3/24→당시조건 가능2/24; 시행4/24", "주 분모24; 자료 없는 팀으로 외삽 금지"],
    ["B·GitHub 토론/PR", "목적선정8; 경로별 후보는 아래 합계와 sampling.csv", "원문 생성·수정구간; 인지일 대체 금지", "결정자3(B01,B02,B09)+요청자1(B04)", "기지재평가 B05,B06; 소개 B03; 시험 B07", "자체범위/요구/교육 유지 B01,B02,B09", "B01 KWP·B06 Azure 후발2; B02는 기능 불일치", "B03·B04 실제채택, B09 운영시행 등 미확인", "목적선택8의 사례구성; 발생률 아님"],
    ["B·당사자 회고", "1 채택 B08; 원문/후속코드 별도", "3월2일 코드 표제와3월3일 글 공개 구별", "결정자1 B08", "미인지→출력 경계 부분변경+코드1", "탐색·비교 구조 유지; 후속판에 YAML 추가", "후발 아님; 두 JSONEncoder 호환 구현 존재", "실제 import 환경·시간 절감 미확인", "목적선택1; A에 더하지 않음"],
    ["B 합계", "후보URL257: 채택9·직접열람탈락2·차단1·검색만245; 017중복1은 검색만245의 일부", "계보별 날짜 정밀도 보존", "결정자4/9+요청자만1; 둘을 합친 팀 빈도 없음", "엄격1(B08); 재평가포함 연결2(B05,B08)", "유지 후보3이나 생산 자체구현 엄격유지0", "후발2·요구불일치1 분리", "후속연결 단절과 최초인지일 불명은 원장 보존", "B9 고유추가; 목적표집. A/B 합산비율 금지"],
]

transfer = {
    "A01": "Kubernetes envelope/annotation 타입 관계→catalog 검증; 같은 소프트웨어 생태계의 부분 재사용",
    "A07": "공개 mount API와 내부 라우터를 분리; 외부 라이브러리 전체 API 결합을 피함",
    "A09": "TTL 갱신·삭제·가시성의 관계를 자체 상태 API에 맞춤; 다른 분야 기원 아님",
    "A12": "다른 구현 Blink의 실제 기여와 Java/Scala 모듈 경계; 다른 생태계 구현/코드 기여",
    "A19": "CommonMark destination 문법→rustdoc 이름 해석; 같은 분야 명세 호환",
    "B05": "라이선스·오프라인 렌더링·정적 출력 조건; 외부 plotting 생태계 재사용",
    "B08": "출력 직전 확장점으로 직렬화 위임; Path 의미는 내부 유지, JSON 경계만 변경",
    "B09": "엔진의 격리 설정과 pool hook의 역할 구별; 교육용 hook은 별도 목적",
}
rows3 = []
for row in D:
    records = CC[row["id"]]
    values = [r["value"] + " " + r["unit"] + " [" + r["cost_kind"] + "; " + r["scope"] + "]" for r in records if r["value"]]
    reporters = [r["reported_by"] + "; " + (r["reported_date"] or "진술일 미확인") for r in records if r["value"]]
    rows3.append([row["id"], "; ".join(values) or "투입·절감 수량 미보고/미확인",
                  "; ".join(reporters) or "수량 보고한 결정자 기록 없음",
                  "; ".join(link(r["cost_id"], r["url"]) + ": " + r["avoided_cost_evidence"] for r in records),
                  transfer.get(row["id"], "타 분야 구조 전이 확정 없음; " + records[-1]["reused_work"]),
                  "; ".join(dict.fromkeys(r["limitation"] for r in records))])
rows3.extend([
    ["X-P1 / CF-P1", "인시 미확인; 보조 청구항 수정", "공식 심판2018-06-05", source("CF-P1"), "선행자료 지적 뒤 청구 범위 추가는 관측; 절차상 미수용", "제품 설계·구현·절감과 동일시 불가; 원 통지/청구 diff 없음"],
    ["X-P2 / CF-P2", "추가 검색료6개 환급; 금액/개발시간 미계량", "공식 심판2018-04-16", source("CF-P2"), "청구 발명 통일성 논증을 유지해 재판단; 별도 수정 청구 세트 존재", "최종 청구문구가 전혀 안 바뀌었다고 말할 수 없음"],
    ["X-E1 / CF-E1", "97분·100분 회의; 4,594발화; 회귀N938", "Chan·Schunn2014 원 관찰연구", source("CF-E1"), "먼 유추→연속 국소 개념 탐색; 실제 팀1, 동일 자료 재분석", "147/144유추 서술 불일치; 개념생성은 채택·노동절감 아님"],
    ["X-E2 / CF-E2", "학생34, 녹음30/9팀; 10초 구간;22.1%는 한 팀 활동구간", "Cheong·Hallihan·Shu2014 원 연구", source("CF-E2"), "효소 결합 형상/환경 활성조건→연결/분해 허용조건 두 관계", "활동구간·팀·문제 분모 분리; 생산설계 구현 관측 없음"],
    ["X-S1 (A/B 밖)", "263%→4%는 활용률 계산모형; 노동·실측절감 아님", "Shopify 운영자2020; 공급자 코드2020; 전기문서2018", source("CF-S1") + "; " + source("CF-S3") + "; " + source("CF-S5"), "누적 오류/과전류→차단; 차단 상태→추가 부하 차단, 복구시험/리셋은 조건 차이", "실제 전기문서를 읽었다는 계보 없음; 확인된 경로는 Hystrix/Release It. 등 소프트웨어"],
])

qrows = [
    ["Q1", "결과 비조건 표집 A24와 발견 목적표집 B9 분리", source("ADR-I01") + "; sampling.csv F2/F3; SCOPE 동결commit", "A 29심사→24, B9고유; A/B중복0·017재산입0", "A의 미병합/미실행 A17,A22,A24도 유지; F1 생존편향 기록", "완전 맹검·무작위 표본 아님; 삭제/비공개 결정을 포함할 조직 원장 필요"],
    ["Q2", "공개 필요·초안·공식 수용·발견·시행은 다른 날짜", source("RUST-D01") + "; " + source("RUST-I2285") + "; " + source("AP-M31-ORIG"), "A 사적최초필요24/24·최초공개코드24/24 미확인; 실행 범위확인20/24", "A19 구현이 공식수용보다 먼저; A15 메일이 원장 생성보다 먼저; B09 주석 날짜≠운영", "메시지 revision·실제 push·작업 시작 로그 필요; timeline.csv 전 행"],
    ["Q3", "현재 존재는 과거 가용성과 다름; 필요한 기능·조건 단위 판정", source("ADR-V04") + "; " + source("B-022") + "; " + source("RUST-V13") + "; " + source("B-008"), f"공식판 산입 {ST['sources']['categories'].get('version',0)}건; B01/B06후발, B02요구불일치", "A06최종AAD는동일작성자공동개발; A18custom names는2021stable", "tag author date≠공개/안정판/팀승인일. 당시 설치·정책·자격 로그 필요"],
    ["Q4", "해법 존재 미인지와 제약 교정, 소개자와 결정자 구별", source("RUST-F04") + "; " + source("RUST-F05") + "; " + source("B-027") + "; awareness-audit rows A01–A24", "A표적미인지0/24; 초기기지21/24·미확인3/24; B명시결정자4,요청자만1", "Criterion 선행검토; A21리뷰어미인지; B04요청자·유지자 역할 분리", "생애최초인지24/24불명. A06최종기능 후발 분리 후 U=A07,A09"],
    ["Q5", "발언·문서수용·범위 있는 시행을 따로 대조", source("ADR-F07") + "; " + source("B-024") + "; " + source("B-030") + "; " + source("RUST-T49802"), "A엄격양성0/24; B엄격1(B08), A/B연결4; B03계획만", "후기유지·소개후미변경·외부시험철회18개 검색; B02후속이 초기낙관 반박", "B09운영·B03설정·A24완료 미확인; 6연결 목표 미달"],
    ["Q6", "관측 숫자와 조기 링크의 회피 비용은 별도", source("AP-J31") + "; " + source("B-020") + "; " + source("B-023") + "; " + source("B-001"), "A투입로그1/24·B직접투입2/9; 수량적 인과절감 확인0/24,0/9", "13h50m 귀속불명; 하루/약1시간/4일의 작업 범위 서로 다름; 재사용 보존", "같은작업의 시간기록·폐기/재사용diff·당사자 반사실 설명 한 묶음 필요"],
    ["Q7", "구조 대응과 역사적 유입 인지는 별개", source("CF-P1") + "; " + source("CF-P2") + "; " + source("CF-E1") + "; " + source("CF-E2"), "타분야2×2원문; E1팀1, E2녹음9팀; X-S1은추가A/B아님", "청구수정 미수용·통일성유지, 유추가 큰도약 아닌 국소개념탐색, 구조유사와직접전이 분리", "EPO원심사dossier403; 전기→Semian최초인지/사후명명새사례 미확인"],
    ["Q8", "조건을 충족한 구체적 결정 경계에 링크; 효과 크기는 미확인", source("ADR-T01") + "; " + source("RUST-V01") + "; " + source("B-038") + "; " + source("B-031"), "A관측하한0/24; 인지기록완성 시나리오0~2/24; 인과상한 아님", "B08/B09, B05/B06, B02/A07, B07/B03의 채택·유지 짝", "그날 이용가능한 링크라도 사적 고민을 외부에서 볼 수 있었는지 별도. 효과·제품절감 외삽 금지"],
]

out = ["# AF-RES-022 · 늦게 알게 된 해법이 실제 선택을 바꾼 조건\n"]
out += ["## 표 1 · 선택·인지·실행의 사례별 대조\n", table([
    "표본 A/B·사건 ID", "원 결정·목적·날짜 정밀도", "당시에 가능한 대안·판", "인지 주체·진술·시점",
    "이전→이후 선택·실행 근거 주소", "경쟁 설명", "미확인"], rows1)]
out += ["## 표 2 · 모집 경로와 해석 가능한 분모\n", table([
    "표본·기록 계열", "검토·탈락·채택 수", "날짜 대리", "명시 미인지", "발견·재평가", "기지 거절·유지", "후발 제공", "판단 불가", "해석 가능한 분모"], rows2)]
out += ["## 표 3 · 비용·재사용·전이 조건\n", table([
    "사건 ID", "관측한 비용·단위", "비용을 보고한 사람·날짜", "실제로 피했다는 근거 또는 반증 주소", "전이한 관계·적용 조건", "미확인"], rows3)]
out += ["## 표 4 · 질문별 주장과 반증 가능한 근거\n", table([
    "Q 번호", "주장·판정 범위", "근거 자료 주소·정확한 위치", "확인한 내용·분자와 분모", "반례를 찾은 경로·결과", "미확인·결정을 바꿀 자료"], qrows)]

out.append(f"""## 핵심 판정과 읽는 방법

**인계 판정은 REVIEW_READY_WITH_GAPS다.** 결과를 선정 기준에 쓰지 않고 날짜순으로 고른 공개 선택 A24에서, 결정자가 외부 해법을 몰랐다는 직접 진술·당시 가용성·발견 때문에 바뀐 선택·후속 시행까지 이어진 엄격 관측은 **0/24**다. 이것은 실제로 그런 일이 없었다는 뜻이 아니다. 동일 기준으로 원 의도부터 후속 시행을 잇되 기지 제약의 교정도 포함하면 A01·A19 **2/24**가 남는다. 발견 경로를 의도적으로 찾아 모은 B9에서는 B08 **1건**이 엄격 조건을 충족한다. B05의 기지 재평가를 더한 B 연결은2건이다. A/B의 발생률을 합치지 않는다.

표적 해법을 초기 공개 선택에서 이미 알았다는 근거는 A **21/24**, 미확인은 **3/24(A06,A07,A09)**다. A06의 최종 필요 기능은 뒤에 제공되었고, 그 요구 자체가 최초안에서 확정돼 있었는지도 불명이다. 이를 별도로 두면 당시 기능 조건을 갖춘 인지 기록완성 후보는 **A07·A09 2/24**다. 모두 음성/모두 양성으로 가정한 **0/24~2/24(0~8.3%)는 인지 기록만 완성하는 조건부 시나리오**다. A07의 발견 인과는 불명이고 A09는 대안을 거절했으므로 엄격 인과효과의 상한이 아니다. 생애 최초 인지일은24/24 미확인이며 이 수를 초기 해법 미인지 수로 바꾸지 않는다. 정의와24행 재판정은 [인지 감사](streams/apache/awareness-audit.md), 기계 집계는 [statistics.json](evidence/statistics.json)에 있다.

직접 읽은 자료 원장은 **{ST['sources']['ledger_rows']}행**, 보수적 최소 산입은 **{ST['sources']['counted_unique_originals']}개 원문**이다. 당시 결정/제안 {ST['sources']['categories'].get('decision',0)}, 별도 후속 {ST['sources']['categories'].get('followup',0)}, 공식 과거판/조건 {ST['sources']['categories'].get('version',0)}, 두 타 분야 {ST['sources']['categories'].get('crossfield_patent',0)+ST['sources']['categories'].get('crossfield_engineering',0)}, 기타 원문 {ST['sources']['categories'].get('other',0)}다. 자료 수는 독립 사건 수가 아니다. 동일 PR의 여러 댓글·동일 파일의 여러 판·발표와 구현의 관계는 계보로 묶었다. 산입/제외 이유와 사실·당사자 진술·이번 실행·연구자 해석은 [sources.json](sources.json)에, 검색만 본 후보와 차단은 [sampling.csv](sampling.csv) 및 stream search-log에 있다.

관측 창은 최초 공개 선택2018–2024, 후속 확인은2026-11-22 UTC까지다. 역사판 코드·공식릴리스·동시대 메일과 현재 회고를 구별했다. 모든 A의 사적 최초 필요와 전체 저장소를 통틀어 가장 이른 공개 구현은 미확인이다. 이 조사에서 읽은 가장 이른 구현, 병합, 특정 릴리스는 별도 확인했다. **문서 Accepted/PR merge가 곧 기능 배포라는 코딩은 하지 않았다.** 표1의 대체/유지 역시 명시된 후속 범위만 뜻하며 이후 영구 유지나 모든 배포를 보증하지 않는다.

## Q1. 결말과 독립적으로 선택한 기록은 무엇인가?

동결 커밋은 `00c2a14633e7503880f4aceb7c4909845298b3d7`이다. [SCOPE.md](SCOPE.md)에 달력 구간·적격 규칙·정렬·시작점·프로젝트당 상한을 먼저 저장했다. F1은 Backstage 보존 ADR와 Kibana의 과거 RFC, F2는 Apache Flink의 제안 페이지 원장에 연결된 메일·표결, F3는 Rust 조직의 설계 검토 PR이다. 같은 GitHub 호스트를 쓴다고 같은 원장 유형으로 취급하지 않았지만, 네 공개 프로젝트의 문화·규모가 일반 팀을 대표한다고 보지도 않는다.

F1은 각 프로젝트 최초 공개 제안 시각순으로4건씩 골랐다. Backstage 고정판 `ffe93e7…`의 `docs/architecture-decisions/` 파일 목록과 그 기록 절차를 설명하는 `index.md`, Kibana `dd31e406…`의 `legacy_rfcs/README.md`를 확인했다. Backstage index 본문 자체가14개 파일을 열거하는 것은 아니며 같은 고정판 디렉터리 목록을 함께 사용했다. 현재 Kibana의 workflow ADR들은2024년 이후라 역사표본에 쓸 수 없었다. 전환을 숨기지 않고 공개 과거 RFC 원장으로 고정했다. 상한 전9개 가운데 관리 절차 ADR001을 제외했고8개를 포함했다. 이후28개는 ‘검토 후 부적격’이 아니라 상한 뒤 보류다. A02/A03은 export 이름만 고친 문체 사례가 아니라 외부 공개 API와 실제 재수출 경계를 바꾸는 구현 선택으로 포함했다. {source('ADR-I01')}.

F2는 메일 날짜순이라고 가장하지 않는다. 동결 CQL의 **제안 페이지 생성순**에서 FLIP25–33을 검토했다. FLIP28과32는 Java/Scala 모듈·Blink 통합으로 이어지는 같은 선택 A12라 중복을 묶었고 다음33을 포함했다. 페이지가 비어 있거나 다른 템플릿이던 판과 최초 실질 판을 비교했다. 실제 원 제안일은 연결 메일에서 따로 복원했다. 예컨대 A15는2019년 페이지 생성보다 앞선2018-08-27 메일이 있으며 Message-ID는 `35ed5893-6f6b-47fb-9df2-49832bd6b4d2.wangzhijiang999@aliyun.com`이다. {source('AP-M31-ORIG')}.

F3는2018-01-01부터 생성순인 처음11개 PR 중 오탈자/관리3개를 제외한8개다. 채택된 언어 제안만 남기지 않았으므로 A17·A22의 거절과 A24의 완료 구현 미확인이 분모에 남는다. 초안의 header Start Date, commit author timestamp, PR 공개 생성일을 섞지 않았다. 사례별 선정 순번·제목·URL·탈락·중복은 sampling.csv로 재현한다.

B는 발견·재평가·거절의 언어를 직접 찾는 별도 경로다. GitHub 토론/PR과 당사자 회고에서9개의 고유 선택을 얻었다. 검색 후보257개 중245개는 제목/요약만 본 탐색 기록으로, 원문 심사나 부정 사례로 세지 않았다. 직접 읽고 제외한2건은 mbmd와 DeSmuME다.017의 Pendo 중복1건은 검색만 본245개에 포함되며, 기존 고정 입력과 대조해 제외했으므로 새 원문 열람으로 세지 않았다. A/B 중복0은 프로젝트 이름만 다른지 검사한 값이 아니라 같은 팀의 같은 선택과 연결 문서를 대조한 결과다. 017의40행과7기원,020의B21은 입력과 중복 대조용이며 새 원문·사례 수에 넣지 않았다.

한계는 남는다. F1은 보존된 문서의 생존편향이 있고, F2는 제안 작성자가 먼저 문서화한 선택을, F3는 공개 검토 가능한 설계를 본다. 비공개 구매와 폐기된 제안, 대안을 알 필요가 없었던 팀은 관측하지 못했다. 또한 제목·메타데이터에서 부수적으로 상태가 보였으므로 실험적 맹검이라고 부르지 않는다. 결과·미인지·revert를 선정 규칙에 쓰지 않은 표집이다.

## Q2. 선택 당시 어떤 질문을 했고, 어느 날짜를 확인했는가?

최초 질문은 ‘쓸 만한 제품을 찾았는가’ 하나로 묶이지 않았다. A01은 사람이 작성하고 기계가 검증할 catalog 형식, A07은 앱 mount 계약의 결합 수준, A09는 상태 삭제와 읽기 가시성, A20은 benchmark가 무엇을 측정하고 누가 확장하는가, B08은 Path 객체를 잃지 않고 출력하는 방법이었다. 이 필요는 당시 초안의 문장/코드에 귀속시켰다. 연구자가 나중에 정리한 need를 당사자의 당시 미인지 진술로 취급하지 않았다. 원문 절은 표4와 각 source ID의 location에 있다.

[timeline.csv](timeline.csv)는 필요 기록·공개 제안·최초 공개 구현·공식 결정·인지 기록·시행을 별도 열로 둔다. 최초 공개 코드 열의 A24개 null은 해당 프로젝트가 구현을 안 했다는 뜻이 아니다. 이번에 가장 이른 것으로 읽은 PR/릴리스는 존재하지만 전체 최초 공개 push를 검증할 수 없다는 뜻이다. 범위 있는 시행은20/24에서 확인했고 A04·A17·A22·A24는 남겼다. A04의 후속 문서 PR3957은 개념 문서화이므로 실제 KCC 처리기를 구현한 증거로 올리지 않았다.

A19는 순서 반례다. 2017-12-28 생성된 rustdoc 구현 PR47046에서 CommonMark 제약을 확인하고2018-01-10 개정 초안을 냈다. 구현 병합은1월23일, RFC 공식 병합은3월8일이다. ‘공식 결정→구현’의 직선 순서를 날짜에 강제하면 발견 기회를 잘못 놓는다. 원 RFC1946의2017 header도 새 개정의 시작일이 아니다. {source('RUST-D03')}; {source('RUST-I2285')}.

A17의 초안 commit author time은2018-01-04인데 header는1월27일이다. 이것을 사적 고민일의 정답으로 보정하지 않고 불일치를 남겼다. A01 댓글은 생성·최종 수정 사이 구간을, B07의 비용 댓글은2019-05-16~06-06 구간을 보존했다. B06 현재 PR 본문의 ‘하루’는 PR가2018-10-05에 열렸다는 사실과 별개이며 문구 최초 작성일은 불명이다. 원 revision이 없는 현재 댓글의 문장에 초 단위 최초 인지를 부여하지 않았다.

B09는 후속 검증으로 갭 하나를 실제 닫았다. 공개 gist Git 이력에서2023-02-05 최초 예제,2월9일 세션 생성 변경, 같은 날03:11:41Z의 공식 옵션 링크 주석4행 추가를 분리했다. 그러나 작성 시각은 공개 push 시각과 다르고, 예제에는 자리표시자 URL과 `enginer` 오타가 있다. 주석을 추가하며 후크를 보존했다는 사실은 확인되지만 운영 실행은 미확인이다. [b09-git-audit.json](streams/b/b09-git-audit.json)에 전체 SHA·diff와 읽은 명령을 보존했다.

## Q3. 그때 실제로 사용할 수 있었던 대안인가?

필요한 조건의 존재, 패키지/서비스 공개, 안정판, 해당 팀의 허용판은 별개의 주장이다. tag의 과거 파일은 옵션이 그 코드에 있었음을 보여주지만 tag 생성/배포 시각이나 팀의 라이선스 승인까지 항상 보여주지는 않는다. 각 alternatives 항목의 version·condition·availability_date·date_precision·limitation을 함께 읽어야 한다. 전체 최초 공개 저장소일을 현재 GitHub 생성일 하나로 대신하지 않았다.

**늦게 나온 기능의 반례**는 B06이다. Pulumi의 원 WIP 당시 제안자는 go-cloud를 이미 고려했지만 Azure backend가 없었다고 나중에 직접 설명한다. 공급자의2019-01-03 Azure Blob 추가 commit을 확인한 뒤 재평가와4월25일 병합을 연결했다. 원2018-10-05에 현재 go-cloud 링크를 보냈다면 하루 작업을 없앴을 것이라는 주장은 성립하지 않는다. 기능 commit은 조기 소개 후보의 하한일 뿐 안정판·팀 도입 승인의 정확한 날짜는 아니다. {source('B-022')}; B06의 후속 [답글](https://github.com/pulumi/pulumi/pull/2455#issuecomment-464600656).

B01도 OBD 라이브러리의 존재와 필요한 KWP 기능을 구별해야 했다. 당사자의 미인지 진술은 직접적이지만 외부 기능이 자체 프로젝트 시작 이후에 합쳐졌다는 공급자의 반증이 함께 있다. A06은 더 복잡하다. 최종 AAD 기능은 최초 encrypted-attributes 제안 뒤 node-crypto에 추가되고 소비자 의존성이0.1.2에서1.0.0으로 올라갔다. 같은 작성자가 필요와 공급 코드를 함께 발전시킨 계보여서 ‘이미 있던 외부 해법을 뒤늦게 발견’한 독립 사건으로 볼 수 없다. 최초안에 최종 AAD 필요까지 고정돼 있었는지도 불명이다. {source('ADR-V04')}; {source('ADR-F06')}.

**이름이 비슷하지만 조건이 다른 반례**는 B02다. UnixSocketStatsClient를 처음 알고 감사한 답글만 읽으면 재사용 성공처럼 보인다. 당시 고정 코드의 `connect`는 `AF_UNIX/SOCK_STREAM`이고 요청자의 서버는 Unix datagram이었다. 후속 PR128에서 차이가 명확해지고 유지보수자는 범용 수요가 약하다고 거절한다. 이미 존재한 클라이언트는 필요한 전송 방식을 대체하지 못했다. {source('B-008')}; [후속 거절](https://github.com/jsocol/pystatsd/pull/128#issuecomment-496703485).

**미리 알면서 거절한 반례**는 A20이다. Criterion0.1.1의 공식 문서와 MIT/Apache 라이선스, 매크로 진입점은 원 제안 전에 존재했다. 리뷰어가 소개한 뒤 제안자 Manish는 이미 고려했다고 답한다. 팀의 관심은 benchmark harness와 언어/도구 확장 모델이어서 새 custom test framework 경로를 선택했다. Criterion 소개가 최초 인지였다는 코딩을 최종 감사에서 제거했다. {source('RUST-V02')}; {source('RUST-F04')}.

현재 문서를 과거로 소급하지 않는 추가 검사로 A18을 다시 읽었다. Cargo profile override와 사용자 정의 이름은 같은 시점에 안정화되지 않았다.2020 문서에서 override 안정화와 named profile의 불안정 상태를 구별했고,2021-12-02 Rust1.57 릴리스에서 custom profiles의 안정화를 확인했다. A21의 associated type bounds는2024-06-13의1.79 배포, A22의 free function과 불안정 pointer method도 구별한다. {source('RUST-V09')}; {source('RUST-V13')}; {source('RUST-V10')}; {source('RUST-V04')}.

## Q4. 누가 무엇을 언제 알게 됐다고 말했는가?

인지 코딩의 주체는 한 팀의 표적 선택을 책임진 사람이다. 공급자가 어떤 기능을 알고 있던 시점, 리뷰어가 처음 읽은 시점, 제안자가 답한 시점은 서로 대신할 수 없다. ‘처음 소개됨’은 해당 대화의 첫 소개이고 생애 첫 인지라는 뜻이 아니다. 선택을 바꾼 것은 새 해법의 존재일 수도, 기존 해법의 타입·라이선스·성능 조건을 바로 이해한 것일 수도 있다.

A에서 명시적인 표적 해법 미인지는0/24다. A21의 Lukas는 기존 where 표현을 몰랐다고 말하지만 제안자와팀이 같은 상태였다는 근거는 없다. A09의 ‘고려하지 않았다’는 compliance 요구에 관한 말이지 RocksDB TTL이라는 해법의 존재를 몰랐다는 말이 아니다. A04의 최초 초안은 이미 GCP Config Connector를 인용하므로 나중 댓글에 다시 등장했다는 이유로 초기 미확인에 넣지 않았다. {source('RUST-F05')}; {source('AP-M25-NEWNEED')}; {source('ADR-D04')}.

A01과A19는 엄격 미인지 대신 **기지 제약 교정**으로 묶었다. A01 작성자는 Kubernetes 형식을 이미 알고 있었으나 annotation 값이 string이어야 하는 제약을 리뷰의 오류 재현으로 바로잡았다. A19 작성자는 CommonMark를 구현하다 원안의 공백이 허용되지 않음을 발견했다. 두 경우 모두 새 조건→수정→코드가 연결되지만, Kubernetes나CommonMark라는 해법의 존재를 처음 알았다고 말하지는 않는다. 공급 명세와 실제 소비 코드가 같은 주장에 종속되는 관계도 표시했다.

B의 명시 미인지 결정자는 B01·B02·B08·B09 네 사례다. B04의 미인지 당사자는 기능을 요청한 mgrouch이고 결정 유지보수자 mairas와 다르므로 별도 한 사례의 역할 불일치다. B03은 소개를 받고 재구현 계획을 바꾸겠다는 직접 답이 있으나 최초 미인지 표현과 실제 설정 변경까지 모두 확인되지는 않는다. B05의 라이선스 혼동은 이미 유력한 Plotly 후보를 재평가한 것이고, 나중에 본인이 기억 오류를 정정했다. 동시대 정정을 처음의 ‘위험’ 진술과 함께 남겼다.

초기 인지 미확인3건의 범위를 좁히는 이유도 구체적이다. A07은 최초5월10일 초안에 전체 Router API 거절이 없고,5월28일 개정에서 추가되었다. 최종6월18일 의존성 파일은 초기 제안자의 인지 증거로 소급할 수 없다. A09의 최초 메일 다음날 소개 대상은 SQL/Table idle retention이다. 표적 RocksDB DBWithTTL은5월2일 설계에서 알고 거절하지만 최초2월6일 제안 당시 인지와 그 사이 최초 소개/답글은 불명이다. A06은 최종 AAD 기능을 초기 인지 대상으로 잡으면 기능 자체가 후발이므로 당시 제공 가능한 미인지 후보에서 분리한다. 이 판정은 표집 대상을 바꾼 것이 아니라 같은24행의 측정 대상을 명확히 한 후속 감사다.

## Q5. 새 정보가 실제 선택을 바꿨는가?

범위 있는 실제 변경은 많지만 그것이 모두 발견의 효과는 아니다. A의 결과 구성은 {ST['A']['outcomes']}다. B의 결과 구성은 {ST['B']['outcomes']}다. 여기서 유지·대체는 표적 선택의 전후 관계이며 문서 수용이나 제안 철회만 있으면 시행 미확인으로 둔다. A17·A22는 제안이 기각됐다는 사실만으로 개발자가 수동 wrapper를 실제 배포했다고 판정하지 않았다.

가장 직접적인 B08에서는 Frank Mitchell이 초기 코드 뒤 JSONEncoder 확장점을 알았고 다음 판에서 고치겠다고 쓴다. 후속3월7일 코드는 Path를 내부에 보존하고 출력 직전 `json.dumps(..., cls=PathEncoder)`로 위임한다. 코드L158,173–178이 직접 대응한다. **변경한 결정은 Path를 언제 문자열로 바꾸는가**다. 전체 중복파일 탐색 프로그램을 외부 라이브러리로 교체한 사건은 아니다. 코드가 설치돼 있으면 `simplejson`을 먼저 가져오므로 실제로 CPython json만 실행했다고 단정하지 않는다. 두 당대 구현에서 같은 확장점을 확인했으며 실행 환경·성능·시간 절감은 미확인이다. {source('B-027')}; {source('B-030')}; {source('B-056')}.

비슷한 직접 미인지라도 B09는 교육 목적 때문에 자체 후크 예제를 남겼다. 같은 날 링크 주석을 추가한 고정 이력이 그 유지 설명과 맞는다. 그러나 엔진 격리 옵션이 비공개 PgBouncer 설정·DEALLOCATE 요구 전체를 대신하는지는 불명이고 운영 실행 증거도 없다. 따라서 날짜가 고정된 예제 유지 사슬과 실제 시행 사슬을 분리했다. B01은 초기 대안 후발과 차량 범위 차이가 확인되지만, 그것이 후기 자체 구현 유지를 결정했다는 연결은 미확인이다. B02에서는 필요한 datagram과 제공된 stream의 불일치가 확인된다. **후기 발견 뒤 생산 자체구현 유지3건이라는 보강 목표는 엄격하게는0건**이며 이 세 후보의 끊어진 고리를 명시했다. 유지가 없었다는 모집단 주장은 아니다.

외부 도입 뒤 되돌림은 B07에서 보았다. inert를 넣은5월31일 commit 뒤6월1일 되돌렸고,6월3일 추가 폴리필·성능·IE10 조건을 설명했다. 전체 접근성 개선은6월11일 병합됐다. 이는 **merge 전 시험 분기 철회**이지 생산 장애 뒤 rollback이 아니다. B03은 반대 형태다. 링크가 재구현 계획을 바꿨다는 답은 강하지만 그 뒤 `.pre-commit-config.yaml`이 실제 바뀐 기록은 없다. 말의 인과성과 구현의 관측 강도는 서로 다른 축이다. {source('B-024')}; [B03 답글](https://github.com/pre-commit/pre-commit/issues/3142#issuecomment-1973848542).

기지 대안의 부분 재사용은 A07이다. 전체 React Router API를 앱 계약으로 노출하는 안은 거절했지만 후속 `ui/app_router.tsx`에서는 내부 Router를 사용했다. ‘외부 대안을 알면 전부 채택/전부 거절’이라는 이분법이 맞지 않는다. A12의 범위 변화는 Alibaba의 Blink 코드 기여라는 동시 사건이 더 직접적인 설명이며, A16은 histogram 비용에 대한 리뷰어 반대와 작성자의 microbenchmark 옹호를 모두 남겼다. 나중 gauge 중심 지표가 채택되었다고 이전 반대가 틀렸다는 식으로 지우지 않았다. {source('ADR-F07')}; {source('AP-M32-ORIG')}; {source('AP-M33-REVIEW')}; {source('AP-M33-REPLY')}.

유지·소개 후 미변경·외부 도입 뒤 철회의 세 방향마다3개 표현을 두 기록 계열에서 실제 검색했다.18개 쿼리와 포함/제외, 실패/차단은 [B search-log](streams/b/search-log.json)에 남겼다. 같은 프로젝트의 반복 PR를 사건으로 늘리거나, 반례가 충분히 강하지 않다는 이유로 성공 사례로 바꾸지 않았다. 전체 연결은 A01,A19,B05,B08 **4건**이며6건 보강 목표에는 못 미친다.

## Q6. 줄일 수 있었다고 말할 수 있는 비용은 무엇인가?

**같은 작업 범위의 투입·폐기·재사용을 연결한 조기 소개의 수량적 인과 절감은 확보하지 못했다.** A24와B9 모두에서 미확인이며0원·0시간이라고 주장하지 않는다. 통합 비용 원장은 {ST['costs']['rows']}행으로33개 선택 모두를 덮는다. 원 stream에서 비용 행이 없던 A17·A21·A22·A24에는 미보고 행을 추가했다. 비용 행 수는 사례 수가 아니고 종류가 겹친다.

관측 숫자 네 가지가 이 한계를 보여준다. A15의 JIRA `Logged 13h50m`은 화면 집계이며 누가 언제 어느 하위 작업을 기록했는지 없다. reporter/assignee를 worklogger로 대신하지 않았다. B06의 ‘하루’는 초기 코드베이스 작업을 한 당사자의 현재 PR 본문 진술이다. 전체 Azure 기능의 총 투입이나 표준8시간 인일이 아니다. B07의 ‘약 한 시간’은 button이 div로 바뀐 리뷰 문제를 이해한 시간으로 inert 선택 비용이 아니다. B01의4일은 ESP32 특수 baud 오류에 귀속된다. 서로 다른 범위·주체·정밀도의 숫자를 시간 단위로 환산해 더하지 않았다. 각 원문 위치는 표3과 costs.csv의 scope에 있다.

A01–A08의8개 값은 문서 PR 생성→병합의 달력 간격이다. B06의17,421,976초, 즉201일15시간26분16초도 WIP와 대체 PR의 공개 시각 차다. 그 사이에는 기능 후발·다른 담당자·대기·다른 업무가 들어간다. B03 답변까지9분 남짓 걸렸다는 사실도 실제 절감 시간으로 기록하지 않았다. 원문이 직접 보고한 ‘하루’와 달력201일을 더하면 동일 노동을 측정한다는 근거가 사라진다.

변경 규모도 인시와 다르다. Rust 네 구현 PR의 추가/삭제와 파일 수는 PR 전체에 속하며 테스트와 유지된 기능을 포함한다. B07의80줄은29추가+51삭제이며 lockfile이 섞인다. B08의68줄→181줄은 전체 스크립트 크기로, 새 CLI·YAML 기능이 함께 생겼다. 발견 뒤 줄이 늘었다는 사실을 비용 증가의 인과 증거로 쓰지도, 최초68줄을 모두 버린 노동으로 쓰지도 않았다.

재사용한 일은 같은 사례에서 남겼다. B08은 디렉터리 순회·비교 목적을 유지하면서 JSON 출력 경계를 바꿨고, 후속판에 추가한 YAML 출력은 별도 자체 변환으로 처리했다. B07은 전체 접근성/키보드 개선을 병합하며 inert 부분만 철회했다. B06은 filestate 틀·로컬 저장 레이아웃을 이어갔지만 이전 PR의 정확한 재사용량은 불명이다. B05는 Plotly 전환 뒤에도 기존 Highcharts/Matplotlib 출력을 선택 템플릿으로 남겼고, 후속1.21의 Kaleido/버전 대응은 도입 후 통합 일이 존재했음을 보여준다. 수량 보고가 없으므로 이를 무료 도입으로 간주하지 않는다.

각 결정의 `minimum_next_record`는 최초 시간표나 동일 범위 diff, 해당 작성자의 폐기/재사용 귀속 설명을 지정한다. 비용과 조기 소개 효과를 가르기 위해 필요한 것은 새 시장 추정치가 아니라 **같은 작업에 대한 당시 기록 한 묶음**이다. 실제 투입 보고와 대체 불가능 조건이 함께 있는 B06에서는 먼저 당시 Azure 부재를 해결해야 하므로 더 이른 링크만으로 줄일 수 있었다는 주장이 반박된다.

## Q7. 다른 분야에서 빌린 것은 이름인가, 구조인가?

타 분야의 형식이 논문이라는 이유만으로 분야 전이라고 세지 않았다. A19는 문법 명세 간 호환, A12는 다른 구현의 코드/설계 기여, B05는 plotting 생태계 통합이다. 모두 소프트웨어 내부 재사용이다. 구조 대응이 보여도 원 분야를 팀이 언제 읽었는지 없으면 최초 유입 시점을 확정할 수 없다.

보조 X-S1은 전기 차단기와 Semian을 두 관계로 대조했다. Eaton2018 문서는 지속 과전류→trip과 접점 개방→전류 차단을 설명한다. Semian의2020 고정 코드에는 오류 횟수/시간창→open 상태, open 상태→호출 전 예외가 있다. README는 circuit breaker의 worker-local 상태와 bulkhead의 server-wide semaphore를 구별한다. 이름만 비슷한 것은 아니지만, 실제 Shopify가 이 Eaton 문서를 읽었다는 증거는 없다.2015 당사자 글이 밝힌 경로는 Hystrix·Release It. 및 다른 소프트웨어 논의다. 전기 분야→이 팀의 직접 발견 사슬이라고 승격하지 않았다. {source('CF-S2')}; {source('CF-S3')}; {source('CF-S4')}; {source('CF-S5')}.

2020 운영자 글은 Hystrix의 조정값을 비교하면서 Semian의 오류창·복구 조건을 설명하고 계산식도 정정한다.263%→4%는 모형의 활용률 계산이고 실제 측정한 노동 절감이 아니다. 그 글만으로 ‘Hystrix를 검토하고 버린 채 Semian을 유지하기로 결정한 날짜’를 새로 만들 수 없다. 이 사례는 대응 관계의 관찰과 역사적 유입 인과가 갈라지는 보조 대조다. 사후에 유래만 붙인 새 엄격 사례를 찾는 세 표현·두 검색엔진 경로도 실행했으나 최초 사용 이전 원기록과 후대 명명이 연결된 새 사례를 확보하지 못했다.017 Kanban을 다시 채우지 않았다.

### 타 분야 1: 특허 선행자료 제시와 청구 범위

EPO register의 사건 상세와 원 dossier는403이었다. 같은 공식 공개기록인 심판 결정 PDF 두 건을 읽고 대체 계보와 한계를 보존했다. **T2074/13**에서는 D1/D2 쟁점 뒤2018-05-04 보조 요청에 wet heat/HF 조건을 넣었으나6월5일 심판은 늦은 범위 확대와 추가 검색 필요 때문에 수용하지 않았다. 수정은 확인되지만 새 해법의 제품 구현·비용 회피와 같은 사건은 아니다. **T2526/17**에서는32청구/7발명과6개 추가검색료가 문제였고, 부분 소자보다 dummy-pixel 전체 회로의 관계를 보아야 한다는 논증이 받아들여져6개 검색료 환급으로 이어졌다. 별도2017-07-12 수정 청구 세트가 있으므로 ‘청구 문구가 전혀 바뀌지 않았다’고 쓰지 않았다. {source('CF-P1')}; {source('CF-P2')}.

판정 단위는 각각 한 사건의 요청/청구항과 통일성·검색료 절차다. 모든 특허의 분모나 등록률이 없으며, 심판문이 요약한 이전 기록과 원 통지서·청구 세트의 직접 대조도 다르다. 소프트웨어 조사로 가져온 규칙은 **무엇이 바뀌었는가, 절차에서 받아들였는가, 실제 구현했는가를 나눌 것**이다. 남은 최소 입력은 심사관 통지, 출원인 응답, 제출시각이 있는 각 청구 세트다.

### 타 분야 2: 시간순 공학 설계 관찰

Chan·Schunn2014는 실제 팀1의97분/100분 회의,4,594발화(2,382+2,212)를 분석했다. 먼 유추가 큰 설계 도약과 바로 연결되기보다 더 많은 국소 개념 생성과 이어졌다는 결과다. 같은 자료를 세 분석으로 나눴으므로 독립 연구3건으로 세지 않았다.97유추 블록과843비유추 블록, 회귀N938은 서로 분모가 다르다. 방법의144유추와 다른 절의147유추 서술도 일치한다고 고치지 않았다. lag0 OR1.99와lag1 OR1.88의 대상은 개념 생성이며 제품 채택·절감시간이 아니다. {source('CF-E1')}.

Cheong·Hallihan·Shu2014는 학생34명 중30명을9팀에서 녹음하고 나머지4명은 질적 자료로 다룬다.10초 구간 코딩이며 세 disassembly 팀 중 예상 생물학적 관계를 가장 잘 활용한 Team2의22.1%는 활동 구간 비중이다. 이를9팀의 성공률이나34명의 도입률로 바꿀 수 없다. 효소 결합의 형상 대응→부품 연결, pH/온도 활성조건→분해를 허용하는 환경조건 두 관계가 설계 대화에 대응한다. 실제 생산 코드/제품은 관측하지 않았다. 활동모드 κ.79와 유사성 판정의 합의 코딩도 서로 다른 신뢰도 측정이다. {source('CF-E2')}.

두 분야 모두 새로운 단서가 곧 최종 선택 변경이라는 단순 설명을 반박한다. 특허에서는 절차 허용·청구 범위가, 공학 관찰에서는 다음 국소 탐색이 매개한다. 이 결과를 소프트웨어 팀의 발생률·인과 절감량으로 옮기지 않았다.

## Q8. 어느 시점에 어떤 링크가 결정을 바꿀 수 있었는가?

링크의 후보는 존재하는 패키지 이름만이 아니라 **그 시점의 특정 제약과 작업 경계**여야 한다. 아래 날짜 중 실제 공개 필요가 드러난 날과 나중에 복원한 내부 작업일은 구별한다. ‘제공할 수 있었음’은 해당 팀이 그날 받았다는 뜻도, 판단을 바꿨다는 뜻도 아니다.
""")

intervention_rows = [
    ["A01 ↔ A19", "A01 2020-05-18 리뷰; A19 2017-12-28~2018-01-10 구현/개정 구간", source("ADR-V01") + "; " + source("RUST-V01"), "annotation은string; link destination에 공백불가. 기존 모델/링크기능은유지", "기지 제약 교정→설계/코드 변경 직접연결. 새 해법 최초인지 아님", "제약을 더 일찍 보였을 때 피한 수정량·일정은미확인"],
    ["B08 ↔ B09", "B08 2023-03-02코드표제는사후후보; 첫공개3월3일에는이미발견. B09 2월5일공개예제", source("B-031") + "; " + source("B-056") + "; " + source("B-038"), "JSONEncoder호환cls와Path출력경계; SQLA엔진격리와후크교육목적 구별", "B08변경직접진술+후속코드; B09배운뒤교육예제유지진술+주석diff", "B08외부에서필요를미리볼수있었는지/실제import불명; B09운영성공불명"],
    ["B05 ↔ B06", "B05 2022-10-30공개제안/31일라이선스정정; B06 2019-01-03기능commit뒤 후보", source("B-015") + "; " + source("B-016") + "; " + source("B-022"), "MIT·오프라인renderers vs Azuredriver·인증·상태이관·잠금", "B05이미아는후보의위험정정,최종전환의단독원인불명; B06당시Azure부재직접설명", "2018-10-05에미래기능링크를줄수없음; 안정판/팀승인·통합인시불명"],
    ["B02 ↔ A07", "B02 2019-05-11공개질문; A07 5월10일mount제안·거절문구5월28일추가", source("B-008") + "; " + source("ADR-V05") + "; " + link("BrowserRouter.js v4.3.1", "https://github.com/remix-run/react-router/blob/v4.3.1/packages/react-router-dom/modules/BrowserRouter.js"), "stream/datagram vs 전체Router계약/내부구현 분리", "B02미인지해소해도부적합유지; A07전체API거절하며내부부분재사용", "정확한설치판·사용환경·초기인지·통합비용불명"],
    ["B07 ↔ B03", "B07 2019-04-29접근성PR부터조건점검후보,확실한판연결5월31일; B03 2024-03-01T20:06:22Z공개요청", source("B-025") + "; " + source("B-011"), "브라우저추가polyfill·성능조건 vs 정규식·대상파일·실패처리", "B07시험시행뒤철회확인; B03소개뒤재작성계획철회진술", "B07최초인지/초기npm게시일불명; B03실제설정커밋없음. 비용수량불명"],
]
out.append(table(["짝", "개입 후보 시점·정밀도", "당시 링크·해당 부분", "필요 조건·남는 도입 일", "직접 진술/가능성/유지 근거", "미확인"], intervention_rows))

out.append("""제품 판단으로 옮길 수 있는 것은 과대 절감액이 아니라 검증해야 할 입력이다. 원 질문과 필요한 조건이 공개돼 있는가, 그 조건을 충족한 판이 그때 이미 있었는가, 소개받을 결정자가 누구인가, 전체 교체와 부분 재사용 중 어느 경계가 열려 있는가, 시험·통합 작업이 얼마나 남는가를 묻는 입력이다. 이 자료로 자동 추천 제품의 수익·시장·전 팀의 미인지 발생률을 계산할 근거는 없다.

통합 감사에서 초기 가설은 실제로 축소되었다. A20의 외부 Criterion 소개는 선행 인지가 확인돼 발견사슬에서 빠졌고, A07은 ‘전체 거절’에서 내부 부분 재사용으로 바뀌었다. B02의 감사 답글은 후속 datagram 요구로 반박됐고, B09는 개정 날짜를 확보했어도 운영 시행은 여전히 불명이다. 좋은 결과가 나오는 항목만 남기는 대신 끊어진 연결을 보존한 이유다.

## 재현·출처 계보와 열린 판단

고정 입력 SHA·관측 창·모델/실행 위치는 SCOPE.md, 번들별 커밋과 이어갈 위치는 PROGRESS.md, 모든 사례의 다음 최소 자료는 decisions.jsonl에 있다. `sources.json`의 `lineage`와 `same_work_as`는 동일 생산자·동일 판/저작의 종속을 표시한다. 원자료를 길게 복제하지 않고 URL·고정판·읽은 절·확인 UTC·짧은 요약·한계만 보존했다. 독립 원문 수와 선택 수를 구별해 재현할 수 있다.

통합 파일 생성과 구조 검사는 아래 명령이다. 이것은 자료 일관성 검사이며 역사적 프로그램을 실행하거나 당사자의 회고를 실험 검증하는 명령이 아니다. 실제 결과는 evidence/validation.json과 SELF_CHECK.md에 저장한다.

```bash
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-022/tools/assemble.py
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-022/tools/write_result.py
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-022/tools/validate.py
PYTHONDONTWRITEBYTECODE=1 python -m workbench.session check docs/workstreams/research/AF-RES-022/manifest.json --fetch
```

미충족은 acceptance-evidence.json에 false로 남긴다. 엄격 연결6건·생산 자체구현의 후기 유지3건은 보강 목표이며0~4라는 관측을 고쳐 채우지 않았다. EPO 원 dossier, 사후 명명만이 선택에 개입한 새 사례, 과거 실행 환경·비용 반사실도 추가 입력 없이는 확정하지 않는다. 공통 계약/색인은 수정하지 않고 인계에서 담당자에게 반영 후보만 제안한다.

## 중요한 불일치와 다음 최소 확인
""")
out.append(table(["중요한 불일치·약점", "근거 ID·주소", "이 약점이 바꿀 판단", "다음 조사 질문·자료·최소 확인"], [
    ["초기 인지와 최초 사적 필요가 분리되지 않음; A07/A09 인지기록완성0~2/24는 인과상한이 아님", source("ADR-D07",False) + "; " + source("AP-M25-ORIG",False) + "; awareness-audit A06/A07/A09", "0/24는 엄격 관측하한만 지지. 빈도·조기 개입 가능시점·6연결 목표는 확정 못함", "A07 최초5월10일초안의연결메시지, A09 GoogleDoc revision/첫소개답글, A06 최종AAD필요가고정된시점 한 묶음"],
    ["실제 투입·유지·폐기·절감의 귀속이 끊김; B09예제의날짜는확인했으나운영시행은불명", source("AP-J31",False) + "; " + source("B-020",False) + "; " + source("B-036",False), "13h50m/하루/4일/LOC를 비용절감으로 합산 불가; 엄격 생산유지3건도 미달", "이름/날짜/범위있는worklog와같은작업diff, B09실제운영구성·성공로그, B03실제설정커밋 한 건부터"],
    ["타분야의단위와유입계보가다름; EPO원dossier403, 공학유추144/147 불일치와활동구간분모", source("CF-P1",False) + "; " + source("CF-E1",False) + "; " + source("CF-E2",False) + "; " + source("CF-S2",False), "구조유사·개념생성·법적청구변경을 실제소프트웨어채택/절감과동일시못함", "EPO원통지/청구세트전후diff, E1코딩데이터/정오표, 구조를처음소개한동시대메시지와실제규칙변경 각각1쌍"]
]))
(BASE / "RESULT.md").write_text("\n".join(out).rstrip() + "\n")
print(json.dumps({"report": "RESULT.md", "case_table_rows": len(rows1), "cost_table_rows": len(rows3),
                  "required_tables": 4, "last_table_data_rows": 3}, ensure_ascii=False))
