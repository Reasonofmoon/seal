# S6 — Vein (봉인 전이만 학습)

## 정복 대상
App Factory `hebbian_engine`이 **모듈 프롬프트 체인**에 가중치를 쌓던 방식.

생성·모듈 실행은 Vein을 움직이지 않는다. **봉인(seal) 성공**과 **락 실패(strike fail)**만 엣지를 갱신한다.

## 모델
- 엣지: `from_gap=>to_gap` (루트는 `:start`)
- 성공: `w ← w + 0.25·(1−w)` , parents = requires ∩ sealed (없으면 이전 sealed, 없으면 `:start`)
- 실패: 기존 엣지만 `w ← w·0.85`
- `seal next`: open + unblocked gaps를 부모→자식 weight로 순위

## CLI
```bash
python3 src/seal/cli.py next --graph PATH
python3 src/seal/cli.py vein --graph PATH
python3 src/seal/cli.py status --graph PATH   # includes "next"
```

## 커널 위치
- `src/seal/vein.py`
- `try_seal` 성공 → `record_success` / lock_failed → `record_fail`
