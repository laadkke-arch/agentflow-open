"""Render the explicit post-hoc A/B comparison against documented reversals."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    data = json.loads((ROOT/'evidence/REVERSAL_JUDGMENTS.json').read_text())
    assert len(data['rows']) == 9
    assert sum(r['adopted_reversal'] for r in data['rows']) == 6
    assert all(r['A'] and r['B'] for r in data['rows'])
    lines = ['# 결정의 대체·부분 번복과 기준선의 원 응답', '',
             '판정자: **작업자**. 독립 후속 문서를 읽은 뒤 시행한 정성 대조이며, 미래 예측 정확도의 사전 등록 실험이 아니다. 채택 후 변화 6개와 기각/초안 교체 3개를 구별한다. 원 gold 176개와 접두부는 수정하지 않았다.', '',
             '| 사례 | 원 결정일 | 변화 종류 | 후속 원문(고정 판) | A 원 응답의 대조 | B 원 응답의 대조 |',
             '|---|---|---|---|---|---|']
    for r in data['rows']:
        fs = r['followup'] if isinstance(r['followup'], list) else [r['followup']]
        f = fs[0]
        date = f.get('date', f.get('decision_date'))
        category = '채택 후 대체·부분 번복' if r['adopted_reversal'] else '기각/초안 교체'
        columns = [r['case_id']+' '+r['canonical_id'],r['original_decision_date'],category,
                   '['+str(date)+']('+f['url']+')']
        for b in ['A','B']:
            j=r[b]
            columns.append(j['assessment']+' — '+j['observation']+' '+j['timing']+
                           f" [원 응답](runs/{b}/{r['case_id']}.json)")
        lines.append('| '+' | '.join(x.replace('|','\\|').replace('\n',' ') for x in columns)+' |')
    lines += ['', '## 적용 범위', '',
              '후속 문서의 날짜·고정판·실제 변경 범위와 비교한 후보 rank는 [구조화 대조](evidence/REVERSAL_JUDGMENTS.json)에 있다. 원 결정의 판과 공식 결정 기록은 [CASES](cases/CASES.json)에 연결되어 있다. 이후 구현 변경·실사용의 불편을 원 입력에서 알 수 있었던 정보처럼 취급하지 않는다.', '',
              '“연관 메커니즘을 찾음”은 새로운 결정이나 정확한 번복 이유를 미리 예측했다는 뜻이 아니다. 예를 들어 같은 타입의 분할 선언이 private 권한을 공유하는 선례와 Swift의 동일 파일 extension 제한은 일치 범위가 다르다. 부품의 존재와 정책 선택을 분리했다.', '',
              '## 한계', '', data['limits'], '',
              '사후 자료와 날짜 미확인 자료는 결정 전 발견으로 세지 않는다. 이 정성 대조에는 별도의 미래 예측 적중률이나 실제 설계자 효용 지표를 붙이지 않았다.', '']
    (ROOT/'REVERSALS.md').write_text('\n'.join(lines))
    print('Rendered 9 explicit reversal comparisons, including 6 adopted reversals.')


if __name__ == '__main__':
    main()
