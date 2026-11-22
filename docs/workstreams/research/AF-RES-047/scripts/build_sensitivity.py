#!/usr/bin/env python3
"""Forty explicit evidence-removal audits; not a user experiment or model trial."""
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ['시간 목적', '자료 식별자', '실제 사용 근거', '당시 값', '현재 정정']
# state, after decision, lost claim / reason, minimum restoration.
SPEC = {
 'RJ01': ('보류', [
  ('present','보류','1992와2018이 다른 대상기간이라는 제한을 잃는다. 0.44가 같아도 동일판이라는 주장은 불가.','1992/2018 기준기간과 원 PCA 목적'),
  ('present','보류','INS1992 후보판과 연구 workbook을 구별할 대상 식별을 잃는다. P의 적용 대상 미확인.','INS 표·판과 research_data.xlsx의13열 대응'),
  ('partial','보류','논문의 census 이용 진술과 부록의 workbook 경로가 사라져 이용 선언도 유지 못 한다.','소비자 §2 및 부록12,17–21행'),
  ('missing_exact','보류','정확한 PC1 값은 원래 결측이다. 새 정보 손실0; 2.40²로 대체하지 않는다.','Fig2 원 값과 생성 행렬'),
  ('missing','보류','같은 기준기간의 현재 정정값은 원래 결측이다. 새 정보 손실0.','같은13필드·1992행의 발행자 정정표'),
 ]),
 'RJ02': ('유지', [
  ('present','보류','1998 선택 표본이라는 제한이 없어져1999 다음판이나2020 저장행을 같은 분석에 넣는 것을 거르지 못한다.','§2.1 시간범위와config.R 종료연도'),
  ('present','보류','16개 filename/version을 잃으면 취득일만 남는다. 외부 파일 사용 선언 U1→0.','고정 target_meta의1998 16경로'),
  ('present_specific','보류','발행자16파일은 존재해도 저자가 선택했다는 당대 명세가 사라져 U1→0.','target_meta와syntax_feature의같은16경로'),
  ('present_record','보류','0/386과 NULL/export 필터를 잃어 정확0%의 기록 재독을 평가할 기준이 없다.','feature record386개와figures.R 계산식'),
  ('missing_corpus_next','유지','코퍼스 전체의 다음판·정정은 원래 미확인. 주장의 범위는1998파일선언이고 새 손실0. 개별package 후속판은 보조.','동일선정 코퍼스의차기판/정정명세'),
 ]),
 'RJ03': ('유지', [
  ('present','보류','논문 이후 공개된4.2.1을 원 공개 소비판 후보로 쓰지 못한다는 시간 제한을 잃는다.','논문2022-06-21 및release2022-04-22/06-23'),
  ('present','보류','어느 R 멤버/변형에서 Df2를 계산했는지 잃는다. 후보값 양립의 대상이 사라진다.','두 tar URL과iris.R 멤버 SHA256'),
  ('missing_original','유지','원 실행ID/사용판 증거는 원래 없다. 후보의 Df2 양립은 유지, 진본 사용판은 계속 보류.','당대 저장Rmonad 객체·input hash·run ID'),
  ('present','보류','논문의 Df2와 비교할 기준이 사라진다. 후보값 대조1→0.','§5 ANOVA Species Df=2'),
  ('present_auxiliary','유지','Df2라는 좁은 목적에는 유지 가능. 단35/38행 정정을 잃으면 Petal.Length 값까지 같다고 확장하는 오류를 거르지 못한다.','UCI Additional Information와두변형35/38행'),
 ]),
 'N-E00': ('유지', [
  ('present','보류','WoRMS2021 이용과2026 live register, author release2의 시점을 구별하지 못한다.','§3 인용연도와IOW release2 날짜'),
  ('present','보류','WoRMS 입력과 IOW 자체 출력을 혼동할 수 있어 자료군 이용 진술의 대상이 사라진다.','WoRMS DOI170와IOW release DOI를별도기록'),
  ('partial','보류','§3의 실제 nomenclature 표준화 진술을 빼면 현재 분류객체 존재만 남는다.','소비자§3 실제사용문장'),
  ('present_record','보류','Table2/당대 F5의Amphipoda를 잃어 Group 기록 재독 성공도 판정할 수 없다.','Table2 첫Group 및release2 F5/G5'),
  ('present_output_only','유지','역사적 Group 재독은 유지. 지역 이동·행 이동을 잃으면 현재지역별 변환계수 재사용에서 정정 필요를 놓친다. 외부WoRMS정정은 원래미확인.','IOW v1/v2 ID7315/13306과키별요약'),
 ]),
 'N-E01': ('보류', [
  ('present','보류','캠페인기간·1시간이내 pair·20m 격자를 잃어 같은 점을 정의하지 못한다.','§4/Fig5 시간·고도 pair조건'),
  ('present','보류','BCO v3.0.0과 자체RAAVEN B1의 역할을 구별할 식별자가 사라진다.','BCO DOI137/level 및RAAVEN별도ID'),
  ('partial','보류','실제 radiosonde 비교를 했다는 진술이 사라지고 후보판 존재만 남는다.','소비자§4 비교방법'),
  ('missing_exact','보류','고유 첫점 키·정확값이 원래 없다. 새 정보 손실0. 그림에 수치축이 있다는 것과 정확값은 다르다.','Fig5 paired-point table'),
  ('missing','보류','같은BCO입력판의 다음판·정정값은 원래미확인. 새 정보 손실0.','실제소비판 및다음발행판의같은행'),
 ]),
 'N-E02': ('보류', [
  ('present','보류','1994–2016 훈련과2020-01-19 출력, 후대2020-01-27 예제를 혼동할 위험을 거르지 못한다.','AppendixA/19Jan Table3/후대book날짜'),
  ('present','보류','RUC 원입력과IGRA대체/자체출력DOI235의 구별이 사라진다.','RUC주소·station00078954·원export식별자'),
  ('partial','보류','훈련자료 이용 진술과 local input recipe가 사라진다. 원 run은 원래없어 R 변화0.','AppendixA와ZenodoV1코드·당대훈련명세'),
  ('present','보류','LWP1 g/m²와nanmean 필터를 잃어 원 표값 재독·다음판 대조의 기준이 사라진다.','Table3 19Jan값/단위·stats코드'),
  ('present_output_only','보류','DOI156→235 정정 공지를 잃으면 최신 출력 재사용에 구판을 권하는 오류를 거를 수 없다. 실제RUC정정값은 원래미확인.','소비자§5 정정사유 및같은19Jan두파일'),
 ]),
 'RUN01': ('정정', [
  ('present','보류','원test와나중preprocess를 하나의 당시실행으로 합치지 못하게 하는 시간 제한이 사라진다.','v1/v1.1 각actionID와timestamp'),
  ('present','보류','CAMELYON16과원기술prostate의 불일치,localH5와publisherXML의 구별을 특정하지 못한다.','CAMELYON원문/파일ID와crate멤버ID'),
  ('present_local','정정','입력질병영역 설명의 정정은 publisher자료로 유지. local실행 연결2층 중 이 사례는 사라져R_local1→0.','같은archive의testID→localH5선언'),
  ('present_record','정정','질병영역 설명 정정은 유지. coord_x63488 재독과sameoutputbytes 비교의 해당필드 기준은 사라진다.','logical non_index_axes와firsttable row'),
  ('present_auxiliary','정정','prostate/lymph-node 목적 정정은 유지. normal_86/test_049 정오표와바뀐preprocess를 빼면 최신파일/계보재사용 검토가 약해진다.','publisherREADME Notes와consumer두판로그'),
 ]),
 'RUN02': ('유지', [
  ('present','보류','2023 원실행,2014 source 객체,2026 감사fetch를 한 시점으로 오인할 수 있다.','같은archive action start/end와publishertimestamp'),
  ('present','보류','같은basename의다른flowcell을 가를수없다. fullpath사용선언U1→0.','fullflowcell/project/sample/R1path와localhash'),
  ('present_local','보류','publisher객체가있어도archive action→Collection→R1이 사라져사용선언과R_local을 잃는다.','Zenodo동일archive의bdfcc6a4 action/object'),
  ('present_record','보류','CHROM1/POS1/DP0를잃어동일출력 재독의범위를 말할수없다.','첫gVCF비header행과output hash'),
  ('present_representation_difference','유지','공식정정은미확인이라는원판정은유지. 압축크기차이/decodedprefix일치 검사를빼면수치정정과재압축을 구분할제약을잃는다.','원/현재gzip전체decodeddigest 또는입수변환영수증'),
 ]),
}


def main():
    cases = json.loads((ROOT / 'cases.json').read_text())
    rows = []
    for case in cases:
        baseline, items = SPEC[case['case_id']]
        for index, (state, after, reason, restoration) in enumerate(items):
            before_axes = {key: case[key] for key in ['publisher_exists','specific_usage','run_link','value_checked']}
            after_axes = dict(before_axes)
            if index == 1:
                after_axes['publisher_exists'] = False
                after_axes['specific_usage'] = False
            elif index == 2:
                after_axes['specific_usage'] = False
            missing = state.startswith('missing')
            rows.append({
                'case_id': case['case_id'], 'removed_item': FIELDS[index], 'original_evidence_state': state,
                'baseline_decision': baseline, 'after_removal_decision': after,
                'decision_changed': baseline != after,
                'scope': '원래 목적에 한정한 가장 강한 기록문장 유지/정정/보류; 진본 사용판 판정은 별도',
                'baseline_allowed_claim': case['strongest_claim'], 'lost_claim_or_limit': reason,
                'new_information_loss': not missing,
                'actual_used_edition_before': '보류', 'actual_used_edition_after': '보류',
                'strict_positive_before': False, 'strict_positive_after': False,
                'axes_before': json.dumps(before_axes, ensure_ascii=False),
                'axes_after': json.dumps(after_axes, ensure_ascii=False),
                'source_url': case['consumer_url'], 'source_location': case['consumer_locator'],
                'additional_evidence': json.dumps(case['C']['visible_urls'], ensure_ascii=False),
                'minimum_restoration': restoration,
                'not_observed': '실제사용자채택/맹검판독/인과적정확도실험은미실시',
            })
    with (ROOT / 'sensitivity.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    summary = {'rows': len(rows), 'unit': 'case × one of five removed evidence items',
               'decision_changes': sum(row['decision_changed'] for row in rows),
               'strict_actual_use_changes': 0,
               'already_missing_no_new_information_loss': sum(not row['new_information_loss'] for row in rows),
               'by_removed_item': {item: {'rows': 8, 'decision_changes': sum(row['decision_changed'] for row in rows if row['removed_item'] == item)} for item in FIELDS},
               'limitation': 'Deterministic evidence-removal reasoning, not observed users or blinded classification trials. Same strong claim may weaken while an already-held decision stays held.'}
    (ROOT / 'sensitivity-summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == '__main__':
    main()
