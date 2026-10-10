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
import pandas as pd

from config import path, ENCODING

# [1] 원본 읽기 -----------------------------------------------------------------------------------------
rentals_raw = pd.read_csv(path('raw-rentals.csv'), encoding=ENCODING, dtype=str, keep_default_na=False)


def clean_rentals(df):
    """
    raw-rentals.csv 원본을 정제한 DataFrame 을 반환
    Args:
        df : dtype=str, keep_default_na=False 로 읽은 원본
    """
    rentals = df.copy()

    # [2] 공통 전처리 : 앞뒤 공백 제거 ------------------------------------------------------------------
    for col in rentals.columns:
        rentals[col] = rentals[col].str.strip()

    # [3] 컬럼별 정제 ---------------------------------------------------------------------------------------
    # [3-1] distance_km, fee
    for col in ['distance_km', 'fee']:
        rentals[col] = pd.to_numeric(
            rentals[col].str.replace(',', '', regex=False),
            errors='coerce'
        )

    # [3-2] rent_time, return_time
    for col in ['rent_time', 'return_time']:
        rentals[col] = pd.to_datetime(rentals[col], format='mixed', errors='coerce')

    # [3-3] payment_method
    rentals['payment_method'] = rentals['payment_method'].str.upper()

    # [4] 중복 제거 -----------------------------------------------------------------------------------------
    rentals = rentals.drop_duplicates(subset=['rental_id'], keep='first').reset_index(drop=True)

    return rentals


# [5] 검증 ----------------------------------------------------------------------------------------------
if __name__ == "__main__":
    pd.set_option("display.width", 140)

    rentals = clean_rentals(rentals_raw)

    print(f"[행 수] {len(rentals_raw):,} -> {len(rentals):,} ({len(rentals) - len(rentals_raw):+,} 행)")
    print()
    print("[정제 후 dtype]")
    print(rentals.dtypes.to_string())
    print()
    print(rentals.head())
    print("-" * 100)
    pay = sorted(rentals['payment_method'].unique().tolist())

    checks = [
        ("중복 제거 후 행 수 14,500", len(rentals) == 14500),
        ("distance_km 결측 200", rentals['distance_km'].isna().sum() == 200),
        ("fee 결측 0", rentals['fee'].isna().sum() == 0),
        ("payment_method ['APP', 'CARD', 'MEMBERSHIP']", pay == ['APP', 'CARD', 'MEMBERSHIP']),
        ("날짜 변환 실패 0", rentals[['rent_time', 'return_time']].isna().sum().sum() == 0),
        ("rental_id 중복 0", rentals['rental_id'].duplicated().sum() == 0),
    ]

    print("[기대 결과 확인]")
    for name, ok in checks:
        print(f"  {'OK  ' if ok else 'FAIL'} {name}")

    print()
    print("[실제 값]")
    print(f"  - 행 수               : {len(rentals):,}")
    print(f"  - distance_km 결측    : {rentals['distance_km'].isna().sum()}")
    print(f"  - fee 결측            : {rentals['fee'].isna().sum()}")
    print(f"  - payment_method 고유값 : {pay}")
    print(f"  - 대여 기간           : {rentals['rent_time'].min()} ~ {rentals['rent_time'].max()}")