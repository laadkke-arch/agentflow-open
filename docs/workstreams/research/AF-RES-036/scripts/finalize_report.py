"""Render the research report from preserved observations; never rerun or change readers."""
import csv
import json
from pathlib import Path

P = Path(__file__).resolve().parents[1]


def jl(name):
    return [json.loads(x) for x in (P / name).read_text().splitlines() if x.strip()]


def js(name):
    return json.loads((P / name).read_text())


def cell(value):
    return str(value).replace('|', '&#124;').replace('\n', ' ')


def table(headers, rows):
    return '\n'.join(['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(['---'] * len(headers)) + ' |'] +
                     ['| ' + ' | '.join(cell(x) for x in row) + ' |' for row in rows])


def link(label, url):
    return f'[{label}]({url})'


R = {r['ref_id']: r for r in jl('references.jsonl')}
C = {r['ref_id']: r for r in jl('components.jsonl')}
D = {(r['ref_id'], r['view']): r for r in csv.DictReader((P / 'decisions.csv').open())}
AD = {r['ref_id']: r for r in csv.DictReader((P / 'adjudication.csv').open())}
S = {r['source_id']: r for r in jl('sources.jsonl')}
ALIASES = {alias: s for s in S.values() for alias in s['source_aliases']}
A = {a['attempt_id']: a for a in jl('attempts.jsonl')}
AN = js('evidence/analysis-summary.json')
SC = js('evidence/source-counts.json')
CS = js('evidence/cost-summary.json')
REPLAY = js('evidence/replay-summary.json')
RET = js('evidence/retention-summary.json')
UNITS = {r['ref_id']: r for r in js('evidence/replay-units.json')}
actions = {'KEEP': '유지', 'REPLACE': '교체', 'HOLD': '보류'}
strata = {'current': '현재 작업', 'historical': '특정 판 재현', 'ambiguous': '시간 의도 애매'}


def source_variant(alias):
    s = ALIASES[alias]
    return next((v for v in s['variants'] if v['source_id'] == alias), s)


def source_link(alias):
    v = source_variant(alias)
    return link(alias, v.get('fixed_url') or v.get('url') or v.get('original_url') or ALIASES[alias]['original_url'])


now_note = {
    'G01': '301→200. 2018 Issue 7 및 Shell 본문. 현재 문서 안에 newer 안내도 존재.',
    'G02': '200. GNU/Unix 명령의 completion recipes와 helper 설명. 기준판정은 실제 find/make 멤버도 확인.',
    'G03': '200. 원 인용이 명명한 2018판을 그대로 전달. 2024판으로 바꾸면 요구 판이 달라짐.',
    'G04': '200·원 anchor 있음. 현재 5.4의 coprocess, print/printf→stdin 및 getline←stdout 설명.',
    'G05': '200·원 anchor 있음. -MM은 system-header dependency를 제외. 10.1.0과 좁은 규칙 동일.',
    'G06': '200. gettext 1.0 배포 파일 목록. 기준판정은 2026-01-29 공식 stable 발표로 보강; 목록 수정일01-28과 구별.',
    'R01': '301→404·Page Not Found. 기준판정에서 별도 3.11 workflow의 정확한 FASTQ→count 절 검증.',
    'R02': '302→200. 3.11 IRanges 2.22.2의 integer-range/S4 infrastructure 설명.',
    'R03': '302→200 landing만으로 부족. 연결된 0.50.3 source의 setValidity2 정의까지 N에 포함.',
    'R04': '302→200. 3.11 DESeq2 1.28.1 PDF pp.9–10에서 RangedSummarizedExperiment와 rowRanges 확인.',
    'R05': '302→200. 3.11 SCE landing 및 intro의 클래스·scater 관계. intro는 R06 소비자와 같은 원고군.',
    'R06': '302→200. 3.11 scater 1.16.2 설명과 Depends SingleCellExperiment.',
}
limits = {
    'G01': 'G03과 같은 표준 목적지·후행 노출. B는 최신판 연도를 지정하지 않음.',
    'G02': 'G01과 같은 Bash 배포·GNU 발행자 배경 단서. 실제 completion 실행 호환성 미검증.',
    'G03': '특정 판 층 n=1. B 자체에 2018이 있음. H의 선행 gawk5.0.1 각주는 2008 표기.',
    'G04': '기능 설명의 문서 적합성만 확인. 실제 coprocess 실행 미검증. wrapper 포함 N 2113자.',
    'G05': '실제 compiler 실행 미검증. 현·과거 규칙이 반복돼 H의 비중복 정보가 적음.',
    'G06': '소비자 선정 전 target 목록 열람. B의 stable은 수집자 추가 한정. 기본 결과에서 보존하고 민감도 제외.',
    'R01': 'BNH 후보는 tarball이며 판독 때 미검증. 기준판정의 검증 HTML 대체 URI와 구별.',
    'R02': '시간 의도 미지정. 3.11 href만으로 역사 재현 의도를 추정하지 않음.',
    'R03': 'N/H 함수 발췌 동일 원문군. source 실행/API 호환성 및 standalone tutorial 품질 미검증.',
    'R04': '소비자 선정 전 DESeq2 landing 노출. N에 원문의 과거 버전 주석 포함. wrapper 포함 1692자.',
    'R05': 'R06과 소비자↔목적지 중복·같은 intro 문장 노출. 전체 상호운용 실행 미검증.',
    'R06': 'R04와 같은 소비자 프로젝트·R05 상호 단서. 특정 판 목적층은 아님.',
}
history_notes = {
    'G01': 'Bash 5.1, 2020-12-07 발표; 배포 HTML 포함 설명. target의 과거 내용 전체는 아님.',
    'G02': 'bash-completion 2.11 README와 release notes.',
    'G03': 'gawk 5.0.1 / Edition5.0 info; 선행판 POSIX 각주의 2008 표기.',
    'G04': 'gawk 5.0.1 / Edition5.0 info; 동일 coprocess 메커니즘.',
    'G05': 'GCC 10.1.0 preprocessor -MM 규칙.',
    'G06': 'gettext0.21의 2020-07 배포 공지.',
    'R01': 'rnaseqGene1.12.0 실제 HTML member의 end-to-end workflow.',
    'R02': 'IRanges2.22.0 / IRanges-class.Rd.',
    'R03': 'S4Vectors0.26.0 / R/S4-utils.R. N과 같은 함수 내용으로 중복 산입 제외.',
    'R04': 'DESeq2 1.28.0 / DESeqDataSet.Rd. N PDF와 같은 reference-entry군.',
    'R05': 'SingleCellExperiment1.10.0 / SingleCellExperiment/man/SingleCellExperiment.Rd.',
    'R06': 'scater1.16.0 / plotColData.Rd.',
}
rows1 = []
for rid in R:
    r, c, ad = R[rid], C[rid], AD[rid]
    hl = ', '.join(source_link(x) for x in c['H']['source_ids'])
    nl = ', '.join(source_link(x) for x in c['N']['source_ids'])
    if rid == 'R01':
        current = link('현재 오류 본문', c['N']['current_section_url']) + '; ' + link('검증 대체절', ad['replacement_url'])
    else:
        current = link('현재 필요 절', c['N']['current_section_url'])
    criterion = actions[ad['criterion_action']] + '·기준 확정; 별도 문맥/추가 원문, 발행자·핵심 본문 공유. 외부 독립 정답 아님.'
    rows1.append([
        rid + ' · ' + link(r['consumer_title'], r['original_distribution_url']) + ' · ' + strata[r['purpose_stratum']] + ': ' + r['minimal_purpose'] + f" ({r['source_id']})",
        link('원 href', r['original_href']) + ' · 소비자 ' + r['consumer_version'],
        current + ' · ' + now_note[rid] + ' ' + nl,
        hl + ' · ' + history_notes[rid],
        ' · '.join(actions[D[(rid, v)]['action']] for v in ['B', 'BN', 'BH', 'BNH']),
        criterion + ' 원장: adjudication.csv ' + rid,
        limits[rid],
    ])


def score_text(s):
    return f"유지 {s['correct_keep']}, 교체 {s['correct_replace']}"


def error_text(s):
    return f"오교체 {s['wrong_replace']}, 잘못 유지 {s['wrong_keep']}, 보류 {s['hold']}"


selected = [
    ('BN→BNH', 'all_presealed', 'all', '주 비교·전체'),
    ('BN→BNH', 'all_presealed', 'current', '주 비교·현재 작업'),
    ('BN→BNH', 'all_presealed', 'historical', '주 비교·특정 판'),
    ('BN→BNH', 'all_presealed', 'ambiguous', '주 비교·시간 의도 애매'),
    ('BN→BNH', 'all_presealed', 'R_historical', '주 비교·R 특정 판'),
    ('B→BH', 'all_presealed', 'all', '보조·B→B+H'),
    ('B→BN', 'all_presealed', 'all', '보조·B→B+N'),
    ('BN→BNH', 'exclude_collector_preexposure', 'all', '수집 사전노출 제외'),
    ('BN→BNH', 'exclude_N_card_history', 'all', 'N 카드 자체 이력 제외'),
    ('BN→BNH', 'exclude_N_source_history', 'all', 'N 원문 전체 이력 제외'),
    ('BN→BNH', 'all_controls_combined', 'all', '공통 프로젝트·목적지·사전노출·카드이력 등 결합 제외'),
    ('BN→BNH', 'no_reported_prior_and_no_card_history', 'all', '판독자가 보고한 선행 연관사례 및 카드이력 제외'),
    ('BN→BNH', 'exclude_all_collector_purpose_paraphrase', 'all', '목적 번역·해석 전부 제외'),
    ('BN→BNH', 'external_independent_gold_only', 'all', '외부 독립 기준만'),
]
rows2 = []
for comp, filt, stratum, label in selected:
    v = next(x for x in AN['comparisons'] if (x['comparison'], x['filter'], x['stratum']) == (comp, filt, stratum))
    n = v['paired_refs']
    included = v['ref_ids']
    stratum_pool = [rid for rid, r in R.items() if stratum == 'all' or r['purpose_stratum'] == stratum or (stratum == 'R_historical' and rid.startswith('R') and r['purpose_stratum'] == 'historical')]
    detail = '포함: ' + (','.join(included) if included else '해당 없음') + '; 해당층에서 제외: ' + (','.join(rid for rid in stratum_pool if rid not in included) or '없음')
    rows2.append([label + f' ({comp}; sensitivity.csv {filt}/{stratum})', n,
                  '해당 없음' if n == 0 else score_text(v['before']) + ' → ' + score_text(v['after']),
                  '해당 없음' if n == 0 else error_text(v['before']) + ' → ' + error_text(v['after']),
                  '해당 없음' if n == 0 else ('없음(0/' + str(n) + ')' if comp == 'BN→BNH' else 'N고정 비교 아님'),
                  detail + f"; 기준 미확정 {v['unresolved_criterion_refs']}" + ('; 무효과 관측으로 해석 금지' if n == 0 else '')])

next_material = {
    'G01': '[Bash5.1 doc/bash.html SEE ALSO](https://ftp.gnu.org/gnu/bash/bash-5.1.tar.gz)와 [2018 Shell](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html#tag_18): 특정 연도 요구가 추가로 있었는지 원 인용 문장 대조.',
    'G02': '[고정 find.bash](https://github.com/scop/bash-completion/blob/ddf4f5e44818e00c51e984c019c15b6d73a2e79b/completions-core/find.bash)와 소비자 Bash5.1의 completion API를 비교: 예제 내용의 실제 호환성이 필요해지는 요청인지 확인.',
    'G03': '[gawk-doc5.1.0-1 Preface](https://archive.debian.org/debian/pool/non-free/g/gawk-doc/gawk-doc_5.1.0-1_all.deb)의2018 각주와 [2018/2024 실제 절](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html#tag_19)을 판별해 원판 목적 누락 여부를 확인.',
    'G04': '[gawk5.1.0 배포](https://ftp.gnu.org/gnu/gawk/gawk-5.1.0.tar.xz)의 coprocess 절과 현5.4 절을 같은 print/printf/getline 조건으로 대조; 문서 범위를 넘어 실행할 때 별도 고정판 재생.',
    'G05': '[GCC10.1.0 -MM](https://gcc.gnu.org/onlinedocs/gcc-10.1.0/gcc/Preprocessor-Options.html)과 현 옵션을 같은 system/user header 입력으로 실제 비교하면 문서 동일과 동작 동일을 구분 가능.',
    'G06': '[gettext 공식 공지 목록](https://lists.gnu.org/archive/html/info-gnu/2026-01/)의1.0 발표 원시 Date와 [배포목록](https://ftp.gnu.org/gnu/gettext/)을 비교: newest/stable 한정 및 후속판 출현을 별도 확인.',
    'R01': '[검증3.11 준비 절](https://bioconductor.org/packages/3.11/workflows/vignettes/rnaseqGene/inst/doc/rnaseqGene.html#preparing-quantification-input-to-deseq2)을 저장구성별2GET 예산으로 실제 다시 찾고 원 helpURI 이전 공지를 대조.',
    'R02': '[IRanges2.22.0](https://bioconductor.org/packages/3.11/bioc/src/contrib/Archive/IRanges/IRanges_2.22.0.tar.gz)의 IRanges-class.Rd와 원 GenomicRanges1.40.0 문장이 요구하는 범위가 같은지 재확인.',
    'R03': '[S4Vectors0.50.3](https://bioconductor.org/packages/3.23/bioc/src/contrib/S4Vectors_0.50.3.tar.gz)의 R/S4-utils.R·NAMESPACE를 원 Extensions 예제와 함께 고정하여 실행하면 제공자 확인과 실행 호환성을 구분 가능.',
    'R04': '[DESeq2 1.28.1 PDF pp.9–10](https://bioconductor.org/packages/3.11/bioc/manuals/DESeq2/man/DESeq2.pdf#page=9)와1.28.0 Rd의 rowRanges 조건을 원 SCE devel 문맥과 재대조.',
    'R05': '[SCE1.10.0 archive](https://bioconductor.org/packages/3.11/bioc/src/contrib/Archive/SingleCellExperiment/SingleCellExperiment_1.10.0.tar.gz)의 SingleCellExperiment.Rd와 scater1.16.0 overview의 실제 데이터 구조 요구를 별도 판독.',
    'R06': '[scater1.16.0](https://bioconductor.org/packages/3.11/bioc/src/contrib/Archive/scater/scater_1.16.0.tar.gz)의 DESCRIPTION/plotColData.Rd와 SCE1.10.0 intro를 고정한 상호운용 실행이 더 강한 기능 주장을 바꿀 자료.',
}
rows3 = []
for rid in R:
    u = UNITS[rid]
    ids = list(dict.fromkeys([u['base_acquisition_attempt_id']] + u['N_attempt_ids'] + u['H_attempt_ids']))
    aa = [A[x] for x in ids]
    received = sum(x.get('received_body_bytes') or 0 for x in aa)
    stored = sum(x.get('stored_bytes') or 0 for x in aa)
    failed = sum(bool(x.get('error')) or (x.get('status') or 0) >= 400 for x in aa)
    seconds = sum(x.get('elapsed_seconds') or 0 for x in aa)
    rows3.append([f'{rid} · 1회차 B/N/H에 사용된 취득 단위', f'{len(ids)} GET / 실패 {failed}; ' + ','.join(ids),
                  f'{received:,}B 수신 / {stored:,}B 취득 당시 임시; C1(B) {next(x for x in RET["record_units"] if x["ref_id"]==rid)["serialized"]["C1_B_presealed"]["bytes"]:,}B, C2 {next(x for x in RET["record_units"] if x["ref_id"]==rid)["serialized"]["C2_BH_with_provenance"]["bytes"]:,}B 직렬화',
                  f'공유 취득은 다른 참조 행과 중복 가능; 요청 경과 합 {seconds:.6f}s; 재열람 노동 미계측',
                  '실측 요청 단위. 12행 합을 물리 총계로 쓰지 않음. 출처: evidence/replay-units.json 및 attempts.jsonl',
                  next_material[rid]])
for label, scope in [('수집·카드 구성 전체', CS.get('collection_only_scope', CS)), ('결정 봉인 뒤 기준판정', CS['post_decision_adjudication_scope'])]:
    rows3.append([label + (' · 수집·카드 구성 단계' if label.startswith('수집') else ' · 별도 기준 확인 단계'), f'{scope["actual_get_operations"]} GET / 실패 {scope["transport_failures"]}',
                  f'{scope["received_final_body_bytes"]:,}B 수신 / {scope["temporary_fetch_stored_bytes"]:,}B 취득 당시 임시',
                  f'{scope["minimum_http_exchanges"]} HTTP exchanges 이상; 요청 경과 합 {scope["sum_request_elapsed_seconds"]:.6f}s',
                  '실측·실패 포함. ' + ('수집자 비용' if label.startswith('수집') else '기준판정자 비용') + '; 사람시간·wire bytes 미계측',
                  '동일 독자의 재조회·실서비스 계측 필요; evidence/cost-summary.json'])
for q in REPLAY:
    ph = q['shared_source_physical_lower_bound']
    rows3.append([f"전체12 · 2회차 {q['configuration']} · {q['task']}",
                  f"실제 0; 모의 물리 {ph['operations']} GET / {ph['http_exchanges']} exchanges / 가정상 오류응답 {ph['observed_failure_responses']}",
                  f"실제 수신 미계측; 모의 물리 {ph['body_bytes']:,}B / 실제 구성파일 {q['concrete_serialized_example_bytes']:,}B",
                  f"공유 URL 합침; H local read 모의 {q['local_H_reads']}; 실제 재조회 경과 미계측",
                  '모의. 1회차 응답 크기·상태 고정, 경로를 이미 앎. 정확 packet 재현 아님',
                  '동일 2 GET/각30초 예산으로 실제 재생; replay-costs.csv 12행 및 evidence/replay-summary.json'])

head = '# AF-RES-036 · 현재 원문을 확인한 뒤에도 어떤 링크에는 과거 이력이 필요한가\n\n'
head += table(['참조 ID·원배포/목적', '원 href·버전', '현재 절 URL·확인 내용', '과거 근거 URL·판', '네 보기의 행동(B·B+N·B+H·B+N+H)', '기준판정·독립성', '미확인'], rows1) + '\n\n'
head += table(['대조·목적 층', '짝지은 참조 수', '옳은 유지·교체', '오교체·잘못 유지·보류', 'N 고정 후 H로 바뀐 사건 ID', '노출 제외·판정 불가'], rows2) + '\n\n'
head += table(['참조·조회 회차·구성', '실제 요청·실패', '받은 바이트·저장 바이트', '같은 판 재사용·재열람·경과', '실제·모의·미계측', '결론을 바꿀 다음 자료'], rows3) + '\n\n'

body = r'''## 판단 범위와 핵심 결과

**REVIEW_READY_WITH_GAPS. 동일하게 구성한 현재 증거 N에 H를 더해 유지·교체 행동이 바뀐 사례는 0/12였다.** B+N과 B+N+H는 모두 유지 11·교체 1이며, 사후 별도 문맥 기준판정의 유지 11·교체 R01과 일치한다. B와 B+H는 각각 12/12 보류다. 기준 보류를 정답으로 더한 행은 없고, 이 자료의 기준 미확정은 0/12다. 이 숫자는 사전 고정 카드와 내부 기준의 일치이며 사용자 정확도·인과효과·운영 실패율이 아니다. 재계산 입력은 [decisions.csv](decisions.csv), [adjudication.csv](adjudication.csv), [sensitivity.csv](sensitivity.csv)다.

이 결과가 허용하는 결론은 **원 인용의 판·목적이 이미 보존되고, 그 목적에 필요한 현 본문까지 확인한 이 12개에서는 추가 H가 행동을 더 바꾸지 않았다**는 것이다. B는 href와 짧은 설명만으로 구성되지 않았다. 배포판·문서명·멤버·목적을 포함했다. N은 한 페이지의 HTTP 상태뿐 아니라 필요하면 frame 안쪽 절, 연결 PDF 또는 source tarball까지 읽은 증거다. 따라서 원판 정보를 버린 순수 링크 목록이나 첫 GET 한 번의 충분성을 검증하지 않았다. N/H가 실제로 말하는 내용과 조인 위치는 [components.jsonl](components.jsonl)에 있다.

R01에서는 H를 추가한 판독자가 rnaseqGene1.12.0 **tarball 후보**를 제시했다. BN은 후보 주소를 제시하지 않았다. 두 판독 모두 REPLACE이며, BNH의 후보는 제공 카드에서 검증되지 않았다. 이후 기준판정자가 실제 확인한 대체지는 같은 목적을 제공하는 [3.11 HTML의 preparing-quantification-input-to-deseq2 절](https://bioconductor.org/packages/3.11/workflows/vignettes/rnaseqGene/inst/doc/rnaseqGene.html#preparing-quantification-input-to-deseq2)이다. 후보 발견 단서를 검증된 URI 선택 이익으로 가산하지 않는다. 해당 한 사건은 [analysis-summary.json의 candidate_uri_changes_at_fixed_N](evidence/analysis-summary.json)과 BC-rnaseq311-vignette 원문에 연결된다.

## Q1. 표집과 목적은 무엇이었나

봉인한 기간은 2020–2022, 원 경로는 GNU 도구 배포 HTML과 Bioconductor 릴리스 배포 HTML이었다. 결과는 **G6/R6, 서로 다른 출판 문서 12, 프로젝트 9, 프로젝트당 최대2**다. G 경로는 GNU 직접 배포와 Debian의 공식 doc 재배포를 구별한다. R 경로는 모두 Bioconductor3.11의 실제 HTML 멤버다. 문서 분할 장을 별개 출판으로 늘리지 않았고, B/H 원 archive를 새로 빌드한 HTML도 쓰지 않았다. [frame.csv](frame.csv)의 58후보 행은 요청 수가 아니다. 원 배포 9개를 공유하는 참조를 포함하며 멤버·배포물 hash와 실제 href는 [references.jsonl](references.jsonl)에 고정되어 있다.

목적 층은 현재 작업7(G02/G04/G05/G06/R01/R03/R05), 특정 판1(G03), 시간 의도 애매4(G01/R02/R04/R06)이다. ‘현재 작업’은 문서가 설명하는 작업을 지금 수행한다는 층화이며 2026년 최신판만을 요구한다는 뜻이 아니다. ‘애매’도 최소 목적 자체가 없다는 뜻은 아니다. G03은 문장이 2018 POSIX를 명명하므로 특정 판이고, Bioconductor3.11 href만으로 역사 재현 의도를 추정하지 않았다. R의 특정 판 층은 0으로 남겼다. 결과를 본 뒤 그 층을 보충하지 않았다.

세 가지 표집 한계를 보존한다. G06은 원 href의 배포목록을 소비자 선정 전에 읽었고, R04는 DESeq2 landing을 배포 metadata 수집 때 먼저 읽었다. 따라서 전12개가 target 상태 미노출로 선정됐다고 할 수 없으며 둘을 뺀10개도 별도로 집계했다. G06의 봉인 목적에는 원 문장에 없는 stable 한정이 더해졌다. 마지막으로 Debian coreutils9.1-1 및 Bioconductor 중간 patch판을 모두 소진한 것은 아니므로 모든 공식 과거 HTML을 전수 탐색했다고 주장하지 않는다. 이전 A/B 소비자·목적 중복 제외는 [review/exclusions.json](review/exclusions.json), 정확한 편차는 [review/base-audit.md](review/base-audit.md)에 있다. 봉인12개를 사후 교체하지 않았다.

## Q2. 현재와 이력 증거는 얼마나 분리되었나

B 12개는 `bd3c17ef2f989b3d9e0566405d82357fc17f47bb`, N/H와 보기48개는 `442292b34237fa7aa2d68493e2a96802f52ed728`에서 봉인됐다. N은 당시 원 href의 GET/redirect/도착 절, H는 그보다 앞선 판·배포 멤버·공식 발표다. 현재 조회 UTC와 발행·판·사건 시각은 별도 필드다. H의 현재 관측·판정자 권고·정답 포함 flags는 모두 false다. H의 발표 자료를 원 목적지의 당시 전체 snapshot이라고 확대하지 않는다. G01의 H는 Bash 배포 발표이고 G03/G04는 선행 gawk5.0.1 info, G06은 후속 gettext0.21 발표다.

각 B/N/H의 문자열을 한 번 만든 뒤 네 보기에 재사용했다. BN/BNH의 N, BH/BNH의 H, 모든 보기의 B는 12/12 동일 hash·bytes이며, 순서도 고정했다. [packet-verification.json](evidence/packet-verification.json)은 그 바이트 조건을 확인한다. 발췌는 원 위치·normalized hash·offset·exact text를 가진다. 원문 발췌는 N/H 모두1600 Unicode 문자 이내다. **metadata wrapper까지 포함한 전체 N은 G04 2113자, R04 1692자**다. 일부 옛 메모의 ‘모든 component1600자’ 표현은 원문 발췌 범위로 정정하며 입력을 다시 자르지 않았다. 총길이·원문길이는 원장에 따로 남는다.

완전한 의미적 독립은 달성하지 못했다. N 카드 자체에 판 관계가 들어간 것은 G01/G03/R02/R04/R06의5개다. 현재 도착 문서 전체가 과거판 관계를 이미 제공하는 경우도 있다. R03의 setValidity2 함수는 H와 N의 해당 내용이 같고, R04 PDF/Rd 설명도 같은 reference-entry군이며, R05 N의 intro는 R06 소비자 원고와 중복이다. 이들을 새로운 독립 원문으로 더하지 않았고, 카드이력·원문이력·모든 판표식 제외를 각각 계산했다. 원본 전체를 원격에 보관했다고 주장하지 않으며 exact card 재현과 가변 URL의 전체 응답 재취득을 구별한다.

## Q3. 네 보기의 판독은 어떻게 고정했나

seed360032, 사례 순서 R06/G05/R01/R03/G04/G06/G02/R04/G03/R02/G01/R05, Latin-square 배정을 N/H 공개 전에 고정했다. 네 새 내부 문맥은 각각12개 사례를 한 번씩 보았고 각 보기3개를 받았다. 같은 사례의 다른 보기를 같은 문맥에 주지 않았다. 판독자는 유지/교체/보류, 이유·근거절·주소 검증 여부·선행 연관사례를 순서대로 기록했다. 48결정은 `5fbde38a04613fbd6f057fd562bd173b7193f2c9`에 기준판정 전 봉인됐다. [reading-plan.json](reading-plan.json), [reader-launch.json](evidence/reader-launch.json), [readers](readers/), [decision-verification.json](evidence/decision-verification.json)이 실제 입력·출력 hash와 실행 범위를 보존한다.

같은 모델 계열의 내부 판독이며 사람이 네 그룹으로 무작위 배정된 실험은 아니다. 동일 사례의 다른 보기 노출 보고는0이나, G01/G03의 같은 표준, 동일 Bash/Gawk 프로젝트, R의 소비자↔목적지 관계는 간접 단서를 전달할 수 있다. 원 자료 수집자와 이번 재개 검토자는 이미 내용에 노출되어 있다. 새 기준판정 문맥은 결정 파일을 받지 않았지만 발행자·핵심 원문까지 외부 독립이 되는 것은 아니다.

주 비교 BN→BNH는 변화0/12, 보조 B→BH도 행동 변화0/12, B→BN은 보류→기준에 맞는 유지11·교체1이다. B/BH가 현재 접근을 보증하지 않으면 보류하도록 한 사전 규칙은 이 차이를 만드는 설계 조건이다. 이를 모든 정보검색에서 N의 절대 우위라고 해석하지 않는다. N 없는 historical reading 과업 자체를 별도로 시험한 것도 아니다.

## Q4. 기준과 대체 URI는 무엇으로 확인했나

48결정 봉인 뒤 GNU/Bioc 별도 문맥이 원 B와 발행자 원자료를 직접 재취득했다. GNU 원 href6개는 최종200이며 실제 절·추가 구현/발표를 확인했다. Bioc은 R01이 최종404이고 나머지5개가 최종200이다. 소비자 배포물·멤버 hash도 재대조했다. 기준은 유지11/교체R01로 확정했으나 전12개가 카드와 핵심 발행자 또는 본문을 공유한다. 추가 원문 없이 같은 발췌만 쓴 경우는0/12로 기록하되, **외부 독립 gold만 남기면 분모0**이다. [adjudication.csv](adjudication.csv), [criterion-dependence.json](evidence/criterion-dependence.json), [adjudicators/gnu/notes.md](adjudicators/gnu/notes.md), [adjudicators/bioc/notes.md](adjudicators/bioc/notes.md)에 근거와 틀릴 조건을 남겼다.

실제 반례 탐색은 원12개 분모를 바꾸지 않았다. G03의 [2018판](https://pubs.opengroup.org/onlinepubs/9699919799/mindex.html)은 최신판 안내가 있어도 원 목적에 더 맞는다. 2024 Shell chapter의 옛 anchor `tag_18`을 실제 요청하면200이지만 해당 id/name이 없고 `tag_19`가 있다(GNU-P-NEWSHELL). 이는 원 href가 실패했다는 사건이 아니라, 새판 하위절로 기계적으로 옮길 때의 보조 반례다. bash-completion의 고정 commit `ddf4f5e44818e00c51e984c019c15b6d73a2e79b`의 completions 하위 디렉터리도200이나 기대한 구현이 아니라 README/Makefile을 전달하고 completions-core로 안내한다. 원 인용은 repository root이므로 G02 KEEP과 충돌하지 않는다.

R03은 landing과 PDF가 모두200이어도 필요한 함수 설명을 제공하지 않는 반례다. N은 source 구현까지 확장했고 기준판정은 함수와 export를 별도로 확인했다. 이를 단순 HTTP 검사 성공으로 표현하지 않는다. 현재와 과거 함수 핵심 내용이 같다는 관측도 전체 패키지/API 실행 동등성을 증명하지 않는다. 원12개에서 기준을 결정할 수 없었던 경우는 없었다. 그 유형을 채우려 애매한 목적을 억지로 HOLD로 바꾸지 않았으며, 판단 보류의 실제 예는 보조 서지 귀속 충돌에서 별도로 남겼다.

## Q5. 보완과 불필요함을 어디까지 말할 수 있나

현재 작업7·특정 판1·시간 의도 애매4 모두 BN→BNH의 행동 변화가0이었다. 현재 작업의 올바른 결과는 유지6·교체1, 특정 판은 유지1, 애매층은 유지4다. 같은 N에서 H로 맞음→틀림, 보류→옳음, 보류→틀림으로 바뀐 사건은 모두0이다. 같은 H에 N을 추가하는 BH→BNH의 내용은12개의 보류 해소지만, 별도로 보존한 주 비교표는 BN→BNH/B→BH/B→BN이며 추가 비교를 사전 주 지표처럼 바꾸지 않는다.

G05는 이력 없이 충분한 좁은 반례다. 원 소비자가 -MM의 system-header 제외를 물으며 현 공식 절이 그 규칙을 직접 설명한다. H의 GCC10.1.0도 같은 규칙이므로 추가 H가 행동을 바꾸지 않았다. R03 역시 N에 이미 실제 함수 구현이 있어 H의 같은 정의는 행동 정보를 추가하지 않는다. G03은 원판 보존이 중요한 사례이나 그 판이 B와 현재2018 문서에 이미 명시되어 있어 **H가 없으면 실패하는 사례는 아니다**. 동일 N에서 원래 판 H가 꼭 필요했던 소프트웨어 사례는 이번 표본에서 발견되지 않았다.

단독 필터 결과를 하나의 엄격 분모로 합쳐 부르지 않는다. 수집 사전노출 제외10, 프로젝트/목적지 관계까지 제외3(G05/R02/R03), 거기에 N 카드이력 제외2(G05/R03), 판독자가 보고한 선행 연관사례와 카드이력 제외1(G05)에서 행동 변화는 여전히0이다. 모든 목적 번역·수집자 해석을 제외하면0, 외부 독립 gold만 남겨도0이다. 두0은 이력 무효과의 증거가 아니라 해당 검증이 없는 범위다. 필터별 모든12행의 포함/제외와 분자·분모는 sensitivity.csv에 보존되어 있다.

한 번의 내부 판독,9개 프로젝트의 상관,특정 판1개,이미 풍부한 N,중복된 H 때문에 작은 이익이나 드문 중요한 이익을 배제할 수 없다. 양성 사례를 만들기 위해 새 참조를 넣거나 당시 판독을 바꾸지 않았다. AF-RES-023/032와 표본·보기·규칙이 달라 그 연구의 숫자와 정확도 향상을 직접 차감하지 않는다.

## Q6. 실제 비용과 모의 비용은 누가 부담했나

수집·카드 구성의 실측은157 GET,169회 이상 HTTP exchange,실패11,수신/취득 당시 저장200,386,741B,요청별 경과 합1453.758885초다. 결정 봉인 뒤 기준판정은 추가59 GET,67 exchanges,실패2,56,698,339B,493.333131초다. **재개 감사 이전 두 단계 합은216 GET·236 exchanges·실패13·257,085,080B·1947.092016초**다. 후반 기준판정 원장이 원래 통합 집계에서 빠져 있던 것을 이번 재개에서 연결했다. 과거157값은 수집 단계 범위로 보존했고 과거 영수증을 새 합계로 덮지 않았다. [cost-summary.json](evidence/cost-summary.json), [review/resume-quant](review/resume-quant/), [ERRATA.md](ERRATA.md)를 참조한다. 이후 재개 감사의 GET/웹열람은 별도 phase 원장이며 그 합계를 [resume-cost-summary.json](evidence/resume-cost-summary.json)에 둔다.

수신 bytes는 fetch 도구가 받은 최종 응답 body이며 redirect 중간 body·header·wire bytes는 포함하지 않는다. 저장 bytes는 당시 임시 파일 크기이지 모든 원문이 원격 Git에 보존됐다는 뜻이 아니다. 병렬 요청 경과의 합은 사람 노동·총 벽시계·서비스 요금이 아니다. 실패·검색·도구 오류와 재요청을 지웠던 비용으로 만들지 않으며, 같은 archive 재사용4건은 새 네트워크 요청0과 논리 읽기를 분리했다. 표3의 참조별 취득 단위는 공유 배포물 때문에 서로 겹치므로 행 합을 전체 물리 비용으로 더하지 않는다.

2회차는 **실제 실행하지 않은 조건부 모의 계산**이다. 사전예산은 참조당 명시적 retrieval operation 최대2회·각30초이며 redirect exchange≤2도 별도 센다. 1회차와 같은 URL/응답크기/상태를 가정하고 경로를 이미 알고 있는 낙관적 C1이다. 현재 N 내용을 다시 얻는 과업에서는 C1/C2가 모두 물리17 GET·24 exchanges·3,056,003B(논리19/26/3,322,608B)로 같아 이력 보관의 조회 절감이 없다. N 전체 재구성에2 GET가 부족한 G01/G03도 그대로 남겼다. C1/C2 모두 operation수 기준10/12,exchange수 기준7/12만 예산 내이며 실제 timeout 성공은 미계측이다.

**같은 N/H 근거 내용을 다시 구성하는 별도 과업**에서는 C1 물리29 GET·37 exchanges·16,067,466B, C2 물리17 GET·24 exchanges·3,056,003B와 저장 H 읽기12회다. 차이는 모의12 GET·13 exchanges·13,011,463B다. 이 경우에만 H 보관이 재취득을 줄이는 조건이 생긴다. C1의 operation수 예산 충족6/12·exchange수3/12, C2는10/12·7/12다. H의 로컬 읽기 시간·판독시간은 측정하지 않았고 새 현재 UTC가 들어가면 원 packet hash도 그대로 복구되는 것이 아니다. 실제 시간 절감·서비스 손익분기점은 내놓지 않는다.

직렬화한 실제 저장 예시는 문맥+링크만 C1 7,754B,판·멤버를 이미 포함하는 봉인 B C1 12,153B, B+H+provenance C2 38,145B다. 모의 비교는 둘 중 더 강한 C1(B)을 사용했다. 따라서 C2 추가25,992B는 그 구체적 표현 사이 차이이며 데이터베이스·Git 압축·인덱스·보안·백업·모델 요금을 포함한 운영 원가가 아니다. C0의 최초 제품 발견비와 C1의 잃은 locator 재발견비는 미측정이다. 파일별 값은 [retention-options.jsonl](retention-options.jsonl)과 [retention-summary.json](evidence/retention-summary.json), 모든 모의 가정은 [replay-costs.csv](replay-costs.csv)에 있다.

## Q7. 다른 분야에서 최신판 교체는 무엇을 손상시키나

**지리의 실제 연결 쌍:** [Census 2022-06-06 공고](https://www.federalregister.gov/documents/2022/06/06/2022-12063/change-to-county-equivalents-in-the-state-of-connecticut)(CX-G04)를 [BLS QCEW 방법문서](https://www.bls.gov/cew/classifications/areas/new-2024-connecticut-counties.htm)(CX-G03)가 직접 링크한다. Connecticut의8개 historic county 대신9개 planning region을 쓰는 전환에서 BLS는2024 이전자료에 옛 county를 유지한다. 따라서2023Q4 원 집계를 재현하는 인용을 현재 지역코드로 일괄 교체하면 대상 지역을 바꾼다. 반대로 [ONS 2021–2023 ABPE 방법문서](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/internationalmigration/articles/dynamicpopulationmodelimprovementstodatasourcesandmethodology/localauthoritiesinenglandandwalesmid2021tomid2023)(CX-G02)는 과거 연도까지2023 경계로 제공한다. ‘과거 연도=옛 경계’도 실패한다. 원 데이터 수치나 이용자 피해·편집 노동을 측정한 것은 아니다.

**판·번역을 명시한 실제 서지 쌍:** [NLI vtls000410311](https://catalogue.nli.ie/Record/vtls000410311)(CX-B03)은1953 Blackwell·Anscombe 번역을 식별한다. [SEP Summer2022 Wittgenstein](https://plato.stanford.edu/archives/sum2022/entries/wittgenstein/)(CX-B04)의§3.6은1953 p.222를 지목하고 참고문헌은1953과2009 제4판을 따로 둔다. NLI로의 직접 href가 아니라 판·번역 식별자 일치에 의한 쌍이다. 단지 오래됐으므로 역사 목적이라고 추정하지 않았다. 1953와2009의 해당 문장을 실제로 대조하지 않았으므로 문구가 달라졌다고 주장하지 않는다.

**실제 정정과 남은 불일치:** [Nagoya NULDL000040](https://da.adm.thers.ac.jp/en/item/n003-20230901-00040)(CX-B16)의 Note는 head판 일부의 인쇄자 귀속을 Norton에서 Warren으로 고쳤다는 내용과 Takano2016 논문 pp.1–17을 명시한다. [그 원 논문](https://nagoya.repo.nii.ac.jp/record/21891/files/01_TAKANOAkira.pdf)(CX-B17)을 직접 읽어 문헌 연결을 확인했다. 현재 정정 문구는 실재한다. 다만 같은 catalog의 날짜 있는 정정 전후 snapshot은 없다. 별개 ornaments판 ESTC R13935의 [Nagoya](https://da.adm.thers.ac.jp/en/item/n003-20230901-00039)(CX-B11)와 [Grub Street](https://www.grubstreetproject.net/publications/R13935/)(CX-B13)는1680/ca1700/1695 귀속이 충돌한다. 이를 head판의 정정 사슬이나1953판 참고문헌 사슬과 합치지 않는다. 어느 연도가 참인지 판단할 원 연구의 일부 접근도 실패해 보류한다.

오늘의 독자는 현재 작업에 맞는 통계 범위나 책 판을 선택하고, 원판 재현 독자는 명시된 기간·경계·번역·페이지를 유지해야 한다. 편집자는 주소 이전과 의미 변경을 분리하고, 기록을 소비하는 설계자는 원 식별·정정 근거·적용 기간을 보존할지 결정한다. 현재 문서 자체가 예외·옛판 관계를 모두 서술하고 그 판을 재취득할 수 있다면 C1 재방문으로도 충분할 수 있다. 서로 충돌하는 귀속은 C2를 더 저장해도 자동 해결되지 않는다. 소급 정책,작품/판/소장본 구별을 소프트웨어 버전과 동일시하지 않는다. 두 분야는 소프트웨어12개의 수정률에 넣지 않았다. [collectors/cross/notes.md](collectors/cross/notes.md), [collectors/root/notes.md](collectors/root/notes.md)에 실패와 반대 해석도 남겼다.

## Q8. 보관 선택과 새 참조·정정·폐기 경로

이번 결과로032의 필드를 일괄 채택하지 않는다. 선택 가능한 작업을 다음처럼 한정한다.

| 선택 | 이번에 직접 비교할 수 있는 작업 | 채택 조건 | 잃거나 여전히 모르는 정보 |
| --- | --- | --- | --- |
| C0 요청 때 새 검색 | 발견용 검색/실패 로그의 일부만 있음; 제품의 최초 탐색과 질의 재구성 비용은 없음 | 반복 요청이 드물고 저장 이익을 따로 검증할 때 후보 | 같은 목적의 재발견률·시간·비용 비교는 이번 자료로 불가 |
| C1 문맥·조건부 링크 재방문 | 풍부한 B와 필요한 N을 제공한 현재 행동 판정12개; 조회 모의비용 | 최소 목적·필수 판이 남고 현재 필요 절과 적절한 판을 다시 찾을 수 있을 때 | 순수 링크-only7,754B 표현을 실제 판독한 결과는 없음; 배포 멤버/당시 근거를 버리면 재발견 필요 |
| C2 원 인용·근거·판·판정 이력 | 여기서 측정한 하위구성은 B+H+provenance 38,145B와 동일 N/H 재구성 모의; 판정이력 전체 비용은 미계측 | 감사·정정·과거 판단 이유 재현이 요청되고 필요한 원자료의 상실 위험/복구비를 감수하기 어려울 때 | 발췌는 전체 문서·새 기준·새 목적을 보장하지 않음; 이번12개에서 행동 개선은 관측0 |

**사례1, G05 현재 규칙 확인:** 새 참조에는 Make4.3의 Rules.html에서 -MM을 지목한 실제 문맥·href·배포/member hash를 등록한다. 이후 현재 GCC 절을 재방문해 같은 좁은 규칙을 확인하면 이번 행동 판정에는 충분했다. GCC10.1.0 H를 폐기하면 현재 규칙 확인은 가능하지만 당시 판과의 대조 근거를 다시 얻으려면 [고정10.1.0 절](https://gcc.gnu.org/onlinedocs/gcc-10.1.0/gcc/Preprocessor-Options.html)을 재취득해야 한다. 위 URL까지 버렸다면 탐색 비용은 미측정이다. 이번 표본에서 C2는 현재 행동보다 과거 대조 기록 재현에 가치를 남겼다.

**사례2, R01 workflow 정정:** 원 DESeq2 1.28.0 배포 HTML의 FASTQ→count 목적과 죽은 href를 보존하고, 오늘의404를 별도 관측으로 남긴다. 정정 때는 검증한3.11 HTML의 정확한 절을 새 도착지로 추가하되 원 href·원판을 덮어쓰지 않는다. H와 provenance를 폐기한 C1은 동일 과거 workflow를 복원하려면 rnaseqGene1.12.0 tarball/배포 멤버를 다시 찾고 읽어야 한다. C2는 저장 H의 정확한 바이트는 재생하지만 살아 있는 대체 HTML의 현재 적합성은 별도 확인해야 한다. 원래의404 판정 시각을 그대로 재현하려면 N 관측 영수증도 필요하며, 여기의 C2(B+H) 예시만으로는 그 시각이 보존되지 않는다.

특정 판 재현 목적은 B에 명시된2018과 현재2018 원문으로 G03 KEEP을 유지할 수 있다. 현재 최신 규격을 원하는 새 요청이라면 원 인용을 덮어쓰기보다 새 목적을 별도 기록하고2024판의 정확한 절을 검증해야 한다. 두 목적에서 다른 권고가 가능하다. 서지 귀속처럼 현재·이력이 모두 있으나 기준이 충돌할 때는 판정 보류와 결론을 바꿀 다음 원자료를 함께 보관한다.

## 원문 최소수·검산·재개 상태

최소수는 **고유 원문50 = 원 소비자12 + 현재 목적지10 + 별개 과거 원자료10 + 보조 분야16 + 기타 발행자 본문2**다. 현재 목적지10에서 코드와배포목록을 제외해도 설명 본문8이 남는다. ‘별개 과거 원자료’는 원문 단위 중복 제거이지 독립 발행자나 독립 정답이라는 뜻이 아니다. 현재/과거 함수·PDF/Rd·intro 중복은 하나의 원고군으로 세었다. 추가 기준판정64개 source record는 기존 행의 variants 또는 보충 비산입행으로 연결하며 원문 최소수50을 늘리지 않았다. [source-counts.json](evidence/source-counts.json), [source-aliases.json](evidence/source-aliases.json), [sources.jsonl](sources.jsonl)에서 모든 참조·판정 ID를 되찾을 수 있다.

재개 환경·시작판은 [resume-context.json](evidence/resume-context.json), 원래 시작 manifest는 [manifest.json](manifest.json)이다. 이번 재개는 기존 커밋을 초기화하지 않고 마지막 f403243 뒤의 미완료 집계·보고 묶음을 완성한다. 검산은 원문 의미의 참값을 증명하지 않는다. 동일 작성팀의 자체 검산,별도 문맥 판독,별도 문맥 기준 확인,새 원문 재조회,Git 계약·소유경로 검사를 구별한다. 최신 근거는 [SELF_CHECK.md](SELF_CHECK.md), [evidence/acceptance-evidence.json](evidence/acceptance-evidence.json), [PROGRESS.md](PROGRESS.md)에 있다. 최종 HANDOFF는 이 결과와 수용 근거를 고정 원격 SHA에서 재독한 뒤 작성한다.

## 가장 중요한 불일치 또는 약점

| 가장 중요한 불일치 또는 약점 | 근거 자료 주소 | 영향을 받는 결론 | 다음 조사 제안과 첫 자료 |
| --- | --- | --- | --- |
| 0/12는 풍부한 B/N·겹치는 H·같은 모델계열·특정 판1개 조건이다. G06/R04 사전노출, G06 stable 추가 한정과 후보 소진 공백도 있다. 모든 해석 또는 외부 종속 기준 제외 시 분모0이다. | [G03 원배포](https://archive.debian.org/debian/pool/non-free/g/gawk-doc/gawk-doc_5.1.0-1_all.deb), [G05 현 절](https://gcc.gnu.org/onlinedocs/gcc/Preprocessor-Options.html#index-MM), [sensitivity.csv](sensitivity.csv), [base-audit](review/base-audit.md) | 이력 일반무용론·순수 링크-only 충분성·실사용 정확도·H 인과효과는 판단 불가 | 첫 비교는 고정G05/G03의 현재 목적 질문에서 B의 edition/member를 보존한 입력과 문맥+href만 남긴 입력을 별도 미노출 판독한다. 같은사례 재사용 노출을 기록하고, 원판 재현 목적을 명시한 새 독립 소비자 묶음은 별도 사전 봉인한다. |
| 비용은 전체 수집·기준 확인 실측과 조건부 재조회 모의가 다르다. C1의 locator 재발견·사람 판독·실서비스·C0는 미측정이며 C2 예시는 원 N시각/전체원문을 보존하지 않는다. | [retention-options.jsonl](retention-options.jsonl), [replay-costs.csv](replay-costs.csv), [R01 대체절](https://bioconductor.org/packages/3.11/workflows/vignettes/rnaseqGene/inst/doc/rnaseqGene.html#preparing-quantification-input-to-deseq2) | 모의13,011,463B 차이를 실제 시간·돈 절감이나 전체서비스 최적해로 사용할 수 없음 | 첫 실행은 R01과G05의 저장구성별 파일만 제공한 새 문맥에서 최대2 GET·각30초를 실제 재생한다. 조회·실패·source 선택·본문 판독을 기록하고 N시각재현과 현재목적판정을 분리한다. |
| 서지의 명시 정정은 있으나 같은 catalog의 날짜 있는 정정 전후·소비자 반영 사슬이 없고, ornaments판 귀속도 충돌한다. | [NULDL000040](https://da.adm.thers.ac.jp/en/item/n003-20230901-00040), [Takano2016](https://nagoya.repo.nii.ac.jp/record/21891/files/01_TAKANOAkira.pdf), [R13935](https://www.grubstreetproject.net/publications/R13935/) | 현재 정정문구를 실제 수정일·전파율·정답독립성으로 확대할 수 없음 | 첫 자료는 ESTC R17253/NULDL000040의 Norton 표기 당시 고정record와 수정 영수증이다. 이어 R13935의2021 연구 pp.827–859 원문을 확보해 ornaments판 귀속충돌만 별도로 대조한다. |
'''
(P / 'RESULT.md').write_text(head + body, encoding='utf-8')

counts = {
    'references': len(R), 'routes': {'G': 6, 'R': 6}, 'publication_documents': 12,
    'projects': len({r['project'] for r in R.values()}), 'decisions': len(D),
    'views': AN['views'], 'fixed_N_H_action_changes': 0,
    'source_counts': SC, 'actual_costs_before_resume_audit': CS,
    'strict_all_collector_interpretation_removed_denominator': 0,
    'external_independent_gold_denominator': 0,
    'raw_excerpt_limit': 1600,
    'full_N_card_over_1600': {rid: c['N']['codepoints'] for rid, c in C.items() if c['N']['codepoints'] > 1600},
    'required_table_rows': [len(rows1), len(rows2), len(rows3)],
    'final_weakness_table_rows': 3,
    'limitation': 'Descriptive ledger recount; not a human outcome or causal effect estimate.'
}
(P / 'evidence/final-counts.json').write_text(json.dumps(counts, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'written': ['RESULT.md', 'evidence/final-counts.json'], 'required_table_rows': counts['required_table_rows'], 'references': len(R), 'decisions': len(D)}, ensure_ascii=False))
