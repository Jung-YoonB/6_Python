"""
## STEP 4 · 결합
대여 기록에 자전거 정보와 대여소명·자치구를 붙입니다.
```
rentals ─(bike_id)→ bikes ─(station_id)→ stations
```

### 요구사항
- `how`, `validate` 를 명시할 것
- **`indicator=True` 로 매칭 실패를 확인**하고, 몇 건이 왜 실패했는지 설명할 것
- 매칭 실패한 행은 제외하고 진행

⚠️
**행 수가 늘어나면 안 됩니다**
결합 전후 행 수를 반드시 비교하세요.
늘어났다면 오른쪽 테이블에 중복이 남아 있다는 뜻입니다. STEP 2 로 돌아가세요.

### 확인 문항
1. 매칭에 실패한 `bike_id` 는 무엇입니까? 몇 건입니까?
2. 이런 데이터를 실무에서는 무엇이라고 부릅니까? 어떻게 처리해야 합니까?
3. 자치구명이 결측인 행이 있습니다. 원인은 무엇입니까?

### 기대 결과
| 항목 | 값 |
| --- | --- |
| 결합 후 행 수 | 14,500 (변화 없음) |
| 매칭 실패 | 80 건 |
| 제외 후 행 수 | 14,500 |
| 자치구 결측 | 304 |
"""
import pandas as pd

from config import path, ENCODING
from step2 import bikes_raw, clean_bikes
from step3 import rentals_raw, clean_rentals

# [1] 데이터 준비 ----------------------------------------------------------------------------------------
stations = pd.read_csv(path('stations.csv'), encoding=ENCODING)


def merge_all(rentals, bikes, stations):
    """
    대여 기록 + 자전거 + 대여소를 결합하여 (결합 결과, 매칭 실패 행) 반환
    Args:
        rentals  : STEP 3 정제 결과
        bikes    : STEP 2 정제 결과
        stations : stations.csv
    """
    # [2] rentals + bikes (bike_id) --------------------------------------------------------------------
    df = rentals.merge(bikes, on='bike_id', how='left', validate='many_to_one', indicator=True)

    # [3] 매칭 실패 확인 -> 제외 --------------------------------------------------------------------------
    fail = df[df['_merge'] == 'left_only']
    df = df[df['_merge'] == 'both'].drop(columns=['_merge'])

    # 결합 후 타입 되돌리기
    for col in ['gear_count', 'daily_fee']:
        df[col] = df[col].astype('int64')

    # [4] + stations (station_id) ----------------------------------------------------------------------
    df = df.merge(stations, on='station_id', how='left', validate='many_to_one')

    return df.reset_index(drop=True), fail

# [5] 확인 문항 -----------------------------------------------------------------------------------------
if __name__ == "__main__":
    pd.set_option("display.width", 140)

    rentals = clean_rentals(rentals_raw)
    bikes = clean_bikes(bikes_raw)
    df, fail = merge_all(rentals, bikes, stations)

    # 결합 후 행 수 = 성공 + 실패 (실패 행을 빼기 "전")
    n_merged = len(df) + len(fail)

    print("[결합 전후 행 수]")
    print(f"  - 결합 전 (rentals)  : {len(rentals):,}")
    print(f"  - 결합 후            : {n_merged:,} ({n_merged - len(rentals):+,})")
    print(f"  - 매칭 실패          : {len(fail):,}")
    print(f"  - 제외 후            : {len(df):,}")
    print()
    print(df.head())
    print("-" * 100)

    # value_counts() : 실패한 bike_id 별 건수
    fail_ids = fail['bike_id'].value_counts()

    # 자치구 결측 행의 원인 찾기 : 결측 행들의 bike_id, station_id 확인
    no_district = df[df['district'].isna()]

    print("[확인 문항]")
    print(f"""
    1. 매칭에 실패한 bike_id 는 무엇입니까? 몇 건입니까?
        - {fail_ids.to_dict()} -> 총 {len(fail)} 건
        - 대여 기록에는 있지만 자전거 마스터(raw-bikes.csv)에 없는 자전거

    2. 이런 데이터를 실무에서는 무엇이라고 부릅니까? 어떻게 처리해야 합니까?
        - 고아 레코드(Orphan Record) : 참조하는 대상(부모, 자전거 마스터)이 없는 데이터 / 참조 무결성 위반
        - 분석에서는 제외하되 버리지 말고 따로 기록 -> 운영팀에 마스터 누락인지, 잘못 입력된 ID 인지 확인 요청
        - 마스터가 보완되면 다시 결합

    3. 자치구명이 결측인 행이 있습니다. 원인은 무엇입니까?
        - 결측 {len(no_district)} 건의 bike_id : {no_district['bike_id'].unique().tolist()}
        - 해당 자전거의 station_id : {no_district['station_id'].unique().tolist()}
        - STEP 2 에서 station_id 가 빈 값이었던 자전거라 stations 와 연결할 키가 없음
    """)
    print("-" * 100)

    # [6] 검증 ----------------------------------------------------------------------------------------------
    checks = [
        ("결합 후 행 수 14,500 (변화 없음)", n_merged == len(rentals) == 14500),
        ("매칭 실패 80 건", len(fail) == 80),
        ("제외 후 행 수 14,420", len(df) == 14420),
        ("자치구 결측 304", df['district'].isna().sum() == 304),
    ]

    print("[기대 결과 확인]")
    for name, ok in checks:
        print(f"  {'OK  ' if ok else 'FAIL'} {name}")