# AF-RES-257 — 사전 범위 봉인

착수 통합 3c32c1b44bd139819485548cb50e69e254288fad, 진행표 blob 3b6997ad21b0ae605433c65d930a2fff3b68b6c3. 본인 RUNNING, depends_on=[AF-RES-244], branch work/research-af-res-257, owned_path docs/workstreams/research/AF-RES-257/. 중앙 244 DONE/result_commit 363def3f2385c3bb51518bda891ca04302d5bfa5; 자체 PARTIAL, 결과 659cc8a613e2ee49e1b2f6e3833ac8346f9bb794. HANDOFF, RESULT, gallery-all, gallery, uses를 363def3에서 읽었다. [입력판](https://github.com/laadkke-arch/agentflow-open/tree/363def3f2385c3bb51518bda891ca04302d5bfa5/docs/workstreams/research/AF-RES-244). 요청 기준 933a0f7d534314470c083b0aa284044a9ad45443의 brief 및 현행 AGENTS/STATE/DOT_AUTOMATION/RESEARCH_WORKFLOW 읽음. 진행표 contents API 빈 본문 → blob API로 원문 JSON 파싱 성공. 242,251,254,255 제외. NLM/SQL/SG version 및 신규 검색 순위 제외.

## 모집 봉인 — tail 본문 열람 전
게시 1.6.1 commit 34aafaf61b4a20a7520817c02a5924baf026e3fe, tag f159b78dc59f250cdde8fe391a21f0bc871960ad. 244 gallery-all.csv selected=no 정확 8개:
| symbol | rank | relative example path (auto_examples/) |
|---|---:|---|
| C | 3 | ensemble/plot_voting_decision_regions.html |
| C | 4 | neighbors/plot_caching_nearest_neighbors.html |
| C | 5 | neighbors/plot_nca_classification.html |
| C | 6 | neighbors/plot_nca_dim_reduction.html |
| C | 7 | neighbors/plot_classification.html |
| C | 8 | preprocessing/plot_scaling_importance.html |
| C | 9 | text/plot_document_classification_20newsgroups.html |
| G | 3 | cluster/plot_ward_structured_vs_unstructured.html |

N rank1 only, rank2+ structural vacancy; C 9, G 3. 13 unique total, 5 selected, 8 tail. HTML href recheck pending; no selection based on outcome. Baseline N1, C1/C2, G1/G2 conditional, strict direct 0/5; N2 vacant; API N/C direct, G connectivity only (partial). Exposure: prior results and filenames/brief hypotheses read before seal; no tail scripts or HTML opened yet. No blind evaluation claim.

## Qualification before outcomes
C: fitted KNeighborsClassifier (or transparent pipeline ending in it) predicts genuinely new/held-out feature vectors; label array consumed/visible as individual labels (including individually attributable prediction report), not just aggregate score, probabilities, training y, or ensemble output. Synthetic grid whose rendered regions alone are exposed is conditional per C2 baseline; explicitly identify countercriterion where actual KNN label grid is consumed/rendered, do not retroactively change strict metric. G: actual kneighbors_graph construction and use of both connectivity and distance modes, with graph axis and include_self, not weighted symmetrization or different API. Report each mode separately; same-mode examples cannot complete full goal. N: distance and row-index returned together and exposed. Hidden internal use/mention is conditional. Missing access unknown, never structural vacancy. Distinguish source-supported algorithm, published result, newly executed measurement (none planned). If a source visibly uses y_pred for per-document error analysis or confusion alone, check individual linkage; do not silently equate aggregate confusion with individual output.

Predictions competing: H0 tail all conditional; H1 at least one C shows individual held-out labels beyond depth2, plausible text classification or explicit grid (test exact consumer); H2 G third fills distance mode versus all connectivity. Neither a title nor call count settles. For each depth 2/3/end report observed links / planned slots, structural vacancies, unknowns, strict direct counts per link and per symbol; end is per-symbol natural stop (N1/C9/G3). Costs: from API already open, distinct destination URLs (anchors same document cost 0 new URL; click/scroll distinct action) vs source files needed to verify exact calls (tag copy not independent author work; separate file if explicitly opened). API pre-existing solution not novel. Same next-open budget per symbol: rank3 vs exact in-page example, N no next link. No runtime/causal estimates.

Source quota 8 example authors + 3 API/guide + 6 implementation/test/change + 4 other-field distinct works. Same HTML/download/tag counted once; failed access excluded. Recipe pair use fixed CPython version and code/test; one docs file multiple recipes counts once. No new execution or installs; if needed exact Codex inputs and reversal criteria in handoff.
