"""Materialize the observed pre-outcome Homebrew ledger. No network or future inputs."""
from pathlib import Path
import json,datetime,hashlib
P=Path(__file__).parent
CHECK='2026-11-22T05:00:41Z'
cases=[
 dict(id='A-H01',repo='fish-shell/fish-shell',sha='efa9d5dd6a1a4f90e5a6d9372cddf539634be27e',date='2019-12-31T22:16:20Z',anchor=2019,path='CONTRIBUTING.md',line='L259–267',package='cppcheck',kind='installation_manual',purpose='fish C++ 소스의 정적 분석과 lint/lint-all 점검',version='미기재',callpath='build_tools/cppcheck.sh',callline='L1–3',call='cppcheck --enable=all --std=posix --quiet ./src/',intent='개발환경의 lint 도구. 역사 결과 재현 또는 항상 최신 안정판 사용이라는 별도 의도는 미기재.',sources=['H-S01','H-S02'],selection='본문 앞 iwyu는 jasonmp85 개인 tap, oclint는 oclint/formulae 별도 tap이므로 제외. 다음 공식 카탈로그 이름 cppcheck 선택.'),
 dict(id='A-H02',repo='kovidgoyal/kitty',sha='003f77b25733aee73981423e3464c59812558d2b',date='2019-12-29T16:33:08Z',anchor=2019,path='Brewfile',line='L1',package='pkg-config',kind='brewfile',purpose='kitty native code 빌드 때 libpng·harfbuzz 등의 컴파일/링크 플래그 조회',version='미기재',callpath='setup.py',callline='L45,L60–68,L260–275',call='PKGCONFIG 기본값 pkg-config; subprocess.check_output로 cflags/libs 조회',intent='소스 빌드용. docs/build.rst L62–68은 소스 app과 의존성을 포함한 배포 dmg를 구별. 특정 pkg-config 판의 역사 재현 요구는 미기재.',sources=['H-S03','H-S04','H-S05'],selection='Brewfile 첫 이름 pkg-config; 앞서 선택한 cppcheck와 다름.'),
 dict(id='A-H03',repo='neovim/neovim',sha='6fa0f303d7f0823bfc5ba6cc7b4e7a7cd76143ac',date='2023-12-31T14:10:53Z',anchor=2023,path='BUILD.md',line='L415–424',package='ninja',kind='installation_manual',purpose='Neovim을 병렬로 더 빨리 빌드하는 빌드 도구',version='미기재',callpath='Makefile',callline='L41–61,L93–108',call='ninja가 PATH에 있으면 CMAKE_GENERATOR=Ninja 및 BUILD_TOOL=ninja',intent='Ninja 설치를 개발 빌드 가속용으로 권장. BUILD L9의 stable은 Neovim checkout 선택이며 Ninja를 지금도 최신으로 유지하라는 말이 아니다.',sources=['H-S06','H-S07'],selection='2019·2021 CI 단독 Homebrew는 직접 연결한 설치 매뉴얼 부재로 제외. 2023 BUILD.md 첫 brew install 이름 ninja.'),
 dict(id='A-H04',repo='obsproject/obs-studio',sha='1dd96124e3504edf970ff17ac9dd1a08d335b2be',date='2021-12-31T06:32:24Z',anchor=2021,path='CI/scripts/macos/Brewfile',line='L2',package='cmake',kind='brewfile',purpose='OBS와 CEF의 macOS native 빌드 구성을 생성',version='Brewfile 미기재; 선택한 빌드 호출은 별도 최소판을 여기서 주장하지 않음',callpath='CI/full-build-macos.sh',callline='L7–13,L42,L130–146,L227–234,L276–284',call='brew bundle --file ${CI_SCRIPTS}/Brewfile 후 cmake 구성',intent='macOS 앱·패키지 생성용 개발/배포 스크립트. 소스의 구성 지시를 공개 배포 성공으로 취급하지 않음.',sources=['H-S08','H-S09'],selection='2019 단독 설치 CI는 제외. 2021의 실제 Brewfile에서 tap 선언을 건너뛰고 첫 brew 이름 cmake 선택; 개인 tap xcnotary는 대상 아님.'),
 dict(id='A-H05',repo='Genymobile/scrcpy',sha='83d48267a734e999fac0eccd93173b93019bf006',date='2019-12-19T10:52:09Z',anchor=2019,path='BUILD.md',line='L145–157',package='sdl2',kind='installation_manual',purpose='scrcpy native client의 SDL2 GUI/runtime 의존성',version='메이저 이름 sdl2; 설치 지시에서 세부 판 미기재',callpath='app/meson.build',callline='L26–34,L130–135',call="dependency('sdl2')를 scrcpy executable의 dependencies에 전달",intent='클라이언트 빌드·실행. BUILD가 시스템과 무관한 prebuilt server 대안을 설명하므로 서버 재현과 macOS 클라이언트 의존성을 혼동하지 않는다.',sources=['H-S10','H-S11'],selection='예비 wezterm·tmux에서 적격 참조 미확보 후 BUILD의 첫 공식 brew 이름 sdl2 선택.'),
 dict(id='A-H06',repo='qutebrowser/qutebrowser',sha='d38ade9ee9791bf01c7466458f3efbb4e298e93d',date='2019-12-31T15:55:22Z',anchor=2019,path='doc/install.asciidoc',line='L340–359',package='qt5',kind='installation_manual',purpose='소스/Python 패키지 qutebrowser의 Qt5·QtWebEngine GUI 기반',version='Qt5 계열; 정확한 Qt/PyQt 판 미기재',callpath='qutebrowser/browser/webengine/webenginetab.py',callline='L28–32',call='PyQt5.QtWebEngineWidgets에서 QWebEnginePage/QWebEngineScript import',intent='당시 macOS 수동 설치 지시. Qt5 C++ 라이브러리와 PyQt5 binding은 별도이므로 brew qt5만으로 모든 Python runtime가 충족된다고 보장하지 않는다.',sources=['H-S12','H-S13'],selection='앞선 cask의 자기 제품 qutebrowser는 제외. Manual Install/Homebrew 첫 공식 brew 이름 qt5 선택.')
]

def url(repo,sha,path):return f'https://github.com/{repo}/blob/{sha}/{path}'
historical=[]
for c in cases:
    historical.append({
      'reference_id':c['id'],'cohort':'A','ecosystem':'Homebrew','consumer_project':c['repo'],
      'source_kind':c['kind'],'snapshot_anchor':f"{c['anchor']}-12-31T23:59:59Z",'consumer_commit':c['sha'],'consumer_commit_date':c['date'],
      'consumer_path':c['path'],'consumer_fixed_url':url(c['repo'],c['sha'],c['path']),'citation_locator':c['line'],
      'original_reference':c['package'],'original_citation_url':None,'original_citation_url_note':'원문은 brew 패키지 이름을 명시한다. 특정 formula URL 자체를 붙인 것은 아니며 아래 catalog URL은 연구자가 정규화한 조회 주소다.',
      'researcher_catalog_url':f"https://formulae.brew.sh/formula/{c['package']}",'url_state_at_freeze':'미조회',
      'expected_function':c['purpose'],'allowed_version':c['version'],'intent':c['intent'],
      'same_revision_callsite_url':url(c['repo'],c['sha'],c['callpath']),'same_revision_callsite_locator':c['callline'],'same_revision_callsite_observation':c['call'],
      'source_vs_release':'공개 source snapshot; 이 판이 배포된 소비자 release와 동일한지는 봉인 단계에서 미확인',
      'selection_reason':c['selection'],'source_ids':c['sources'],'latest_version_intent':'미확인','historical_reproduction_intent':'미확인',
      'upstream_or_future_opened_before_freeze':False,'evidence_level':'D1 공개 지시 + D2 같은 판 호출부 정적 판독; 설치/빌드 실행 아님'
    })

source_details=[
 ('H-S01','A-H01','CONTRIBUTING.md','L20–27,L37–43,L259–267','공식 brew cppcheck 설치와 C++ lint 목적; 앞선 iwyu/oclint는 별도 tap.',True),
 ('H-S02','A-H01','build_tools/cppcheck.sh','L1–3','cppcheck CLI를 POSIX/std/all 설정으로 src에 호출.',False),
 ('H-S03','A-H02','Brewfile','L1–5','첫 brew 항목 pkg-config; 같은 환경에 imagemagick/harfbuzz/python/sphinx-doc.',True),
 ('H-S04','A-H02','docs/build.rst','Dependencies L15–33; source app vs dmg L55–68','pkg-config가 build-time dependency. source app 의존성과 배포 dmg의 포함 의존성을 구별.',False),
 ('H-S05','A-H02','setup.py','L45,L60–68,L260–275','pkg-config 실행파일 기본값과 실제 플래그 조회 호출.',False),
 ('H-S06','A-H03','BUILD.md','L4–22,L38–43,L415–424','Homebrew ninja 설치 및 자동 선택/빠른 개발 빌드라는 목적.',True),
 ('H-S07','A-H03','Makefile','L41–61,L93–108','PATH의 ninja를 탐지하고 실제 build tool로 사용.',False),
 ('H-S08','A-H04','CI/scripts/macos/Brewfile','L1–5','Brewfile 첫 공식 패키지는 cmake; 다른 개인 tap 이름과 구별.',True),
 ('H-S09','A-H04','CI/full-build-macos.sh','L7–13,L42,L130–146,L227–234,L276–284','Brewfile을 설치하고 CEF/OBS에 cmake 호출. 실행 성공 영수증은 아님.',False),
 ('H-S10','A-H05','BUILD.md','Requirements; Mac OS L145–157; Common steps L174–213','sdl2/ffmpeg runtime 설치, meson/ninja 빌드, 별도 서버 구성 선택.',True),
 ('H-S11','A-H05','app/meson.build','L26–34,L130–135','native client executable에 SDL2 dependency 전달.',False),
 ('H-S12','A-H06','doc/install.asciidoc','On macOS/Manual Install L340–359; tox system Qt L411–417','brew qt5와 pip3 qutebrowser 설치 안내, QtWebEngine 기본/QtWebKit 제한.',True),
 ('H-S13','A-H06','qutebrowser/browser/webengine/webenginetab.py','L28–32','PyQt5의 GUI/QtWebEngineWidgets import를 실제 호출부에서 확인.',False),
]
sources=[]
for sid,cid,path,loc,facts,count in source_details:
    c=next(c for c in cases if c['id']==cid)
    sources.append({'source_id':sid,'related_questions':['Q1','Q2'],'case_ids':[cid],
      'url':url(c['repo'],c['sha'],path),'retrieved_url':f"https://raw.githubusercontent.com/{c['repo']}/{c['sha']}/{path}",
      'publication_or_revision_date':c['date'],'date_role':'repository snapshot commit; not initial insertion or consumer release date','fixed_version':c['sha'],
      'checked_utc':CHECK,'checked_utc_note':'직접 첫 판독 뒤 2026-11-22T05:00:40–05:00:41Z에 같은 13원문을 connector로 재열람하여 확보됨을 확인',
      'read_location':loc,'confirmed_content':facts,'limits':'소스/문서 정적 판독. 이 참조의 현재 적합성·수정·배포·실제 실행/피해는 아직 조사하지 않음.',
      'producer':c['repo'],'lineage':f"consumer:{c['repo']}@{c['sha']}",'unique_original_group':f"consumer:{c['repo']}@{c['sha']}",
      'category':'historical','counted_original':count,'count_reason':'주 표본의 서로 다른 소비자 고정판 대표 1개' if count else '같은 소비자·같은 snapshot의 목적/호출 보조 파일; 동일 commit의 복수 파일로 최소수를 늘리지 않음',
      'evidence_type':'source/document observation','actual_execution':False})

snapshots={
 'alacritty/alacritty':[(2019,'77acb26d7328f678b26c8aff2ee5706d78949c44'),(2021,'e2b5219eb40eaf36d8255cd87c5202bbb8ba0825'),(2023,'659550ee34fe1b45ea176b88e60901d277d210a3')],
 'fish-shell/fish-shell':[(2019,'efa9d5dd6a1a4f90e5a6d9372cddf539634be27e')],
 'kovidgoyal/kitty':[(2019,'003f77b25733aee73981423e3464c59812558d2b')],
 'mpv-player/mpv':[(2019,'934f8e102682901d77e0990aa594f46d745e0396'),(2021,'f40d66f62454b66280a5a25c3f718fdafba860cf'),(2023,'abc2a7484dce9d043f20cee6c52cd6112af286d5')],
 'neovim/neovim':[(2019,'ac6ebfcc1db8daf30533c42d5c4246bb95ec3d85'),(2021,'6a932f68e6853e4fdcb49621fb1d89829a23238b'),(2023,'6fa0f303d7f0823bfc5ba6cc7b4e7a7cd76143ac')],
 'obsproject/obs-studio':[(2019,'e5871483abab2948dcda083a4ec6b4f72dcd9eff'),(2021,'1dd96124e3504edf970ff17ac9dd1a08d335b2be')],
 'wezterm/wezterm':[(2019,'364fc147bec73115605c835354a2b0f85d87b9ed'),(2021,'2b38c3dd32754373c5b8f894da661f4fee026854'),(2023,'ff2743748c238e5cdd6e7cb4ed19517d08dd511f')],
 'tmux/tmux':[(2019,'566ab9aa286f6d0468d2d5196367eb6d3c658270'),(2021,'080079c55a7f94af5ead4fad71ee2b33f54b154b'),(2023,'4266d3efc89cdf7d1af907677361caa24b58c9eb')],
 'Genymobile/scrcpy':[(2019,'83d48267a734e999fac0eccd93173b93019bf006')],
 'qutebrowser/qutebrowser':[(2019,'d38ade9ee9791bf01c7466458f3efbb4e298e93d')]
}
reasons={
 'alacritty/alacritty':'세 기준판 INSTALL.md의 macOS는 make app만 제시. 읽은 문서/ci/install/CONTRIBUTING에서 적격 brew 외부 도구 참조 미확보.',
 'mpv-player/mpv':'2019 .travis.yml의 Homebrew dependency는 존재하나 당시 매뉴얼이 그 파일을 설치 지시로 연결하지 않음. 2021/2023 README도 일반 waf/meson 지시만. 단독 CI를 매뉴얼로 확장하지 않고 제외.',
 'wezterm/wezterm':'2019/2021/2023 설치 source 매뉴얼이 get-deps를 연결하나 읽은 script에 brew 설치 지시 없음. macOS 다운로드 자체/자기제품 설치를 외부 도구 참조로 대체하지 않음.',
 'tmux/tmux':'README/.github README와 공식 Installing wiki 고정판에서 Homebrew 지시는 자기제품 tmux뿐. libevent/ncurses 수동 소스 빌드는 있으나 Homebrew 외부 의존성 지시 아님.'
}
frame=[]
for rank,(repo,ss) in enumerate(snapshots.items(),1):
    selected=next((c for c in cases if c['repo']==repo),None)
    for year,sha in ss:
      inc=selected is not None and selected['sha']==sha
      note=selected['selection'] if inc else reasons.get(repo,'더 이른 기준판에서 직접 연결된 설치 매뉴얼/Brewfile 적격 참조 미확보; 후속 기준년으로 진행')
      frame.append({'frame_id':f'H-F{rank:02d}-{year}','cohort':'A','ecosystem':'Homebrew','consumer_project':repo,'project_rank':rank,'anchor':f'{year}-12-31T23:59:59Z','snapshot_sha':sha,'status':'INCLUDED' if inc else 'EXCLUDED_AT_ANCHOR','reference_id':selected['id'] if inc else None,'reason':note,'outcome_known_at_selection':False,'project_reference_count':1 if inc else 0})

# Non-counted exploration sources: each directly inspected distinct file/edition is retained.
extras=[]
def extra(repo,sha,path,loc,facts,limit='적격 본표본으로 채택하지 않음. 현재/후속 이력 판단의 근거로 쓰지 않음.'):
 extras.append((repo,sha,path,loc,facts,limit))
for yr,sha in snapshots['alacritty/alacritty']:
 extra('alacritty/alacritty',sha,'INSTALL.md','Dependencies/macOS/Building','다른 OS에는 의존성 설치 명령이 있으나 macOS는 make app. brew 개발도구 참조를 확보하지 못함.')
extra('alacritty/alacritty',snapshots['alacritty/alacritty'][0][1],'CONTRIBUTING.md','Testing/style/release process','cargo test와 rustfmt 및 릴리스 절차. 외부 Homebrew 도구 지시 없음.')
extra('alacritty/alacritty',snapshots['alacritty/alacritty'][0][1],'ci/install.sh','전체 11행','선택한 탐색 패턴의 brew 설치 명령 없음.')
extra('alacritty/alacritty',snapshots['alacritty/alacritty'][0][1],'.travis.yml','L1–60','Rust/Linux/macOS CI 정의와 ci/install.sh 연결. brew 외부도구 설치 지시 없음; 암호화 배포 설정은 수집 요약에 보존하지 않음.')
extra('fish-shell/fish-shell',cases[0]['sha'],'README.md','Running/Building','fish 자체 brew 설치와 일반 CMake 빌드. 본 참조는 별도 CONTRIBUTING cppcheck에서 선택.')
extra('kovidgoyal/kitty',cases[1]['sha'],'INSTALL.md','전체 7행','별도 설치/빌드 안내 경로를 확인. 실질 목적은 docs/build.rst와 Brewfile에서 판독.')
for yr,sha in snapshots['mpv-player/mpv']:
 extra('mpv-player/mpv',sha,'README.md','Compilation','waf/meson 빌드 및 일반 의존성. 적격 Homebrew 설치 매뉴얼은 이 범위에서 확보되지 않음.')
for path,loc,facts in [('DOCS/waf-buildsystem.rst','L44–89','pkg-config 기반 feature 확인의 의미를 설명하지만 brew 설치 참조는 없음.'),('DOCS/contribute.md','Sending patches/developer policy','기여 지침이며 CI Homebrew dependency 파일로 직접 설치 안내를 연결하지 않음.'),('ci/build-macos.sh','L13–26','python3로 bootstrap/waf configure/build/install; brew 설치 지시 없음.'),('.travis.yml','L49–58,L78–91','Homebrew packages autoconf 등과 python link 존재. 단독 CI이므로 본표본에서 제외.')]:
 extra('mpv-player/mpv',snapshots['mpv-player/mpv'][0][1],path,loc,facts)
for yr,sha in snapshots['neovim/neovim'][:2]:
 extra('neovim/neovim',sha,'CONTRIBUTING.md','Developer guidelines/automated builds','ninja 권장과 CI 링크는 있으나 이 기준판 문서에서 Homebrew 설치 manifest 직접 연결 미확보.')
extra('neovim/neovim',snapshots['neovim/neovim'][0][1],'.travis.yml','L87–91','Homebrew ccache/ninja를 선언하나 매뉴얼 직접 연결 요건이 없어 제외. 기타 암호화 설정은 저장하지 않음.')
extra('neovim/neovim',snapshots['neovim/neovim'][0][1],'ci/before_install.sh','L49–60','별도 CMake 2.8.12 설치검사. Homebrew 소비자 인용으로 고르지 않음.')
for path,loc,facts in [('INSTALL','전체 1행','외부 wiki를 가리키는 설치 입구.'),('CONTRIBUTING.rst','L5–8','공식 설치 wiki 링크; CI/install-dependencies-osx.sh를 직접 설치 매뉴얼로 연결하지 않음.'),('CI/install-dependencies-osx.sh','L30–40','brew jack 등 실제 설치 명령은 있으나 2019 단독 CI이므로 제외.'),('plugins/CMakeLists.txt','L27–35','APPLE 분기에도 linux-jack이 포함되어 설치 목적 자체는 Linux 전용이라고 단정할 수 없음.'),('plugins/linux-jack/CMakeLists.txt','L8–32','Jack lookup와 target library 연결. 2019 CI를 본표본으로 승격하지 않음.')]:
 extra('obsproject/obs-studio',snapshots['obsproject/obs-studio'][0][1],path,loc,facts)
for yr,sha in snapshots['wezterm/wezterm']:
 path='docs/installation.markdown' if yr==2019 else ('docs/install/source.markdown' if yr==2021 else 'docs/install/source.md')
 extra('wezterm/wezterm',sha,path,'Installing from source','get-deps 및 cargo build를 직접 연결하나 brew는 확인되지 않음.')
 extra('wezterm/wezterm',sha,'get-deps','OS dependency branches','공식 당시 script에서 brew/Darwin 설치 분기를 확보하지 못함.')
extra('wezterm/wezterm',snapshots['wezterm/wezterm'][0][1],'README.md','Installation','공식 installation.html을 연결하여 동일 snapshot의 문서 소스를 읽음.')
extra('wezterm/wezterm',snapshots['wezterm/wezterm'][0][1],'CONTRIBUTING.md','L14–20','get-deps 설치 지침 기여를 연결.')
for yr,sha in snapshots['tmux/tmux']:
 extra('tmux/tmux',sha,'README','Dependencies/Installation','libevent/ncurses와 소스 빌드/설치. Homebrew 외부도구 설치 참조는 미확보.')
 extra('tmux/tmux',sha,'.github/README.md','Installation/From version control','공식 Installing wiki 및 일반 build tools. Homebrew 자기제품 외부 의존성 지시는 미확보.')
extra('qutebrowser/qutebrowser',cases[-1]['sha'],'requirements.txt','전체 의존성 목록','추가 Python requirements를 확인. qt5 시스템 설치와 PyQt binding 동등성을 단정하지 않음.')
for i,(repo,sha,path,loc,facts,limit) in enumerate(extras,14):
 sources.append({'source_id':f'H-S{i:02d}','related_questions':['Q1','Q2'],'case_ids':[],'url':url(repo,sha,path),'fixed_version':sha,'publication_or_revision_date':'고정 commit의 연말 기준판; snapshot 세부 날짜는 frame과 API 원장 참조','checked_utc':'2026-11-22T04:51:00Z/2026-11-22T05:00:20Z','checked_utc_note':'첫 판독 범위. 개별 HTTP receipt가 있는 URL은 retrieval-receipts.jsonl의 정확한 시각 우선. connector 탐색자료는 세션의 이 구간에서 읽음.','read_location':loc,'confirmed_content':facts,'limits':limit,'producer':repo,'lineage':f'consumer:{repo}@{sha}','unique_original_group':f'consumer:{repo}@{sha}','category':'exploration','counted_original':False,'count_reason':'표집 탈락/추가 확인 자료; 주 표본 원문 최소수 밖','evidence_type':'source/document observation'})
for i,(sha,date,loc,facts) in enumerate([
 ('44b9c9c14e135d6076f53a86f2b7d86b08879cb0','2019-12-13T12:30:30Z','tree listing','Installing.md 파일이 없음; 이 판에서는 그 페이지를 원문으로 열 수 없었다.'),
 ('0b5feb678dc588c38ccb6e19c8a1867ec159067c','2021-12-21T14:34:51Z','Installing.md 전체; Homebrew table/Building dependencies','Homebrew는 자기제품 tmux 설치만. 외부 의존성은 소스 빌드 설명.'),
 ('0a233ea2c07d10bca99f78db13977d19d67ca347','2023-12-15T10:41:59Z','Installing.md L11–17,L24–40,L163–171','Homebrew 자기제품 설치 유지, 외부 의존성의 brew 지시 없음.')],1):
 sources.append({'source_id':f'H-W{i:02d}','related_questions':['Q1'],'case_ids':[],'url':f'https://github.com/tmux/tmux/wiki/Installing/{sha}','fixed_version':sha,'publication_or_revision_date':date,'checked_utc':'2026-11-22T04:59:26Z/2026-11-22T05:00:20Z','read_location':loc,'confirmed_content':facts,'limits':'공식 wiki Git 이력을 읽은 범위. 2019에는 파일 부재이며 직접 원문 수에 넣지 않음. 현재 wiki 화면/후속 내용은 읽지 않음.','producer':'tmux/tmux.wiki','lineage':'same tmux consumer','category':'exploration','counted_original':False,'count_reason':'표집 탈락 근거','acquisition':'git clone --bare --filter=blob:none https://github.com/tmux/tmux.wiki.git; git log --until; git show fixed SHA:Installing.md'})

logs=[]
for f in frame:logs.append({'search_id':f['frame_id'],'search_utc':'2026-11-22T04:51:00Z/2026-11-22T05:00:20Z','query':f"GET https://api.github.com/repos/{f['consumer_project']}/commits?until={f['anchor']}&per_page=1; fixed tree paths; brew/install/build snippets",'period':f['anchor'],'host':'github.com/api.github.com/raw.githubusercontent.com','candidate':f['consumer_project'],'snapshot_sha':f['snapshot_sha'],'result':f['status'],'reason':f['reason'],'outcome_history_opened':False})
logs.extend([
 {'search_id':'H-ACCESS-01','query':'public API historical snapshots for wez/tmux/scrcpy/qutebrowser','search_utc':'2026-11-22T04:56:01Z','result':'HTTP503 via anonymous urllib; retried publicly via GitHub connector, succeeded','limitation':'HTTP fail is not source deletion; exact original dates from connector'},
 {'search_id':'H-IDENTITY-01','query':'wez/wezterm historical commit endpoint','search_utc':'2026-11-22T04:57:00Z/2026-11-22T04:57:42Z','result':'moved endpoint returned repository ID120568143; metadata resolves wezterm/wezterm. Only historical files subsequently read.','limitation':'current repository identity mapping, not future consumer citation outcome'},
 {'search_id':'H-WIKI-01','query':'official tmux wiki git log --until each anchor then fixed Installing.md','search_utc':'2026-11-22T04:58:00Z/2026-11-22T05:00:20Z','result':'2019 path absent; 2021/2023 only self-install brew tmux','limitation':'no outside Homebrew dependency ref qualifies'},
 {'search_id':'H-FREEZE-01','search_utc':CHECK,'result':'A-H01–06 all old refs and same revision callsites read; no supplier or consumer outcome history opened','phase':'pre-outcome','raw_metadata_note':'Reading later candidate anchors was only to find an eligible historical frame row, not to investigate corrections; for selected 2019 fish/kitty/scrcpy/qutebrowser no later consumer content was opened.'}
])
for name,data in [('historical.json',historical),('sources.json',sources),('frame.json',frame)]:
 (P/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(P/'search-log.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in logs))
print(json.dumps({'references':len(historical),'projects':len(set(x['consumer_project'] for x in historical)),'primary_historical_originals':sum(x['counted_original'] for x in sources),'source_rows':len(sources),'frame_rows':len(frame),'files_sha256':{n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in ['historical.json','sources.json','frame.json','search-log.jsonl']}},ensure_ascii=False,indent=2))
