"""Record directly read supplemental primary sources and bounded observations."""
from pathlib import Path
import datetime as dt
import json

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
CACHE = ROOT / ".cache/root-supplement"
reads = json.loads((CACHE / "acquisition.json").read_text())
(OUT / "acquisition.json").write_text(json.dumps(reads, ensure_ascii=False, indent=2) + "\n")
(OUT / "failures.jsonl").write_text("".join(json.dumps(r) + "\n" for r in reads if "error" in r))
meta = {r["id"]: r for r in reads}
now = dt.datetime.now(dt.timezone.utc).isoformat()
definitions = [
 ("SUP-QUICK-IMAGE", "quick-magick", ["IM-A1"], "Ahmed ElDawy / QuickMagick",
  "QuickMagick 0.8.0 implementation; gem and GitHub source are the SAME work",
  "3473e473b61a1783e150fcdf7e9b0b718f1a5793 lib/quick_magick/image.rb L18–28,96–103,115–182,212–214,367–376",
  "Image.read는 image 배열을 만들고 연산 메서드는 args.join으로 CLI 인수를 붙인다. alpha는 WITH_EQUAL_METHODS에 있어 alpha=로 정의된다. threshold(15)에 %를 보충하는 구현은 없고 composite의 객체 인수도 일반 문자열 연결 경로다. 공식 0.8.0 gem의 이 파일 SHA-256이 고정 GitHub 파일과 일치한다.",
  "C1을 검증된 RMagick식 객체 API로 취급하는 해석을 반박; threshold 15와15% 동일성 반박.",
  "질문자의 gem 판/패치/추가 로딩 미확인. Ruby 실행 없음. Object#clone 세부 효과까지 단정하지 않음.", True),
 ("SUP-RMAGICK-CHANGELOG", "rmagick-changelog", ["IM-A1"], "RMagick contributors",
  "RMagick release history, same upstream package as binding source",
  "RMagick_5-3-0 / 02f37ca0d6c2b8fff316e0668efa690f5c90a429 CHANGELOG.md L228–244 (4.0.0 section)",
  "4.0.0 breaking changes에서 Image#matte 및 matte=가 제거됐다고 명시한다. 제거 판은 5.0.0이 아니라 4.0.0이다.",
  "C2의 image.matte=false를 판과 무관한 유효 호출이라고 단정하는 해석 반박.",
  "5.3.0 파일로 읽은 과거 변경 이력이며 실제 질문자 설치판은 모른다. 옛 RMagick 판에서 원 후보 전체 성공 여부는 미실행.", True),
 ("SUP-RMAGICK-BINDING", "rmagick-binding-c", ["IM-A1"], "RMagick contributors",
  "RMagick native binding implementation, distinct file from changelog",
  "02f37ca0d6c2b8fff316e0668efa690f5c90a429 ext/RMagick/rmmain.c L358–359,411–412,448–450,597–598",
  "Image alpha/composite/threshold 메서드 등록은 존재한다. matte_color와 matte_flood_fill은 있지만 Image의 matte= 등록은 없다. 메서드 이름의 부분 일치를 근거로 matte=가 남았다고 읽을 수 없다.",
  "5.3.0의 matte= 부재를 구현으로 교차확인; 다른 이름의 matte 계열을 별칭으로 간주하는 해석 반박.",
  "외부 monkey patch/이전 판은 확인하지 않았으며 실제 Ruby 실행은 없다.", True),
 ("SUP-RUBY-OPEN3", "ruby-open3", ["IM-A1"], "Ruby core team",
  "Ruby standard library Open3 implementation",
  "Ruby3.2.2/e51014f9c05aa65cbf203442d37fef7c12390015 lib/open3.rb L32,69–104,216–234,763–764",
  "Open3는 프로세스 stdin/stdout/stderr와 wait thread를 다루고 문자열 command를 Process.spawn에 전달할 수 있다. 이 파일의 require는 open3/version과 조건부 JRuby 파일이며 shellwords를 직접 require하지 않는다.",
  "C3의 외부 CLI 호출 방식 자체는 공식 API와 맞지만 shellescape 메서드 제공까지 보장한다는 해석은 지지하지 않는다.",
  "Rails 등 주변 프로그램이 이미 Shellwords를 로드했을 수 있다. Ruby가 없어 standalone snippet은 미실행.", True),
 ("SUP-RUBY-SHELLWORDS", "ruby-shellwords", ["IM-A1"], "Ruby core team",
  "Ruby standard library Shellwords implementation; separate module",
  "Ruby3.2.2/e51014f9c05aa65cbf203442d37fef7c12390015 lib/shellwords.rb L148–172,219–226",
  "Shellwords는 문자열을 Bourne 계열 셸 인수로 escape하고 String#shellescape를 정의한다. C3의 .shellescape에는 이 모듈 로딩이라는 선행조건이 있다.",
  "같은 grouped convert를 감싸는 새 호출 경로에 별도 상태/의존성이 생길 수 있음을 지지.",
  "질문자 프로세스에서 이미 require됐는지는 미확인. escape는 임의 프로그램 옵션 의미의 안전/정확성을 대신하지 않는다.", True),
 ("SUP-CSS-BORDERS", "css-borders", ["TY-A1"], "W3C CSS Working Group",
  "CSS Backgrounds and Borders Level3 Candidate Recommendation 2020-12-22",
  "§3.2 line styles, §3.3 widths, §3.4 border shorthand; downloaded HTML L1664ff #border-shorthands",
  "border shorthand는 line-width, line-style, color의 결합이다. 후보 border:2px 2px black에는 너비값이 두 번 나오며 두 번째 2px는 line-style이 아니다. per-edge widths의 1~4값 규칙은 border-width에 속한다.",
  "TY-A1-C1 원 literal을 유효 CSS 경로라고 보는 해석 반박. Typst 문서 입력이 CSS hook을 제공한다는 독립 증거도 없다.",
  "실제 CSS 호스트가 제시되지 않았고 브라우저 실행은 하지 않았다. 연구자가 2px solid black으로 수정한 것은 원 후보와 다르다.", True),
]
sources = []
for sid, key, cases, publisher, lineage, locator, observed, relation, limits, counted in definitions:
    r = meta[key]
    sources.append({"source_id":sid,"q":["Q5","Q7"],"case_ids":cases,"category":"supplemental_primary",
                    "original_url":r["url"],"direct_open_url":r["url"],"fixed_url":r["url"],
                    "checked_at_utc":r["accessed_at_utc"],"author_publisher":publisher,"lineage":lineage,
                    "version_section_locator":locator,"fingerprint":{"sha256":r["sha256"],"bytes":r["bytes"]},
                    "observed":observed,"claim_relation":relation,"limits_unknown":limits,
                    "counted":counted,"duplicate_reason":None})
for sid, key, note in [
    ("SUP-QUICK-METADATA","rubygems-quick-magick","등록 metadata: 0.8.0, version_created_at2010-10-31, 저자 Ahmed ElDawy. 단독 동작 증거로 산입하지 않음."),
    ("SUP-QUICK-PACKAGE","quick-magick-package","gem 내부 lib/quick_magick/image.rb가 SUP-QUICK-IMAGE와 바이트동일. 배포 계보 확인이며 중복 산입 안함.")]:
    r = meta[key]
    sources.append({"source_id":sid,"q":["Q5"],"case_ids":["IM-A1"],"category":"lineage_verification",
                    "original_url":r["url"],"direct_open_url":r["url"],"fixed_url":r["url"],
                    "checked_at_utc":r["accessed_at_utc"],"author_publisher":"RubyGems registry / Ahmed ElDawy",
                    "lineage":"QuickMagick0.8.0","version_section_locator":"metadata / gem!lib/quick_magick/image.rb",
                    "fingerprint":{"sha256":r["sha256"],"file_sha256":r.get("file_sha256")},
                    "observed":note,"claim_relation":"배포판과 저장소 파일 일치 교정",
                    "limits_unknown":"질문자 설치판 미확인; registry metadata는 현재 관측",
                    "counted":False,"duplicate_reason":"same QuickMagick work or supporting registry metadata"})
(OUT / "sources.jsonl").write_text("".join(json.dumps(s,ensure_ascii=False)+"\n" for s in sources))
assessments = [
 {"candidate_id":"IM-A1-C1","literal_required_output":"반박(QuickMagick0.8.0 경계)","immutable_conditions":"미확인",
  "evidence":["SUP-QUICK-IMAGE","probe-receipt.json:grouped-raw15"],
  "finding":"alpha('off')와 composite 객체 API를 그대로 유효하다고 할 수 없고 15와15%는 합성 근회색 alpha를 바꾼다. 사용자 후속 없이도 원 literal의 불완전성이 보인다.",
  "limits":"원판/원입력/Ruby 실행 없음; 수정형 실패와 원 literal은 별도."},
 {"candidate_id":"IM-A1-C2","literal_required_output":"반박(RMagick5.3.0); 사용자판 미확인","immutable_conditions":"미확인",
  "evidence":["SUP-RMAGICK-CHANGELOG","SUP-RMAGICK-BINDING"],
  "finding":"이미4.0.0에서 제거된 matte=를 사용. QuantumRange*.15는 원15%에 맞지만 이것만으로 전체 파이프라인은 유효하지 않다.",
  "limits":"RMagick3.x 등 이전판에서는 다를 수 있어 원 사용자 실패라고 확정하지 않는다."},
 {"candidate_id":"IM-A1-C3","literal_required_output":"조건부 지지(연구판 CLI 부분만)","immutable_conditions":"미확인",
  "evidence":["SUP-RUBY-OPEN3","SUP-RUBY-SHELLWORDS","probe-receipt.json:grouped-percent"],
  "finding":"grouped CLI는 합성회색을 alpha0으로 만들며 red/blue/green을 보존. 이미 알려진 CLI의 새 Ruby 호출 경로이고 Shellwords 로딩이 필요하다.",
  "limits":"전체 Ruby snippet과 사용자입력은 미실행. 원3위로 B도 반환하지 않는다."},
 {"candidate_id":"IM-A2-C1","literal_required_output":"반박(연구 셸의 인수 전달)","immutable_conditions":"미확인",
  "evidence":["probe-receipt.json:c1-interpolation-argv-only"],
  "finding":"구문 검사는0이지만 문자열의 역슬래시 괄호8개와 인용부호가 실제argv에 남는다. 변수확장은 명령어를 다시 parsing하지 않는다.",
  "limits":"이 제어는 argv만 수집하며 원 Cygwin7.0.10-61 명령 전체를 실행한 것이 아니다. 배열/별도 인수 수정은 새 연구 조작."},
 {"candidate_id":"IM-A2-C2","literal_required_output":"반박(원 제안 bash 구문)","immutable_conditions":"미확인",
  "evidence":["probe-receipt.json:literal-syntax-77797051"],
  "finding":"rev1 pre3를 그대로 bash -n 하면 잔여fi에서 exit2. dims typo 외에도 patch크기가30x40 고정이고 dims가 mpr앞 size로 이동해 단순치환과 다르다.",
  "limits":"후속수정/사용자가 실제 채택한 교정형 미확인. 감사문만으로 실행 성공 판정 안함."},
 {"candidate_id":"TY-A1-C1","literal_required_output":"반박(CSS 문법); Typst 적용 미확인","immutable_conditions":"미확인",
  "evidence":["SUP-CSS-BORDERS"],
  "finding":"원 border:2px 2px black은 width중복으로 유효 shorthand가 아니며 제공된 Typst 경로에 CSS hook 근거가 없다.",
  "limits":"조건부 다른호스트/수정된CSS는별도; 원후보 유효대안 분모에 넣지 않는다."}
]
(OUT / "assessment.json").write_text(json.dumps({"judged_utc":now,"blinding":"after stage2 seal; root has seen OP followup summaries, source observations and tests are independent of those summaries","candidates":assessments},ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"sources":len(sources),"counted":sum(s["counted"] for s in sources),"assessments":len(assessments)}))
