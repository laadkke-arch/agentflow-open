# AF-RES-050 진행·커밋 원장

2026-11-23: 통합판522ea9092d4d56ef6db0bd4f707bfc90032e179e에서 새 작업 브랜치 생성. 필수 운영문서·배정표·034/046 고정 HANDOFF 직접 읽음. 요청한 session start --fetch exit0. 새 외부관측 전 SCOPE와 고정8군을 첫 묶음으로 봉인한다. 외부조사 분담은 NCQ/eXoaDocs, Blueprint/CodeMend, Unakite/Strata 세 갈래이며 root는 분야대조·측정방법·선택보강과 통합/검사를 맡는다. 각 분담은 자기 streams 경로만 쓰고 root가 커밋한다.

① 사전 규칙 원격 커밋: `f3c8de473b52a64c92c862cc64927ce787525c1a`. 외부 원자료 관측 전에 봉인. 로컬 git push는 인증정보 부재로 exit128이었으며, 승인된 GitHub 연결의 tree/commit/ref API로 같은 트리를 게시하고 fetch 후 동일성을 확인했다.

② 고정 입력·출처·기준선: 8군의 원 논문, 배정/종점/품질 정의와 탐색 경로를 보존한다. Blueprint browser 허용 차이와 eXoaDocs40분 상한은 원문 확인으로 기존 요약/초기 코딩을 정정했다. NCQ 보관 CSV의 P/T는 코드북 확인 전 조건으로 간주하지 않는다. 배당 수는 파일 수와 분리하며 현재 공개성에 따라 연구군을 탈락시키지 않는다. 후속 관측 감사·join·반례 파일은③에서 별도로 커밋한다. 이 묶음 SHA는 다음 묶음에 기록한다.

② 원격 커밋: `35576f16914c9f62b5c4d91bf015092b2e93aa34`.22파일. 최초 fetch가 FETCH_HEAD만 갱신하여 remote-tracking ref 검사는 exit1이었고, 명시적 refspec fetch 후 원격 tree와 index 일치/HEAD 전진을 확인했다.

③ 관측·연결·반례: NCQ142/156 snippet행, CodeMend361 IR행, Blueprint20그래프 위치, Strata6집계행을 원자료 종류별로 감사했다. 배정×시간×최종품질 person join의 행수는 미확인으로 두고, 새 성공 비교를 찾은 연구군은 관측0/8로 센다. 고유 실질1차자료25개를 열었지만 요구배당8/6/6/4는8/2/3/6, 충족슬롯17/24이므로 자료요건 부분 충족이다. 검색·판복제·동일repo구성파일·실패를 독립수에 넣지 않았다.
