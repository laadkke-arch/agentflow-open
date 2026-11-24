# SELF_CHECK — AF-RES-221
상태 PARTIAL. 자체 검토 실시; 독립 검토 미실시. 실행/설치/자동 검사 없음.
| Q | 직접 근거 | 반증·검토 | 상태 |
|---|---|---|---|
| Q1 | M01 M02 M03 I02 I04 | array y vs Cartesian, strict equality code로 보강; real M input 미확인 freeze | control static confirmed |
| Q2 | P01 pp84–85 figs5–8, P02 §3.1 Eq1–2, P03 p3/p7 | 스캔 plus vs 유도 minus; alternate original/errata 미확인; 3D 전체 보장 배제 | formula supported, publication ambiguity |
| Q3 | P_FREEZE, M_FREEZE, P01–03 | C1/2 magnitude, C3 mismatch, C4 crossing, C5 no ambiguity; sign/flip | prospective control derivation; runtime unknown |
| Q4 | I01 I02 E01 | orientation reversal not pair, masks/NaN and open endpoints, actual case bits | static, public expectation |
| Q5 | I03 I04 I05 M02–05 E05 | log positive-only, quad_as_tri not AD; equality low | static, nondefault test |
| Q6 | E01–E07, E08 helper | R1 ref coexposure, R2 compare generated; E03 separate fixed points; generated config selection alternative | PARTIAL |
| Q7 | D01–04 M01 M02 | category adjacency vs continuous interpolation; GDAL NODATA, GRASS exact value | supported qualitative, no utility measurement |

Planned source min 22, counted 24 (P3/3, M5/5, I5/5, E7/5, D4/4); 33 ledger records incl 9 excluded (I06 E08 E09 X01–06). P01–03 separate works but shared AD lineage; M/I/E same two producer families, E07/E08 linked; D02/D04 same institution different operation. 7 ledger lineage IDs; 6 if contourpy-config merged. Independent new cases evaluated against blind truth=0, independent run=0, independent human review=0. No search snippet counted; P02 screenshot HTTP400 large file but relevant text direct; P01 p85 and P03 p7 screenshots rechecked. Source per-open UTC not captured, session UTC approx 2026-11-24 22:10 start; stable domain docs no exact version; fixed code via tags/blob hashes. 
Planned 7 inputs: 5 controls and 2 real, 7 available as numerical inputs (real retrospective). 28 slots: 15 prospectively frozen M/P/I controls, 6 retrospective real M/P/I, E=1 explicit selected quad public pair (R1), 1 relative assertion without absolute expected (R2), 5 absent. Both real co-exposed -> independent accuracy denominator zero. No observed failure count for execution. R1 test direction nondefault but same pair. R2 first literal numerical grid in selected directory order under eligibility; earlier generated config alternative and whole-tree completeness unknown, exact expected absent. E03 dechunk fixed vertices not substitute. 
Read original Nielson p85 scan again; visible plus; later Lewiner p7 minus. Check P freeze includes C4 crossed level and paper separate tie policy; source inference C4 center strict > leads A. C3 D16 Q−4, C2 D8 Q8. No geometry beyond selected edge pairing claimed. Input full R2 fixture committed. 
Controls M freeze cf4c203ea5745d4f16f92fe5263eb6b3c91f0490, P freeze 52a60e2e9cfbf7e1f1acfd4290a700b083b51404, I freeze f466ff4854cfbe98c529c4cfc5186aa79f389aac. Input/expected exposures after I. No claim of blind real evaluation. Reopen exact result SHA and compare changed paths prior to HANDOFF.
