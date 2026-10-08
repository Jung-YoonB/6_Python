"""
## STEP 3 · 대여 기록 정제
`raw-rentals.csv` 를 정제합니다.

### 요구사항
- **`distance_km`, `fee`** — 콤마 제거 후 숫자로. 변환 실패는 결측으로
- **`rent_time`, `return_time`** — `datetime` 으로 통일 (형식 3종 혼재)
- **`payment_method`** — 공백 제거 후 대문자로 통일
- **중복 제거** — `rental_id` 기준


💡
**콤마를 먼저 지우세요**
`"12,345"` 를 그냥 `to_numeric` 에 넣으면 멀쩡한 값이 결측이 됩니다.

### 기대 결과
| 항목 | 값 |
| --- | --- |
| 중복 제거 후 행 수 | 14,500 |
| `distance_km` 결측 | 200 |
| `fee` 결측 | 0 |
| `payment_method` 고유값 | `['APP', 'CARD', 'MEMBERSHIP']` |
"""