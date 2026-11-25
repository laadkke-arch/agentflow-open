# 반례·정정 기록
- 전판: 6931ef06a34e4bffe7039b41eede778f3e470b43 predictions.csv, B P4 F,N,N. 원판 J04 L173–198: F.visible=true이면 100−10=90, 90>=90 유지, 95>=90 유지. 후판: F,F,F. 봉인 파일은 수정하지 않음. B′ 수정은 사후. T05/T06의 서로 다른 등호는 온도조절기 일반론으로 정밀 판정을 할 수 없다는 독립 반례.
- P1: C도 N으로 정확; 추가 분야 불필요한 사례. h=0은 네 경로 모두 최종 N, 전부 동률. unknown initial x=95는 두 상태 모두 가능; 앞에 80/120을 한 번 처리하면 상태가 고정된다.
- J01 nominal distance + hysteresis fraction + J02 zoom은 이미 유용한 지식. A+가 전환 규칙을 스스로 가설화하는 경우 B 순증분이 사라질 수 있음. 분리 맹검 필요.
- x=d/z; 동일 world d=95에서 z=1→.9→1→1.1→1, 초기 N, N,F,F,N,N. 원근/정사영 화면 높이 및 raycast의 raw distance(예 d80,z.8, update F, raw query N)와 구분. 정확한 visible flag에 외부 개입 시 _currentLevel과 분리될 수 있음.
- Unity E01/E02/E05의 거리/화면비 blend는 경계 안에선 두 렌더러를 사용하며 공간형 fade는 이전 상태가 필요하지 않을 수 있다. 시간형 fade는 진행시간을 기억하더라도 단일 임계 상태의 Schmitt 규칙과 다름. Godot E03/E04 fade와 renderer에 따라 margin 동작 변경.
- 실제 타 엔진 보고 D01 parent/child margin, D02 GPU Resident Drawer abrupt, D03 설정 보존, D04 shadow batching은 단순 hysteresis 하나로 해결되는 문제가 아니다. 모두 원당사자 보고/수정이며 이 과제에서 재현 안 함. 
- J08/J09 설계 변경은 Unreal/Unity/Blender 및 VR flicker 문제와 연결되어 있으나 온도조절기 직접 차용 문장 미확인. 역사 인과 주장 철회 상태. 시험 TODO는 정상 미구현 기대 항목이지 성공 영수증 아님.