# Homebrew A 과거 참조 봉인 메모

6개 참조와 6개 소비자를 확보했다. 자료 자체가 패키지명으로 설치를 지시하므로 이들은 문자열 패키지 참조다. `formulae.brew.sh/formula/...`는 연구자가 보조 조회를 위해 정규화한 주소이며, 소비자 원문에 그 URL을 직접 붙여 놓았다고 말하지 않는다. 당시 지시 파일의 full SHA URL이 일차 인용 주소다.

## 채택과 탈락

- fish-shell/cppcheck: 개인 tap의 iwyu/oclint를 제외한 첫 공식 패키지. 동일 판의 C++ 분석 호출을 읽었다.
- kitty/pkg-config: Brewfile 첫 항목. 같은 판 setup.py가 실행파일을 부르고 cflags/libs를 해석한다.
- neovim/ninja: 2019·2021 CI는 매뉴얼 직접 연결 요건을 충족하지 않아 제외했고, 2023 BUILD.md의 Homebrew 설치 지시를 골랐다. stable checkout은 소비자 Neovim 판 선택이지 Ninja 최신판 요구가 아니다.
- OBS/cmake: 2019 단독 CI는 제외. 2021에는 실제 Brewfile이 있고 같은 판 full-build-macos.sh가 이를 설치하고 cmake를 호출한다.
- scrcpy/sdl2: 2019 BUILD의 첫 runtime 패키지, 같은 판 Meson의 executable dependency를 확인했다.
- qutebrowser/qt5: 자기 제품 cask를 제외한 수동 설치의 첫 brew 패키지. 같은 판은 PyQt5.QtWebEngineWidgets를 import한다. Qt와 Python binding이 별개라는 한계를 남겼다.

alacritty, mpv, wezterm, tmux는 사전 anchor와 경로를 조사했으나 적격 Homebrew 외부도구 설치 참조를 확보하지 못했다. 특히 mpv/neovim의 과거 단독 CI와 OBS의 2019 script를 숫자 충족 목적으로 설치 매뉴얼로 확대하지 않았다. tmux는 공식 wiki Git의 2019 파일 부재와 2021/2023 원문까지 확인했지만 Homebrew 명령은 자기 제품 tmux 설치뿐이었다. 이 미발견은 저장소의 모든 과거 판에 참조가 없다는 전수 결론이 아니다.

## 판독·수치의 경계

현재 13개의 핵심 파일 URL을 직접 읽고 다시 열었지만 같은 소비자 snapshot의 목적/호출 보조 파일을 합쳐 **원문 최소수에는 6개만** 넣었다. 나머지 탐색/탈락 파일은 sources.json에 모두 비산입으로 기록했다. 실제 설치, solver 선택, 과거 CI 성공, 소비자 release 포함은 이 단계에서 확인하지 않았다. 역사 재현 의도와 현재 최신판 요구도 추정하지 않았다.

원격 봉인 전까지 선택된 A의 상류 변경, 후속 소비자 수정/배포를 읽지 않았다. 2019에서 적격 자료를 확보하지 못한 후보를 다음 anchor로 옮긴 것은 정해진 모집 절차다. 저장소 URL 이동(wez→wezterm)은 2019 고정판에 접근하기 위한 식별 보조 정보였으며 이를 소비자 인용 정정 결과로 산입하지 않는다.

후속 단계는 `future-sources.json`, `chains.json`, `upstream.json`, `future-search-log.jsonl`에 기록하여 본 `historical.json`, `sources.json`, `frame.json`, `search-log.jsonl`의 봉인 해시를 유지한다. 임시 tmux wiki bare clone은 고정판을 읽은 뒤 제거했다. 재개 시 `git clone --bare --filter=blob:none https://github.com/tmux/tmux.wiki.git` 후 sources.json H-W01–03의 SHA로 읽으면 된다.
