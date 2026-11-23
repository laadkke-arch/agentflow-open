"""Render the report from sealed AF-RES-069 records; no network or product execution."""
from pathlib import Path
import csv
import json

P = Path(__file__).resolve().parents[1]
FREEZE = "03d1e436cfa7dc209b57b19508ef4b2e75942824"
SEAL = "de1727aada52835ebcde4ff1c92c3940db215476"
BASE = "https://github.com/laadkke-arch/agentflow-open/blob/"
OWN = "docs/workstreams/research/AF-RES-069/"

def fixed(path, label, sha=SEAL):
    return f"[{label}]({BASE}{sha}/{OWN}{path})"

def cell(value):
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=False)
    return str(value).replace("|", "&#124;").replace("\n", "<br>")

def table(headers, rows):
    return "\n".join(["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"] + ["| " + " | ".join(cell(x) for x in row) + " |" for row in rows])

queries = [json.loads(x) for x in (P / "queries.jsonl").read_text().splitlines()]
runs = [json.loads(x) for x in (P / "runs.jsonl").read_text().splitlines()]
sources = {x["source_id"]: x for x in map(json.loads, (P / "sources.jsonl").read_text().splitlines())}
judgments = list(csv.DictReader((P / "judgments.csv").open()))
counts = json.loads((P / "evidence/counts.json").read_text())
costs = {(x["problem_id"], x["arm"]): x for x in counts["arm_stats"]}

parts = ["""# AF-RES-069 · 분야 이름 없이 관계로 찾은 대안의 범위

**결과: PARTIAL.** 관측한 세 요구에서 A와 B 모두 두 필수조건 전체를 만족한다고 확정한 해법은 0건이다. 그러나 일반 탐색 A는 실제 수정 위치와 기존 인터페이스를 찾았고, 관계 탐색 B는 일부 조건부 시험 관점을 제공했다. 이를 같은 성과나 같은 실패 원인으로 합치지 않는다. 이번 기록은 ‘관계 탐색이 불가능하다’는 증거도, ‘같은 비용으로 더 좋은 해법을 찾았다’는 증거도 아니다.

독립 원저작 최소수는 봉인 당시 **25건**으로 충족했다. 사후 항공 절차 2문서를 보수적으로 1계보로 추가해 최종 산입은 **26계보**다. 최초 본문판을 입증한 문제는 없어 엄격층 짝 분모는 **0**, 관측 본문으로 실행한 짝 분모는 **3**이다. 질의·원문 접근 상한은 같았지만 같은 문서 추가 접근을 포함한 실제 연구 연산은 **A 25회, B 33회**여서 동일 비용 비교는 미성립이다.

## 표 1 · 요구, 선정 순번, 동결 조건과 사전 노출

원행은 `frame_id`, `problem_id`, `source_id`로 조인한다. 아래 본문 줄 번호는 최초판을 뜻하지 않고 각 관측 응답을 줄로 나눈 위치다.
"""]
t1 = [
 ["P1 / JupyterLab #19647 / F1-01 (첫째)", "새 disable이 원래 lock을 바꾸지 않음; C1 lock 불변, C2 빈 초기 목록·빈 사전 제거 뒤 새 항목을 구판으로 오인하지 않음", "page_config 없음 → disable → 새 프로세스 enable; sys_prefix/system 경로 같음·다름", "연구자 가정: 저장부의 완료 구분 최소 수정 + 회귀 확인", "원인 함수, 빈 표식 실패, 일반 완료 표식 개념은 이미 앎", "ethanstoner; 2026-08-30 생성; 09-27 갱신; 관측 body a4193d92…; 최초판 미확인; 보고 코드 9312e29b…", "RQ-F1-01 L3–13,17–59,63–65", fixed("problems.jsonl", "P1 고정 입력", FREEZE)],
 ["P2 / HA Core #180207 / F2-04 (넷째)", "현재 Mini→Doorbell→Chime에서 제어 노출; C1 연결 유지, C2 부모 대신 실제 Chime 볼륨 변경", "Chimes={}이고 부모 볼륨은 무효이나 원 앱은 작동", "연구자 가정: discovery/API 경로 확인 후 기존 entity 연결", "독립 장치 또는 부모의 entity라는 두 표현은 본문이 이미 제안; 연결 유지 C1은 연구자 운영화", "jlock556-create; 2026-08-25 생성; 09-20 갱신; body 2a7698db…; 최초판 미확인; Core2026.8.3", "RQ-F2-04 L3–69", fixed("problems.jsonl", "P2 고정 입력", FREEZE)],
 ["P3 / Inkscape #13819 / F3-03 (셋째)", "도구 아이콘·행동 수·행동의 열 의미 설명; C1 초보자 이해, C2 작은 기존 대화상자에 표시", "긴 수량 제목의 넘침 또는 짧은 Number의 모호함은 연구자 가설; 실제 폭 미제공", "연구자 가정: 기존 열 제목 표시와 긴/짧은 문구 비교", "열 제목 추가 및 Tool Icon, No. of Actions/Number, Action 문구는 본문 노출; 새 발상 아님", "brynn3; 2026-08-28 생성; 08-29 갱신; body aa565a58…; 최초판 미확인; 1.5-dev e1e8684/GTK4.22.4", "RQ-F3-03 L8–32", fixed("problems.jsonl", "P3 고정 입력", FREEZE)]
]
parts.append(table(["요구·원순번", "목표·필수조건", "경계 입력", "후보 전 선택", "기존 노출·해석", "관측 원문판", "근거 원행·절", "고정 링크"], t1))
parts.append("""

## 표 2 · 실제 질의와 두 경로의 결과

각 행의 세 질의는 실제 실행 문자열이다. 순위는 검색 도구가 최초 반환한 텍스트 블록 순서이며 엔진 HTML 순위나 ref 번호에서 추정하지 않았다. 원문별 조건·반례·다음 확인은 뒤의 ‘표 2 상세’ 30행, 읽지 못한 자리까지 포함한 전체 90행은 고정 `judgments.csv`에 있다. 아래 ‘지지’는 해당 원문의 기능 또는 원리 범위에 한정하며 대상판 전체 성공과 구분한다.
""")
arm_text = {
 ("P1","A"): ["Q1 R1 원이슈, R2 전환 지침, R3 CLI, R4 설정층, R5 CLI 다른 판", "부품: CLI/설정 시험 재료. 원리: 구판 기능 유지. C1·C2를 만족하는 지속 표식 구현은 없음 (S02 §4.0→4.1, S03 lock/unlock)", "disable 뒤 무조건 unlock은 기존 True lock을 깨뜨림. 기존 lock 보존과 빈/비빈 초기 상태를 분리 시험; 저장 구현 선택은 미정"],
 ("P1","B"): ["Q1 R1–R5 NARA 기록 보존·처분 문서 (5문서, 2계보)", "전부 무관. ‘record/copy/status’의 대상은 행정 기록이며 프로그램의 disable/lock·재기동 완료 상태가 아님 (S01 FAQ15, S02 cutoff, S04 p.8)", "복사본을 완벽히 보존해도 새 항목을 잘못 잠글 수 있음. 이 다섯 문헌은 채택하지 않고 반환 후순위는 미확인 유지"],
 ("P2","A"): ["Q1 R1 원이슈, R2 HA 문서, R3 Reolink 연결, R4 제품 요약만, Q2 R1 Chime 설정", "부품: 기존 Chime entity/action과 원 앱 시험 동작. C2 기능 지지는 있으나 정확한 Mini 연결·펌웨어 C1 및 leaf API는 미확인 (S02 number/action, S03 연결절)", "부모 볼륨이나 Hub 소리를 Chime 성공으로 셀 수 없음. 기존 entity 재사용 전에 leaf 식별·setter 계약 확인; Mini와 Hub/Pro 절차 구별"],
 ("P2","B"): ["Q1 R1 센서망, R2 decision tree 특허, R3 control-cell 특허, R4 분산 감독 제어, R5 무선 동기화", "조건부 원리: S01 명령 역할, S03 ID·능력·native 제어, S04 질문/응답/명령. S02/S05는 물리 연결·속성 쓰기와 불일치. C1·C2 대상 지지 미확인", "정확한 ID/값 echo 후에도 leaf가 그대로일 수 있음. 중간 수락과 실제 말단 상태를 분리 시험; 필요한 adapter/setter는 얻지 못함"],
 ("P3","A"): ["Q1 R1 역사 문서, R3 실제 소스, R4·R5 Debian h/cpp, Q2 R1 GTK ColumnViewColumn; R2는 R1 별칭", "부품: TreeView의 headers_visible=false와 제목/데이터 바인딩이라는 수정 지점. GTK ColumnView는 다른 위젯. 현 코드는 C1 반대, C2는 판·폭 미확인 (S02 소스40–84)", "표시만 켜고 Children을 남기면 초보자 의미 전달이 실패할 수 있음. e1e8684의 위젯을 먼저 확인하고 제목·가로/세로·번역을 시험"],
 ("P3","B"): ["Q1 R1 HHS/GSA 지침, R2 Mass.gov 403, R3 PDF 판독 불가, R4 역사 명령메뉴, R5 Tarkan 지침", "동종 UI 원리: 의미가 분명한 제목/약칭/줄바꿈. R4는 데이터 열이 아닌 명령군. S05 §2.2.5/2.2.8은 조건부 지침이며 대상 성공 미확인", "줄바꿈이 폭을 줄여도 높이 때문에 잘릴 수 있음. 긴/짧은 문구·두 줄을 동일 실제 창에서 비교; 아직 하나로 확정하지 않음"]
}
t2=[]
for prob in ["P1","P2","P3"]:
    for arm in ["A","B"]:
        qs=[]
        for qi in [1,2,3]:
            rr=next(r for r in runs if r["query_id"]==f"{prob}-{arm}-Q{qi}")
            qs.append(f"Q{qi}: `{rr['query']}`")
        a=arm_text[(prob,arm)]; c=costs[(prob,arm)]
        t2.append([f"{prob}-{arm}", "<br>".join(qs), a[0], a[1], a[2], f"3질의+5최초접근+{c['same_document_extra_accesses']}추가={c['research_operations']}회; 본문 {c['direct_read_source_records']}/5", f"{arm}-{prob}-S01…S05; {prob}-{arm}-Q1…Q3", fixed("runs.jsonl","원순위")+" / "+fixed("judgments.csv","조건·반례")])
parts.append(table(["요구·경로", "실제 질의 3개", "최초 순위·후보", "부품/원리·조건별 근거", "반례·새 선택·다음 확인", "비용", "원행 키", "고정 링크"],t2))
parts.append("""

## 표 3 · 짝 분모, 확정 적합과 남은 미확인

‘둘 다 미확정’은 실제 읽은 예산 안에서 확정 적합이 없다는 뜻이다. 미열람 문헌까지 모두 실패했다고 판정하지 않는다. URL과 저작 계보를 별도 분모로 유지한다.
""")
t3=[]
for r in counts["pair_stats"]:
    prob=r["problem_id"]
    extra={"P1":"없음; 일반 완료 표시 개념은 사전 노출", "P2":"역할/대상/실제 결과의 분리 시험; 조건부 3원문(타분야2·동종1), 완성 대안0", "P3":"약칭·줄바꿈 비교라는 동종 UI 원리; 타분야 이전 확정0"}[prob]
    t3.append([prob,"관측1 / 엄격0","0 / 0 / 0 / 1",extra,f"{r['direct_read_url_union']}/{r['returned_url_union']}",f"{r['direct_read_lineage_union']}/{r['returned_lineage_union']}",f"읽은 source에 미연결인 순위 {r['uninspected_or_unknown_ranks']}개; 실제 적용 미측정",fixed("evidence/counts.json",prob+" pair_stats")])
t3.append(["합계","관측3 / 엄격0","0 / 0 / 0 / 3","조건부 원리와 직접 부품은 합산하지 않음","27 / 76","18 / 52","반환 A/B URL·계보 교집합은 각 문제0; 이는 기능적 동등성0이 아님",fixed("evidence/ledger-audit.json","후속 감사는 아래 파일 목록 참조")])
t3[-1][-1]=fixed("evidence/counts.json","봉인 합계")+"; [후속 감사](evidence/ledger-audit.json)"
parts.append(table(["문제", "짝 분모", "A만 / B만 / 공통 / 둘 다 미확정", "원리만의 추가 대안", "직접 읽은 URL / 반환 합집합", "읽은 계보 / 반환 계보", "미확인·주의", "원행·고정 링크"],t3))
parts.append("""

위 표는 `de1727aada52835ebcde4ff1c92c3940db215476`의 원실험을 보존한다. 이후 댓글·PR·FAA·독립 재판독은 `sources.jsonl` 뒤에만 추가했고 검색 순위·질의·초기 채점은 고치지 않았다. 최종 source 원장은 99행이지만 독립 독해 99건이라는 뜻은 아니다. [최종 수량](evidence/final-counts.json), [41항목 원장 감사](evidence/ledger-audit.json), [검사 및 수용 상태](SELF_CHECK.md)를 함께 본다.

## Q1 · 실제 설계 선택이 드러난 문장과 모집의 한계

P1의 기대 행동 L47–49는 disable와 lock을 분리한다. 원인 L53–59는 빈 사전이 지워져 전환 완료를 나타낼 수 없다고 설명한다. 증상과 원인 분석은 이미 노출되어 있다. 남은 열린 선택은 완료 상태를 어떻게 저장하고 새 항목과 구판 항목을 구분할지다. 같은 문제의 정답을 처음 발견했다고 주장하지 않는다.

P2의 관측 본문은 현재 연결, 비어 있는 Chimes, 무효인 부모 볼륨, 원하는 실제 Chime 조작을 제시한다. 독립 장치와 부모 entity는 작성자가 이미 열어 둔 선택이다. 단, ‘현 연결을 절대로 바꾸지 말라’는 직접 인용은 없다. C1은 보고된 설치를 유지하는 연구자의 운영화다. 이 제약을 A에만 풀어 재페어링을 성공으로 세지 않았다. P3도 열 제목 자체와 후보 문구가 이미 제안되어 있지만 좁은 공간에서 표현을 고르는 구현 선택이 남는다. ‘원문에 대안이 있다’와 ‘해결이 이미 확정되었다’를 구별했다.

75개 모집행은 T0=2026-11-23T08:24:37Z 직전 90일 창에서 JupyterLab, HA, Inkscape, 예비 Godot, 예비 KiCad 각15개를 순서대로 고정했다. 제목·본문은 첫 로컬 커밋 뒤 읽었다. 그 커밋은 인증 없는 shell push 실패 후 동일 tree로 GitHub에 발행되었으므로, 첫 본문 읽기는 **로컬 봉인 뒤이지만 원격 발행 완료 전**이었다. 이를 원격 선봉인이라고 바꾸어 쓰지 않는다. 정확한 명령 실패와 tree 대응은 `evidence/operations.jsonl`에 있다.

Jupyter 첫째, HA 넷째, Inkscape 셋째를 택했다. 단순 재현 오류만 있고 보존할 제약·변경할 선택이 불명확한 선행 행은 제외 이유를 남겼다. Inkscape 셋째를 ‘문구가 이미 있다’고 잠정 제외했다가, P2의 두 entity 표현과 같은 기준을 적용하여 **검색 전** 첫 적격으로 바로잡았다. 그때 추가로 읽은 넷째 QR 이슈는 노출 기록만 남기고 표본에 넣지 않았다. 이런 적격 기준은 잘 서술된 설계 요구 쪽으로 모집단을 좁힌다.

수집은 T0보다 약188–218초 뒤의 live open 상태다. 포함 행의 마지막 갱신이 T0 이전이라는 확인만으로 그 사이 닫혀 누락된 이슈가 없다고 증명할 수 없다. GitHub 첫100개의 정렬된 prefix에서 첫15를 얻었으나 제외된 원응답 전체를 보존하지 않았다. GitLab 저자 bot 필드는 없고 공개 사용자 조회가403이어서 확인 불능이다. 세 관측 자리가 채워져 예비 프레임은 사용하지 않았고, 최초판 미확인을 예비로 편의 교체하지 않았다. [frame 감사](evidence/frame-audit.json)의 제한을 유지한다.

## Q2 · 무엇을 지우고 무엇을 살렸는가

P1-B는 JupyterLab/CLI/API 식별자와 Python/Windows를 지우고 과거 항목의 1회 복사, 새 비활성 상태와 별도 잠금, 빈 초기 집합, 재시작, 빈 사전 제거를 살렸다. 입력에는 같은/다른 설정 경로 경계도 남아 있다. 그런데 첫 질의의 records/copy가 행정 기록 보존 문헌으로 이어졌다. 이는 관계 표현의 핵심 변수가 소프트웨어 상태인지 기록물인지 타입이 약해진 실제 실패다. ‘어느 분야든 관계만 같으면 된다’는 해석을 거부하게 만든다.

P2-B는 제품 이름을 지우고 root/intermediate/paired leaf, 비어 있는 목록, 부모 속성과 말단 속성의 차이, 노출 위치 선택을 보존했다. 다만 관측 주체인 HA와 Hub를 root 하나로 압축하면 실제 네 층을 세 층으로 오해할 수 있다. 이 위험은 입력 감사 IA-01에 있으며 사후 질의를 고쳐 성공으로 바꾸지 않았다. P3-B는 아이콘·수량·행동과 초보자·좁은 폭을 남겼지만 Q3의 persistent는 원문보다 강한 표현이다. 그것을 B만의 추가 합격조건으로 쓰지 않았다.

A-P3-Q2의 ColumnView도 실제 사용 위젯이 확인되기 전 세운 검색 가설이다. A에 프로젝트 단어가 있다고 모든 기술어가 사실인 것은 아니다. [입력 감사](evidence/input-audit.md)는 삭제 손실과 추가 가정을 검색 전에 기록했다. 이후 개선 질의를 시험하려면 새 봉인이 필요하며 현재 질의는 유지한다.

## Q3 · 원순위, 종류, 중복과 접근 실패

90개 반환 자리를 모두 보존했고 독립 완성품은 확정하지 않았다. 직접 부품 분류에는 실행을 고칠 완성 부품뿐 아니라 CLI 시험 재료, 설정 fixture, 기존 entity, 실제 수정 지점도 들어 있다. 그러므로 `classification=부품`을 `confirmed_fit=true`로 읽으면 안 된다. 동종·타분야 원리도 이전 전제가 남아 있으면 별도 조건부 후보다.

각 갈래는 최초 서로 다른 URL 5개 접근 시도를 소비했다. 같은 저작의 다른 판·미러가 후에 밝혀져도 그 비용을 환급해 더 좋은 후보로 바꾸지 않았다. Jupyter 매뉴얼 판, NARA 전후 판, Inkscape Doxygen/Debian h/cpp는 최소수에서 계보별로 합쳤다. ReleaseNotes045와 Release_notes/0.45는 같은 source의 별칭이다. 읽은 URL을 반환 별칭까지 확장하면28이 되지만 실제 대표 접근 URL은27이다.

30회 중 A-P2 제품 페이지는 재작성 요약만, B-P3 Mass.gov는403, B-P3 Ishikawa PDF는 텍스트 판독 불가이며 screenshot도 실제 이미지 없이 marker만 반환했다. 세 건 모두 비용에는 넣고 독해 수에는 넣지 않았다. 접근 실패는 부적합 증명이 아니다. 나머지 미열람 순위는 제목이나 snippet만으로 채점하지 않았다. 원장에는 자동 반환이 5자리를 넘은 경우도 표시하며 추가 블록을 시험 후보/독해로 채택하지 않았다. 도구가 노출한 내용을 기술적으로 가릴 수 있었다고 주장하지 않는다.

## Q4 · 실제 대응과 이름만 같은 반례

P2-B의 센서망 논문은 사용자 명령을 root가 나누고 cluster가 해석하며 leaf가 환경에 작용하는 역할을 나눈다. 대상에서는 HA의 요청, 중간 장치의 라우팅, 실제 Chime 동작을 구분하는 데 쓸 수 있다. 그러나 통신 가능한 논문 노드와 현재 폐쇄된 장치 프로토콜은 같은 전제가 아니다. 센서망과 홈 IoT도 인접한 분야이며, ‘타분야2건’이라는 태그가 분야 거리의 객관적 측정값은 아니다.

Reedman 특허는 하위 ID·능력을 받아 상위에 노출하고 native 명령으로 실제 장치를 움직이는 조작을 제시한다. 목표의 leaf 식별·노출·명령 대상 연결과 실질 대응은 있지만, 그 명세가 Reolink의 leaf setter를 제공하지는 않는다. Schmidt의 질문/답/명령은 공유 discrete event의 동기화이며 이를 볼륨 쓰기와 잇는 별도 모델·구현이 필요하다.

반대로 Williams 특허의 root/intermediate/leaf는 한 기기에 질의하는 결정 트리의 검사와 결과다. 실제 세 기기의 연결도가 아니다. 무선 그룹 특허는 역할·계층이 바뀌어도 동기화를 유지하는 설계여서 고정 연결 보존과 동일시할 수 없다. P3의 세 열 명령메뉴도 ADD/FIND/HELP의 명령군이지 icon/count/action 데이터 열이 아니다. 이런 반례는 봉인된 첫5 순위에 나타난 원문을 실제 읽어 찾았으며, 결론을 방어하려고 나중에 유리한 실패 예만 고른 것이 아니다.

## Q5 · 같은 판의 조건별 근거와 적용 수준

표 2와 `judgments.csv`는 C1/C2 각각의 원문 절을 붙인다. 단, 동적 매뉴얼 URL의 판 제목이 달라지고 Inkscape Doxygen의 소스 커밋도 노출되지 않아 대상판 동일성은 확인하지 못했다. Debian1.4-6과 보고된 Inkscape1.5-dev e1e8684를 같은 판으로 합치지 않는다. 아이콘·수량 데이터 셀 renderer 폭24, 설명 열 최소폭150을 더해 실제 대화상자 최소폭을 계산하지도 않는다. 셀의 말줄임은 머리글의 말줄임 증거가 아니다.

초기 support의 범위도 명시한다. A-P2-S02/S05는 Chime 조작이라는 기능을, B-P3-S01/S05는 명료한 제목/폭과 높이의 절충이라는 지침을 지지한다. 정확한 대상의 모든 조건을 만족한다는 뜻은 아니다. 별도 문맥 판독자는 기존 점수를 보지 않고4원문·8조건을 재검토했다. root가 나중에 조인한 결과 Tarkan의 두 조건에서 초기 원리 지지와 대상 성공 미확인이 다른 라벨로 나타났다. 두 판독을 모두 남겼고 확정 적합은 어느 쪽도0이다. 이를 통계적 판독자 신뢰도나 인간 검증으로 보고하지 않는다. [판독 원문](evidence/semantic-review.md), [대조8행](evidence/review-reconciliation.json).

결과가 갈릴 최소 관측은 명확하다. P1에서는 새 프로세스 후 원래 lock과 완료 구분이 유지되는가, P2에서는 같은 Chime의 실제 설정·출력이 바뀌는가, P3에서는 대상 revision의 실제 작은 창에서 세 의미가 이해되는가다. 이 연구는 프로그램·장치·사용자 실험을 실행하지 않았다.

## Q6 · 바뀐 선택, 바꾸지 못한 선택과 최소 기각 입력

P1은 원래 알고 있던 완료 표식 가정에서 검색만으로 더 나은 구체 표현을 결정하지 못했다. 얻은 CLI/설정층은 검증 fixture를 구체화한다. 무조건 unlock이라는 쉬운 우회는 기존 True lock 하나로 기각된다. P2는 entity를 어디에 그릴지보다 동일 leaf의 식별·native setter·실제 결과를 확인하는 순서를 더 명확히 했다. ID와 요청값이 맞는 응답도 부모나 요청 캐시만 반영하면 기각된다. P3는 새로운 UI 계열로 옮기기 전에 기존 숨김 설정·제목·바인딩을 확인하는 국소 수정 후보를 얻었다. 표시만 켰을 때 Children이라는 제목이 남거나 두 줄 제목이 잘리면 각각 C1/C2가 실패한다.

이는 연구자의 다음 시험 선택이다. 원 개발자가 채택한 설계나 절약된 시간으로 올려 쓰지 않는다. 각 최초 접근 후보의 최소 반례와 다음 확인은 표 2 상세에 전부 남겼다. 무관 원문은 억지로 새로운 설계로 포장하지 않고 ‘채택하지 않음’을 결과로 보존한다. [결정 원장](decisions.md)과 [재개 명령·입력](evidence/resume-checks.md)에 실행하지 못한 확인을 특정했다.

## Q7 · 분모, 비용, 빈 층과 관측 0

관측층은3짝, 엄격층은0짝이다. 전자의 확정 적합0은 측정된 검색 결과이고 후자는 적격 원자료가 없는 빈 분모이므로 0%로 계산하지 않는다. 반환은76 canonical URL/52계보이고 그 안에서 실제 읽은 것은27 URL/18계보다. 문제별 A/B의 반환 URL·계보 교집합은0이지만 서로 다른 문서가 같은 생각을 말할 수 있으므로 의미적 중복0을 뜻하지 않는다.

봉인한 counts의 `uninspected_or_unknown_ranks` 16/13/20은 실제로 `runs.direct_read=false`, 즉 읽은 source에 연결되지 않은 순위 자리다. 순위별 inspection이 direct_read가 아니거나 classification이 미확인인 자리를 합치는 정의는21/22/22다. 읽은 원이슈도 해결 분류는 미확인일 수 있고 중복 자리도 있으므로 두 분모를 혼용하지 않는다. 이 명칭 한계는 후속 감사 LA-07에 남기고 봉인 수치를 조용히 바꾸지 않았다.

총58연산=18질의+30최초접근+10동일문서 추가접근이다. A는25, B는33이며 A-P1/B-P1은각8, A-P2/B-P2는9/13, A-P3/B-P3는8/12다. 실패와 불충분 접근도 포함된다. 원문 cap은 같지만 같은 비용이라는 상위 비교 목표에는 미달했다. 도구 토큰·금액·작업자 사고 시간·시간 절감·전체 웹 재현율은 측정하지 않았다. 논문의 연도와 검색엔진의 ‘몇 달 전’ 상대 날짜도 혼용하지 않았다.

독립25건의 첫 역할은 선정 문제3, 선별 과정6, 반환 신규16이다. 반환 독해18계보 중2개는 선정 문제의 재노출이다. 사후 FAA는 관련 절차1계보만 추가해26이다. 댓글·연결 PR·미러·동일 문헌 재판독은 추가0이다. 반례는 반환 원문과 논리적 입력에서 찾아 별도 새 원저작 수로 중복 가산하지 않았다. 방법상 tracker 확인 자료도 최소수에서 제외했다.

## Q8 · 봉인 뒤 댓글·PR와 새로움의 범위

P1의 2026-09-04 작성자 댓글5542831932는 항목별 False 기록과 항상 남는 전환 완료 표식을 이미 비교한다. 원이슈 생성32초 뒤 열린 PR19648도 사후 열람했다. 열람 시 head는 f12cea5b7d7296fabfabcb362005763a879ae06f, state=open, merged_at=null이었다. 패치는 setdefault로 기존 lock을 보존하는 구체 동종 수정과 새 handler를 거치는 회귀 검사를 담는다. 작성자의 테스트 통과 보고는 우리 실행이 아니다. merge_commit_sha가 있다는 이유로 병합되었다고 하지 않는다. 이 더 직접적인 사후 대안은 **A의 봉인 검색 성공으로 소급하지 않는다**. 일반 완료 표식은 조사자 사전 노출에도 있어 양쪽 의미에서 신규 발견이 아니다. [작성자 댓글](https://github.com/jupyterlab/jupyterlab/issues/19647#issuecomment-5542831932), [PR](https://github.com/jupyterlab/jupyterlab/pull/19648), `PS-P1-COMMENTS/PS-P1-PR19648`.

P2에서 2026-09-20 관리자는 Mini에 직접 재페어링할 가능성을 제시했으나 성공 관측은 없고 고정 C1을 바꾼다. 더 결정적으로 신고자는 같은 날 Mini 반품과 카메라 초기화를 보고했다. 기준일에 이슈가 열려 있었다는 사실만으로 원 신고자의 진행 중인 채택 기회가 확보되지 않는다. 다른 사용자의 원 앱/HA 차이 보고는 문제 가능성을 남기지만 원 신고자의 장치 실험을 대신하지 않는다. 읽은 댓글에 B 문헌을 인용한 내용은 없었으나 원 개발자의 전체 선행 지식을 알 수 없으므로 새로움은 미확인이다. [관리자](https://github.com/home-assistant/core/issues/180207#issuecomment-5749383050), [신고자](https://github.com/home-assistant/core/issues/180207#issuecomment-5750354113), `PS-P2-COMMENTS`.

P3 notes API는401, 공개 웹 fallback은 DisabledError였다. 댓글·연결 PR·수정 이력과 원 개발자의 선행 검토는 미확인이다. 권한을 변경하거나 제한을 우회하지 않았다. 후속 폐쇄 여부를 모집 기준일 상태에 덮어쓰지 않으며, 이번에는 세 문제의 당시·후속 전체 이벤트 계보를 확보한 것도 아니다. [후행 응답 메타데이터](evidence/postseal-discussion-metadata.json), [PR 고정 head와 파일 해시](evidence/postseal-pr19648-metadata.json).

## 사후 다른 분야 비교 · 항공 절차는 언제 도움이 되는가

root가 봉인 뒤 고른 FAA AIM과 JO7110.65는 실제 항공 업무 절차다. 수신 확인, 이행 의사, 지시 내용 확인, 실제 상태 보고의 근거를 나누어 읽었다. **명령을 되말하는 readback은 실제 장치 상태 getter와 동의어가 아니다.** 따라서 같은 Chime ID와 요청값을 echo해도 leaf의 값이 변하지 않을 수 있다는 반례를 명확히 할 수 있다. 이 비교는 누락된 leaf API를 만들어 주거나 실제 제어를 입증하지 않는다.

정확한 leaf setter와 신뢰할 결과 계약이 있으면 기존 HA entity/action이 더 직접적이다. setter 응답 자체가 leaf 완료 결과를 보증한다면 별도 GET을 무조건 추가할 필요도 없다. 일반 ACK 또는 요청 캐시만 있으면 실제 결과의 관찰이 더 필요하다. 부모 endpoint에서 온 응답이라는 이유만으로 거짓인 것도 아니다. 대상·값 출처·최신성·완료 의미가 판별 기준이다. API가 없으면 어느 경로도 구현 능력을 제공하지 못한다. [AUX-FAA-01 AIM](https://www.faa.gov/air_traffic/publications/atpubs/aim_html/chap5_section_3.html), [AUX-FAA-02 §2-4-3](https://www.faa.gov/air_traffic/publications/atpubs/atc_html/chap2_section_4.html), [전체 대응·최소 반례](evidence/aviation-comparison.md).

FAA 검색1·본문 open2는 사후 별도 비용이다. JO7110.65가 AIM을 참조하므로 최소수에는1근거군만 더했다. 연구자가 분야를 나중에 선택했으므로 B 적중·같은 비용 성과·해결률 향상에는 산입0이다.

## 표 2 상세 · 최초 접근 30건의 원문별 판단

다음은 실제 접근을 시도한 source S01–S05의 첫 노출 행이다. 정확한 질의는 표 2의 같은 Q번호와 아래 질의 시간표에서 결합한다. source마다 저자·판·UTC·직접 읽은 절은 고정 source 원장에 있다. 조건별 support/contradict/unknown은 초기 판정을 그대로 옮겼으며 후행 재판독으로 덮어쓰지 않았다. 반례는 실행 결과가 명시되지 않은 한 분석용 입력이다. 각 행의 최초 접근 비용1회와 공통 질의/추가 비용을 분리한다.
""")
detail=[]
for prob in ["P1","P2","P3"]:
    for arm in ["A","B"]:
        for n in range(1,6):
            sid=f"{arm}-{prob}-S{n:02}"
            j=next(x for x in judgments if x["source_id"]==sid)
            s=sources[sid]
            evidence=f"C1 {j['C1_status']}: {j['C1_evidence']}<br>C2 {j['C2_status']}: {j['C2_evidence']}"
            detail.append([j["rank_id"]+" / "+sid, f"[{s.get('title',sid)}]({s['original_url']})",j['classification'],evidence,j['minimal_rejection_counterexample'],j['new_design_choice'],j['next_check'],"최초접근1; "+f"{prob}-{arm} 전체{costs[(prob,arm)]['research_operations']}회",fixed("judgments.csv",j['rank_id'])+" / "+fixed("sources.jsonl",sid)])
parts.append(table(["원행·첫 순위", "후보 원문", "종류", "조건별 근거", "최소 반례", "새 선택", "다음 확인", "비용", "고정 링크"],detail))
parts.append("\n\n## 실제 질의 시간표 · 봉인 질의 18개\n\n모두 영어 `system2_search_query`, domain/recency 필터 없음, response_length=long이다. 각 행은5순위와 조인된다. 시간은 검색 호출 시작·반환이며 본문 독해까지 걸린 전체 작업시간이 아니다.\n")
qt=[]
for prob in ["P1","P2","P3"]:
    for arm in ["A","B"]:
        for n in [1,2,3]:
            qid=f"{prob}-{arm}-Q{n}"
            r=next(x for x in runs if x['query_id']==qid)
            qt.append([qid,r['query'],r['query_started_utc'],r['query_completed_utc'],"R1–R5 / 검색1회",fixed("runs.jsonl",qid)])
parts.append(table(["질의 키", "실제 질의", "시작 UTC", "반환 UTC", "자리·비용", "고정 원행"],qt))
parts.append("""

## 재현·가림·인수 경계

문제·질의는 03d1e436…에 모두 봉인하고, P1 A→B, P2 B→A, P3 A→B로 실행했다. 두 작업자는 같은 모델의 별도 `fork_turns=none` 문맥이었다. 상대 input/원장을 읽지 않도록 지시했지만 공유 파일시스템은 기술적 격리가 아니었다. root는 양쪽을 볼 수 있는 조정·모집·통합 판독자다. 선정 감사자는 root의 잠정 판단을 받았고, 사후 의미 판독자만 기존 점수를 보지 않은 별도 문맥이었다. 인간 판독자는 없다. 모델의 학습 노출을 확인하거나 제거할 수 없어 ‘새로 찾음’은 명시 사전 노출 목록 이후의 문서·구체 기능에 한정한다.

A-P1의 자동 검색 반환은 원이슈 본문과 바깥의 PR19648 포인터를 노출했다. 원이슈는 이미 아는 입력이지만 PR 포인터는 추가 노출이다. 봉인 전 댓글/연결 PR 본문 open은0이었다. 이 사건과 첫5 밖 자동 반환을 가림이 완전했다는 주장에 숨기지 않는다. `arms/A/P1-summary.json`의 노출 기록을 유지했다.

시작 foundation은76b8c1d15812fbf91b879f8444fd188ae7445802, 계획 기준은320424d87f99e70c42eeb8cb7211467de27f2c2e, 선행은065 HANDOFF@18e4449eb0ac04464aee8fa6cc07f1f6a54d0b5d 한 건이다. 선행의 과거 후보 원장·결과는 다시 읽지 않았다. `session start`는 저장소 root에서 실제 종료0이다. 최종 `session check --fetch`, 결과 고정 SHA GitHub 재열람, 수용 파일 확인은 [SELF_CHECK](SELF_CHECK.md), [acceptance-evidence](evidence/acceptance-evidence.json), 마지막 HANDOFF에 실제 영수증과 함께 적는다. 연구품질 판단과 Git 계약 검사의 성공을 구분한다.

## 남은 약점 3건과 결론을 바꿀 최소 관측

1. **최초판·모집 시점·진행 중인 요구의 불확실성.** 엄격층은 비었고 GitLab bot·T0 직후 누락을 확인하지 못했다. P2 신고자의 반품은 open이라는 모집 표지가 실제 채택 기회를 보장하지 않는 반례다. 결론을 바꿀 최소 원자료는 선택된 한 문제의 최초 본문 수정 이력, 정확한 기준일 상태, 당시 실제 설계 선택이 열려 있었다는 날짜 있는 당사자 기록이다. 그 한 짝부터 엄격층으로 재분류할 수 있지만 현재 원판은 소급 수정하지 않는다.

2. **관계 표현의 타입 손실과 얕은 반환 독해.** records가 기록물로, leaf가 결정 결과로 바뀌었으며 P2 관측자/Hub 압축도 남는다. 52반환 계보 중18만 읽어 일반적 성공·실패를 말할 수 없다. 결론을 바꿀 최소 관측은 봉인 반환 안의 아직 읽지 않은 한 원문이 고정 C1/C2와 구체 조작을 함께 충족한다는 절과 대상판 확인이다. 이는 후행 검토 성공으로 따로 기록해야 한다. 새로운 역할 보존 질의의 효능은 새로운 사전 봉인 실험으로만 평가한다.

3. **비용 불균형과 실제 적용 효과 미측정.** A25/B33이며 지원되는 지침·수정 지점이 실행 성공은 아니다. 확정 해법0이라는 결론을 바꿀 최소 관측은 P1의 기존 True lock/빈 상태 경계까지 통과한 고정판 실행, P2의 같은 연결에서 정확한 Chime의 값 변화, 또는 P3의 고정 revision·창 크기에서 세 의미와 공간을 함께 확인한 한 사례다. 동일 비용 우열을 말하려면 먼저 후속 모든 접근을 포함한 예산을 사전 일치시킨 별도 짝 실험이 필요하다. 시간 절감과 원 개발자 채택은 그와도 다른 관측이다.
""")
(P / "RESULT.md").write_text("\n".join(parts).strip()+"\n")
print("RESULT.md written",len((P / "RESULT.md").read_bytes()),"bytes")
