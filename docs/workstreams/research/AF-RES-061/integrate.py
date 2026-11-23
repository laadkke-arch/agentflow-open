"""Rebuild the research's derived CSV/JSON indexes, without modifying forecasts.

Run from repository root. All outputs stay within this workstream. This is a
document integration utility, not an upstream library test.
"""
from pathlib import Path
import csv
import io
import json
import subprocess

P = Path(__file__).resolve().parent
SEAL = "02359364000057f69b00594d8b43571ac72df298"
OWN = "docs/workstreams/research/AF-RES-061/"


def read_csv(path):
    return list(csv.DictReader(path.open(newline="", encoding="utf-8")))


def write_csv(path, rows, columns=None):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, columns or list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def compact(x):
    return json.dumps(x, ensure_ascii=False, separators=(",", ":"))


def frame():
    rows = read_csv(P / "frame.csv")
    extra = {
        "D3": {
            "release_url": "https://github.com/d3/d3-force/releases/tag/v3.0.0",
            "tag_object": "44492c7db3859da5120768af50f6d4bfee4e6939",
            "next_excluded_release": "3.0.1 / 2026-11-03T05:55:31Z",
            "support_environment": "ESM; Node>=12; browser UMD export; component package manifest G004",
            "source_distribution_match": "4 relevant installed source files byte-equal pinned commit; streams/graph/source-receipts.json and d3-run.json",
            "first_donor_path": "tagged README -> Wikipedia Barnes-Hut -> Barnes&Hut1986 DOI10.1038/324446a0 (body unavailable); B fallback Demmel1996",
            "normal_question": "fixed two-node positions: direct force(1) velocity increment, not simulation.tick position",
            "boundary_question": "same input distanceMax4: excluded interaction; coincidence/theta supplementary",
            "first_eligible_issue": "#166 JFLopez7; bounded 24-record roster; mutable D3v5 bundle, exact component version unconfirmed",
            "selection_status": "component release and source bytes verified; exact-version user report unconfirmed",
        },
        "GV": {
            "release_url": "https://gitlab.com/graphviz/graphviz/-/releases/14.1.1",
            "tag_object": "release/tag target a74b50c20fc624f46f72e24f981b261f6e5edf71",
            "next_excluded_release": "14.1.2 / 2026-01-24T06:11:09.781Z",
            "support_environment": "bundled engine with_sfdp ON; CMake>=3.21 C17 C++17; release assets Linux/Windows/macOS arm64; not all platforms executed",
            "source_distribution_match": "official release tag + included sfdp sources verified; native binary build/run not performed",
            "first_donor_path": "official sfdp page -> Hu2005 author manuscript sections3-4 -> bibliography[2] Barnes&Hut1986",
            "normal_question": "can fixed positions(0,0),(3,4), K1 and one internal movement be specified by public sfdp?",
            "boundary_question": "same graph with coincident fixed positions; random initialization and minimum-distance domain",
            "first_eligible_issue": "#2852 / original forum3392; bounded7-record roster; 15.1.1 report, not14.1.1; window right censored",
            "selection_status": "component release/source verified; public one-step input contract unresolved",
        },
        "AN": {
            "release_url": "https://developer.android.com/jetpack/androidx/releases/dynamicanimation#1.1.0",
            "tag_object": "release-log endpoint rather than invented git release tag",
            "next_excluded_release": "no later stable component release in inspected official list",
            "support_environment": "published AAR minSdk21 / minCompileSdk34 / minAGP8.1.1; JVM21 with declared Android stubs used, no device",
            "source_distribution_match": "sources.jar SHA256 d730234d4276722a13721feea2630a5aaa189d5dc11681aacc7cfe94527d7b94; four Java files byte-equal release endpoint",
            "first_donor_path": "official API -> SpringForce source; no named physics work found in reviewed four files; MIT2011 B is researcher-selected equation comparison",
            "normal_question": "0px->100px, v0, stiffness100,zeta.5: crossing and samples16/250ms",
            "boundary_question": "99.9f->100px,v10px/s,stiffness100,zeta1,minVisibleChange1: continuous state versus UI stop",
            "first_eligible_issue": "미확인: incomplete official tracker release-window roster; supplementary182190872 outside window",
            "selection_status": "component release and four source files byte-verified; first eligible issue and real-device output unconfirmed",
        },
        "RS": {
            "release_url": "https://github.com/pmndrs/react-spring/releases/tag/v10.0.3",
            "tag_object": "abc0cd15a943440942aa7655dd6a4ca7bc543ac2",
            "next_excluded_release": "10.0.4 / 2026-05-21T20:32:05Z",
            "support_environment": "core ESM+CJS; React^16.8||^17||^18||^19; no core Node minimum declared; actual Node24.22.3/React19.1.2",
            "source_distribution_match": "registry gitHead equals selected commit; tarball integrity verified; installed transpiled JS member byte-equal tarball; TS/JS byte equality not claimed",
            "first_donor_path": "v10 docs Andy Matuschak by name; v8.0.27 README -> animated/react-motion explicit software inspiration; no named physics source; MIT2011 B researcher-selected",
            "normal_question": "0->1,mass1,tension100,friction10,v0,clampfalse: crossing and direct advance16/250ms",
            "boundary_question": "same configuration clamptrue: step ordering, emitted overshoot, idle and residual velocity",
            "first_eligible_issue": "#2377 terrymun;9-title roster;10.0.1 report and10.0.2 workaround;#2381 same lineage",
            "selection_status": "component release and published package provenance verified; exact-version user report unconfirmed",
        },
    }
    for r in rows:
        r.update(extra[r["implementation_id"]])
        r["release_cutoff_utc"] = "2025-12-31T23:59:59Z"
        r["recruitment_rule"] = "SCOPE.md: official component release, non-prerelease; user issue created within release+-365days, sorted, first eligible; preserve missing slots"
        r["exclusion_rule"] = "other module/repo latest, post-cutoff release, duplicate/bot/install-only/PR, missing original body; historical extras do not replace main cases"
        r["postseal_update"] = "Version/input selection unchanged; source-match and issue recruitment results filled after prediction seal"
    write_csv(P / "frame.csv", rows)


def transfers():
    original = subprocess.check_output(["git", "show", f"{SEAL}:{OWN}transfer.csv"], text=True)
    rows = list(csv.DictReader(io.StringIO(original)))
    base = {r["implementation"]: r for r in rows}
    details = {
        "D3": dict(
            citation_class="mediated_algorithm_attribution",
            receiver_url="https://github.com/d3/d3-force/blob/156712c8c3285d77cb487e1685c5adafcd0394a4/src/manyBody.js#L29-L91",
            donor_variables="cell size D / distance r / source weights; gravity vector proportional to delta/r^3 in full Demmel notes",
            receiver_symbols="signed strengths; quad.value; center weighted by abs aggregate; theta; alpha; squared distance l",
            receiver_file_function="manyBody.js accumulate29-53; apply55-91; simulation.js tick39-59",
            changed_assumptions="delta_v=alpha*s_j*delta/r^2 gives magnitude1/r, not gravity1/r^2; signed-zero cells pruned even theta0; strict distanceMax; distanceMin caps; jitter; direct force has no physicalseconds",
            judgment="Named tree algorithm and equation-level receiver mapping confirmed; primary-paper reading/adoption history unconfirmed; own D3-N/B outputs auxiliary",
            discriminating_evidence_needed="explicit maintainer primary-paper design record; sameversion/input independent retained output; actual UI goal for first-link choice",
        ),
        "GV": dict(
            citation_class="direct_Hu_mediated_BarnesHut",
            receiver_url="https://gitlab.com/graphviz/graphviz/-/blob/a74b50c20fc624f46f72e24f981b261f6e5edf71/lib/sfdpgen/spring_electrical.c#L545-664",
            donor_variables="Hu K,C,r; attraction r^2/K, repulsion -C*K^2/r; normalized sequential movement; cell width/distance<=theta",
            receiver_symbols="K,p,C=.2; KP=K^(1-p); CRK=C^((2-p)/3)/K; step; random_start; quadtree half-width and geometric center",
            receiver_file_function="sfdpinit.c tuneControl200-224; spring_electrical.c567-660; QuadTree.c73-82; update_step171-184",
            changed_assumptions="initial positions randomized; public maxiter mapping absent; executable coefficients differ from header simplification; force normalized before sequential move; adaptive steps lack Hu five-success counter; stop step<=.001 ormaxiter500; packing/overlap later",
            judgment="Explicit Hu link and multilevel/tree family confirmed, same field intermediary. Public fixed-coordinate one-step output unconfirmed; private arithmetic is posthoc unexecuted auxiliary",
            discriminating_evidence_needed="upstream instrumented one-step trace with real initialization/public contract; archived exact-version output; missing eligible A worked example",
        ),
        "AN": dict(
            citation_class="same_equation_only_researcher_selected_primary_text",
            receiver_url="https://android.googlesource.com/platform/frameworks/support/+/d5923c378c00b537f3421786eb3a50e6f6868386/dynamicanimation/dynamicanimation/src/main/java/androidx/dynamicanimation/animation/SpringForce.java#272",
            donor_variables="m*y''+b*y'+k*y=0; y=x-target; initial y and y'; continuous seconds",
            receiver_symbols="normalized mass1; omega=sqrt(stiffness); b=2*omega*dampingRatio; deltaT=timeElapsed/1000; velocity property/s",
            receiver_file_function="SpringForce setStiffness135-140,getAcceleration215-222,updateValues272-313,isAtEquilibrium229-234; SpringAnimation259-302",
            changed_assumptions="analytical three-regime solver then float; physical kg not guaranteed; property threshold.75*minVisibleChange and velocity62.5*threshold; both strict<; snap target/zero; cancellation; half-frame retarget; SDK>=33 durationScale",
            judgment="Four deployed source files byte-matched; conditional ODE mapping confirmed; no explicit primary citation in bounded source. Main numeric evidence is JVM platform-stub auxiliary, not original/device",
            discriminating_evidence_needed="maintainer attribution record; exact input independent original output; real-device schedule/settings trace; complete release-window issue roster",
        ),
        "RS": dict(
            citation_class="explicit_software_inspiration_plus_same_equation_only_physics",
            receiver_url="https://github.com/pmndrs/react-spring/blob/b6fbb98101f2cf00a6668cffed6d1b4d0012ae3a/packages/core/src/SpringValue.ts#L220-L325",
            explicit_reference="v8.0.27 README names/links animated and react-motion; v10 WhySprings names Andy Matuschak; no observed specific physics-paper citation",
            intermediate_or_donor_url="https://github.com/pmndrs/react-spring/blob/caec34387ffc28c289265f55280a5163a8fe2b8c/readme.md; https://github.com/chenglou/react-motion/blob/8bd4f7223a8d79535586220f7173f078d4604e07/src/stepper.js",
            donor_variables="m*y''+b*y'+k*y=0; continuous seconds; displacement relative goal",
            receiver_symbols="mass,tension,friction; velocity pt/ms; spring factor1e-6 and damping1e-3; steps=ceil(dt/1ms)",
            receiver_file_function="SpringValue.advance220-325; _resume skipAnimation; rafz firstdt16.667/subsequentcap64; useReducedMotion hook",
            changed_assumptions="semi-implicit Euler1ms; clamp checked before step allows transient emitted overshoot; frame quantization; precision uses distance not docs.01; restVelocity=precision/10; residual velocity when idle; cancel retargets goal; preference requires hook/start lifecycle",
            judgment="Published package provenance verified; own fixed-package runs support code mapping. Software inspirations explicitly named; mechanical source adoption unconfirmed. Conditional MIT model not an unconditional library forecast",
            discriminating_evidence_needed="sameversion/input independent original trace with schedule; named physics adoption record; actual mounted UI preference/cancel trace; genuine donor-link action study",
        ),
    }
    for slot in ["D3", "GV", "AN", "RS"]:
        r = dict(base[slot])
        r.update(details[slot])
        r["transfer_id"] = f"T-{slot}-POST"
        r["stage"] = f"post-outcome-source-verification; pre-outcome rows preserved at {SEAL}"
        rows.append(r)
    write_csv(P / "transfer.csv", rows)


def observations():
    cols = ["case_id", "implementation", "version", "source_sha", "input", "operation_schedule", "unit", "rule_source_ids", "rule_source_urls", "expectation_sources", "observation_class", "observed", "observation_status", "raw_file", "raw_key", "independent_original_same_version_input", "original_output_search_scope", "verdict", "limits"]
    out = []
    for r in read_csv(P / "streams/graph/observations.csv")[:4]:
        out.append(dict(zip(cols, [r["case_id"],r["slot"],r["version"],r["source_commit"],r["input"],r["settings"],r["observation_unit"],r["rule_source"],r["source_url"],f"predictions.csv case_id={r['case_id']}, API/A/B; seal {SEAL}",r["evidence_type"],r["observation"],r["actual_run_status"],"streams/graph/"+r["evidence_file"],r["evidence_key"],"미확인; located 관측 0", "streams/graph/test-inventory.json; selected tag five D3 suites or listed Graphviz regression/fixtures, not entire ecosystem",r["verdict"],r["limits"]])))
    for r in read_csv(P / "streams/android/observations.csv"):
        rules=json.loads(r["rule_sources"])
        out.append(dict(zip(cols,[r["case_id"],"AN",r["component"],r["source_sha"],r["input"],"fresh direct force16/250ms and manual timestamp cadence; first pulse establishes baseline; separate continuous/internal/public output", "px; velocity px/s; long milliseconds -> seconds", ";".join(x["source_id"] for x in rules),compact([x["url"] for x in rules]),f"predictions.csv case_id={r['case_id']}, API/A/B; conditional B model not retroactively unconditional",r["evidence_class"],r["observed"],"performed compiler_exit0/run_exit0; device 미실시","streams/android/"+r["raw_output"],r["case_id"]+" force/manual frame records","미확인; located 관측 0","same-SHA SpringTests.java and related design/cancellation history; declarations are not retained passing output",r["judgment"],r["unconfirmed"]])))
    for r in json.loads((P / "streams/react/observations.json").read_text()):
        obs={k:r[k] for k in ["direct_16ms","direct_250ms","one_ms_schedule","sixty_hz_schedule"]}
        inp=dict(r["input"]); inp.pop("calls",None)
        out.append(dict(zip(cols,[r["case_id"],"RS",r["component"],r["source_commit"],compact(inp),"fresh directadvance16 and250; separate1ms and60Hz manualadvance schedules; rawadvance is not RAF elapsedtime", "unitless numeric property; velocity pt/ms; dt ms", ";".join(r["source_ids"]),r["source_url"],f"predictions.csv case_id={r['case_id']}, API/A/B; separate conditional continuous model",r["observation_class"],compact(obs),"performed Node exit0; mounted React/OS preference 미실시","streams/react/raw-outputs.json",compact(r["run_ids"]),"미확인; located 관측 0",r["original_output_search_scope"],"Own observed direction and boundary support implementation explanation; no distinct operational A/B forecast, donor-hit accuracy 해당 없음", "RS-B1ms emits overshoot242ms, target243ms, idle244ms;60Hz emits no overshoot; do not average different schedules or infer pixels/physicalmass"])))
    assert len(out)==8 and len({r["case_id"] for r in out})==8
    write_csv(P / "observations.csv", out, cols)


if __name__ == "__main__":
    frame()
    transfers()
    observations()
    print("Integrated 4 version rows, 4 preserved + 4 post-seal transfer rows, 8 main observation rows; forecasts untouched.")
