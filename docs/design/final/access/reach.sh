#!/usr/bin/env bash
# 이 클라우드 환경(세션 네트워크)에서 어느 호스트가 열리는지 한 번씩 본다. GET 한 번, 본문은 버린다.
# 결과: 상태 코드(000 = 프록시가 연결을 거절했거나 닿지 않음). 재실행: bash docs/design/final/access/reach.sh
set -u
date -u +"# %Y-%m-%dT%H:%M:%SZ"
while read -r group url; do
  [ -z "$group" ] && continue
  code=$(curl -s -o /dev/null -m 15 -w "%{http_code}" "$url" 2>/dev/null)
  printf "%s\t%s\t%s\n" "$code" "$group" "$url"
done <<'LIST'
origin https://docs.python.org/3.13/library/asyncio-queue.html
origin https://support.mozilla.org/en-US/kb/future-of-pocket/history
origin https://blog.mozilla.org/en/feed/
origin https://www.openarchives.org/OAI/openarchivesprotocol.html
origin https://example.com/
origin https://en.wikipedia.org/wiki/Main_Page
github https://raw.githubusercontent.com/python/cpython/v3.13.0/README.rst
github https://api.github.com/rate_limit
github https://api.github.com/search/code?q=Queue+repo:python/cpython
github https://api.github.com/repos/python/cpython/commits/v3.13.0
github https://github.com/python/cpython
github https://codeload.github.com/python/cpython/tar.gz/refs/tags/v3.13.0
forge https://gitlab.com/api/v4/projects/278964
registry https://pypi.org/pypi/requests/json
registry https://registry.npmjs.org/express
registry https://proxy.golang.org/golang.org/x/sync/@v/list
registry https://sum.golang.org/lookup/golang.org/x/sync@v0.7.0
registry https://index.crates.io/config.json
registry https://static.crates.io/crates/serde/serde-1.0.200.crate
registry https://rubygems.org/api/v1/gems/rails.json
registry https://repo.maven.apache.org/maven2/
registry https://api.nuget.org/v3/index.json
registry https://packagist.org/packages/laravel/framework.json
archive https://web.archive.org/web/2025/https://docs.python.org/3/
archive https://archive.org/wayback/available?url=docs.python.org
archive https://index.commoncrawl.org/collinfo.json
archive https://data.commoncrawl.org/crawl-data/index.html
archive https://archive.ph/
archive https://archive.softwareheritage.org/api/1/
mirror https://cdn.jsdelivr.net/npm/express@4.18.2/package.json
mirror https://unpkg.com/express@4.18.2/package.json
mirror https://docs.rs/
mirror https://r.jina.ai/https://example.com
LIST
