# HANDOFF — AF-RES-245
- 상태: **PARTIAL** (웹 조사/자료 산술·통제 검산·반례 정정·자체 점검 완료, 독립 예측/실재 음향 경로 및 일부 엄격 자료 판독 미달).
- Result SHA (검증 대상, HANDOFF 제외): `7c0e46d4ec78948ae1109377898c3ee69f2430c4`
- Branch: `work/research-af-res-245`; owned_path: `docs/workstreams/research/AF-RES-245/`
- 시작 통합: `c8a31b50457954c096a3c0b88ddcf316974c4c4d`; 계획판 `7369707441e2eb70e84004ca6cb3bfeefc8b4061` 대비 +10/-0, dot-control.json만 변경. 최신 진행표 contents 비어 blob `d7ecd4aa62b5d7608beb68644fb5987656c5b8bb` 원문 읽음: AF-RES-245 RUNNING, depends_on [AF-RES-232]; 232 중앙 DONE/result SHA `430a1a5ec049f58878d963cb8ca539c9375f93d0` 자체 PARTIAL 확인. 238–242의 입력/출력 사용 안 함.
- 사전 판정 봉인 `2c0fea7164a5130f5edc716023156ef72c36353d` (ASAP SHA/표집/선형식/허용오차/통제; JSON·TSV 전). Source ledger `51c0b7d4e036407e1344537548a24ce6a6c300a6`, cohort `d7c8b7d63bf832616d08b2231a835d49bff83e7b`, beats `78e79bcf94598f782fc1dbb712302b624002ae2e`, paths `e11a22fb0e4952a7ef37cf7cf23ba1c6407efc7c`, 반례 정정 `b7ec3209cb512e65bf70861d24d7ca075ba66ae7`, 원장 보충 `8771f15d61d1048a56d73a71faf09da0dbb1cea3`, RESULT `8821771edf724eebf4cc38aa253046da153fdc32`, SELF_CHECK `7c0e46d4ec78948ae1109377898c3ee69f2430c4`.
 
## 핵심 결과
ASAP pin `afc815c75c42e83a79c03feb6da8a35e77d4c6b8`, 1067 metadata rows/13 cols, JSON equal-count flag true/false(31 false), 2 first eligible different works. BWV846 Shi05M 선형 잔차 50ms 2/7, 100ms 5/7, max +185.303375ms; BWV848 Denisova06M 7/7 및 7/7, max abs46.548750ms; 합산 내부 9/14 및12/14(상관된 관측; 독립 성능 아님). C1 unique DD; C2 two ties; C3 r=1 사전 예상 실패, HDV 0 유지, r=0 DD9; 4×4 correction r=1 min9 vs r=2 min0. bR first challenge Taverna01 579/579 but 4 bR, false first LuoJ03M 648/646; 정확 누락 위치 미확인. 단조/대역은 경로만 제한하고, 음악 특징이 실제 대응점을 정한다. 반복 인쇄 악보 역행은 펼침/전이 그래프 필요. 실제 acoustic DTW 경로 0/2 관측, 0/14 잔차 관측(결측14, 오차 0이 아님). 
자료 28 ledger rows / counted 24 distinct work/case units / 9 lineage IDs / S5 M7 A6 I4 D2. 음악 M05 평가 안내만, M04/M07 이미지 실패(텍스트 성공), 3개 모두 제외하는 엄격 기준 M4로 미달. 같은 데이터의 재포장/같은 곡 제외 기록. 주석 원행과 저자 결과는 자체 실행값과 구분. 
## 대표 파일 (검증 SHA 고정)
- [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/7c0e46d4ec78948ae1109377898c3ee69f2430c4/docs/workstreams/research/AF-RES-245/RESULT.md)
- [SCOPE.md](https://github.com/laadkke-arch/agentflow-open/blob/7c0e46d4ec78948ae1109377898c3ee69f2430c4/docs/workstreams/research/AF-RES-245/SCOPE.md)
- [sources.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/7c0e46d4ec78948ae1109377898c3ee69f2430c4/docs/workstreams/research/AF-RES-245/sources.jsonl)
- [cohort.csv](https://github.com/laadkke-arch/agentflow-open/blob/7c0e46d4ec78948ae1109377898c3ee69f2430c4/docs/workstreams/research/AF-RES-245/cohort.csv)
- [beats.csv](https://github.com/laadkke-arch/agentflow-open/blob/7c0e46d4ec78948ae1109377898c3ee69f2430c4/docs/workstreams/research/AF-RES-245/beats.csv)
- [paths.md](https://github.com/laadkke-arch/agentflow-open/blob/7c0e46d4ec78948ae1109377898c3ee69f2430c4/docs/workstreams/research/AF-RES-245/paths.md)
- [COUNTEREXAMPLES.md](https://github.com/laadkke-arch/agentflow-open/blob/7c0e46d4ec78948ae1109377898c3ee69f2430c4/docs/workstreams/research/AF-RES-245/COUNTEREXAMPLES.md)
- [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/7c0e46d4ec78948ae1109377898c3ee69f2430c4/docs/workstreams/research/AF-RES-245/SELF_CHECK.md)

## 마지막 검토
고정 result SHA에서 8/8 파일 직접 다시 읽음. 원장 parse 28행, counted24/unique work24/lineage9, 필수 식별·근거 필드 공석 없음(내용상 미확인 별도). cohort 4행/22열, beats 18행/15열(내부14, 끝점4), 식/부호 재계산 오류0, 임계 통과9/12. 모든 18개 score/perf raw row를 동일 고정 ASAP SHA의 4 TSV와 다시 비교해 불일치0, RESULT TSV anchor 링크28개 모두 고정 SHA, table1 17행/6열, table2 8행/5열, 마지막 약점표3행/4열. 13 경로표 확인. Q1–Q7 RESULT/SELF_CHECK 양쪽 및 원장 연결 존재. Q별 반례/미확인 재독. integration→result +9/-0, 변경 8파일 전부 owned_path. 동일 작업자의 점검만 시행. 독립 심사자 없음; 엔진/바이너리/사용자 서비스 동작 실행하지 않음. 최종 HANDOFF는 이 result 검토 이후 단독 commit.
 
## 미달 및 다음 첫 행동
1. 후속 독립 작업자는 위 result SHA와 SCOPE 사전 봉인, cohort/beats 원행을 먼저 확인. 자료는 노출됨: 공식/규칙은 먼저 봉인했지만 JSON 오류 접두사 및 TSV endpoint/internal 동시 노출로 독립적인 endpoint-only 수치 예측 봉인은 없음. 원장 M05 실제 WP 및 M04/M07 원문 화면 확인, 다른 독립 음악 논문/저자 평가 추가. ConcertCue Dvorak 두번째 열 정의 및 verify script의 filename 차이 확인.
2. 실행 검증 필요하면 승인된 별도 환경에서 아래 합성 입력부터 실행(라이브러리 설치 명령 없음; 이미 있으면 실행). 정확 입력·기대 비용, 라이브러리 버전/경로 raw 출력/exit code 저장. r=0은 극단 통제; 원전 weighted DTW 검증은 아님. 실제 반복 허용은 M03 별도 모델.
```sh
python - <<'PY'
import numpy as np, librosa, json
A=[[[0,4,4],[4,0,4],[4,4,0]],[[0,0,4],[0,1,0],[4,0,0]],[[0,0,0],[9,9,0],[9,9,0]]]
expected=[[0,0,0],[0,0,1],[0,0,9]]
print("librosa",librosa.__version__)
for k,m in enumerate(A):
    for n,r in enumerate([2,1,0]):
        C=np.array(m,dtype=float)
        i,j=np.indices(C.shape)
        C[abs(i-j)>r]=np.inf
        D,wp=librosa.sequence.dtw(C=C,step_sizes_sigma=np.array([[1,1],[0,1],[1,0]]),weights_add=np.zeros(3),weights_mul=np.ones(3),backtrack=True)
        print(json.dumps({"control":k+1,"radius":r,"minimum":float(D[-1,-1]),"path":wp[::-1].tolist()}))
        assert float(D[-1,-1])==expected[k][n]
PY
```
동률 반환 하나와 가능한 동률 전체는 다르므로 paths.md 13경로에 대해 별도 predecessor enumeration. 원 음향 실험은 권리/원음 crop 확인 후 새로운 독립 구간(현 2곡은 참고용), frame timestamps·feature extractor·metric 및 weights·endpoint/skip/repeat·path→beat 집계 계약을 미리 봉인한 뒤 score/perf MIDI+audio로 local C 생성; RESULT 비용·대안 절의 정확 입력·영수증 규격 참조. 실제 비용을 아직 확보하지 못했으므로 R1/R2 actual DTW 실행 명령 전체는 특징 파이프라인 결정 전 미확인; fabricated output 없음.
3. 색인 제안: `speech time-warp constraints → score/performance beat alignment`; 태그 affine baseline, admissible path, cost ambiguity, bR, score repeats, endpoint uncertainty, online/offline, withheld performance. R1/R2 original data vs synthetic controls vs author evaluation 분리. PARTIAL 상태 및 미달 보존; dot-control.json 수정하지 말 것.
