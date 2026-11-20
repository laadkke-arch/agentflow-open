# AF-RES-014 남은 확인

연구 보고서 커밋은 `d4364cff82c41d2f00e31abbba6231ba29423de5`다. 동결 61개 요약과 485개 자료의 BM25·LSA·RRF, 풀링, 내부 별도 판정과 재현 검사를 완료했다. [RESULT.md](RESULT.md)와 [검증 기록](VERIFICATION.json)이 재개의 기준이다. 현재 브랜치의 실제 HEAD와 HANDOFF 커밋은 원격에서 읽는다.

남은 첫 행동은 허용된 실행 환경에서 다음 표준 요청의 응답을 확인하는 것이다.

```sh
curl -fsSIL --max-time 20 https://huggingface.co/intfloat/multilingual-e5-small/resolve/0a1c1d9ee03224db176563ffcfbc3bbc38f35266/model.safetensors
```

현재 환경은 이 요청과 Hugging Face config, ModelScope 모델 URL에 프록시 CONNECT 403을 반환했다. 접근이 허용되면 [VERIFICATION.json](VERIFICATION.json)의 `resume_e5` 명령을 사용해 고정 자료와 61개 해시의 E5 순위를 별도 출력 디렉터리에 만든다. 새 상위 10 후보와 T002·T044의 근접 오답을 먼저 대조한다.

최초판 회복을 별도로 검증할 때는 현재 브랜치를 복제하고 소유 폴더에서 `PYTHONDONTWRITEBYTECODE=1 python -m queries.generate --write-metadata`를 실행한다. 입력은 AF-RES-011 `478c301b693896e2c6d777f46ac441f071bfdfe8`의 CASES다. Stack Exchange 본문과 revisions를 확인하여 요약과 동일 질문으로 짝짓고 기존 고정 결과와 구분한다.
