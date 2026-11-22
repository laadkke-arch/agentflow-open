"""Render RESULT.md from the unified ledger plus scoped, source-linked interpretation."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    sources={x["source_id"]:x for x in json.loads((ROOT/"sources.json").read_text())}
    refs={x["reference_id"]:x for x in map(json.loads,(ROOT/"references.jsonl").read_text().splitlines())}
    totals=json.loads((ROOT/"evidence/counts.json").read_text())
    metrics=json.loads((ROOT/"evidence/retrieval-metrics.json").read_text())
    out=["# AF-RES-027 · 정정이 실제 소비자의 인용에 도달하는 시점",""]
    def link(sid,label=None):
        return "["+(label or sid)+"]("+sources[sid]["original_url"]+")"
    def url(label,u):return "["+label+"]("+u+")"
    def table(headers,rows):
        out.append("| "+" | ".join(headers)+" |");out.append("| "+" | ".join("---" for _ in headers)+" |")
        for row in rows:out.append("| "+" | ".join(str(c).replace("|","/").replace("\n"," ") for c in row)+" |")
        out.append("")
    # Four required tables appear immediately after the title, in the required order.
    desc={
      "A-H01":("fish 기여 C++ lint; cppcheck; 2019-12-31","2019 rules=yes "+link("H-U01")+" → 2026-01-11 rules OFF "+link("H-U15")+"; merge01-11과 실제 시행 미확인 구별",
        "같은2019판 --rule-file "+link("H-F02")+"; 2024-04-12 기여 문서 안내 삭제 "+link("H-C02")+"; 정정 배포 미확인","보류. 옛 호출↔현재 recipe 정적 불일치; 당시 오류·현재 fish 실행 실패·고의 고정은 미확인"),
      "A-H02":("kitty source 빌드의 compiler flags; pkg-config; 2019-12-29","0.29.2 recipe "+link("H-U02")+" → pkgconf2.3.0_1 alias "+link("BH-S01")+"; PR merge2024-11-12, 시행 미확인",
        "2024-11-23 직접 설치줄 삭제 "+link("H-C01")+"; v0.38.0 실제 source archive "+link("H-R02")+"; 최초 공개 시각은 미확인","보류. source archive 내용 반영은 확인; 실행명은 유지, CI 효과·첫 배포 지연 미확인"),
      "A-H03":("Neovim 빌드; ninja; 2023-12-31","과거 "+link("H-U03")+" / 현재 recipe "+link("H-U09")+"; 관련 이름·산출물 소실 사건 미관측",
        "2026-11-22 고정 BUILD.md "+link("H-F03")+"에 Ninja 유지; 수정·수정배포는 해당 없음","소스 역할 유지. Zig 추가가 Ninja 폐기는 아님; 실행 성공·고의 고정 미확인"),
      "A-H04":("OBS macOS CI 구성; cmake; 2021-12-31","3.22.1 "+link("H-U04")+" / 현재4.x "+link("H-U10")+"; major 증가만으로 해당 목적 실패 판정 안 함",
        "Brewfile 첫 이동 "+link("H-F04")+"; 다음 이동 "+link("H-C09")+"; 2023-07-17 새 경로/호출 "+link("H-F10")+" "+link("H-F13")+"; 배포 미확인","소스 역할 유지 판정은2023 확인판까지. 현재4.x로 옛 OBS가 빌드되는지는 미확인"),
      "A-H05":("scrcpy 렌더링/SDL2 API; sdl2; 2019-12-19","옛 recipe "+link("H-U05")+" → 2026-06-18 source에서 sdl2-compat 연결 "+link("H-U16")+"; merge06-19, 실제 시행 미확인",
        "소비자 SDL3 전환2026-01-06 "+link("H-C04")+"; v4.0 source2026-05-12 "+link("H-R03")+"; 둘 다 상류 교체 이전","보류. 다른 API·개발 목적의 선행 변화; 같은 정정의 음수 지연 아님. 옛판 호환층 실행 미확인"),
      "A-H06":("qutebrowser Qt5/PyQt WebEngine; qt5; 2019-12-31","2021-01-04 qt5→qt@5는 같은 Qt5 "+link("BH-S03")+"; 이후 qt→Qt6는 별도 "+link("BH-S14")+"; 실제 시행 미확인",
        "2020 qt로 이동 "+link("H-C05")+"; 2023-01 pyqt@5 수정 "+link("H-C06")+"; v2.5.3 이전 안내 "+link("H-F07")+" / v3.0.0 pyqt@6 "+link("H-F08"),
        "보류. alias 유지가 Qt5 목적엔 맞을 수 있음. 같은 pyqt@5 수정의 첫 배포·실제 피해 미확인"),
      "A-C01":("Dask Windows Python3.6 시험; python=3.6.*; 2019-12-28","해당 minor recipe "+link("C-F02")+"; win-64 3.6.10 artifact2020-03-05 "+link("C-F47")+"; 실제 solve 미확인",
        "AppVeyor→Actions/새 환경 경로 "+link("C-F08")+"; 365일 창 말3.6 유지 "+link("C-F09")+"; 창 뒤 지원정책 변경은 별도","소스 목적 유지. 옛minor 시험과 최신 Python 사용은 다른 요구; 역사 재현 의도는 미확인"),
      "A-C02":("JupyterLab 문서; sphinx>=1.8와 Python3.5; 2019-12-30","2.3.1→2.4.0 recipe "+link("C-F03")+" "+link("C-F37")+"; noarch upload2020-02-10 "+link("C-F48"),
        "conda→pip "+link("C-F10")+" → conda 재도입 "+link("C-F58")+"; 창 말 "+link("C-F11")+"; 실제 RTD 배포 미확인","소스 목적 유지. 같은 창 말 문자열만으로 중간 경로를 알 수 없음"),
      "A-C03":("napari Python3 CI의 개발 설치/시험; setuptools; 2019-12-30","42→44 후계 "+link("C-F65")+"; 플랫폼 upload2020-01-02 "+link("C-F66")+"; 뒤 Python2 제외 "+link("C-F36")+"는 다른 요구",
        "문서 작업과 전체 CI의 pip 이동을 분리 "+link("C-F12")+" "+link("C-F13")+"; 창 말 고정판 "+link("C-F67"),
        "소스 목적 유지. Python2 지원 중단만으로 Python3.6/3.7 실패를 채우지 않음"),
      "A-C04":("Pandas 개발·문서 환경; numpy>=1.15; 2019-12-31. 문서 호출 연결은 봉인 뒤 같은 SHA에서 보강","recipe 작성2020-06-20 "+link("C-F33")+"; PR merge07-16 "+link("C-F34")+"; Linux artifact07-16 "+link("C-F50")+"; 실제 실패 build 미확인",
        "07-16 문서 실패 직접 보고 "+link("C-F16")+" → 같은 날 상한 수정 "+link("C-F15")+" → rc0 "+link("C-F56")+" / 안정판 "+link("C-F19")+"; 실제 문서 서버 배포 미확인",
        "특정 문서 작업의 부적합 직접 보고. 모든 NumPy 사용 실패 아님. 임시 호환 pin; 실제 수정 효과·사람 오추천 피해 미확인"),
      "A-C05":("scikit-image Gaussian/ndimage; scipy>=1.8; 2023-12-22","옛 안정1.11.4에 이미 scipy/scipy-tests 다중 출력 "+link("C-F70")+"; 1.12 후계 "+link("C-F60")+" / artifact "+link("C-F51")+"; 정확 플랫폼 미확인",
        "뒤 최소판 상향 "+link("C-F42")+" "+link("C-F44")+"; 새 sparse-array 요구 "+link("C-F59")+"; 창 말 "+link("C-F45"),
        "보류. 옛 Gaussian 실패 증거 없음; 새 함수의 최소판 요구를 늦은 옛 정정으로 계산 안 함"),
      "A-C06":("Spyder macOS 파일 등록/시작; applaunchservices>=0.1.7; 2021-12-31","누락 의존성·OS metadata 수정 "+link("C-F38")+" "+link("C-F40")+"; 0.3.0 artifact05-24~29 "+link("C-F52"),
        "2022-04-29 시작 실패 보고 "+link("C-F28")+"가 상류 수정보다 앞섬; conda.txt→main.yml→macos.yml 뒤07-03 최소0.3 "+link("C-F25")+"; v5.3.2 "+link("C-F57"),
        "해당 환경의 부적합 직접 보고. 옛 범위도0.3허용; 최소판 수정일≠모든 사용자 정상화일. 유지관리 계보 겹침"),
      "B-H01":("A-H02와 같은 kitty 인용. pkg-config 공식 변경 원장에서 역추적","2019–2023 검색의 첫 적격 사건 미확보; 2024 PR194885 범위 밖 보조 "+link("BH-S01")+" "+link("BH-S04"),
        "A-H02 사슬 연결. source archive 내용은 확인, 첫 시행·효과는 미확인","A 중복1; A 비율·소비자·사건 수에 추가하지 않음"),
      "B-H02":("Borg source/pip 설치의 Python>=3.5; python3; 2019-12-23","2020 python 기본3.7→3.8 "+link("BH-S02")+"; PR의 merge workflow404·최초 배포 미확인",
        "2020 cask/formula 수정 "+link("BH-S08")+"와2021 FUSE 수정 "+link("BH-S09")+"은 다른 참조. 2021-07 고정판 python3 유지 "+link("BH-S10"),
        "python3 설치명·source 설치 목적 유지; 하한3.5→3.6이며 기본3.8은 두 범위에 포함. 실행 미확인. Tu불명이라 형식적365일 우측검열 아님"),
      "B-H03":("A-H06와 같은 qutebrowser 인용. qt 공식 관계 원장에서 역추적","qt@5 alias 사전 준비 PR68241 "+link("BH-S03")+" "+link("BH-S05")+"; Qt6 전환과 별도",
        "A-H06 사슬 연결. 당시 qt5→qt@5는 Qt5를 유지하나 현재 WebEngine 포장까지 자동 보장하지 않음","A 중복1; 같은 산출물 유지와 이후 다른 major를 분리"),
      "B-C01":("Xarray 문서 그림 생성; matplotlib=3.0.2; 2019-01-27","2019 root recipe명 정리 "+link("BC-S01")+"; 실제 출력명 유지 / Linux 메타패키지 upload01-30 "+link("BC-S02"),
        "첫 후속 "+link("BC-S04")+"; 문서 환경 개편에서 직접 참조 폐기 "+link("BC-S05")+"; 창 말 "+link("BC-S06"),
        "소비자 출력 목적 유지 근거. 2018 실제 분리나2020 다른 CI용도 전환을 이 정정으로 치환 안 함"),
      "B-C02":("Snakemake 설치·workflow 환경 생성 CLI; mamba; 2021-11-17","mamba/libmamba/libmambapy 분리 "+link("BC-S10")+"; 실제 CLI archive에 bin/mamba 유지 "+link("BC-S11"),
        "첫 후속 "+link("BC-S13")+"; 창 말 v7.18.2 "+link("BC-S14")+"; API 대안은 최초 관측부터libmambapy "+link("BC-S16"),
        "CLI 목적 유지. API 소비자 전환 존재/시점 미확인이라 좌측검열 산입 보류"),
      "B-C03":("QtPy 옛 Qt5.12 시험; qt 변수참조; 2022-05-31","qt를 qt-main+qt-webengine 메타패키지화 "+link("BC-S17")+"; 공지04-23과 Linux wrapper06-02 upload "+link("BC-S19")+" 분리",
        "Python3.11/Qt5.15의 별도 요구 R2 오류·우회 "+link("BC-S21")+" "+link("BC-S22")+" → 2023 수리 후 qt 복귀 "+link("BC-S26")+"; v2.3.1은 이미 복귀 "+link("BC-S27"),
        "원래R1은 보류. R2의 약5.47시간은 별도 후속 수리→source 수정만; A 또는 최초분리 지연에 합산 안 함")
    }
    order=[f"A-H{i:02d}" for i in range(1,7)]+[f"A-C{i:02d}" for i in range(1,7)]+[f"B-H{i:02d}" for i in range(1,4)]+[f"B-C{i:02d}" for i in range(1,4)]
    table(["참조 ID·A/B","소비자 옛 판·목적·인용 URL","상류 전후 판·시행 근거","소비자 확인·수정·배포 URL","용도 충족·의도적 고정·미확인"],
      [[rid+" · "+refs[rid]["sample"],desc[rid][0]+"; "+url("소비자 고정 원문",refs[rid]["consumer_file_url"]),*desc[rid][1:]] for rid in order])
    table(["생태계·모집 방식","소비자·참조·독립 사건 수","전후 사슬 완성·부분·무사건","유지·오류·보류","날짜 쌍·검열 수","관측 지연 범위"],[
      ["A Homebrew · 소비자 먼저 봉인","6프로젝트 /6참조 /4사건키","0/4/2","소스 유지2 / 확인 실행오류0 / 보류4","정식 Tu→Tc0; 적격 Tc→첫 배포0; R/L0/0","미확인. H02의22.4743일은 메타데이터 산술만"],
      ["A conda-forge · 소비자 먼저 봉인","6프로젝트 /6참조 /6사건키(일상 버전 후계 포함)","0/6/0; 이름·기능 손실 미관측도 포함","소스 유지3 / 특정용도 당사자 부적합 보고2 / 보류1","정식 Tu→Tc0; source판 출판2참조3쌍; R/L0/0","source edit→RC/안정판 76,027~1,004,454초; 실제 실행 적용 지연 미확인"],
      ["A 전체 · 원장 분모 유지","12프로젝트 /12참조 /10서로다른 상류사건키","0/10/2","5/2/5; 실제 사람 오추천 피해0확인·12미확인","정식 Tu→Tc0/12; source판 출판2참조3쌍; R/L0/0","전체 전파율·평균/중앙 지연 추정 안 함"],
      ["B Homebrew · 사전 공식 원장3회","3프로젝트 /3참조 /3사건키; A 중복2","0/3/0","1/0/2(원래 목적)","원래 사건 적격 지연0; R/L0/0","미확인; B-H01은2024 보조 확장"],
      ["B conda-forge · 사전 공식 원장3회","3프로젝트 /3참조 /3사건키; 별도 대안3건","0/3/0","2/0/1(원래 목적)","원래 사건 지연0; R2 보조 수리 source응답1·병합1·source출판1; 검열 산입0","R2만 upload→commit19,700.839초, →merge86,726.839초; commit→확인 source판6,487,807초"],
      ["B 전체 · 탐색 시도 분모","6시도 /6프로젝트 /6참조 /6사건키; A 중복2 제외 시 새참조4","0/6/0","3/0/3(원래 목적)","B 성공·지연을 A 분자에 더한 수0","A+B 중복제거 사건키14; 보조 수리/모든 버전변화의 총수 아님"]
    ])
    masks={
      "A-H01":("cppcheck라는 이름/주소","--rule-file와 recipe의 rules 지원","2024 기여 안내 삭제와2026 기능 삭제의 다른 시계",["H-F02","H-U15","H-U18","H-C02"],"옛 호출의 정적 검토에는 명령·판이 최소. 현재 수정 의무/실제 실패는 추가 정책·실행 필요"),
      "A-H02":("pkg-config 주소/이름; 실제 구현 미확인","compiler flags 호출이 계속 필요함","alias 구현 관계와 실제 archive 내용 반영; created/updated로 최초 배포는 못 정함",["H-S05","H-C01","H-R02","R-S01"],"호출 의미·의존성 공급경로 필요. 더 많은 역사도 사라진 CI 결과를 복원하지 못함"),
      "A-H03":("ninja 항목 존재","Ninja/CMake 빌드 역할","고정 후속판에서 역할 유지·무사건 관측 범위",["H-S07","H-U09","H-F03"],"이 좁은 기능명 구별에는 역할+같은 판 호출로 충분. 성공률 질문이면 로그가 더 필요"),
      "A-H04":("옛 경로만으로 이동 여부 불명","cmake 구성 역할","두 번 이동한 Brewfile과 같은 판 호출 연결",["H-F04","H-C09","H-F10","H-F13"],"소스 역할은 확인; 2023 뒤 배포·최신 CMake 호환은 미확인"),
      "A-H05":("sdl2 이름만으로 구현/ABI 불명","SDL2 API와 SDL3 API 구별","소비자 migration·release가 공급자 교체보다 앞섬",["H-S11","H-U17","H-C04","H-R03"],"API세대+소비자판이 최소. 호환층의 같은 동작은 실행 필요"),
      "A-H06":("toolkit·Python binding·WebEngine 혼동 가능","PyQt5.QtWebEngineWidgets의 기대 기능","main의 pyqt@5와 tag의 qt/pyqt@6 불일치",["H-S13","H-C06","H-F07","H-F08"],"기능·major·채널 역할을 저장. 같은 수정의 문서/nightly 배포가 추가 필요"),
      "A-C01":("기본 Python recipe로 오인 가능","Windows64/Python3.6 시험","AppVeyor→Actions, 창 뒤3.6 지원 종료",["C-S01","C-F02","C-F08","C-F09"],"minor·플랫폼·목적만으로 잘못된 기본branch 대체를 막음; 정확한 solve는 별도"),
      "A-C02":("sphinx 문자열 유지","Python 범위와 문서 entrypoint","conda→pip→conda의 숨은 중간 경로",["C-S02","C-F03","C-F10","C-F58"],"기능 정체성에는 L2가 가벼움. 전파 경로를 묻는 때만 이력이 필요"),
      "A-C03":("setuptools 이름 유지","Python3 빌드와 Python2 중단을 구별","문서 작업 변경과 전체 CI 이행을 구별",["C-S03","C-F12","C-F13","C-F36"],"Python 범위+build 호출이 반례 배제에 충분; 실제 설치판은 로그 필요"),
      "A-C04":("NumPy 주소·패키지명 존속; import 실행 미확인","warnings-as-errors 문서 목적에서 경고 실패","제안·merge·artifact·pin·RC·stable 시계 구별",["C-F53","C-F54","C-F16","C-F50","C-F56"],"같은 판 환경과 문서 호출은 필요. 정확한 artifact/최초 성공 로그는 끝내 추가 질문"),
      "A-C05":("scipy와 recipe root/시험 출력 혼동 가능","Gaussian/ndimage와 scipy-tests 구별","후속 sparse-array 사용의 다른 목적",["C-S16","C-F06","C-F44","C-F59"],"출력/모듈 정보면 정체성 구별 가능. 늦은 수정인지에는 목적 이력이 필요"),
      "A-C06":("noarch 라벨만으로 모든 OS 추론 위험","macOS 등록 목적·하한·의존성","conda.txt→main.yml→macos.yml→0.3하한·source판",["C-F32","C-F25","C-F40","C-F57"],"판·플랫폼으로 후보를 줄이되 실제 solve·GUI 효과는 별도; 옛 하한도 새판 허용")
    }
    rows=[]
    for rid in order[:12]:
        a,b,c,ids,limit=masks[rid];m=metrics["by_A_reference"][rid]
        rows.append([rid+" · "+refs[rid]["package"],a,b,c,"; ".join(link(i) for i in ids),
          limit+f"; 원장 URL{m['documented_unique_direct_read_urls']} /고정Git판{m['documented_distinct_fixed_git_revisions']} (비용·최소 읽기량 아님)"])
    rows += [
      ["B-C02 · CLI/API","mamba 한 이름으로는 역할 불명","CLI는 mamba, Python API는 libmambapy","선행 API 참조 미확인이라 전환도 미확인",link("BC-S11")+" "+link("BC-S12")+" "+link("BC-S16"),"같은 후계 추천을 두 목적에 일괄 적용하면 틀림. 역사 전환을 따지지 않을 때 역할이 가벼운 충분 정보"],
      ["X-LIB01 · 역사 주제/지역","현재 국가명만으로 좁은 후계 선택 위험","1938/1968의 전체 역사 영역과 서지 역할","지리 코드/국가명전거/주제전거 및 snapshot 날짜 역할 분리",link("X-S04")+" "+link("X-S05"),"e-cs 보존 조건을 확인. sh85035319→두n계열 ID 직접 split은 미확인; 생성 이력은 추가 필요"]
    ]
    table(["참조와 기대 기능","주소만으로 확인","판·용도로 추가 확인","이력·시점으로 추가 확인","최소 근거 URL","대가·반례·남은 질문"],rows)
    table(["Q 번호·주장·적용 범위","근거 원문 URL·정확한 절 또는 실행 영수증","확인한 내용·분자·분모","반례를 찾은 곳과 결과","미확인·판단을 바꿀 최소 자료"],[
      ["Q1 · 소비자 먼저 정한 목적표본","[SCOPE](SCOPE.md), [봉인](evidence/a-seal.json), [원격 영수증](evidence/commit-log.json), [frame](frame.csv)","A12/12프로젝트, 생태계6씩. B6의 A중복2. 고유 원문 최소수87=12옛A+37상류+30후속+4B옛판+4타분야","alacritty/mpv 등 날짜순 탈락 보존; 성공·변경 발견 뒤 A 교체0","대표성·통계적 독립 미확인. 독립 모집틀의 새 사전등록 표본이 있어야 전체 비율 판단 변경"],
      ["Q2 · 같은 파일의 같은 용도가 핵심",link("C-F53")+"의 ENV_FILE/Ubuntu docs/setup_env; "+link("C-F54")+"의 pin직전 호출; "+link("H-F02")+" lint.fish95–107","12/12 과거 목적·호출 자료. H01/C04/C06의 세부는 봉인 뒤 같은 옛SHA 보강으로 표시","SciPy의 뒤 sparse 사용 "+link("C-F59")+"을 옛 Gaussian과 구별; Python2 중단 "+link("C-F36")+"도 napari Python3 실패 아님","당시 solver와 실제 버전 미확인. 같은판 실행 로그/명시 목적 변경 문서 필요"],
      ["Q3 · 이름·출력·시행은 별도 필드",link("BH-S03")+" alias diff; "+link("H-U15")+" HAVE_RULES diff; "+link("C-F34")+" merge metadata; "+link("C-F50")+" upload records","A 상류사건키10(일상 후계 포함), 이름·출력 사건 미관측2. Homebrew 사건4의 실제 최초 시행일 미확인","같은 Qt5를 보존하는 alias와 같은 cppcheck명 아래 rules 소실을 대조; 2020-06 recipe를07-16배포로 오인하지 않음","정확한 formula API/bottle 최초 공급 영수증과 소비 artifact가 날짜를 바꿀 최소 자료"],
      ["Q4 · source·release·실행은 다른 도착점",link("H-C06")+" 수정 diff / "+link("H-F07")+" v2.5.3 안내; "+link("H-R02")+" 실제 archive; "+link("C-F25")+" macOS 하한","엄격한5시점 사슬 A0/12·B원사건0/6. 실제 archive 내용1건과 source판 포함은 별도 확인","qutebrowser 다음release에수정불포함; Dask/OBS/Spyder 경로 삭제가단순폐기아님","각 chains 행에 마지막판·다음불변판. 첫 문서/nightly/CI 적용 로그가 필요"],
      ["Q5 · 미변경을 오류로 일반화 못함",link("BC-S11")+" bin/mamba / "+link("BC-S12")+" CLI; "+link("BC-S26")+" qt복귀; "+link("BH-S08")+" Borg의다른참조수정","A 소스유지5/특정목적실패보고2/보류5. 의도적 역사재현 pin 확인0; 실제 사람 오추천 피해 확인0/12, 전부미확인","선택된 QtPy R1과 새R2를 분리; 새이름을 알고도 qt복귀; 옛범위>=0.1.7도0.3허용","정적/당사자보고와 실제 효과를 구별. 일치하는 릴리스·환경·전후 실행이 필요"],
      ["Q6 · 적격 끝점에서만 산술","[intervals](intervals.csv); "+link("C-F56")+" rc0 / "+link("C-F19")+" stable / "+link("C-F57")+" Spyder; "+link("R-S01")+" asset update79–104","정식 A Tu→Tc0; source edit→공개source판2참조3쌍. R/L검열0/0; BC-S16좌측검열산입보류","H02 created/updated는 첫배포구간 아님; C04약5.3h는 조건부; B-C03-R2만 별도source간격","패키지·판·기능·공급/배포 역할이 고정돼야 범위 축소. 누락은0일/무수정/검열로 치환 안 함"],
      ["Q7 · 옛 식별자가 정확할 수 있음",link("X-S01")+" Notice / "+link("X-S03")+" p5,p22; "+link("X-S04")+" CSB60pp2–4 / "+link("X-S05")+" MARC043·651·852·876","두 분야 각 상류1+소비자1=4고유원문. 실제 후속 인용·실제 소장기록. 날짜있는소비자수정사슬0","정정notice DOI로 연구DOI를대체하지않음; 역사범위e-cs유지. 주제/국가명전거/지리코드를직접split으로묶지않음","정정첨부PDF 두판 접근실패, subjectURI1993이전이력·최초snapshot배포미확인. 공공보존본·선행레코드필요"],
      ["Q8 · 가장 가벼운 충분 기록은 질문에 따라 다름","[verdicts](verdicts.csv), [재열람 지표](evidence/retrieval-metrics.json); "+link("BH-S11")+" installed_alias_path271–313","A12/12 L1/L2/L3 구조적 가림점검. 원장 직접판독 URL"+str(metrics["documented_unique_direct_read_urls"])+", 고정Git판"+str(metrics["documented_distinct_fixed_git_revisions"])+", root재열람영수증16","Ninja/CLI 역할 판정엔 L2가가벼움; H02·C04의 실제효과는 L3도로그없어불충분; 같은주소라도설치alias가다름","같은자료를본연구자의자기점검. 사람시간·전체전파율·저장비용·속도개선은측정/추정하지않음"]
    ])
    out += [
      "## 판독 요약과 수용 상태","",
      "**REVIEW_READY_WITH_GAPS.** 정한 모집틀과 원장은 조사했고, 직접 원문·반례·분모 조건을 충족했다. 그러나 상류의 정확한 최초 공급, 소비자가 실제 해결한 artifact, 동일 수정의 첫 실행·배포를 모두 고정한 사슬은 얻지 못했다. 이를 빠른 전파나 장기 미수정의 수치로 채우지 않았다. [수용 근거](evidence/acceptance-evidence.json)와 [자체 점검](SELF_CHECK.md)은 완료된 확인과 남은 확인을 별도 표시한다.","",
      "표1의 ‘인용 URL’은 그 참조가 실린 소비자 원문 URL이다. 이 표본의 직접 참조는 대부분 brew/conda의 **패키지명과 채널 문자열**이며, 개별 카탈로그 URL은 연구자가 정규화했다. 소비자가 원래 그 URL을 적었다고 하지 않는다. 고정 Git 원문 접근과 현재 카탈로그 HTML의 HTTP 상태도 독립 필드로 남겼다.","",
      "표2의 ‘사건’은 같은 공급자 편집/에피소드를 중복 제거한 키다. conda의 일상적인 버전 후계도 포함하므로, 오류 발생 사건이나 통계적으로 독립인 실험의 수가 아니다. B-C03의 추가 수리 R2, H06의 후속 Qt6 변경 등 해석용 사건을 사전 선택 사건 수에 다시 더하지 않았다. A의 12개 저장소도 독립 작성자 12명을 뜻하지 않는다. Spyder/applaunchservices의 유지관리 계보 겹침은 독립 뒷받침으로 세지 않았다.","",
      "‘유지’는 표시한 source 목적·출력 계약의 범위다. 실제 설치와 실행 성공을 확인했다는 뜻이 아니다. ‘부적합 보고2’는 Pandas 문서 빌드와 Spyder의 특정 시작/의존성 확인에 대한 당사자 원문이다. 실제 사람에게 잘못된 추천이 도달해 생긴 피해는 12행 모두 미확인이다. 따라서 2/12를 사람 피해율로 읽을 수 없다.","",
      "## Q1 · 결말을 보지 않고 확보한 참조와 분모","",
      "계획 기준 e2d0917ccd0e0010e14627a2f919265c332cec53과 실행 때 최초 확인한 foundation b420fb7e1e01f4a366512fa71c0f507051aa6a19를 구별했다. 입력은 지정된 AF-RES-023 결과 a9178ca95979564fd8801559d90d15db4ddac91b뿐이다. 023의18개주사건·지정교정사례·ROR현재4페이지는 신규 최소수에 넣지 않았다. [입력 교정](evidence/input-calibration.md)과 [제외 사건](evidence/excluded-prior-events.json)에 경계를 남겼다.","",
      "먼저 후보 프로젝트·호스트·2019→2021→2023 연말 앵커·파일/본문 순서·프로젝트 상한2·중복 규칙을 고정했다. 적격 참조가 없었던 앵커도 frame에 남겼고, 바뀐 패키지를 나중에 찾아 A에 보태지 않았다. 전체 A는 1714a55a529c7da42596ac0779d398f3aacf97c3에서 고정됐고 원격 재열람 뒤에만 미래 이력을 열었다. 불변 A 행과 수집 파일 해시는 최종 검산에서도 비교한다.","",
      "이 모집틀은 알려진 공개 개발 프로젝트를 고른 목적표집이다. 일반 설치·개발 도구를 재사용 가능한 소프트웨어 패키지로 해석해 런타임·빌드 도구·라이브러리를 포함했으며, CLI만의 표본이라고 하지 않는다. 전체 봉인·미래 이력 개방 전 해석 명확화는 [protocol-clarifications](evidence/protocol-clarifications.md)에 있다. 이름 자체가 도구인 경우와 라이브러리인 경우를 역할별로 읽어야 하며, 생태계 전체의 정정률로 외삽할 수 없다.","",
      "B는 pkg-config/python/qt 및 matplotlib/mamba/qt의 공식 원장6개를 먼저 정한 역추적 시도다. 발견된 성공뿐 아니라 무관한 수정·원문 실패·선행 참조 미확인도 결과다. B-H01/B-H03은 A-H02/A-H06와 같고, 나머지4개는 새 참고 참조다. 현재 알려진 성과로 A의 성공률을 늘리지 않았다.","",
      "## Q2 · 원래 요구를 한 줄보다 넓게, 같은 판에서 읽기","",
      "참조 줄만으로는 실행파일, 모듈, API세대, 문서 생성, 테스트 매트릭스를 구별할 수 없다. 같은 SHA에서 설치 파일과 호출부를 연결했다. 예를 들어 Dask의3.6.*는 Python 최신판을 요구하는 문구가 아니라 특정 Windows 시험 설정이다. qutebrowser의 Qt5는 C++ toolkit만이 아니라 PyQt5.QtWebEngineWidgets와 연결된다. source파일에 ‘stable’이 등장하더라도 그 말이 설치하는 모든 의존성의 현재 최신판을 뜻한다고 채우지 않았다.","",
      "Pandas는 특히 목적 보강을 명시했다. 봉인된2019판의 ENV_FILE=environment.yml, Ubuntu web_and_docs, setup_env의 conda 환경 생성, warnings-as-errors 문서 호출을 나중에 다시 읽었다(C-F53). 수정 직전2020 parent에도 같은 문서 호출 연결을 확인했다(C-F54). 그러나2019의 Python3.7과2020 parent의 Python=3은 다르다. 오래된 minor를 실패한2020 artifact에 대입할 수 없어, 보고가 있어도 정확한 공급→수정 지연은 보류했다.","",
      "H01의 --rule-file, C04의 문서 CI, C06의 macOS 등록 호출은 봉인 뒤 동일 옛 SHA에서 보강한 내용이다. 이를 최초 봉인 때부터 알았던 필드로 위장하지 않았다. 이후 쓰인 새 sparse-array 기능은 SciPy의 옛 Gaussian 호출과 합치지 않았다. 원래 목적과 다른 새 기능은 정정의 지연 끝점이 될 수 없다.","",
      "## Q3 · 공급자의 관계와 실제 공급 시각","",
      "이름 정리, 같은 산출물의 별칭, 버전 후계, CLI/라이브러리 분리, 구성요소 메타패키지, 기능 삭제와 구현 교체가 서로 달랐다. 사전 관계 enum에 기능 삭제·구현 교체가 없던 H01/H02/H05는 UNRESOLVED와 구체 relation_detail을 함께 남겼다. 이는 diff 자체가 미확인이라는 뜻이 아니라 사전 분류 어휘의 한계다. 보고서에서 확인된 기능 삭제를 일반적인 자료 부족과 섞지 않았다.","",
      "Qt alias 사례는 이름이 바뀌어도 같은 산출물을 보존하는 반례다. Jan4 PR은 Qt6 기본 전환 전에 외부 tap가 qt@5를 선택할 수 있도록 만들었다. 반대로 Cppcheck의 rules 옵션은 패키지명·일반 CLI가 남아도 없어졌다. 기대 명령 옵션을 저장하지 않으면 주소의 생존만으로 적합하다고 잘못 판단할 수 있다. 이 사실은 옛 fish 문서가2019년에 틀렸다는 증거가 아니다.","",
      "원고/recipe 작성, 제안, merge, bottle metadata, 패키지 업로드를 별도 열에 뒀다. NumPy1.19 recipe는6월20일에 작성됐지만, 해당 conda PR 병합과 보존된 Linux artifact 업로드는7월16일이다. Homebrew python PR은 merged_at=null이어도 실제 공개 sourcecommit과 merge-trigger comment가 있었다. 한 API 필드의 부재를 사건 부재로 바꾸지 않았다. 반대로 merge 시각만으로 사용자의 첫 공급을 확정하지 않았다.","",
      "Anaconda 자료는 현재 보존된 **특정 파일의** 업로드 시각과 의존성을 알려 준다. 선택 플랫폼·Python·build를 적었고, 모든 플랫폼의 최초 공개나 그 소비자가 실제 선택한 파일로 일반화하지 않았다. 전체 repodata의 과거 상태를 복원한 실험도 아니다.","",
      "## Q4 · 소비자까지 이어지는 경로와 끊긴 사슬","",
      "참조의 이동을 source파일, branch, release 내용, 공개 실행으로 나눴다. Dask의 AppVeyor 파일 삭제는 다른 CI환경으로 이어졌고, OBS Brewfile은 두 차례 이동했으며, Spyder 요구사항은 conda.txt→main.yml→macos.yml로 이어졌다. 파일 삭제 한 건으로 ‘참조 폐기’나 ‘미수정’을 결론 내리지 않았다.","",
      "소스 수정과 배포는 더 엄격하게 분리했다. qutebrowser의 main에 pyqt@5를 권한 커밋이 있어도 이후2.5.3/2.5.4 파일은 이전 안내였고,3.0.0은 pyqt@6였다. 따라서 다음 release날을 같은 수정의 배포일로 쓰지 않았다. QtPy에서도 우회 commit이 release ancestry에 포함됐지만 최종 tag 파일은 이미 qt로 복귀했다. ancestry 포함과 특정 상태의 실제 출판은 다르다.","",
      "kitty는 공식 source archive를 실제로 읽어 pkg-config 설치줄 삭제를 확인했다. 원본8,927,688바이트를 메모리에서 열었고 archive SHA256과 멤버 경로를 남겼다. 그러나 asset created_at/updated_at을 최초 공개 시각의 하한·상한으로 보장할 수 없다는 별도 판독을 수용했다. 수정된 source판의 존재는 확인됐지만 최초 배포 구간은 미확인이다. 배포된 바이너리의 CI 효과도 확인되지 않았다.","",
      "Homebrew 사건4개의 Tu가 고정되지 않아 형식적인 Tu+365일 창을 확정하지 못했다. 마지막 읽은 소비자판과 다음 필요한 불변판을 각 행에 적었다. conda 및 B의 날짜 있는 창은 특정 artifact 가용 시각을 기준으로 만들었으며, 정확한 소비자 노출을 뜻하지 않는다. 창 말 파일은 그때의 상태를 보여 줄 뿐 그 사이 내내 수정이 없었다는 독립 증거가 아니다.","",
      "## Q5 · 남아 있는 인용이 오류인 조건","",
      "실제 목적에 대한 부적합, 단순 버전 변화, 의도적인 옛판 시험, 소비자 목적의 변경을 가렸다. A에서 역사 결과 재현을 위해 옛 참조를 일부러 고정했다는 직접 명시는0건이다. 이0은 원문에서 그런 의도를 확인한 행이 없다는 뜻이며, 재현 목적이 존재하지 않는다는 뜻이 아니다. 버전 constraint나 immutable commit만으로 의도를 추정하지 않았다.","",
      "Pandas의 임시 상한은 문서 경고를 피하려는 호환 목적을 당사자가 설명한다. Spyder의 최소0.3 상향은0.3미만을 제외하지만 옛>=0.1.7도 이미0.3을 허용한다. 따라서 최소판 수정일이 모든 사용자의 최초 정상화 시각일 수 없다. 보고된 시작 오류는 상류의 새 수정 배포보다 먼저다. 공급자가 기존 문제를 고친 사건을 새 break 발생과 같은 시간 구조로 넣으면 해석이 틀어진다.","",
      "B의 Mamba에서는 CLI 패키지가 명령을 계속 제공하므로 Snakemake가 옛 이름을 쓰는 것이 계약상 맞는다. API 소비자에는 libmambapy가 필요하다. 다만 관측한 API 저장소가 처음부터 새 이름을 쓰므로, 실제 이전 참조나 전환이 있었는지는 미확인이다. 별도 판독 후 이를 좌측 검열로 세지 않았다. QtPy가 새 구성요소를 알고도 qt로 돌아간 사례는 ‘새 이름을 알면 반드시 옛 이름을 지워야 한다’는 규칙을 반박한다.","",
      "## Q6 · 계산 가능한 값과 계산하지 않은 값","",
      "원래 A12에서 실제 artifact·같은 기능·정정 끝점이 모두 고정된 Tu→Tc 지연은0건이다. 실제 실행·수정 효과까지 이어진 엄격한 완전 사슬도0건이다. 여섯 완전 사슬은 강화 목표였지만 채우지 못했다. 대신 실패한 사슬의 마지막 확인판·관측 범위·다음 첫 자료를 보존했으며, 미확인을 긍정 건수나 검열 관측으로 바꾸지 않았다.",""
    ]
    table(["적격한 산술의 범위","시작 → 끝","계산","이 값이 뜻하지 않는 것"],[
      ["A-C04 같은 수정의 source 후보판","2020-07-16 22:43:07 → 07-17 19:50:14 UTC","76,027초 = 약0.879942일","정확한 NumPy 노출→실패 해소 시간 또는 문서 서버 배포"],
      ["A-C04 같은 수정의 안정 source판","2020-07-16 22:43:07 → 07-28 13:44:01 UTC","1,004,454초 =11.625625일","RC와 별도 소비자1건 추가 또는 전체 전파율"],
      ["A-C06 같은 macOS 최소판의 source출판","2022-07-03 19:56:02 → 07-13 19:55:59 UTC","863,997초 =약9.999965일","macOS installer의 첫 공급/GUI 정상화"],
      ["B-C03-R2 후속 수리의 source응답","2023-01-12 15:27:37.161 → 20:55:58 UTC","19,700.839초 =약5.472455시간","2022 원사건/Qt5.12 목적의 지연 또는 A의 지연"],
      ["B-C03-R2 후속 수리의 branch통합","같은 upload → 2023-01-13 15:33:04 UTC","86,726.839초 =약24.090789시간","commit 작성 시각이나 최초 CI 적용 시각"],
      ["B-C03-R2 복귀 source판","2023-01-12 20:55:58 → 03-28 23:06:05 UTC","6,487,807초 =약75.090359일","우회 상태가 별도로 출판됐다는 뜻 또는 최초 CI 정상화"]
    ])
    out += [
      "H02의22.4743055556~22.4743287037일은 현재 asset의 created/updated 필드와 Tc 사이 산술로만 남겼다. 최초 배포 시각의 엄밀한 구간 관측에서 제외했다. C04의 약5.2733~5.3231시간도 초기 Linux CPython artifact들 중 하나를 실제 썼을 때의 조건부 metadata 차이이며 주 지연 분자에서 제외했다. 두 값은 intervals에서 eligible=false다.","",
      "형식적인 우측·좌측 검열 산입은 각각0이다. 수정 없이 끝난 오류라고 판정할 수 있는 시작 사건·종료 범위가 없으면 우측 검열이 아니다. 최초 코드가 새 API라는 이유만으로 존재가 확인되지 않은 이전 전환을 좌측 검열이라 할 수도 없다. reference 폐기, 목적 변화, 시작일 미확인, source 수정 후 실행 배포 미확인은 각각 다른 상태다.","",
      "## Q7 · 다른 분야의 옛 식별자와 보존 목적","",
      "PLOS 정정은2016-09-06 재발행을 명시하고 notice는10-21에 게시됐다(X-S01). 이후2018 PeerJ 논문은 기존 연구 DOI .0159614를 서지·본문에서 인용한다(X-S03). 연구 결과를 인용하는 독자에게 정정notice DOI .0165166로 연구 식별자를 덮어쓰는 것이 자동으로 더 정확한 것은 아니다. 이 후속 인용은 정정 후의 출판된 인용이지, 그 소비자가 notice를 읽고 인용을 수정한 날짜의 증거는 아니다. 정정 전·후 첨부 PDF는 접근하지 못해 정확한 제목 diff와 본문 byte 동일성은 미확인이다.","",
      "LC의1993 Bulletin은 새 국가명과 지리 코드, 역사 범위에서 옛 표목/코드를 계속 쓰는 조건을 구분한다(X-S04). Harvard의 실제 소장 레코드는1938/1968 Czechoslovakia에 관한 책에 e-cs와 역사 주제를 사용하며, WID 소장 필드도 있다(X-S05). 현재의 한 국가로 일괄 대체하면 이 책의 공간·시대 범위를 줄일 수 있다.","",
      "여기서 e-cs/e-xr/e-xo는 지리 코드이고, n90718759/n50075233은 국가명 전거이며, sh85035319는 소비자 레코드에 등장하는 주제 전거 URI다. sh URI가 두 n계열 ID로 직접 split됐다고 주장하지 않는다. sh URI의1993 이전 존재·변경은 미확인이다. 코드 시행일1993-05-24, MARC005의2002시각, 파일명20220215, 미러mtime2026-03-12도 서로 바꿀 수 없다. 확보한2,338바이트의 SHA256은 현 판을 다시 읽게 해 주지만 첫 공개일을 증명하지 않는다.","",
      "서지 사례에서는 동일 연구 DOI와 정정 공지 DOI의 역할을, 도서관 사례에서는 역사 지리 범위를 보존하는 조건을 확인했다. PLOS 소비자가 정정 전 과거판 자체를 보존하려 했다는 의도는 미확인이다. 현재 이름으로 일괄 치환하면 연구 대신 공지를 가리키거나 역사 영역을 좁힐 수 있다. 그러나 이 두 쌍만으로 학술·도서관 전체의 정정 전파 속도나 옛 ID 보존 관행 비율을 추정할 수 없다.","",
      "## Q8 · 재확인을 가능하게 하는 최소 기록","",
      "제품이 항상 모든 이력을 복사할 필요는 없다. 우선 원래 참조 문자열/채널, 소비자판·경로, 기대 명령/모듈/API세대/산출물, 허용판·플랫폼, 사용 목적을 연결해야 한다. 주소+기대 기능/판은 Ninja의 역할이나 mamba CLI/API 구별처럼 좁은 질문에 충분할 수 있다. 의미 있는 관계를 저장할 때에는 alias·버전 후계·component/메타패키지·기능 삭제와 식별자의 역할도 구별해야 한다.","",
      "‘언제 정정됐나’를 다시 묻는 경우에는 당시 원문과 출처 ID, 소비자 인용 시점, 공급자 변화의 전후 판, 제안/merge/배포의 날짜 역할, 소비자의 source 수정과 배포된 판의 실제 내용이 더 필요하다. Homebrew의 설치 alias를 기억하는 코드(BH-S11)는 같은 현재 formula로 해결돼도 설치에 사용한 이름이 이후 행동에 영향을 줄 수 있음을 보여 준다. 현재 URL 하나로 이 정보를 복원할 수 없다.","",
      "자료를 모두 붙여도 답할 수 없는 질문은 남는다. C04의 정확한 실패 artifact와 최초 성공 CI, H06의 같은 수정의 docs/nightly 배포, H02의 첫 공개 접근 가능 시각은 원문 이력이 부족하다. L3가 언제나 답을 준다는 결론은 이 자료와 맞지 않는다. 가벼운 충분 기록과 추가 원문이 필요한 경계를 함께 저장해야 한다.","",
      f"통합 원장에는 직접 판독 URL {metrics['documented_unique_direct_read_urls']}개와 서로 다른 고정 Git판 {metrics['documented_distinct_fixed_git_revisions']}개가 명시돼 있다. source행348개와 최소수에 산입한87개는 다른 수다. 동일 commit의 여러 호출 파일·diff/PR/API 렌더링은 최소수에서 중복 배제했고, 실제 관련 URL은 재열람 목록에 보존했다. root의 별도 재열람 영수증16개와 내부 판독문도 남겼다. URL/판 수는 이번 기록의 양이지 최소 읽기량·실제 클릭 수·사람이 소요한 시간·운영 저장비용·효율 향상의 측정값이 아니다.","",
      "## 적용 대안과 조건",""
    ]
    table(["행동 대안","적용할 조건","이 자료가 요구하는 확인"],[
      ["옛 참조를 유지","역사 범위/과거판 자체를 가리키거나 현재 목적이 기존 alias/output으로 충족됨","X-LIB01의시대·서지역할, B-C02의CLI계약. 고의 역사보존 의도는 별도 원문 필요"],
      ["같은 역할의 새 이름/버전으로 수정","같은 소비자 목적에 부적합이 있고 후계의 기능/판·플랫폼이 맞음","C04의문서호출·보고·상한, C06의macOS최소판. 새 이름 자체를 성공 근거로 쓰지 않음"],
      ["목적을 나눠 참조를 병기","API세대·CLI/library·역사/현재 목적에 서로 다른 답이 필요","Mamba두역할, SDL2재현/SDL3개발, QtPyR1/R2. 한 successor로 덮어쓰지 않음"],
      ["소스 수정과 배포 상태를 별도로 표시","commit은 있지만 일치하는 출판판/실행이 없거나 서로 다름","H06의main과release, H02의archive내용/메타데이터시각. 배포 미확인을 오류0건으로 바꾸지 않음"],
      ["판정을 보류하고 다음 원문을 지정","용도·실제 artifact·배포/실행·이전참조가 불명","chains의 next_immutable_input을 재개 입력으로 사용. 운영 전체 전파율은 산출하지 않음"]
    ])
    out += [
      "## 검토·재현과 진행 담당 제안","",
      "수집자 자체 점검과 별도 내부 판독을 구분했다. 같은 모델 계열의 다른 수집자가 Homebrew/Borg, conda 날짜·목적, B/타 분야를 다시 읽었고, 핵심 지적을 수용했다. H02 최초 배포 구간을 제외하고, C06 metadata 보장 표현을 좁히고, BC-S16의 추정 좌측검열을 제거했으며, 도서관 식별자 namespace를 분리했다. 외부 사람의 독립 검토나 실행 재현으로 표현하지 않는다. [별도 판독1](evidence/independent-read-review.md), [판독2](evidence/independent-conda-review.md), [판독3](evidence/independent-b-cross-review.md), [별도 원장 검산](evidence/independent-ledger-check.json)은 47개 조건과 후속 변경7개 조건을 통과했다. 최종 문장 검토에서 드러난 근거 ID 연결·가림 단계·표현 범위는 [해소 기록](evidence/review-resolutions.json)에 남겼다. [문장 감사](evidence/final-report-review.md)와 [Homebrew 내용 QA](evidence/final-homebrew-report-review.md)의 지적은 각 검토판에 대한 기록이므로 해소 기록과 함께 읽는다.","",
      "모든 필수 원장은 소유 경로 아래에 있다. [references](references.jsonl)는 불변 A행과 B참조, [upstream](upstream.csv)은 관계·날짜 역할, [chains](chains.csv)는 다섯 시점·창·다음 원문, [verdicts](verdicts.csv)는 목적·반대 설명·필드 가림, [intervals](intervals.csv)는 계산 자격과 범위를 담는다. [examples](examples.md)는 강한 사슬과 끊긴 사슬을 원문 링크로 펼쳐 읽는 경로다. 기계 판독용 전체 수집 내용은 각 collector와 evidence/consolidated-cases.json에 남겼다.","",
      "다음 명령은 원장 재생성과 정합성 검사다. 이는 역사적 소프트웨어 설치·macOS GUI 실행·CI 성공 검사가 아니다.","",
      chr(96)*3+"bash",
      "PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-027/scripts/append_b.py",
      "PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-027/scripts/consolidate_sources.py",
      "PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-027/scripts/build_ledgers.py",
      "PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-027/scripts/build_report.py",
      "PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-027/scripts/validate.py",
      chr(96)*3,"",
      "진행 담당에게는 AF-RES-027을 REVIEW_READY_WITH_GAPS로 색인하고, ‘원장 조건 충족 / A12·B6 / 보수적 직접 원문87 / 엄격 전파 사슬0 / source출판2참조3쌍 / 실제 사람 피해미확인’을 구별해 반영할 것을 제안한다. 공통 STATE·계약·dot-control·색인은 직접 고치지 않았다. HANDOFF에는 고정 결과 커밋 확인법과 실행하지 못한 검사의 입력·명령을 적는다.",""
    ]
    table(["중요한 불일치·약점","근거 ID·URL","영향을 받는 결정","다음 조사 질문·찾을 자료·최소 확인"],[
      ["공급 artifact와 실제 실패/성공 환경이 연결되지 않아 A의 엄격 지연이0건이다.",link("C-F50")+" "+link("C-F54")+" "+link("C-F16"),"NumPy 제안일부터 늦게 고쳤다는 판단, 당일 약5.3h 전파 주장, 실제 수정 효과","Pandas2020-07-16 web_and_docs의 보존 로그1쌍을 찾아 conda explicit URL/Python minor와 pin 전 실패·pin 후 첫 성공을 같은 목적에서 고정한다."],
      ["소스 수정·source판 존재와 같은 수정의 최초 실제 배포가 다르다.",link("H-C06")+" "+link("H-F07")+" "+link("H-F08")+"; "+link("H-R02")+" "+link("R-S01"),"commit→첫배포 지연·배포 성공률; H02자산메타데이터와 H06다른Qt계열릴리스의 대체 사용","qutebrowser7b53f648의 첫 docs/nightly artifact 또는 배포 로그1건을 찾아 pyqt@5 문구 자체·공개시각을 확인한다. 다른pyqt@6판은 대체하지 않는다."],
      ["도서관의 옛 역할 보존은 보이지만 subject ID의 전후 계보·snapshot 최초 공개일은 미확인이다.",link("X-S04")+" "+link("X-S05")+" "+link("X-S12"),"sh계열이 n계열로 직접 분리됐다는 주장과1993→2022 전파 지연 계산","동일Harvard001의 이전 불변 export1판과 원 배포 영수증을 확보해651/043/소장필드 변화·ID종류·실제 판 공개일을 구별한다."]
    ])
    (ROOT/"RESULT.md").write_text("\n".join(out).rstrip()+"\n")
    print(json.dumps({"result_lines":len(out),"table1_rows":len(order),"table3_rows":len(rows),"last_table_data_rows":3,"source_originals":totals["conservative_unique_originals"]}))
if __name__=="__main__":main()
