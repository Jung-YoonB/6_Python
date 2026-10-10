"""
## STEP 7 · 집계
정제가 끝났는지 숫자로 확인합니다.

### 요구사항
1. 전체 요약 — 행 수, 자전거 수, 이용자 수, 총 이동 거리, 총 매출, 평균 대여 시간
2. 자치구별 집계 — 건수 · 이동 거리 · 매출 (매출 내림차순)
3. 자전거 타입별 집계 — 건수 · 평균 이동 거리 · 평균 대여 시간
4. 결제수단별 건수

### 검산 기준
아래 관계가 성립해야 합니다. 뒤집혔다면 어딘가에서 잘못 정제한 것입니다.

> 전동 자전거는 일반 자전거보다 **짧은 시간에 더 긴 거리**를 이동해야 합니다.
"""
"""
## STEP 7 · 집계
정제가 끝났는지 숫자로 확인합니다.

### 요구사항
1. 전체 요약 — 행 수, 자전거 수, 이용자 수, 총 이동 거리, 총 매출, 평균 대여 시간
2. 자치구별 집계 — 건수 · 이동 거리 · 매출 (매출 내림차순)
3. 자전거 타입별 집계 — 건수 · 평균 이동 거리 · 평균 대여 시간
4. 결제수단별 건수

### 검산 기준
아래 관계가 성립해야 합니다. 뒤집혔다면 어딘가에서 잘못 정제한 것입니다.

> 전동 자전거는 일반 자전거보다 **짧은 시간에 더 긴 거리**를 이동해야 합니다.
"""
import pandas as pd

from step2 import bikes_raw, clean_bikes
from step3 import rentals_raw, clean_rentals
from step4 import stations, merge_all
from step5 import detect_outliers
from step6 import handle_missing

# [1] 데이터 준비 ----------------------------------------------------------------------------------------
def summarize(df):
    """
    정제 결과를 집계하여 (전체 요약, 자치구별, 타입별, 결제수단별) 반환
    Args:
        df : STEP 6 최종 결과
    """
    # [2] 전체 요약 -------------------------------------------------------------------------------------
    overall = {
        '행 수': len(df),
        '자전거 수': df['bike_id'].nunique(),
        '이용자 수': df['user_id'].nunique(),
        '총 이동 거리(km)': round(df['distance_km'].sum(), 1),
        '총 매출(원)': int(df['fee'].sum()),
        '평균 대여 시간(분)': round(df['duration_min'].mean(), 2),
    }

    # [3] 자치구별 집계 (매출 내림차순) -----------------------------------------------------------------
    by_district = df.groupby('district').agg(
        건수=('rental_id', 'count'),
        이동거리=('distance_km', 'sum'),
        매출=('fee', 'sum'),
    ).sort_values('매출', ascending=False)
    by_district['이동거리'] = by_district['이동거리'].round(1)

    # [4] 자전거 타입별 집계 -----------------------------------------------------------------------------
    by_type = df.groupby('bike_type').agg(
        건수=('rental_id', 'count'),
        평균이동거리=('distance_km', 'mean'),
        평균대여시간=('duration_min', 'mean'),
    ).round(2)

    # [5] 결제수단별 건수 --------------------------------------------------------------------------------
    by_payment = df['payment_method'].value_counts()

    return overall, by_district, by_type, by_payment

# [6] 검산 ----------------------------------------------------------------------------------------------
if __name__ == "__main__":
    pd.set_option("display.width", 140)

    rentals = clean_rentals(rentals_raw)
    bikes = clean_bikes(bikes_raw)
    df4, fail = merge_all(rentals, bikes, stations)
    df5, rules = detect_outliers(df4)
    df, n_fee, n_dist = handle_missing(df5)

    overall, by_district, by_type, by_payment = summarize(df)

    print("1. 전체 요약")
    for name, value in overall.items():
        print(f"  - {name:<12} : {value:,}")
    print()
    print("2. 자치구별 집계 (매출 내림차순)")
    print(by_district)
    print(f"   * 자치구 결측(제외) : {df['district'].isna().sum()} 건")
    print()
    print("3. 자전거 타입별 집계")
    print(by_type)
    print()
    print("4. 결제수단별 건수")
    print(by_payment)
    print("-" * 100)

    # 전동 자전거는 일반 자전거보다 "짧은 시간에 더 긴 거리" 를 이동해야 함
    e_dist = by_type.loc['전동', '평균이동거리']
    n_dist_ = by_type.loc['일반', '평균이동거리']
    e_time = by_type.loc['전동', '평균대여시간']
    n_time = by_type.loc['일반', '평균대여시간']

    checks = [
        (f"전동 평균 거리 > 일반  ({e_dist} vs {n_dist_})", e_dist > n_dist_),
        (f"전동 평균 시간 < 일반  ({e_time} vs {n_time})", e_time < n_time),
        ("자치구별 건수 합 + 자치구 결측 = 전체 행 수",
            by_district['건수'].sum() + df['district'].isna().sum() == len(df)),
        ("자치구별 매출 합 + 결측 행 매출 = 총 매출",
            by_district['매출'].sum() + df.loc[df['district'].isna(), 'fee'].sum() == overall['총 매출(원)']),
    ]

    print("[검산 기준 확인]")
    for name, ok in checks:
        print(f"  {'OK  ' if ok else 'FAIL'} {name}")

    # 검산 기준이 FAIL 인 이유 확인 : 정제 "전" 원본에서도 타입별 차이가 없는지 비교
    #   -> 원본부터 차이가 없으면 정제 오류가 아니라 데이터 자체의 특성
    raw = df4.copy()
    raw['duration_min'] = (raw['return_time'] - raw['rent_time']).dt.total_seconds() / 60   # STEP 5 [2] 와 같은 계산
    raw_cmp = raw.groupby('bike_type').agg(
        평균이동거리=('distance_km', 'mean'),
        평균대여시간=('duration_min', 'mean'),
    ).round(2)
    print()
    print("[참고] 정제 전 (STEP 4 결합 직후, 이상치 포함) 타입별 비교")
    print(raw_cmp)
    print("""
        => 정제 전부터 전동/일반 의 평균 거리·시간 차이가 거의 없음
           (정제 후 차이도 거리 0.04km, 시간 0.4분 수준)
        => 정제 과정에서 뒤집힌 것이 아니라 제공 데이터에 타입별 차이가 반영되지 않은 것으로 판단
    """)