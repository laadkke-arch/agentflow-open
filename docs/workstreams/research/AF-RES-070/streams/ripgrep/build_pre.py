"""Assemble the ripgrep preread packet from fetched original public sources."""
import datetime
import hashlib
import json
import pathlib

BASE = pathlib.Path(__file__).resolve().parents[2]
PRIVATE = BASE / "private/ripgrep"
OUT = BASE / "streams/ripgrep"
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()
SHA11 = "7cb211378a2ac6d421c5f6f3f71411937af23136"
SHA10 = "2658bd4e460432034270811e78033506d3333753"
queue = json.loads((PRIVATE / "queue-order.json").read_text())

def read(n):
    current = json.loads((PRIVATE / f"issue-{n}.json").read_text())
    recovered = PRIVATE / f"opened-{n}.json"
    return current, json.loads(recovered.read_text())["payload"]["issue"] if recovered.exists() else current["data"]

def hash_text(text):
    return hashlib.sha256((text or "").encode()).hexdigest()

def write_json(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")

enrollment = []
sources = []
access = []
summaries = {
1808:"포함 glob이 ignore 파일을 존중하고 제외 glob의 우선순위는 보존하기를 요청한다.",
1778:"검색 시작 경로를 바꾸어도 특정 website 디렉터리를 한 ignore 규칙으로 제외하려 한다.",
1814:"알파벳순 기본 도움말은 유지하고 처리 단계별 옵션 목록을 선택적으로 보고 싶다.",
1792:"환경 변수를 config에 쓰면서 --no-config로 해제할 수 있어야 한다.",
1818:"zsh의 --h 완성 결과에 --hidden이 나타나길 기대한다. 자체 수정과 원인 추정도 최초 글에 있다.",
1812:"Linux/macOS 사용자명·홈 경로가 달라도 같은 rg config를 쓰려 한다.",
1840:"숨김 현재 디렉터리의 하위 파일에서도 검색 결과를 원한다. 명시 경로와 기본 경로의 차이를 보고한다.",
1819:"화이트리스트형 .gitignore 프로젝트에서 매번 --no-ignore 없이 파일을 검색하려 한다.",
1847:"Windows의 hidden 속성과 점으로 시작하는 이름을 도움말에서 정확히 설명해 달라는 요청이다.",
1823:"대규모 파일 순회 시 메모리를 400MB 수준에서 50MB 미만으로 줄이려 한다.",
1931:"여러 줄 주석 형태의 정규식과 기대 출력이 있다.",
1837:"여러 로그 파일 각각의 recovery 출현 횟수를 세고 싶다. 쉘 glob 확장이 최초 글에 보인다.",
1965:"파이프로 연결한 apt list 출력을 rg로 처리하려는 목적이다.",
1851:"설치 빌드 E0463 오류 재현과 설치 성공 요구뿐이며 부분 설계 선택이 없다.",
1982:"특정 Unicode/PCRE2 오류 재현과 오류 부재 기대 중심이다.",
1861:"압축 해제 불가 파일의 stderr를 억제하고 다른 오류가 없으면 0 종료코드를 원한다."
}
for row in queue["rows"][:16]:
    n = row["number"]
    current, initial = read(n)
    recfile = PRIVATE / f"recovery-{n}.json"
    rec = json.loads(recfile.read_text()) if recfile.exists() else None
    selected = row["order"] <= 3
    eligible = n not in (1851,1982)
    changed = bool(rec and not rec["current_body_equal"])
    entry = {"enrollment_id":f"RG-E{row['order']:02}","issue_id":f"RG-{n}","repository":"BurntSushi/ripgrep",**row,
      "url":initial["html_url"],"author":initial["user"]["login"],"body_sha256":hash_text(initial["body"]),"body_line_count":len((initial["body"] or "").splitlines()),
      "current_body_sha256":hash_text(current["data"]["body"]),"body_changed":changed if rec else "unknown",
      "original_body_status":"recovered_opened_event" if rec and rec.get("found") else "unknown_current_body_only",
      "original_recovery":rec,"initial_goal_eligible":eligible,"selected_slot":f"RG-S{row['order']:02}" if selected else "",
      "analysis_layer":("reconstructed_exposed" if changed else "prospective_packet") if selected else ("initial_nonselected" if row["order"]<=8 else "extension_access_only"),
      "preread":not changed if selected else False,"comments_read_before_seal":False,
      "selection_reason":"원본문에서 목적·부분동작 식별 가능한 최초3" if selected else ("최초8의 후순위; 처음3 선정 후 대체하지 않음" if row["order"]<=8 else "최초판 미확인 시점에 규칙대로9–16 열람; 이후첫3복구되어 main대체하지 않음"),
      "exclusion_reason":"" if eligible else "pure_build_or_error_reproduction_without_partial_design_choice",
      "verified_initial_claim":summaries[n],"first_read_utc":current["accessed_utc"],
      "preexposure_detail":({1808:"현재 본문에 일반화·패턴·설명 추가가 있어 원본문복구 후에도 완전 가림을 주장하지 않음",1778:"원본문의 src/lib+src/.ignore works가 현재본문에서 fails로 뒤집힘",1792:"현재본문에 --no-ignore-files의 모든 ignore 해제 부작용이 추가됨"}.get(n,""))}
    enrollment.append(entry)
    sources.append({"source_id":f"RG-I{n}","lineage_id":f"github:BurntSushi/ripgrep:issue:{n}","kind":"original_issue","repository_direction":"file_search","author":initial["user"]["login"],"original_url":initial["html_url"],"pinned_url":rec["url"] if rec and rec.get("found") else initial["html_url"]+f"#issue-{initial['id']}","version_date":initial["created_at"],"section_lines":f"opened body lines1–{entry['body_line_count']}" if rec else "current original post; description/reproduction/expected sections; extensive repetitive logs not separately counted","accessed_utc":rec["ended_utc"] if rec else current["accessed_utc"],"selection_reason":entry["selection_reason"],"direct_read":True,"verified_claim":summaries[n],"cannot_determine":"최초글의 도구 동작 보고는 독립 실행 검증이 아니다; 후속 댓글은 A봉인 전 가림","contrary_or_unknown":entry["preexposure_detail"] or ("원본문 이력 미확인" if not rec else "원문 복구와 권고 적합성은 별도"),"count_toward_minimum":True,"body_sha256":entry["body_sha256"],"archive_event_id":rec.get("event_id") if rec else None,"archive_line":rec.get("line") if rec else None})
    access.append({"access_id":f"RG-GET-{n}","url":current["url"],"accessed_utc":current["accessed_utc"],"status":"success","content_read":"initial body only","comments_exposed":False})
    if rec: access.append({"access_id":f"RG-ARCHIVE-{n}",**rec,"lineage_id":f"github:BurntSushi/ripgrep:issue:{n}","count_toward_minimum":False})

docspecs=[
 ("RG-D1","doc-GUIDE.md.json","GUIDE.md",SHA11,"12.1.1","2020-05-29",["Manual filtering: globs L249–315","Manual filtering: file types L316–414","Configuration file L532–615"],"타입에 명명한 glob을 쓰며 config는 각 줄을 그대로 인수로 전달한다.","각 절은 별도 저작이 아니며 GUIDE 한 저작으로만 산입. 당시 사용자의 설치판은 버전 미기재 행에서 미확인."),
 ("RG-D2","doc-crates--core--app.rs.json","crates/core/app.rs",SHA11,"12.1.1","2020-05-29",["TEMPLATE/app L32–70","flag_glob L1344–1367","flag_hidden L1425–1444","flag_no_config L1922–1935","flag_type L2837–2857"],"현재판 도움말은 unified 템플릿; --glob는 다른 ignore 논리보다 우선; --hidden과 --no-config는 서로 별도 기능이다.","이 코드가 사용자의 실제 실행과 일치하는지 미확인. 선택 A packet별로 지정 절만 재사용; 다른 사례 관련 절을 읽었다는 노출 이력도 보존."),
 ("RG-D3","doc-12.1.1-crates--ignore--src--walk.rs.json","crates/ignore/src/walk.rs",SHA11,"12.1.1","2020-05-29",["WalkBuilder Ignore rules L448–480"],"override glob -> ignore files -> file type -> hidden 순서; 타입은 앞선 ignore 제외를 되살리지 않는다.","작성자가 실제 적용했는지/전체 목표가 한 대안으로 충족되는지는 별도. 인접 navigation L395–447도 열람했으나 판정 절은448–480."),
 ("RG-D4","doc-12.1.0-crates--ignore--src--gitignore.rs.json","crates/ignore/src/gitignore.rs",SHA10,"12.1.0","2020-05-09",["Gitignore::matched L175–195","matched_path_or_any_parents L197–240","GitignoreBuilder::new L312–327"],"패턴 매칭의 root는 일반적으로 ignore 파일을 담은 디렉터리이며 입력 path의 접두를 기준으로 상대화한다.","1778 실제 cwd/전체 규칙/실행 원자료가 없으면 이 코드만으로 보고된 실패 원인을 확정할 수 없다. 한 파일의 세 절을 읽은 노출을 숨기지 않는다.")
]
for sid,name,path,sha,v,date,sections,claim,limit in docspecs:
    d=json.loads((PRIVATE/name).read_text())
    sources.append({"source_id":sid,"lineage_id":"ripgrep-source:"+path,"kind":"official_versioned_source" if path.endswith('.rs') else "official_versioned_manual","repository_direction":"file_search","author":"Andrew Gallant and ripgrep contributors","original_url":"https://github.com/BurntSushi/ripgrep/blob/"+v+"/"+path,"pinned_url":"https://github.com/BurntSushi/ripgrep/blob/"+sha+"/"+path,"version_date":date,"version":v,"commit_sha":sha,"blob_sha":d.get('blob'),"section_lines":"; ".join(sections),"accessed_utc":d['accessed_utc'],"selection_reason":"A 후보의 당시 동작/표현을 독립 원문으로 판별","direct_read":True,"verified_claim":claim,"cannot_determine":limit,"contrary_or_unknown":"실사용 성공/사람 질문 효과 미측정","count_toward_minimum":True,"content_sha256":hash_text(d['content'])})
access += [
 {"access_id":"RG-HTML-1808","url":"https://github.com/BurntSushi/ripgrep/issues/1808","accessed_utc":"2026-11-23T08:30:00.511826+00:00","http_status":200,"content_read":"initial issue keys and bodyVersion only; no lastEditedAt; timeline/comment body not printed","count_toward_minimum":False},
 {"access_id":"RG-EDITS-1808","url":"https://github.com/BurntSushi/ripgrep/issues/1808/edits","accessed_utc":"2026-11-23T08:31:00Z","http_status":404,"timestamp_precision":"approximate minute from tool sequence; exact request UTC not captured","content_read":False,"count_toward_minimum":False},
 {"access_id":"RG-WRONG-PATH","url":"https://github.com/BurntSushi/ripgrep/blob/"+SHA11+"/src/app.rs","accessed_utc":"2026-11-23T08:30:00Z","timestamp_precision":"approximate minute","status":"no_file_at_path","count_toward_minimum":False,"next":"correct path crates/core/app.rs fetched"},
 {"access_id":"RG-NAV-LIB","url":"https://github.com/BurntSushi/ripgrep/blob/"+SHA11+"/crates/ignore/src/lib.rs","accessed_utc":"2026-11-23T08:30:00Z","timestamp_precision":"approximate minute","status":"downloaded; heading/navigation only, not substantive adjudication","count_toward_minimum":False}
]

pre=[
 {"issue_id":"RG-1808","slot":"RG-S01","initial_excerpt":"and their behavior should not change.","excerpt_source":"opened body L33, exact contiguous phrase","part":"glob/type와 ignore 우선순위","purpose":"포함 패턴으로 찾을 범위를 줄이되 ignore 파일 제외는 유지","forbidden_condition":"!로 시작하는 제외 glob의 우선순위/기존 동작을 바꾸지 않기","field_category":"forbidden_condition","selected_field":"preserve_negative_glob_priority","A_field_value":"yes; 원본문 L33에 이미 직접 명시","question_action":"skip","question":"제외 glob의 기존 우선순위를 유지해야 하나요? (이미 답이 있어 보내지 않음)","skip_reason":"제외 glob은 바꾸지 말라는 금지조건이 최초 글에 명시됨","interpretation_1":"모든 glob의 우선순위를 ignore 아래로 내린다","interpretation_2":"포함 glob만 낮추고 제외 glob은 현재 우선순위를 유지한다","candidates":[{"id":"RG1808-C1","choice":"양/음 glob 전체 우선순위 변경","A_judgment":"금지조건 위반","evidence":[{"source_id":"RG-D3","section":"L448–480"}]},{"id":"RG1808-C2","choice":"제외 glob 우선순위 보존; 포함 필터만 낮은 우선순위 대안 검토","A_judgment":"요구 방향과 합치; 타입 필터가 ignore 뒤인 사실은 확인, 제안 플래그 구현/실사용 미확인","evidence":[{"source_id":"RG-D3","section":"L448–480"},{"source_id":"RG-D1","section":"L316–414"}]}],"A_recommendation":"RG1808-C2; 알려진 금지조건에 바로 답한다. --type가 --glob와 동일 우선순위라는 원글의 일반화는 코드 순서와 맞지 않는다.","value_to_change":{"yes":"RG1808-C2","no":"금지조건은 제거되지만 전체 설계 우열은 추가로 미확인"},"version":"12.1.1","version_sha":SHA11,"version_attribution":"당시 공개판 조건부; OP 설치판 미기재","analysis_layer":"reconstructed_exposed","preread":False,"preexposure":"현재 편집본문의 패턴·범위 추가를 먼저 읽음; 재구성 A이지 순수 사전판독 아님","extra_prior_exposure":"GUIDE glob 절, app glob/type 절을 별도로 읽었으므로 엄격 노출통제 성과 분모에서 제외","packet_doc_sections_by_candidate":{"RG1808-C1":1,"RG1808-C2":2}},
 {"issue_id":"RG-1778","slot":"RG-S02","initial_excerpt":"I need to ignore `src/lib/snarky/website`.","excerpt_source":"opened body L17, first sentence","part":".ignore 패턴과 검색 시작 경로","purpose":"검색 root가 달라져도 website를 제외하고 ignore 파일 복제를 피하기","forbidden_condition":"여러 하위 디렉터리에 .ignore를 흩뿌려야 하는 구성을 피하려 함","field_category":"execution_setting","selected_field":"working_directory","A_field_value":"미기재; 상대경로만 있음","question_action":"ask","question":"두 rg 명령을 실행한 현재 작업 디렉터리는 프로젝트 루트인가요, 하위 디렉터리인가요?","skip_reason":"","interpretation_1":".ignore와 src가 cwd 바로 아래에 있다","interpretation_2":"cwd가 하위 디렉터리이고 제시 경로는 프로젝트 기준 설명이다","candidates":[{"id":"RG1778-C1","choice":"root/.ignore에 root 기준 src/lib/snarky/website를 유지하고 상대 root 일치 확인","A_judgment":"cwd/root와 실제 ignore 위치가 맞으면 후보; 보고 실패 원인은 미확인","evidence":[{"source_id":"RG-D4","section":"L312–327"}]},{"id":"RG1778-C2","choice":"실제 ignore 파일 디렉터리에 맞춰 패턴 상대경로를 조정","A_judgment":"서로 다른 기준 디렉터리를 섞은 경우에만 후보","evidence":[{"source_id":"RG-D4","section":"L175–195"}]}],"A_recommendation":"조건부 C1/C2; 누락 cwd 하나가 패턴 해석을 가를 수 있으나 정확한 실패 원인을 확정하지 않는다.","value_to_change":{"project_root":"C1 유지; 다른 원인 검토 필요","subdirectory":"실제 .ignore 기준과 입력 경로를 다시 맞춘 C2 검토"},"version":"12.1.0","version_sha":SHA10,"version_attribution":"OP 최초 글 version 직접 기재; 실행 바이너리 해시는 미확인","analysis_layer":"reconstructed_exposed","preread":False,"preexposure":"현재 body가 src/lib+src/.ignore 결과를 works→fails로 변경; 이미 현재 본문을 읽음","extra_prior_exposure":"Gitignore 동일 파일에서 matched_path_or_any_parents와 new 등 여러 절 판독; 엄격 packet 노출통제 분모 제외","packet_doc_sections_by_candidate":{"RG1778-C1":1,"RG1778-C2":1}},
 {"issue_id":"RG-1814","slot":"RG-S03","initial_excerpt":"sorted alphabetically is great as a default","excerpt_source":"opened body L2","part":"rg --help의 옵션 제시 순서","purpose":"기억나지 않는 옵션 이름을 처리 단계별로 좁혀 찾기","forbidden_condition":"알파벳순 기본보기 보존; 그룹 보기는 옵션으로","field_category":"purpose","selected_field":"preserve_alphabetical_default","A_field_value":"yes; 원본문 L2–5","question_action":"skip","question":"알파벳순 기본 도움말을 유지하길 원하나요? (이미 답이 있어 생략)","skip_reason":"기본보기 보존과 보조보기 목적을 최초 글에서 직접 지정","interpretation_1":"기본 도움말을 그룹 순서로 대체","interpretation_2":"기본 알파벳순은 두고 단계별 보조 목록을 제공","candidates":[{"id":"RG1814-C1","choice":"기본 도움말 순서 전면 대체","A_judgment":"원문 default 보존 조건과 충돌","evidence":[{"source_id":"RG-D2","section":"L32–70"}]},{"id":"RG1814-C2","choice":"기존 도움말 유지 + 처리단계 보조 목록 설계","A_judgment":"목적과 합치; 12.1.1의 현재 unified 템플릿에서 이미 제공된다는 주장은 불가","evidence":[{"source_id":"RG-D2","section":"L32–70"}]}],"A_recommendation":"RG1814-C2 방향으로 바로 답하기; 어떤 옵션이 어느 단계인지 별도 정확성 검토는 필요","value_to_change":{"yes":"RG1814-C2","no":"default 대체도 허용되나 선호 우열은 미확인"},"version":"12.1.1","version_sha":SHA11,"version_attribution":"당시 공개판 조건부; OP 버전 없음","analysis_layer":"prospective_packet","preread":True,"preexposure":"현재 body=opened body 완전일치; 댓글미열람","extra_prior_exposure":"같은 app.rs의 다른 옵션 절은 다른 이슈를 위해 읽음; 이 행의 packet 판별 절은 TEMPLATE/app 한 절","packet_doc_sections_by_candidate":{"RG1814-C1":1,"RG1814-C2":1}}
]

# A-prospective diagnostic packets are frozen before any comments as well.
pre += [
 {"issue_id":"RG-1792","slot":"","analysis_layer":"diagnostic_reconstructed_exposed","preread":False,"part":"config 환경 변수","purpose":"환경별 경로를 쓰면서 --no-config 유지","forbidden_condition":"alias만으로 우회하면 --no-config가 효력 없다는 점을 최초 글에서 지적","field_category":"forbidden_condition","selected_field":"no_config_must_disable","A_field_value":"yes; initial L4","question_action":"skip","question":"--no-config로 끌 수 있어야 하나요? (원문에 이미 답)","skip_reason":"이미 명시","initial_excerpt":"use of `--no-config` to disable the configuration","excerpt_source":"opened L4","candidates":[{"id":"RG1792-C1","choice":"literal $VAR config를 그대로 사용","A_judgment":"verbatim이므로 변수확장 요구 미충족","evidence":[{"source_id":"RG-D1","section":"L532–615"}]},{"id":"RG1792-C2","choice":"경로를 외부에서 확정한 config 파일을 쓰고 --no-config로 해제","A_judgment":"조건부 대안; 환경별 생성 단계는 연구자 재구성","evidence":[{"source_id":"RG-D1","section":"L532–615"},{"source_id":"RG-D2","section":"L1922–1935"}]}],"A_recommendation":"C2 조건부; 질문 생략","value_to_change":{"yes":"C2","no":"다른 alias 대안 가능하나 현재 두 후보에서 C1의 literal확장 부재는 그대로"},"version":"12.1.1","version_sha":SHA11,"version_attribution":"conditional public release","preexposure":"현재 body의 --no-ignore-files 부작용 문장을 먼저 읽음"},
 {"issue_id":"RG-1812","slot":"","analysis_layer":"diagnostic_prospective","preread":True,"part":"config의 홈 경로","purpose":"Linux와 macOS 사이 config 이식","forbidden_condition":"built-in 선호, 범위 밖이면 workaround 허용","field_category":"purpose","selected_field":"workaround_allowed","A_field_value":"yes; initial final paragraph","question_action":"skip","question":"내장 기능이 없으면 우회책도 괜찮나요? (최초 글에 이미 답)","skip_reason":"우회 허용 명시","initial_excerpt":"I understand if that's out of scope though and I can work around it.","excerpt_source":"opened final paragraph","candidates":[{"id":"RG1812-C1","choice":"$HOME/~를 config에 literal로 넣음","A_judgment":"verbatim이므로 확장 안 됨","evidence":[{"source_id":"RG-D1","section":"L532–615"}]},{"id":"RG1812-C2","choice":"환경별 경로가 들어간 config를 외부 단계에서 생성","A_judgment":"조건부 우회 후보; 실제 채택/실행 미확인","evidence":[{"source_id":"RG-D1","section":"L532–615"}]}],"A_recommendation":"C2 조건부; 이미 허용한 우회 여부를 다시 묻지 않음","value_to_change":{"yes":"C2","no":"C1도요구불충족; 내장개선요청 외 결론미확인"},"version":"12.1.1","version_sha":SHA11,"version_attribution":"conditional public release","preexposure":"현재=opened 동일;댓글미열람"},
 {"issue_id":"RG-1840","slot":"","analysis_layer":"diagnostic_prospective","preread":True,"part":"숨김 cwd에서 하위 파일 검색","purpose":"명시 subdir과 cwd검색이 원하는파일을 동일하게 찾기","forbidden_condition":"미기재","field_category":"execution_setting","selected_field":"exclusion_reason","A_field_value":"unknown; 작성자는 cwd의 hidden 속성을 원인으로 추정","question_action":"ask","question":"--debug에서 대상 파일을 제외한 이유는 Hidden인가요, ignore 규칙인가요?","skip_reason":"","initial_excerpt":"When the current directory is \"hidden\"","excerpt_source":"opened description first sentence","candidates":[{"id":"RG1840-C1","choice":"--hidden으로 hidden 제외를 해제","A_judgment":"실제원인이 Hidden일때만 후보","evidence":[{"source_id":"RG-D2","section":"L1425–1444"}]},{"id":"RG1840-C2","choice":"해당 ignore 규칙만 수정/해제","A_judgment":"실제원인이 ignore 규칙일때 후보; hidden만으로는그규칙해제안됨","evidence":[{"source_id":"RG-D3","section":"L448–480"}]}],"A_recommendation":"원인이 확인되기 전 C1/C2 조건부","value_to_change":{"Hidden":"C1","ignore_rule":"C2"},"version":"12.1.1","version_sha":SHA11,"version_attribution":"OP version 직접기재","preexposure":"현재=opened 동일;댓글미열람"}
]
for r in pre:
    n=int(r['issue_id'].split('-')[1]);e=next(x for x in enrollment if x['number']==n)
    r.update({"view":"A","cutoff_A":NOW,"cutoff_A_utc":NOW,"data_cutoff_A_utc":e['created_at'],"number":n,"repo":"BurntSushi/ripgrep","body_sha256":e['body_sha256'],"original_url":e['url'],"archive":e['original_recovery'],"author":e['author'],"masked_information":"all comments, subsequent author choices, issue status and comment count","prepared_utc":NOW,"seal_commit":"ROOT_TO_FILL_AFTER_COMMIT","comments_read_before_seal":False,"B_added_fields_limit":1})
pins=[]
for r in pre:
    for c in r['candidates']:
        for ev in c['evidence']:
            s=next(x for x in sources if x['source_id']==ev['source_id'])
            pins.append({"pin_id":r['issue_id']+'-'+c['id']+'-'+ev['source_id'],"issue_id":r['issue_id'],"candidate_id":c['id'],"source_id":ev['source_id'],"section":ev['section'],"commit_sha":s.get('commit_sha'),"pinned_url":s['pinned_url']+'#'+ev['section'].replace('–','-L'),"A_B_same_packet_required":True,"document_budget_per_candidate":2,"section_budget_per_document":1,"prepared_utc":NOW})
write_json('enrollment.json',enrollment)
write_json('pre.json',pre)
write_json('pins.json',pins)
write_json('queue.json',queue)
(OUT/'sources-pre.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sources))
(OUT/'access.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in access))

md=['# ripgrep A 봉인 패킷','',f'준비 UTC: {NOW}. 댓글 아직 미열람. 원 모집슬롯3개와 별도 진단3개.','',
'원래 본문8/8을 GH Archive IssuesEvent/opened에서 복구했다. 1808·1778·1792는 현재본문이 바뀌었다. 특히1778의 works→fails 수정 때문에 현재본문을 최초판으로 쓰면 관측 방향이 뒤집힌다. 이미 현재본문을 읽은 세 행은 재구성층이며 순수 사전판독 수에 넣지 않는다.',
'','9–16은 원본문복구 전 최초판미확인 상태에서 순서대로 연 확장조회다. 첫3 원본문이 복구되어 선정 대체에 사용하지 않는다.','',
'## 봉인 행','', '|행|층|한 필드|질문/생략|A 권고|', '|---|---|---|---|---|']
for r in pre:md.append('|'+ '|'.join([r['issue_id'],r['analysis_layer'],r['selected_field'],r['question_action'],r['A_recommendation']])+'|')
md += ['','## 노출·판별 범위','',
'모든 A/B 후보는 pre.json과 pins.json에 고정한다. 데이터 수신 과정의 GitHub HTML에는 댓글이 포함되어 있었지만 JSON 최초 객체 키만 출력했고 댓글 내용은 보지 않았다. REST 댓글 endpoint는 아직 호출하지 않았다.',
'',
'1808/1778은 사후 편집본문 선행노출과 부가문서절 판독으로 엄격 사전 노출통제 분석에서 제외한다. 이들의 원 최초판과 A 재구성은 별도로 유용하지만 사전예측 정확도라고 부르지 않는다. 1814의 도구판은 OP가 밝히지 않아 당시 공개12.1.1에 대한 조건부 판정이다.',
'',
'본 스트림의 공식 원저작은 GUIDE.md, crates/core/app.rs, crates/ignore/src/walk.rs, crates/ignore/src/gitignore.rs의4계보이다. 같은 파일의 절·버전·API별 응답을 추가원작으로 세지 않는다. GUIDE/소스의 다운로드 전체와 실제판독절은 구분하며 실제판독절은 sources-pre.jsonl에 보존한다.',
'',
'원작성자 발언은 의도 근거이고 도구 동작 판별은 고정판 코드·문서 근거이다. 새 필드 값이 없으면 B=자료없음, 질문이 쓸모없었다는 의미가 아니다.']
(OUT/'A.md').write_text('\n'.join(md)+'\n')
print(json.dumps({'prepared_utc':NOW,'enrollment':len(enrollment),'main_slots':3,'A_rows':len(pre),'official_lineages':4,'issue_lineages':16,'comments_read':False},ensure_ascii=False))
