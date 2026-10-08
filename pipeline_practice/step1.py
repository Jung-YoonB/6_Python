"""
## STEP 1 · 진단
정제하기 전에 **무엇이 얼마나 망가졌는지** 파악합니다.
세 파일을 읽고 아래를 확인해 표로 정리하세요.
- 각 파일의 행 수, 컬럼별 dtype
- 숫자여야 하는데 문자열로 읽힌 컬럼
- 컬럼별 결측 수와 비율
- `bike_id`, `rental_id` 의 중복 건수
- `bike_type`, `district`, `payment_method` 의 고유값 목록

💡
**참고**
`dtype=str, keep_default_na=False` 로 읽으면 파일에 적힌 그대로 볼 수 있습니다.
`read_csv` 는 `"N/A"` 를 자동으로 결측 처리하므로, 원본 상태를 보려면 이 옵션이 필요합니다.

### 확인 문항
1. `raw-bikes.csv` 는 55행인데 자전거는 몇 대입니까? 왜 다릅니까?
2. `bike_type` 의 고유값은 몇 종류입니까? 실제로는 몇 종류여야 합니까?
3. `distance_km` 을 숫자로 못 바꾸는 값에는 어떤 것들이 있습니까?
"""
import pandas as pd

from config import path, ENCODING

# [1] 원본 상태 읽기 ------------------------------------------------------------------------------------
stations_raw = pd.read_csv(path('stations.csv'), encoding=ENCODING, dtype=str, keep_default_na=False)
bikes_raw = pd.read_csv(path('raw-bikes.csv'), encoding=ENCODING, dtype=str, keep_default_na=False)
rentals_raw = pd.read_csv(path('raw-rentals.csv'), encoding=ENCODING, dtype=str, keep_default_na=False)

# [1-1] 원본 info 확인 ----------------------------------------------------------------------------------
print("[stations_raw INFO 확인]")
stations_raw.info()
print("-" * 100)

print("[bikes_raw INFO 확인]")
bikes_raw.info()
print("-" * 100)

print("[rentals_raw INFO 확인]")
rentals_raw.info()
print("-" * 100)


# [2] 기본 상태 읽기 ------------------------------------------------------------------------------------
stations = pd.read_csv(path('stations.csv'), encoding=ENCODING)
bikes = pd.read_csv(path('raw-bikes.csv'), encoding=ENCODING)
rentals = pd.read_csv(path('raw-rentals.csv'), encoding=ENCODING)

# [2-1] 기본 info 확인 ----------------------------------------------------------------------------------
print("[stations INFO 확인]")
stations.info()
print("-" * 100)

print("[bikes INFO 확인]")
bikes.info()
print("-" * 100)

print("[rentals INFO 확인]")
rentals.info()
print("-" * 100)

# [3] 비교 진단 -------------------------------------------------------------------------------------------
raw_dfs = {'stations': stations_raw, 'bikes': bikes_raw, 'rentals': rentals_raw}
nor_dfs = {'stations': stations, 'bikes': bikes, 'rentals': rentals}

print()
print("  >>  [진단 1] 각 파일의 행 수, 컬럼별 dtype * * * * * * * * * * * * * * * *")
for name, df in nor_dfs.items():
    print(f"<{name} 의 행 수 : {len(df)}>")
    print(df.dtypes.to_string())
    print()

print()
print("  >>  [진단 2] 숫자여야 하는데 문자열로 읽힌 컬럼 * * * * * * * * * * * * * *")
numeric_cols = {
    'bikes': ['gear_count', 'manufacture_year', 'daily_fee'],
    'rentals': ['distance_km', 'fee']
}

for name, cols in numeric_cols.items():
    df = nor_dfs[name]
    for col in cols:
        if not pd.api.types.is_numeric_dtype(df[col]):
            print(f"  - {name}.{col} : {df[col].dtype} -> 예시 값 {raw_dfs[name][col].unique()[:5].tolist()}")

print()
print("  >>  [진단 3] 컬럼별 결측 수와 비율 * * * * * * * * * * * * * * * * * * * *")
NA_LIKE = ['', 'N/A', '불명', ' ', '-']

for name, df in raw_dfs.items():
    na = df.isin(NA_LIKE).sum()
    ratio = na / len(df) * 100
    for col in df.columns:
        if na[col] > 0:
            print(f"  - {name}.{col} 결측 개수 : {na[col]:>4} 개 ({ratio[col]:.2f} %)")

print()
print("  >>  [진단 4] bike_id, rental_id 의 중복 건수 * * * * * * * * * * * * * * *")
ID_COLS = {
    'bikes': 'bike_id', 
    'rentals': 'rental_id'
}

for name, col in ID_COLS.items():
    df = raw_dfs[name]
    s = df[col]
    print(f"  - {name}.{col} : 전체 {len(s)} 행 / 고유값 {s.nunique()} 개 / 중복 {s.duplicated().sum()} 건")
    
    dup_rows = df[s.duplicated(keep=False)].sort_values(col)
    print(dup_rows.head(10))
    print()

print()
print("  >>  [진단 5] bike_type, district, payment_method 의 고유값 목록 * * * * * *")
UNIQUE_COLS = {
    'bikes': 'bike_type',
    'stations': 'district',
    'rentals': 'payment_method'
}
for name, col in UNIQUE_COLS.items():
    df = raw_dfs[name]
    s = df[col]
    print(f"  - {name}.{col} : ({s.nunique()} 종류) : {s.unique().tolist()}")


print("-" * 100)

# [4] 확인 문항 ------------------------------------------------------------------------------------------
print()
n_rows = len(bikes_raw)
n_bikes = bikes_raw['bike_id'].nunique()
n_dup = bikes_raw.duplicated().sum()

d = rentals_raw['distance_km']
print(d[pd.to_numeric(d, errors='coerce').isna()].value_counts())

print(f"""
1. `raw-bikes.csv` 는 55행인데 자전거는 몇 대입니까? 왜 다릅니까?
    - {n_rows} 행 중 자전거는 {n_bikes} 대
    - 모든 컬럼이 동일한 행이 {n_dup} 개 반복해서 들어가 있음 (완전 중복값)

2. `bike_type` 의 고유값은 몇 종류입니까? 실제로는 몇 종류여야 합니까?
    - 현재 : 6종류
    - 실제 : 2종류 (일반 / 전동)

3. `distance_km` 을 숫자로 못 바꾸는 값에는 어떤 것들이 있습니까?
    - N/A : 212 건
""")