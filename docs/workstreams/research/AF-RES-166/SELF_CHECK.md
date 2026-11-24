# SELF_CHECK · 단일 작업자 자기검산
④ 고정판 873eafd2146713b6d040c449c0c07bf7ab015fe3의 원격 파일 6개를 실제 다시 읽어 JS로 파싱/검산했다. 독립 평가 아님. 결과:
```json
{
  "source_rows": 61,
  "source_id_unique": true,
  "yes_rows": 42,
  "yes_unique_work": 42,
  "yes_unique_lineage": 42,
  "frame_rows": 264,
  "query_returns": 254,
  "duplicate": 19,
  "cases": 12,
  "mechanisms": 7,
  "predictions": 12,
  "outcomes": 12,
  "pred_join": true,
  "out_join": true,
  "mechanisms_join": true,
  "case_source_join": true
}
```
- Q1 [K407](https://github.com/kubernetes-sigs/kueue/issues/407) 최초 본문, [SGPU](https://lists.schedmd.com/mailman3/hyperkitty/list/slurm-users@lists.schedmd.com/thread/MFYI3SQLYCCD5TIGDBUHWB4FMZ7QCO3O/) L17–19: 12 보충, natural 0/10, strict ID pair 1. 반증: 동일 시점 A/B admission·start 로그가 확인되면 재분류.
- Q2 [D1](https://github.com/kubernetes-sigs/kueue/blob/v0.2.1/apis/kueue/v1alpha2/clusterqueue_types.go#L129-L159) L129–159, [D2](https://github.com/kubernetes-sigs/kueue/blob/v0.8.1/apis/kueue/v1beta1/clusterqueue_types.go#L150-L158) L150–158, [D3](https://github.com/kubernetes-sigs/kueue/blob/v0.3.0/apis/config/v1beta1/configuration_types.go#L49-L70) L49–70, [D4](https://github.com/SchedMD/slurm/blob/slurm-23-02-7-1/doc/html/sched_config.shtml#L53-L80) L53–80, [D5](https://github.com/SchedMD/slurm/blob/slurm-23-02-7-1/doc/html/priority_multifactor.shtml#L239-L252) L239–252, [D8](https://github.com/kubernetes-sigs/kueue/blob/913d53674ec0f535b28e37a3e854b29575eecce0/pkg/scheduler/scheduler.go#L145-L160) L145–160, [D9](https://github.com/kubernetes-sigs/kueue/blob/d9ade1b2c879601d7d626a425278243f9ff73cc6/pkg/scheduler/flavorassigner/flavorassigner.go#L605-L635) L605–635. 6 distinct work IDs, D1/D2 및 D4/D6/D7 중복 제외. 후속 D8/D9 사전 소급 금지. 반증: 같은 당시 설정/버전 재생이 다른 next를 기록.
- Q3 L1/L2 FAQ 위치, [L3](https://www.harvardpubliclibrary.org/about/blog/new-overdrive-and-libby) L49–79, [L6](https://kcls.org/news/burien-library-closed-for-repairs-2/) L228–243, [L8](https://jeffcolibrary.org/wp-content/uploads/sites/46/2017/11/BoardMinutes1610.pdf) p4 L147–156, [L9](https://www.spl.org/Seattle-Public-Library/documents/about-us/levy/reports/2021%20Q4%20and%20Annual%20Library%20Levy%20Report%2022.pdf) p3 L111–122. 7 distinct primary works, 개별 배정 사건 0/2. 반증: 보류 후 원순번 손실/다음 배정 미발생.
- Q4 [A1](https://www.eso.org/sci/observing/phase2/SMPhilosophy/SMScheduling.html) L73–84, [A2](https://support.eso.org/en-GB/kb/articles/program-execution-status) carryover FAQ, [A3](https://www.eso.org/sci/observing/phase2/SMPhilosophy/ProgrammePriority.html) L78–80, [A4](https://www.eso.org/sci/observing/phase2/SMPolicies/TimeCriticalOBfailure.html) L74–80, [A5](https://noirlab.edu/public/media/archives/geminifocus/pdf/geminifocus037.pdf) L3721–3728,3836–3864,3940–3963, [A6](https://www.eso.org/sci/publications/messenger/archive/no.158-dec14/messenger-no158.pdf) pp11–13, [A7](https://www.eso.org/sci/facilities/paranal/instruments/eris/news.html) L262–271. 7 works, 개별 배정 0/2. 반증: 높은 rank가 항상 실제 feasible이며 다음 순서와 일치하거나 rare-window 조건 미보존.
- Q5 ③ cf2ca5b67c190a2ee190247ed3c5c80c8e530316, predictions 12×4, prospective 0/40 target rule cells. 모든 보충 노출/제안/결측. 반증: 미노출 쌍에서 네 규칙 완전 입력/서로 다른 next.
- Q6 [O599](https://github.com/kubernetes-sigs/kueue/issues/599#issuecomment-1448300703) 1448486840 edited, [O1871](https://github.com/kubernetes-sigs/kueue/issues/1871#issuecomment-2189948546) 2189948546/2308556343, [O3405](https://github.com/kubernetes-sigs/kueue/issues/3405#issuecomment-2464418140) 2464418140, [O245](https://lists.schedmd.com/pipermail/slurm-users/2022-January/008275.html) L13–23/82–104, [O138](https://lists.schedmd.com/pipermail/slurm-users/2023-June/010139.html) L13–25, [OGPU](https://lists.schedmd.com/mailman3/hyperkitty/list/slurm-users@lists.schedmd.com/thread/MFYI3SQLYCCD5TIGDBUHWB4FMZ7QCO3O/) L58. 12 outcome rows, all no prospective. 실제 시작순서를 보여주는 타임스탬프 부재. 반증: same-event job IDs + timestamps or explicit accepted allocation decision.
- Q7 경쟁 설명을 실제 고정 소스 D4/D8/D9 및 O599/O138에서 확인. R3≈native backfill, R2≈explicit defer는 owner consent 없음/eviction에는 깨짐. 소프트웨어 정책 대비 외부 링크 추가 예측 0 유효 분모, 효과 추정 불가. 반증: 같은 입력 R1≠R3(or R2), 후속 동일 상태 실제 기록이 한쪽만 지지.
- 원장 누락: 일부 검색 시도/검색 응답 재열람은 frame에 묶음 기록, 모든 웹 호출마다 별도 JSONL 행으로 완전 복원하지 못함. 최초판/정렬 tie 검증 부족; ④ 날짜 정정 S245. L8/A5/A6 PDF screenshot 실패를 숨기지 않음. strict 요청 7 부족, 외부 개별 사건 각 2 부족. 자연층의 빈칸에 보충을 넣지 않음. 별도 실행/CI 미실시.
- 재개: GitHub REST 쿼리 page=2..ceil(total/100), 생성일/ID merge, 본문 edit history; Slurm 월 원장 전체/mbox에서 최초 글만 추출(2022–25; 결과 댓글 제외). 실제 원순위 확인 후 새 독립 세션에서 결과를 보지 않고 새 prediction commit. 기존 보충층 유지.
- Codex(미실행): Kueue v0.2.1 checkout(또는 당사자 확인 버전), 두 노드 1/2 CPU, A .5 B 1 running, C1.5 D.5 submit in order, single CQ aggregate3 vs per-node flavor; `kubectl get workloads,jobs,pods -o yaml`를 단계마다 저장, admission timestamp와 pod scheduled/start 분리. StrictFIFO/BestEffortFIFO 각각; 기대 aggregate C admits/pending vs per-node C cannot fit and later D admits under BEFIFO (conditional). Slurm exact affected version first obtain from `scontrol version`, `scontrol show config` and `scontrol show partition`; reference slurm-23-02-7-1 in isolated test, 3 homogeneous nodes, running A occupies 2 with 1h left, pending B 2 nodes 2h higher, C 1 node 2h lower, D 1 node 30min lowest. `squeue --start`, `scontrol show job <ids>`, `sacct -j <ids> --format=JobID,Submit,Eligible,Start,End,State`; compare sched/builtin vs sched/backfill, priority weights fixed and bf_max_job_test sufficient. Expected backfill D before B without pushing B; C cannot fit protected gap. Perturb equal 48h, no reserved expected start, scan limit 1, shared resource. Record actual code/inputs and run output; not an observed result here.
