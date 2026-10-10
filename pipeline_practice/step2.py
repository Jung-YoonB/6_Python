"""
## STEP 2 · 자전거 마스터 정제
`raw-bikes.csv` 를 정제합니다.

### 요구사항
- **`station_id`** — 대문자로 통일, 빈 값은 결측으로 처리
- **`bike_type`** — `일반` / `전동` 두 가지로 통일
- **`gear_count`** — 단위 문자를 제거하고 정수로
- **`daily_fee`** — 콤마 제거 후 정수로
- **`manufacture_year`** — 정수로 (변환 실패는 결측으로)
- **중복 제거** — `bike_id` 기준

💡
**전각 문자**
`unicodedata.normalize("NFKC", s)` 한 줄이면 전각 문자를 반각으로 통일할 수 있습니다.
전각 공백(`\u3000`)은 `strip()` 으로 지워지지 않으니 NFKC 를 먼저 적용하세요.

### 기대 결과
| 항목 | 값 |
| --- | --- |
| 행 수 | 50 |
| `bike_type` 고유값 | `['일반', '전동']` |
| `station_id` 고유값 | 25종 + 결측 1건 |
| `gear_count` 범위 | 3 ~ 7 |
| `daily_fee` 범위 | 1,000 ~ 2,000 |
"""
import unicodedata
import pandas as pd

from config import path, ENCODING

# [1] 원본 읽기 -----------------------------------------------------------------------------------------
bikes_raw = pd.read_csv(path('raw-bikes.csv'), encoding=ENCODING, dtype=str, keep_default_na=False)

def clean_bikes(df):
    """
    raw-bikes.csv 원본을 정제한 DataFrame 반환
    Args:
        df : dtype=str, keep_default_na=False 로 읽은 원본
    """
    # 원본을 건드리지 않도록 복사본으로 작업
    bikes = df.copy()

    # [2] 공통 전처리 : 전각 → 반각, 앞뒤 공백 제거 ------------------------------------------------------------
    for col in bikes.columns:
        bikes[col] = bikes[col].map(lambda s: unicodedata.normalize("NFKC", s)).str.strip()

    # [3] 컬럼별 정제 ---------------------------------------------------------------------------------------
    # [3-1] station_id
        # 's11' -> 'S11'
    bikes['station_id'] = bikes['station_id'].str.upper()
        # 빈 문자열('') -> 결측
    bikes.loc[bikes['station_id'] == '', 'station_id'] = pd.NA

    # [3-2] bike_type    
    bikes['bike_type'] = bikes['bike_type'].str.replace(' ', '', regex=False)
        # 다른 표기 -> 표준값 ('일반형' -> '일반', 'electric' -> '전동')
    TYPE_ALIAS = {
        '일반': ['일반형'],
        '전동': ['electric'],
    }

    for std, aliases in TYPE_ALIAS.items():
        bikes.loc[bikes['bike_type'].isin(aliases), 'bike_type'] = std
    
    # [3-3] gear_count
    bikes['gear_count'] = bikes['gear_count'].str.replace('단', '', regex=False).astype('int64')

    # [3-4] daily_fee
    bikes['daily_fee'] = bikes['daily_fee'].str.replace(',', '', regex=False).astype('int64')

    # [3-5] manufacture_year
    bikes['manufacture_year'] = pd.to_numeric(bikes['manufacture_year'], errors='coerce')

    # [4] 중복 제거 -----------------------------------------------------------------------------------------
    bikes = bikes.drop_duplicates(subset=['bike_id'], keep='first').reset_index(drop=True)

    # 데이터 반환
    return bikes

# [5] 검증 ----------------------------------------------------------------------------------------------
if __name__ == "__main__":
    n_raw = len(bikes_raw)
    bikes = clean_bikes(bikes_raw)
 
    print(f"[행 수] {n_raw} -> {len(bikes)} ({len(bikes) - n_raw:+} 행)")
    print()
    print("[정제 후 dtype]")
    print(bikes.dtypes.to_string())
    print()
    print(bikes.head())
    print("-" * 100)

    st = bikes['station_id']
    gear = bikes['gear_count']
    fee = bikes['daily_fee']
 
    checks = [
        ("행 수 50", len(bikes) == 50),
        ("bike_type 고유값 ['일반', '전동']", sorted(bikes['bike_type'].unique().tolist()) == ['일반', '전동']),
        ("station_id 25종 + 결측 1건", st.nunique() == 25 and st.isna().sum() == 1),
        ("gear_count 범위 3 ~ 7", gear.min() == 3 and gear.max() == 7),
        ("daily_fee 범위 1,000 ~ 2,000", fee.min() == 1000 and fee.max() == 2000),
        ("bike_id 중복 0", bikes['bike_id'].duplicated().sum() == 0),
    ]
 
    print("[기대 결과 확인]")
    for name, ok in checks:
        print(f"  {'OK  ' if ok else 'FAIL'} {name}")
 
    print()
    print("[실제 값]")
    # nunique() : 결측을 제외한 고유값 개수
    print(f"  - bike_type 고유값 : {sorted(bikes['bike_type'].unique().tolist())}")
    print(f"  - station_id      : {st.nunique()} 종 + 결측 {st.isna().sum()} 건")
    print(f"  - gear_count 범위 : {gear.min()} ~ {gear.max()}")
    print(f"  - daily_fee 범위  : {fee.min():,} ~ {fee.max():,}")
    print(f"  - manufacture_year 결측 : {bikes['manufacture_year'].isna().sum()} 건")   