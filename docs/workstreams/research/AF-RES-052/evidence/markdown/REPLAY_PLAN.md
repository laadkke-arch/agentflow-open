# 미실행 재현 계획 — M-N1 / remark issue941

**상태: 아래 설치·명령·검사는 실행하지 않았다.** npm 접근 가능성, registry의 정확 패키지판 존재, 설치 lockfile, 실제 의존성 해석과 실행 결과는 모두 미확인이다. 이 계획은 현재 구성의 D2 판독을 D3로 확인하기 위한 후속 입력이다. 원요청의 `react-stringify10.0.2; unified10.1.1`을 다른 패키지명·판으로 바꾸는 역사 재현이 아니다.

## 1. 입력과 판의 근거

| 항목 | 직접 확인한 내용 | 실행 전 확인할 부분 |
| --- | --- | --- |
| 원입력 | [issue941](https://github.com/remarkjs/remark/issues/941) 현재 확보 본문 L42–63의 root에 code 노드2개. 첫 lang은 javascript, 둘째는 null, 양쪽 meta는 null, value는 동일하다. | 생성시 최초 본문과 CodeSandbox는 미복원. 아래 입력은 최초 가용 본문을 재구성하며 첨부를 복구한 것이 아님. |
| wrapper | [현재 manifest](https://github.com/remarkjs/remark/blob/1146b3a274fc1f4607111e5d6607a3a769a0e89a/packages/remark-stringify/package.json#L8-L12), L42–51: remark-stringify11.0.0, utility ^2.0.0, unified ^11.0.0. | npm tarball이 이 소스와 일치하는지 미확인. 설치된 이름·판·해석 경로를 아래 검사로 남긴다. |
| utility | 직접 읽은 tag2.0.0의 소스 SHA `655f117443d99a08cb839765ff7489aa759f72d0`; [code handler](https://github.com/syntax-tree/mdast-util-to-markdown/blob/655f117443d99a08cb839765ff7489aa759f72d0/lib/handle/code.js#L20-L72), [시험](https://github.com/syntax-tree/mdast-util-to-markdown/blob/655f117443d99a08cb839765ff7489aa759f72d0/test/index.js#L794-L979). | npm 설치판과 lockfile integrity는 미확인. wrapper가 실제로 해석한 utility도2.0.0인지 검사한다. |
| unified | wrapper manifest의 허용 범위 ^11.0.0만 이번 자료에서 확인했다. | **11.0.0은 계획한 정확 pin**이다. 별도 unified tag·registry 발행기록을 읽어 검증한 판이라고 단정하지 않는다. 해당 설치가 실패하면 다른 판으로 자동 대체하지 않는다. |

source SHA는 목록의 제품판 표시 키가 아니다. 위 정보는 목적지 관측 뒤 얻은 실행 준비용 근거이며 봉인한 C 키를 채우는 데 사용하지 않는다. 관련 원장 ID는 `M-ISS-941`, `M-CODE-PACKAGE`, `M-CODE-COMPILER`, `M-CODE-HANDLER`, `M-TEST-UTILITY`다.

## 2. 고정할 기대 조건

- **M-N1-C1:** lang=null인 둘째 code 노드를 backtick fence로 감싼다. 들여쓰기만 있는 코드 또는 tilde fence는 이 요구의 성공이 아니다.
- **M-N1-C2:** 첫 노드의 javascript 언어 라벨과 value의 모든 문자·줄바꿈을 유지한다. 특히 value 마지막 줄의 `export` 뒤 공백은2개이며, 입력 value 끝에는 추가 줄바꿈이 없다.
- **구분한 모호성:** 원문이 제시한 “correct output”은 둘째 opening fence와 코드의 줄바꿈·들여쓰기가 불명확하다. 그 문자열 전체를 엄격한 byte oracle로 사용하지 않는다. 아래 검사는 두 MUST를 따로 검사하며 실제 전체 출력과 소스 SHA를 기록한다. fence 바깥의 블록 사이 공백이나 최종 newline을 새로운 사용자 필수조건으로 추가하지 않는다.
- **조건부 현재 구성:** `fences=true`, marker=backtick, 추가 handler/extension 없음. 옵션 미지정 default 사례는 별도 행으로 읽고, 설정한 사례의 성공과 혼동하지 않는다.
- **근접 오답:** `fences=false`는 lang 없는 둘째 노드가 들여쓰기 코드가 되어 C1=false/C2=true일 것으로 예상한다. marker=tilde는 Markdown으로는 유효해도 C1=false/C2=true일 것으로 예상한다. 이 결과가 관측되면 반례 검사는 성공한 것이며, 사용자 요구를 충족했다고 세지는 않는다.

## 3. 설치 명령 — 저장소 루트에서, 아직 실행하지 않음

Node.js와 npm이 제공된 격리 실행 환경에서 다음 명령을 수행한다. 모든 생성 파일과 의존성은 소유 경로 안 `cache/replay-current/`에 둔다. 이 디렉터리는 원문·실행 캐시이며 검증 결과를 인계할 때에는 로그·exit code·입력 해시·lockfile 해시를 별도 커밋 가능한 증거 파일에 옮겨야 한다. registry 접속이나 설치가 실패하면 중단하고 실패 로그를 보존한다.

```bash
mkdir -p docs/workstreams/research/AF-RES-052/evidence/markdown/cache/replay-current
cd docs/workstreams/research/AF-RES-052/evidence/markdown/cache/replay-current

cat > package.json <<'JSON'
{
  "name": "af-res-052-current-replay",
  "version": "0.0.0",
  "private": true,
  "type": "module",
  "dependencies": {
    "remark-stringify": "11.0.0",
    "mdast-util-to-markdown": "2.0.0",
    "unified": "11.0.0"
  },
  "overrides": {
    "mdast-util-to-markdown": "2.0.0"
  }
}
JSON

node --version > environment.txt
npm --version >> environment.txt
npm install --ignore-scripts --no-audit --no-fund --registry=https://registry.npmjs.org > install.log 2>&1
AF_RES_052_INSTALL_STATUS=$?
printf '%s\n' "$AF_RES_052_INSTALL_STATUS" > install.exit
if [ "$AF_RES_052_INSTALL_STATUS" -ne 0 ]; then
  printf '%s\n' 'Installation failed; preserve install.log and do not substitute package versions.'
  exit "$AF_RES_052_INSTALL_STATUS"
fi
npm ls --all --json > dependency-tree.json 2> dependency-tree.stderr.log
AF_RES_052_TREE_STATUS=$?
printf '%s\n' "$AF_RES_052_TREE_STATUS" > dependency-tree.exit
```

최초 `npm install`은 직접 의존성3개를 정확하게 고정하지만, 그 밖의 전이 의존성은 설치 시점에 해석된다. 생성된 `package-lock.json`을 보존해야 구체적으로 다시 실행할 수 있는 설치가 된다. 최초 실체를 확인한 뒤의 재시도에서만 `npm ci --ignore-scripts --no-audit --no-fund`를 사용한다. 아직 확인하지 않은 lockfile을 기존 증거로 취급하지 않는다. 위 경로는 비어 있는 새 재현 디렉터리에 적용하며, 기존 실행 증거가 있으면 다른 이름의 owned cache 하위 디렉터리를 사용한다.

## 4. 정확 입력과 검사 파일 — 아직 실행하지 않음

위 cache 디렉터리에서 다음 파일을 만든다. 공유 value를 한 번 정의하고 두 노드에 넣어 원입력과 같은 구조를 만든다. 따라서 생성되는 `input.json`에는 **첫 lang=javascript, 둘째 lang=null인 실제 두 code 노드와 동일한 완전한 value**가 들어간다. HTML처럼 보이는 value는 문자열로만 처리하며 그 내용을 실행하지 않는다.

```bash
cat > replay.mjs <<'JS'
import assert from 'node:assert/strict'
import {createHash} from 'node:crypto'
import {readFileSync, writeFileSync, existsSync} from 'node:fs'
import {dirname, join, parse} from 'node:path'
import {createRequire} from 'node:module'
import {unified} from 'unified'
import remarkStringify from 'remark-stringify'
import {toMarkdown} from 'mdast-util-to-markdown'

// Exact shared value in issue941 body L53 and L60; last line has two spaces.
const value = [
  'function $initHighlight(block, cls) {',
  '  return (',
  '    <div>',
  '      <web-component>test</web-component>',
  '    </div>',
  '  )',
  '}',
  'export  $initHighlight;'
].join('\n')
const codeNode = lang => ({type: 'code', lang, meta: null, value})
const input = {
  type: 'root',
  children: [codeNode('javascript'), codeNode(null)]
}
const inputJson = JSON.stringify(input, null, 2) + '\n'
writeFileSync('input.json', inputJson)
const digest = bytes => createHash('sha256').update(bytes).digest('hex')

// Resolve actual package metadata without assuming package.json is exported.
function installedPackage(name, from = import.meta.url) {
  const resolver = createRequire(from)
  const entry = resolver.resolve(name)
  let directory = dirname(entry)
  while (true) {
    const candidate = join(directory, 'package.json')
    if (existsSync(candidate)) {
      const pkg = JSON.parse(readFileSync(candidate, 'utf8'))
      if (pkg.name === name) return {name, version: pkg.version, entry, manifest: candidate}
    }
    if (directory === parse(directory).root) break
    directory = dirname(directory)
  }
  throw new Error('Cannot locate manifest for ' + name)
}
const wrapper = installedPackage('remark-stringify')
const engine = installedPackage('unified')
const utility = installedPackage('mdast-util-to-markdown')
const wrapperUtility = installedPackage('mdast-util-to-markdown', wrapper.entry)
const versions = {wrapper, engine, utility, wrapperUtility}
writeFileSync('resolved-versions.json', JSON.stringify(versions, null, 2) + '\n')
assert.equal(wrapper.version, '11.0.0')
assert.equal(engine.version, '11.0.0')
assert.equal(utility.version, '2.0.0')
assert.equal(wrapperUtility.version, '2.0.0')

// The fixture contains no fence characters in its value. Collect actual fenced
// output blocks and compare their info/body; do not impose outer whitespace.
function fencedBlocks(output) {
  const lines = output.split('\n')
  const blocks = []
  for (let i = 0; i < lines.length; i++) {
    const opening = /^(`{3,}|~{3,})(.*)$/.exec(lines[i])
    if (!opening) continue
    const marker = opening[1]
    const close = new RegExp('^' + marker[0] + '{' + marker.length + ',}[ \\t]*$')
    const body = []
    let ended = false
    for (i++; i < lines.length; i++) {
      if (close.test(lines[i])) {
        ended = true
        break
      }
      body.push(lines[i])
    }
    if (ended) blocks.push({marker, info: opening[2], body: body.join('\n')})
  }
  return blocks
}

const cases = [
  {id: 'configured_backticks', options: {fences: true, fence: '`'}, expected: {C1: true, C2: true}},
  {id: 'current_default', options: {}, expected: {C1: true, C2: true}},
  {id: 'near_miss_indented', options: {fences: false, fence: '`'}, expected: {C1: false, C2: true}},
  {id: 'near_miss_tilde', options: {fences: true, fence: '~'}, expected: {C1: false, C2: true}}
]
const results = cases.map(item => {
  const output = String(unified().use(remarkStringify, item.options).stringify(input))
  const utilityOutput = toMarkdown(input, item.options)
  writeFileSync(item.id + '.md', output)
  const blocks = fencedBlocks(output)
  const C1 = Boolean(blocks[1] && blocks[1].marker[0] === '`' &&
    blocks[1].info === '' && blocks[1].body === value)
  const C2 = Boolean(blocks[0] && blocks[0].info === 'javascript' &&
    blocks[0].body === value)
  return {
    id: item.id,
    options: item.options,
    expected: item.expected,
    observed: {C1, C2},
    fulfills_request_musts: C1 && C2,
    matches_direct_utility: output === utilityOutput,
    output_sha256: digest(output),
    output
  }
})
const report = {
  claim_scope: 'Current configured replay only; not historical react-stringify10.0.2',
  node_version: process.version,
  input_sha256: digest(inputJson),
  lockfile_sha256: digest(readFileSync('package-lock.json')),
  versions,
  results
}
writeFileSync('replay-result.json', JSON.stringify(report, null, 2) + '\n')
console.log(JSON.stringify(report, null, 2))
// Preserve the full report before any assertion exits nonzero.
for (const result of results) {
  assert.deepEqual(result.observed, result.expected, result.id)
  assert.equal(result.matches_direct_utility, true, result.id + ': wrapper/utility mismatch')
}
JS

node replay.mjs > replay.stdout.log 2> replay.stderr.log
AF_RES_052_REPLAY_STATUS=$?
printf '%s\n' "$AF_RES_052_REPLAY_STATUS" > replay.exit
```

`current_default`가 예상과 다르면 설정한 `configured_backticks`와 나누어 보고한다. 두 근접 오답이 C1=false를 보이는 것은 실패한 사용자 요구 사례를 제대로 관측했다는 뜻이다. 프로세스 exit0은 네 사례가 **각각 미리 적은 예상**과 맞았다는 의미이며 네 사례 모두 요구를 충족했다는 뜻이 아니다. 설치된 실제 경로·판이 다르거나, wrapper와 utility 직접 결과가 다르면 그 차이를 조사하기 전에는 현재 조건부 정답을 실행 검증된 정답으로 바꾸지 않는다.

## 5. 보존할 실행 증거와 역사 재개의 첫 행동

후속 실행자는 `environment.txt`, `install.log`, `install.exit`, `package-lock.json`과 그 SHA256, `dependency-tree.json`·exit, `input.json`·SHA256, `resolved-versions.json`, 네 출력 파일, `replay-result.json`, stdout/stderr 및 `replay.exit`를 보존한다. 실패하면 실패한 첫 명령·입력·오류·exit code를 커밋 가능한 요약에 적는다. npm lockfile 안의 `resolved`·`integrity`를 공급자 소스 SHA와 혼동하지 않는다.

역사판 재현의 **다음 첫 행동**은 원941의 첨부 또는 질문자의 보존된 lockfile에서 `react-stringify`의 실제 패키지 식별과 정확 설치판을 확인하는 것이다. 그 자료가 없으면 이 계획을 실행해도2022년 설치의 성공·실패는 미확인으로 남는다. 원문 예상 문자열의 둘째 fence 줄바꿈 의도까지 엄격히 판정하려면 같은 자료 또는 질문자의 명시적 출력 설명이 추가로 필요하다.
