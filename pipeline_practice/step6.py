"""
## STEP 6 · 결측 처리
### 요구사항
- **`fee` 결측** — 버리지 말고 복원하세요. `대여 시간(분) × 분당요금` 으로 계산할 수 있습니다
- **`distance_km` 결측** — 복원할 방법이 없으므로 해당 행을 제외

> 💡 **왜 요금은 복원하고 거리는 버립니까**
요금은 다른 컬럼으로부터 계산할 수 있지만, 이동 거리는 그럴 수 없기 때문입니다.
"채울 수 있는 근거가 있는가" 가 판단 기준입니다. 평균으로 때우는 것과는 다릅니다.

### 기대 결과
| 항목 | 값 |
| --- | --- |
| 요금 복원 | 0 건 |
| 거리 결측 제거 | 200 건 |
| 최종 행 수 | 13,501 |
"""
import pandas as pd

from step2 import bikes_raw, clean_bikes
from step3 import rentals_raw, clean_rentals
from step4 import stations, merge_all
from step5 import detect_outliers

# [1] 데이터 준비 ----------------------------------------------------------------------------------------
def handle_missing(df):
    """
    fee 결측은 복원, distance_km 결측은 제외하고 (결과, 요금 복원 건수, 거리 제거 건수) 반환
    Args:
        df : STEP 5 결과 (duration_min 열이 있어야 함)

    판단 기준 : "채울 수 있는 근거가 있는가"
        - fee         : 대여 시간(분) x 분당요금 으로 계산 가능 -> 복원
        - distance_km : 다른 열로 계산할 방법이 없음 -> 제외
    """
    df = df.copy()

    # [2] fee 결측 복원 ---------------------------------------------------------------------------------
    fee_na = df['fee'].isna()
    n_fee = int(fee_na.sum())

    # 결측이 있을 때만 복원 (현재 데이터는 0 건 -> 실행되지 않음)
    if n_fee > 0:
        # 분당요금 : 요금이 있는 행들의 (요금 / 대여시간) 중앙값
        per_min = (df['fee'] / df['duration_min']).median()

        # 결측인 행에만 값 넣기
        df.loc[fee_na, 'fee'] = (df.loc[fee_na, 'duration_min'] * per_min).round(0)

    # 요금은 정수(원) -> 결측이 없어진 뒤 int64 로
    df['fee'] = df['fee'].astype('int64')

    # [3] distance_km 결측 제외 -------------------------------------------------------------------------
    dist_na = df['distance_km'].isna()
    n_dist = int(dist_na.sum())

    # ~ (not) : 결측이 아닌 행만 남김
    df = df[~dist_na].reset_index(drop=True)

    return df, n_fee, n_dist

# [4] 검증 ----------------------------------------------------------------------------------------------
if __name__ == "__main__":
    pd.set_option("display.width", 140)

    rentals = clean_rentals(rentals_raw)
    bikes = clean_bikes(bikes_raw)
    df4, fail = merge_all(rentals, bikes, stations)
    df5, rules = detect_outliers(df4)

    df, n_fee, n_dist = handle_missing(df5)

    print("[결측 처리]")
    print(f"  - 요금 복원     : {n_fee} 건")
    print(f"  - 거리 결측 제거 : {n_dist} 건")
    print(f"[행 수] {len(df5):,} -> {len(df):,} ({len(df) - len(df5):+,} 행)")
    print()
    print("[남은 결측]")

    na = df.isna().sum()
    for col in df.columns:
        if na[col] > 0:
            print(f"  - {col:<18} : {na[col]:>4} 건")
    print("    => manufacture_year : STEP 2 에서 제조연도 불명 (분석에 안 쓰는 열이라 유지)")
    print("    => station_id, station_name, district : B043 (배치 대여소 없음) 대여 기록 (STEP 4 확인 문항 3)")
    print("-" * 100)

    checks = [
        ("요금 복원 0 건",          n_fee == 0),
        ("거리 결측 제거 200 건",    n_dist == 200),
        ("최종 행 수 13,501",       len(df) == 13501),
        ("fee 결측 0",              df['fee'].isna().sum() == 0),
        ("distance_km 결측 0",      df['distance_km'].isna().sum() == 0),
    ]

    print("[기대 결과 확인]")
    for name, ok in checks:
        print(f"  {'OK  ' if ok else 'FAIL'} {name}")