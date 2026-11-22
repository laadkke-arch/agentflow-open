#!/usr/bin/env python3
"""Render the required 8-slot / 24-configuration report from the audit ledgers."""
import csv
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]


def cell(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')


def table(headers, rows):
    return '\n'.join(['| ' + ' | '.join(headers) + ' |',
                      '| ' + ' | '.join(['---'] * len(headers)) + ' |'] +
                     ['| ' + ' | '.join(cell(value) for value in row) + ' |' for row in rows]) + '\n'


def url_links(urls):
    labels = []
    for index, url in enumerate(urls, 1):
        parsed = urlparse(url)
        part = parsed.fragment or parsed.path.rstrip('/').split('/')[-1] or parsed.netloc
        labels.append(f'[{index}:{part}]({url})')
    return '; '.join(labels)


def flag(value):
    return '확인(1)' if value else '미확인(0)'


def main():
    cases = json.loads((ROOT / 'cases.json').read_text())
    summary = json.loads((ROOT / 'analysis-summary.json').read_text())
    counts = json.loads((ROOT / 'source-count-summary.json').read_text())
    sens = json.loads((ROOT / 'sensitivity-summary.json').read_text())
    with (ROOT / 'readings.csv').open() as f:
        readings = list(csv.DictReader(f))
    text = '''# AF-RES-047 — 공개 분석의 발행판·사용 선언·실행 입력·정정값

**핵심 관측:** 발행판에 도달한 사실과 그 분석이 그 판을 사용했다는 사실은 다른 기록을 요구했다. 자연층6건에서 발행자가 구별한 후보판은4건, 외부 판·파일의 구체적 사용 선언은1건, 원 실행을 외부 발행자 객체까지 연결한 사례는0건이었다. 실행 보강2건은 local 입력 연결을 둘 다 남겼고, RUN02는 전체 파일 대조 뒤 **발행자의 체크섬과 같은 원 실행의 R1 입력 기록을 연결했다(R=1/2)**. 그러나 고정한 보고 필드까지 독립 확인한 V는 두 층 모두0이다. 입력 객체의 확인과 보고값 검증을 같은 성공으로 합치지 않는다.

이 문서는 **부분 인계**다. 8슬롯·24구성·직접 원문 배당은 채웠지만, 완전히 사전 고정된 최초 적격 표본이라는 조건과 고정 URL/동일bytes의 실제 미사용 음성례 등은 미충족이다. 0은 이 조사에서 해당 근거를 확인하지 못했다는 표시이며, 실제 사용이 없었다는 판정이 아니다. 필수 두 표를 먼저 제시하고 그 뒤에 분모·선정 한계·반증·적용 조건을 둔다.

## 표 1. 핵심 8슬롯

P는 구별 가능한 외부 발행판 존재, U는 외부 판·파일에 대한 구체적 사용 **선언**, R은 같은 원 실행에서 외부 발행자 객체까지의 연결, V는 진본 사용판과 선정 필드의 독립 대조다. R_local은 보관된 local 파일까지의 실행 선언이며 별도다. 후보값 일치와 C의 기록 재독은 V에 합치지 않는다.

'''
    headers = ['층·분석·필드','소비 목적·기준일','소비자 주소·절','발행판·값·주소',
               '사용했다고 지목한 판·근거','실행 ID·입력 근거','확인 가능한 가장 강한 주장','현재 정정·미확인']
    rows = []
    for c in cases:
        layer = '자연/R Journal' if c['case_id'].startswith('RJ') else '자연/ESSD' if c['case_id'].startswith('N-E') else '실행 보강'
        rows.append([
            f"{c['case_id']} · {layer} · {c['analysis_title']}; 주 필드: {c['field']}; 보고값: {c['reported_value']}",
            f"{c['purpose']}; {c['target_time']}",
            f"[소비 원문]({c['consumer_url']}) — {c['consumer_locator']}",
            f"P={flag(c['publisher_exists'])}; {c['publisher_edition']}; {c['publisher_value']}; [발행자]({c['publisher_url']}) — {c['publisher_locator']}",
            f"U_external={flag(c['specific_usage'])}; {c['usage_edition']}; {c['usage_evidence']}",
            f"R_external={flag(c['run_link'])}; R_local={'확인' if c.get('local_run_link') else '미확인'}; {c['run_id']}; {c['run_input_evidence']}",
            c['strongest_claim'],
            f"{c['current_correction']}; 미확인: {c['missing_reason']}",
        ])
    text += table(headers, rows)
    text += '''
## 표 2. 같은 사례의 A/B/C 24구성

A=소비 원문의 목적·인용·링크, B=A+발행자 판/위치, C=B+당대 소비 기록이다. 주소는 누적하고, 원문 URL이 같아도 포함한 절·파일 내부 범위는 아래와 readings.csv에 고정한다. `audit_only_*` 열은 전체 감사 문맥이며 보이는 구성에서 제외한다. RUN A/B의 행 값과 상세 실행 시각은 C가 추가되기 전까지 결측이다. 이 표는 동일 조사자의 누적 근거 감사로, 눈가림 성능 실험이 아니다.

'''
    headers2 = ['사례·자료 구성 A/B/C','보이는 근거 주소','발행판 특정','사용 선언','실행 연결',
                '같은 필드 값 대조','판단·미확인 이유','B−A 또는 C−B에서 새로 확인한 사실']
    rows2 = []
    for r in readings:
        b = lambda key: r[key] == 'True'
        rows2.append([
            f"{r['case_id']} · {r['configuration']}",
            url_links(json.loads(r['visible_urls'])) + ' — 포함 위치: ' + r['exact_locations'],
            flag(b('publisher_specific')),
            '외부 U ' + flag(b('usage_specific')) + ('; local 선언 확인' if b('local_usage_specific') else ''),
            '외부 R ' + flag(b('run_link')) + ('; R_local 확인' if b('local_run_link') else ''),
            '보이는 값: ' + '; '.join(str(x) for x in json.loads(r['visible_values'])) +
            '; strict V ' + flag(b('value_checked')) +
            ('; 후보 동일필드 양립 확인' if b('candidate_value_checked') else '') +
            ('; **기록 재독**' if b('record_reread') else ''),
            r['judgment'], r['new_fact'],
        ])
    text += table(headers2, rows2)
    text += '''
## 1. 분모와 원문 수 — 자연층과 실행 보강을 합쳐 보존율로 부르지 않는다

'''
    rows3 = []
    for key, label in [('natural_primary_after_A01','자연층6: 정정 선정'),
                       ('natural_original_before_A01','자연층6: 최초 선정 감도'),
                       ('execution_supplement','실행 보강2')]:
        item = summary[key]; n = item['denominator']
        rows3.append([label, ', '.join(item['case_ids']),
                      f"{item['publisher_exists']}/{n}",f"{item['specific_usage']}/{n}",
                      f"{item['local_run_link']}/{n}",f"{item['run_link']}/{n}",
                      f"{item['value_checked']}/{n}",f"{item['candidate_value_checked']}/{n}"])
    text += table(['층','사례','P 발행판','U 외부 사용 선언','R_local','R 외부 객체','V 진본 필드','후보 필드 대조'],rows3)
    text += '''
외부 원객체와 원 실행의 연결이 확인된 사례 중 값 검증은 자연층에서 분모0이므로 **해당 없음**, 실행 보강층에서는 **0/1**이다. RUN02의 R은 당사자의 구체적인 원 실행 기록과 독립 발행자의 fingerprint가 만난 결과다. 별도 syscall 관측이나 모든 입력의 검증을 뜻하지 않는다. 원래 선정한 GNIP N-E03을 WoRMS N-E00으로 교체한 A01 전후 수치는 같지만 표본이 같다는 뜻은 아니다. GNIP의3구성은 collection/essd/readings-before-A01.csv와 최신 legacy 사례에 남았다. 원문/판/파일/실행을 각각 세어 얻은 수를 하나의 성공률로 합치지 않는다.

B에서 후보판 확인은6/8, 후보 동일필드 양립은1/8이다. C에서 외부 특정파일 사용 선언은2/8(RJ02,RUN02), local 실행 연결은2/8(RUN01,RUN02), 외부 발행자 객체까지의 기록상 연결은1/8(RUN02), 값/분류가 답 형태로 보존된 추가 기록 재독은4/8(RJ02,N-E00,RUN01,RUN02)이다. **독립 진본 필드 V는 모두0**이다. 두 층을 합친 이 수들은 구성 차이를 설명하는 기술 집계이며 자연층의 보존율 추정이 아니다. 코드 절차 재독(N-E02)과 출력값 재독은 별도다.

'''
    allocation = counts['allocation']
    text += table(['원문 역할','필수','산입 고유 저작','판정'],[
        ['소비 분석/원 실행 보고',8,allocation['consumer_original'],'충족'],
        ['발행자 판·파일·정정',8,allocation['publisher_edition_file_correction'],'충족'],
        ['저자 당대 기록/실제 provenance 사례',4,allocation['author_contemporary_record'],'충족; 초과3을 다른 배당으로 전용하지 않음'],
        ['공식 통계 운영 원문',2,allocation['official_statistics'],'충족'],
        ['지구과학 운영/실제 판 사례',2,allocation['earth_science'],'충족'],
        ['별도 보조 규칙/실제 record',0,allocation['supplementary'],'주 배당의 빈자리를 채우지 않음'],
    ])
    text += f'''
sources.jsonl의 **{counts['ledger_rows']} 접근/열람 행** 가운데 보수적으로 최소수에 산입한 고유 저작은 **{counts['conservative_unique_direct_works_admitted']}개**다. 필수 역할 배당에 해당하는 고유 저작만 세면 **{counts['quota_eligible_unique_works']}개**로24개 이상이고, 각 배당도 충족한다. 여러 R판/UCI 변형은 Iris 한 계보, CRAN16파일은 이번 입력 코퍼스 한 저작, IOW 두판은 한 저작, 원 NOAA의 여러 보존 캡처는 한 저작으로 묶었다. 실패·목록 노출·재방문·다른 절은 추가0이다. 같은 저작의 실제 내용 열람 source ID도 대표행에 연결했다.

보강 기록 배당의 LivePublication와 WOMBAT는 별도 AUX 사례다. LivePublication는 input_data.txt의 외부 생산자/판을 확인하지 못해 핵심 소비표본에서 제외됐고, WOMBAT는 뒤 순서의 실제 실행 산출물·graph를 보조로 읽었다. 이 둘을 핵심8 소비 분석이나 외부 입력판 검증 성공으로 바꾸지 않았다. source-count-summary.json은 보수적 산입 목록과 필수 역할27/전체31을 나눠 재계산한다.

## 2. Q1·Q2 — 판 보존 성과를 보기 전에 고른 방법과 남은 선정 한계

R Journal은 [2022-1](https://journal.r-project.org/issues/2022-1/) 22편과 [2022-2](https://journal.r-project.org/issues/2022-2/)18편의 metadata를 확보해 발행일·식별자 순 첫30을 남겼다. 앞선 실제 본문에서001/003/005는 모의/가정 예제로 분리했고,004/006/007을 선택했다.001 §4의 가정 parameter,003의생성예제,005의모의생존자료가 제외 근거다.006/007/008 본문이 목차순으로 우연히 먼저 보인 노출은 selection_freeze.json에 보존했다. 발행자 판·정정 성과를 보고 교체하지 않았다.

ESSD는 [2022 issue1](https://essd.copernicus.org/articles/14/issue1.html)에서 시작해 [issue2](https://essd.copernicus.org/articles/14/issue2.html)로 이어 첫30을 보존했다. 마지막은2022-02-09의14-559다. 처음에는 첫 논문의 Group와 WoRMS 필드 연결이 불명확해19/33/57쪽을 고정했다. 그러나 [14-1 §3](https://essd.copernicus.org/articles/14/1/2022/#section3)은 실제 nomenclature 재사용을 명시한다. 추적성 결측을 선정 단계의 제외 조건으로 쓰면 약한 사례를 제거한다는 반증을 받아 A01로1/19/33쪽을 주 표본으로 삼았다. 원선정·변경이유·영향·집계를 모두 보존했다. 결정은 WoRMS 열람 전이지만 변경의 원격 커밋은 그 뒤였으므로 엄격한 사전 원격 봉인으로 부르지 않는다. 앞선5쪽 논문의 현장 기상자료 생산주체/공개성은 확인한 범위에서 적격을 확정하지 못한 한계도 남긴다.

실행 프레임은 [Workflow Run RO-Crate 목록](https://www.researchobject.org/workflow-run-crate/)과 그 실제 연결 논문/저장소에서 출발했다. 원19 metadata를 보존하고 연결 examples까지38노출,2021–2024 해당31개 중 날짜·식별자 순 첫30을 기록했다. RUN01은5위, RUN02는18위다. 정의-only, synthetic BackTrackBB, MIRAX test-image 시연, Galaxy collection demo, Autosubmit test domains, private Promort input을 제외/미확인으로 구별했다. 더 이른 LivePublication는 실행이 있지만 제3자 공개 입력의 생산자·객체를 확인하지 못했다. 따라서 **관측한 후보 중 최초 두 적격 확인 사례**이며, 전체 최초 두 적격이 확정됐다고 주장하지 않는다. metadata의 embedded datePublished/export 날짜가 최초 공개일과 같은지도 독립 입증하지 못했다. 근거는 collection/runs/frame-first30.csv의 eligibility/date_basis와 selection freezes다.

한 논문 안에서는 실제 입력을 밝히는 본문 순서, 그 입력을 쓴 첫 표/그림/예의 첫 해당 필드 순서를 적용했다. 정확값을 읽기 어렵다고 다음 필드로 넘어가지 않았다. RJ01의 정확 PC1과 N-E01 첫 산점도 점은 결측이다. RJ03 runtime/error를 Iris 통계값으로 혼동한 가능성을 제거해 Df를 고정했고, RUN01은 HDF5 물리block순과 논리열순의 오인을 A06으로 정정했다. 이 수정이 없는 것처럼 보고하지 않는다.

## 3. Q3·Q4 — 추가 기록이 바꾸는 문장의 단계

**발행자 판을 알면 제공된 객체를 말할 수 있다.** BCO v3.0.0은 [발행자 §4/Assets](https://essd.copernicus.org/articles/13/491/2021/#section4)에서 구별된다. 하지만 [소비자 Fig5](https://essd.copernicus.org/articles/14/19/2022/#section4)의 level·파일·paired point 선택은 따로 필요하다. 자체 RAAVEN B1이나 자체 IOW release2를 외부 입력판의 빈칸에 넣을 수 없다.

**당대 명세가 있으면 사용 선언을 구체화할 수 있다.** RJ02는 취득일만 있는 줄 알았으나 [당대 v1.0 archive](https://zenodo.org/records/4026589)에서1998 선택16개 filename/version을 찾아 U를0에서1로 바꿨다. 고정 target_meta와feature record의경로16/16은 일치했고, 현재 공식 CRAN16/16에 도달했다. 그러나 소비자가 읽은 tar의당시hash는 없고, exact0/386은저자파생기록이다. 이 반증 때문에 “부록도 도움이 없었다”는 결론을 버렸고, 동시에 “같은이름을찾았으니실제입력확인”이라는 승격도 하지 않았다. [고정 commit](https://github.com/chainsawriot/rstyle/tree/07a60457c88dbb20858441047f248d61ce2955c7)의target_meta/feature/figures.R를 같은 저작계보로 취급한다.

**실행 ID와 local 입력에 발행자의 fingerprint가 만나면 한 단계 더 강한 문장을 허용한다.** RUN01은 prov_test.log의 table hash가 전체 HDF5 파일hash가 아니며, v1.1 preprocess는 원 test보다 뒤다. RUN02는 같은 [Zenodo archive](https://zenodo.org/records/12622362) 내부의 action `#bdfcc6a4-3bf4-4fd7-9e8c-cc6b0deaa43d`→Collection `#dcc0e6bb-4888-4bee-bc06-e995b5d18538`→R1과 stderr85/105–114의 처리 기록을 연결했다. GitHub export의 다른 UUID와 합치지 않았다. archive의 전체 R1 gzip487,611,787bytes는 crate SHA256 선언과 일치하고, 계산 MD5 `52f3ed344d88278c703faa1280818ce1`은 [발행자 HG001-part2.md5](https://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/data/NA12878/NIST_NA12878_HG001_HiSeq_300x/HG001-part2.md5) **388행의 정확한 flowcell/project/sample/R1 경로**와 일치했다. 이것이 빠졌던 local 객체→외부 발행자 객체의 연결을 채워 R0→1을 바꿨다(A10).

현재 발행 gzip413,005,346bytes는 그 목록의 MD5와 다르지만, 두 gzip을 전체 해제한1,409,966,879bytes의 SHA256은 모두 `98be27b898b6ae3c12821a30b48adc1bfec9d98903219f0175240ebac66fccf3`이다. 이 결과는 첫20개 read의 부분 일치에 머물렀던 초기 결론을 반증한다. 실행 당시 입력을 지목하는 기록과 발행자 fingerprint의 만남은 확인했지만, 취득·재압축 시각/행위자·공식 이유는 미확인이다. 고정 출력 CHROM=1은 여전히 같은 저자 출력의 재독이며 raw FASTQ의 같은 필드 대조가 아니므로 V=0을 유지한다. [CPM](https://zenodo.org/records/8095888)과 RUN02의 범위를 구별하며, 전체 전송 영수증은 collection/runs/wetlab-full-fastq-comparison.json 및 wetlab-full-checksum-revisit.json이다.

**원문 복원도 판별 성공과 다르다.** NOAA RUC의현행주소는실패했지만 [2021 General Information 보존본](https://web.archive.org/web/20211205084551id_/https://ruc.noaa.gov/raobs/General_Information.html)을직접읽어IGRA/GSL/GTS병합과stationhistory/출력형식을확인했다. 요청한캡처와실제도착캡처를따로썼고,ASCII0.1°C와NetCDFkelvin을같은수치로읽지않았다. RUC원저작은복원됐지만1994–2016훈련export의내용·판·원run은미확인이다. schema문서의Forecast Systems Lab1.3도데이터판이아니다.

이 단계별 판정에는 source lineage가 중요하다. 논문과 그 복사본, 저자가 게시한 같은 archive와 그 GitHub mirror, 같은 artifact의 다른 member는 독립 기준이 아니다. 별도 발행자 파일과 당대 사용기록이 같은 객체·필드에서 만날 때만 더 강한 진본 사용판 주장을 허용한다.

## 4. Q5 — 과거 재현과 지금 재사용의 판단은 같지 않다

'''
    text += table(['사례/쌍','원래/새 값 또는 범주','판정·적용 조건','근거·위치'],[
        ['RJ03 / R4.2.0→4.2.1 후보 멤버','Df2→2, iris.R bytes 동일','발행 연속판 비교는 성공. 어느 판을원논문이썼는지는미확인.','[R4.2.0](https://cran.r-project.org/src/base/R-4/R-4.2.0.tar.gz), [R4.2.1](https://cran.r-project.org/src/base/R-4/R-4.2.1.tar.gz), datasets/data/iris.R'],
        ['RJ03 / UCI 동시게시 변형','35행Petal.Width0.1→0.2,38행Petal.Length1.5→1.4; SumSq436.6/437.1, Df모두2','날짜가매겨진다음판으로확정한쌍은아님. Df예제에는유효,정확측정값/전체ANOVA에는영향.','[UCI](https://archive.ics.uci.edu/dataset/53/iris) Additional Information/ZIP35·38행'],
        ['N-E00 / IOW 자체출력 release1→2','첫Group동일; 두record의Region/Station변경; 같은B148=1의종명이바뀜','과거 Group 재독과현재지역별계수재사용을분리. 외부WoRMS입력성공아님.','[release1](https://doi.iow.de/10.12754/data-2021-0002), [release2](https://doi.iow.de/10.12754/data-2021-0002-01), raw ID7315/13306와Factors Baltic Sea!A148:B148'],
        ['RUN01 / consumercrate v1→v1.1','predictions.h5/prov_test.log byte동일; preprocess ID/날짜변경','결과file불변이실행계보불변을뜻하지않음. 외부CAMELYON다음판쌍아님.','[v1](https://zenodo.org/records/7676924), [v1.1](https://zenodo.org/records/8095888), prov_preprocess.log/prov_test.log'],
        ['RUN02 / publisher와archive gzip','413005346/487611787bytes로압축파일은다름; 전체decoded1409966879bytes/SHA256동일; publisher MD5목록은archive와일치','선택R1의기록상원실행→publisher객체연결R=1. 날짜가매겨진다음발행판/정정사유는미확인; CHROM1독립검증V=0.','[NIST MD5](https://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/data/NA12878/NIST_NA12878_HG001_HiSeq_300x/HG001-part2.md5) L388; [crate](https://zenodo.org/records/12622362) R1 member; wetlab-full-fastq-comparison.json'],
        ['AUX-EARTH-01 / 발행자 next edition','depth0.045m Age2.1→2.574kaBP;230Th310.292동일','현재나이판단에는개정적용;당시문장재현은원판보존. 같다는다른필드로판을특정못함.','[889928](https://doi.pangaea.de/10.1594/PANGAEA.889928?format=html), [936557](https://doi.pangaea.de/10.1594/PANGAEA.936557?format=html), Data/Comment'],
    ])
    text += '''
RJ01의1992→2018, GNIP 감도의1986–1989→2015–2018은 대상시점이 다른 자료이며 정정판쌍이 아니다. RJ02의 acepack 다음파일 하나는 전체16파일코퍼스의다음판이 아니다. N-E01은사용판/다음판파일을읽지못했고, N-E02는자체출력156→235의정정공지와원RUC입력을나눴다. 같은19Jan LWP의구판/신판값은미대조다. 전8사례의빈자리와재개첫행동은contradictions.md §4에있다.

반올림/필터/결측도판별조건이다. RJ01의반올림표준편차2.40을제곱해정확PC1값5.76이라고만들지않았다. RJ02는NULL result제외와exportedfunction분모386을보존했다. N-E02는nanmean을읽었지만cloudy-only median11과all-time median주석2.6817865를같은대상으로비교하지않았다. RUC형식문서의단위·결측코드와실제export선택을구별했고, PANGAEA Age20.4/20.391은소수1자리로같아져도원값이같지않음을확인했다. 접근실패/다른필드/다른기간은수치불일치로세지않는다.

## 5. Q6 — 공식 통계·지구과학·소프트웨어 관행을 서로 시험하기

'''
    text += table(['관행','직접읽은원문·위치','남기는구별','그기록만으로부족한것'],[
        ['공식통계 발표일','[ALFRED help](https://alfred.stlouisfed.org/help), How are Release Dates determined? / growth rates','원발표일,제공자날짜,FRED최초입수일의대체순서; 반올림level에서계산한growth차이','분석실행일/실제download영수증은별도'],
        ['공식통계 빈티지','[ALFRED download](https://alfred.stlouisfed.org/help/downloaddata), Vintage Dates/Output Formats','관측일행과빈티지열; 값불변인발표는revision목록에서빠질수있음','같은값이같은빈티지라는추론불가'],
        ['지구과학 DOI 계층','[NASA CMR DOI](https://wiki.earthdata.nasa.gov/spaces/CMR/pages/107385989/DOI), Element Description/PreviousVersion','collection DOI와이전판·발행/제공기간·폐기일','collection을특정granule/변수/run으로승격불가'],
        ['지구과학 실제정정','[PANGAEA889928](https://doi.pangaea.de/10.1594/PANGAEA.889928) Change history와[936557](https://doi.pangaea.de/10.1594/PANGAEA.936557) Comment/Data','저자목록정정과age-model 새판을구별;동일키실제값비교','소비자가그판을썼다는별도당대기록'],
        ['소프트웨어release/입력manifest','[R4 releases](https://cran.r-project.org/src/base/R-4/), [rstyle v1.0](https://zenodo.org/records/4026589) target_meta','release와파일member,파일명과내부Version,의도된입력과실제run을구별','hash/lock/script만으로실제read증명못함'],
    ])
    text += '''
보조 [GNPC96](https://alfred.stlouisfed.org/series?seid=GNPC96) Notes/Units는같은seriesID에도2012년기준연쇄달러와2017년기준단위기간이달라짐을보여준다. 개별빈티지값을이번에읽었다고하지않는다. [CMIP6 §4](https://pcmdi.llnl.gov/CMIP6/Guide/dataUsers.html)는판/다운로드날짜를, [ESGF errata API](https://ipsl.gitbook.io/esgf-errata-service/errata-service-api)는특정판과전체계보의오류탐색을구별한다. 이운영규칙을읽었다고선정분석이실제로이를준수했다고가정하지않는다.

서로다른정확URL이같은bytes를반환한실제예는 PANGAEA889928의`format=textfile`과`format=textfile&charset=UTF-8`이다. 전체9394bytes/SHA256일치를직접확인했다. DOIresolver를거친실패시도는HTML로도착했으며표현차이로기록했다. 반면 **고정URL의동일bytes와함께그파일을읽지않은특정실제분석실행의음성영수증은찾지못했다.** 미래Rrelease와CPM시간역전은이강한음성주장을대신하지못한다. PANGAEA저자목록정정은메타데이터정정공지까지확인했으며직전/직후payload불변은미확인이다.

'''
    text += table(['관점','목적에필요한최소정보','사라지거나혼동될근거','허용문장'],[
        ['자료발행자','저작/판/파일ID,발행·수정일,기준기간,단위,정정필드','동적URL교체,옛파일철거,collection/granule혼동','그판의그파일/값을제공했다'],
        ['분석작성자','원runID,exact입력객체/취득시각,행·필드·변환·필터·반올림','local latest/glob,미보관입력,실행안한취득script','기록상그실행이그객체를읽었다'],
        ['나중감사자','별도계보publisher객체+당대사용record,같은키값대조','논문복사본을독립증거로세기,다른run로그합치기','확인된고리와필드범위만재확인했다'],
        ['최신값이용자','현재목적/기준일,현행정정영향범위,단위·기간','과거정확인용을현재유효성으로승격','현재용도에서유지/정정/보류;실제채택은별도'],
    ])
    text += '''
## 6. Q7 — 다섯 기록 항목의 정보 제거 감도

시간목적·자료식별자·실제사용근거·당시값·현재정정을8사례에서하나씩뺀40행은sensitivity.csv에있다. 판정대상은 **원래목적에한정한가장강한기록문장**이다. 사용판과선정값을함께확인하는엄격V는원래0이며제거후에도0이다. 반면RUN02의외부입력연결R은자료식별자나실제사용근거를제거하면1→0으로변한다. 이미없는자료를지웠다고새정보손실로세지않는다. 아래숫자는규칙에따른근거감사이며실제사람의오답률/채택률이나인과효과가아니다.

'''
    text += table(['제거항목','행수','유지/정정/보류표시변화','적용사례와잃는판정'],[
        ['시간목적',8,sens['by_removed_item']['시간 목적']['decision_changes'],'RJ02:1999파일을1998표본에넣는오류; RJ03:논문이후release; RUN01:나중preprocess를원test와결합하는오류를거르기어려움'],
        ['자료식별자',8,sens['by_removed_item']['자료 식별자']['decision_changes'],'RJ02 16filename이사라지면U1→0; RUN02 fullflowcellpath를빼면동명파일구별불가; N-E00입력/출력DOI혼동'],
        ['실제사용근거',8,sens['by_removed_item']['실제 사용 근거']['decision_changes'],'RJ02 당대명세제거로사용선언소실; RUN02 action→input연결소실; RJ03 원기록은원래없어새손실0'],
        ['당시값',8,sens['by_removed_item']['당시 값']['decision_changes'],'RJ02 0/386재독기준, RJ03 Df2비교, N-E00 Amphipoda재독기준소실; RJ01/N-E01 정확값은원래결측'],
        ['현재정정',8,sens['by_removed_item']['현재 정정']['decision_changes'],'표시변화0이라도제약은약해짐: IOW지역별이동, UCI35/38행, DOI156→235공지없으면잘못된현재재사용을거르지못함'],
    ])
    text += f'''
총{sens['decision_changes']}행에서기록문장의상태표시가달라지고, 원래결측이라새손실0인행은{sens['already_missing_no_new_information_loss']}행이다. 현재정정제거에서표시변화가0인것은정정정보가불필요하다는뜻이아니다. 대부분의엄격사용판판정은이미보류이고, Df같은좁은역사목적의유지를그대로두었기때문이다. 셀별로잃는현재용도제약을따로썼다. 이한계를없애고'정정정보의효과0'이라고요약하면감도표의목적을벗어난다.

추천이력에남길최소레코드의적용제안은다음과같다. 이제안은관측으로부터의설계추론이며사용자채택실험결과가아니다.

- **시간목적:** 당시재현/현행값재사용,대상기간,판단기준일,조회UTC를따로둔다.
- **자료식별자:** concept/edition/file ID,원/최종URL,실제hash와알고리즘·계산범위,단위/행키를구별한다.
- **실제사용근거:** 인용/구체사용선언/localrun연결/publisher객체연결을따로표시하고runID별입력목록을남긴다.
- **당시값:** 출력필드·값·정밀도·필터/결측/변환,원문절/표/행,author재독인지독립publisher대조인지기록한다.
- **현재정정:** 다음판의같은키값,정정사유·효력범위·확인UTC,목적상유지/정정/보류와미확인재개첫행동을남긴다.

## 7. 검산·실행하지않은일·후속최소행동

고정원문/파일GET,ZIP member/JSON/RDS/HDF5/VCF의선택읽기,바이트hash,작은Iris/IOW값대조와RUN02의두R1 gzip 전체스트리밍/해제hash대조를실행했다. 전체FASTQ검사는2026-11-22T23:00:16Z–23:09:38Z에exit0으로끝났고명령·입력·archive Range응답63개와publisher전체GET1개·실행당시scriptSHA를영수증으로보존했다. 논문의원래R환경,ANN훈련,ML병리분류,variant-calling 전체는재실행하지않았다. codehash는inputhash가아니며원실행ID도아니다. 세부명령/입력은각collection/findings.md와RAW_DISPOSITION/재개문서에있다. source원장각행의직접확인범위밖으로일반화하지않는다.

자체재판독과동일모델별도문맥검토를구별했다. collection/rjournal/root-integration-review.md는초안의A/B/C누출과nestedU이름충돌을찾아수정후확인했지만외부독립판독은아니다. SELF_CHECK.md는Q1–Q7의반대근거/뒤집을최소자료를연결하고,evidence/acceptance-evidence.json은기계적형식충족과내용상미충족을나눈다. 작업세션check는소유경로·입력계약검사이며연구의진본사용검증을대신하지않는다.

가장작게남은판정을바꿀후속작업은**RJ02의1998 선택16tar에대한당대입력fingerprint/run receipt와원export·lintr환경을찾아고정명세에연결하는것**이다. RUN02의전체decodedFASTQ대조는완료됐으며후속은원실행의나머지입력·변환·고정CHROM행을독립검증하는것이다. 당대입수/재압축시각은별도결측이다. 나중재현성공만으로과거실행전체를증명하지않는다. 실제당사자에게연락하거나추가계정접속하는행동은이번작업에서수행하지않았다.

## 남은 불일치·약점 — 종료 시점의 세 항목

'''
    text += table(['불일치 또는 약점','영향받는 결론','근거 주소·위치','다음 최소 조사','판정이 바뀌는 조건'],[
        ['초기선정해석A01/A06수정·앞선적격미확인·export날짜한계','완전사전고정된최초6+2라는주장과모집단보존율일반화','[ESSD14-1 §3](https://essd.copernicus.org/articles/14/1/2022/#section3); [실행목록](https://www.researchobject.org/workflow-run-crate/); amendments.md A01/A06/A08','앞선ESSD5쪽외부입력생산주체와LivePublication input원출처/공개일확인','앞선후보의적격/부적격과발행일이독립자료로확정되면표본확실성판정수정'],
        ['외부입력R은RUN02 1건확인했지만선정필드독립V는0; 정확주값2건결측','그분석이그판의그값을실제로썼다는엄격양성은미확인','[RJ02 v1.0](https://zenodo.org/records/4026589) target_meta/feature; [Wetlab](https://zenodo.org/records/12622362) action/input; [NIST MD5](https://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/data/NA12878/NIST_NA12878_HG001_HiSeq_300x/HG001-part2.md5) L388; readings.csv','당대input명세와같은행키/변환의독립값대조를연결','다른계보의publisher객체와당대run이선정필드값까지만나면해당V만승격'],
        ['고정URL·같은bytes·실제미사용음성례미확보; 순수metadata변경의전후payload도미확인','주소/해시가사용을증명하지못한다는실증범위와현재재사용완전성','[PANGAEA Change history](https://doi.pangaea.de/10.1594/PANGAEA.889928); [CPM v1.1](https://zenodo.org/records/8095888) logs; contradictions.md §3/5','실제run의배타적input-read영수증과동일publisherbytes,정정전후payload확보','실제미사용과bytes동일성이함께확인되거나metadata-only전후파일이확인될때해당조건충족'],
    ])
    (ROOT / 'RESULT.md').write_text(text)
    print(json.dumps({'result_chars':len(text),'primary_rows':len(rows),'configuration_rows':len(rows2)},ensure_ascii=False))


if __name__ == '__main__':
    main()
