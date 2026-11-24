# 본 48행의 1차 실행

입력 커밋 `89c07f5379a364ab443dccf8947db4bce180af46`에서 working tree clean을 확인한 뒤 시작했다. 설치 prefix에는 봉인한 package-lock과 파일 SHA를 사용했다. 도구가 새 프로세스를 만들기 전에 transport가 끊긴 호출은 프로세스·출력이 없음을 확인해 다시 시작했다.

```sh
node docs/workstreams/research/AF-RES-123/replay/drive.cjs --mode matrix --engine /tmp/af123-vendor --out /tmp/af123-primary.tDxbMl/main
python -B docs/workstreams/research/AF-RES-123/replay/analyze.py --main /tmp/af123-primary.tDxbMl/main --out /tmp/af123-primary.tDxbMl/analysis-main
```

driver 종료 0, stdout의 성공 입력 48/48, stderr 0바이트. 분석 종료 0, 원장의 본 시도 48행과 DOM/View callback 5,630행. `suite=matrix`의 모든 시도는 새 페이지·context를 사용했다. 편집 입력과 브라우저 읽기 모두 같은 Codex Cloud 작업자가 수행했다. [환경과 입력 지문](environment.json) · [stdout](stdout.txt) · [stderr](stderr.txt) · [종료값](exit.txt) · [한 실행의 원 이벤트](M-original-svg-empty-mark-1.json)
