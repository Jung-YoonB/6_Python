"""
## STEP 8 · DB 적재
### 8-1. 스키마 설계
`rental_log` 테이블을 설계하고 생성하세요.

**설계 기준**
- 금액과 거리에 `FLOAT` 을 쓰지 말 것
- 날짜·시각을 문자열로 저장하지 말 것
- ID 는 계산하지 않는 값이므로 문자열로
- **`rental_id` 에 유니크 제약** — 재실행 안전성의 출발점

### 8-2. 적재
- `executemany` 또는 `to_sql(method="multi")` 로 벌크 적재
- **청크 단위로 커밋**
- `ON DUPLICATE KEY UPDATE` 로 UPSERT
- 신규 · 갱신 건수를 로그로 남길 것

### 8-3. 재실행 검증
**같은 스크립트를 두 번 실행하세요.**
|  | 1회차 | 2회차 |
| --- | --- | --- |
| 신규 | 13,501 | 0 |
| 갱신 | 0 | 0 |
| 최종 행 수 | 13,501 | 13,501 |

> ⚠️ **2회차에 행이 두 배가 되거나 에러가 났다면**
유니크 제약이 없거나, UPSERT 를 쓰지 않은 것입니다.

### 8-4. 적재 검증
행 수만 보면 놓칩니다. **집계값을 대조**하세요.
- 행 수 · 자전거 수 · 이용자 수
- 총 매출 · 총 이동 거리
- 최소 · 최대 날짜

> ⚠️ **합계가 미세하게 다르다면**
타입 변환에서 소수점이 잘렸을 가능성이 높습니다.
`DECIMAL` 자릿수와 파이썬 쪽 반올림을 맞췄는지 확인하세요.
"""
import time

import pandas as pd

from config import BASE_DIR, connect
from step2 import bikes_raw, clean_bikes
from step3 import rentals_raw, clean_rentals
from step4 import stations, merge_all
from step5 import detect_outliers
from step6 import handle_missing

# [1] 설정 -----------------------------------------------------------------------------------------------
TABLE = "rental_log"
CHUNK_SIZE = 5_000      # 청크 단위 (5,000 행마다 커밋)

# DB 에 저장할 컬럼 순서 (schema.sql 과 같은 이름)
COLS = ["rental_id", "bike_id", "user_id", "rent_time", "return_time", "duration_min",
        "distance_km", "fee", "payment_method", "bike_type",
        "station_id", "station_name", "district"]

# ---- SQL 조각 만들기 ----------------------------------------------------------------------------------
COL_SQL = ", ".join(COLS)                                                     # rental_id, bike_id, ...
MERGE_USING = ", ".join(f":{i + 1} AS {c}" for i, c in enumerate(COLS))      # :1 AS rental_id, :2 AS bike_id, ...
UPDATE_SET = ", ".join(f"dst.{c} = src.{c}" for c in COLS[1:])               # rental_id(기준 열) 제외
INSERT_VALUES = ", ".join(f"src.{c}" for c in COLS)                          # src.rental_id, src.bike_id, ...

# UPSERT : rental_id 가 있으면 UPDATE, 없으면 INSERT
UPSERT = f"""
MERGE INTO {TABLE} dst
USING (SELECT {MERGE_USING} FROM dual) src
ON (dst.rental_id = src.rental_id)
WHEN MATCHED THEN
    UPDATE SET {UPDATE_SET}, dst.updated_at = CURRENT_TIMESTAMP
WHEN NOT MATCHED THEN
    INSERT ({COL_SQL})
    VALUES ({INSERT_VALUES})
"""


def create_table():
    """
    schema.sql 을 읽어서 rental_log 테이블 생성 (이미 있으면 그대로 사용)
    """
    # 파일 읽기
    with open(BASE_DIR / "schema.sql", "r", encoding="utf-8") as f:
        lines = f.read().split("\n")

    # '--' 로 시작하는 주석 줄은 빼고, 끝의 ; 제거 (cur.execute 는 ; 를 붙이면 오류)
    ddl = "\n".join(line for line in lines if not line.strip().startswith("--"))
    ddl = ddl.strip().rstrip(";")

    conn = connect()
    try:
        with conn.cursor() as cur:
            cur.execute(ddl)
        created = True
    except Exception as e:
        # ORA-00955 : 이미 같은 이름의 객체(테이블)가 있음 -> 넘어감, 그 외 오류는 그대로 발생
        if "ORA-00955" not in str(e):
            raise
        created = False
    finally:
        conn.close()

    return created


def reset_table():
    """ 테이블 비우기 (재실행 검증을 처음부터 하기 위함) """
    conn = connect()
    with conn.cursor() as cur:
        cur.execute(f"TRUNCATE TABLE {TABLE}")
    conn.close()


def row_count():
    """ 테이블 전체 행 수 반환 """
    conn = connect()
    with conn.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) FROM {TABLE}")
        n = cur.fetchone()[0]
    conn.close()
    return n


def to_db(df, chunk=CHUNK_SIZE):
    """
    UPSERT 로 청크 단위 적재 후 (신규 건수, 갱신 건수, 소요 시간) 반환
    Args:
        df    : STEP 6 최종 결과
        chunk : 한 번에 실행하고 커밋할 행 수
    """
    # [2] 데이터 준비 -----------------------------------------------------------------------------------
    data = df[COLS].copy()

    # 거리는 실수 -> DB 자릿수(NUMBER(6, 1))와 맞춰서 반올림
    #   (8-4 경고 : 파이썬 쪽 반올림과 DECIMAL 자릿수를 맞추지 않으면 합계가 미세하게 다를 수 있음)
    data['distance_km'] = data['distance_km'].round(1)

    # NaN -> None : oracledb 는 None 을 DB 의 NULL 로 저장
    data = data.astype(object).where(data.notna(), None)

    # list[tuple] 로 변환 [출처] 11_pipeline/etl/load.py 78줄
    rows = [tuple(r) for r in data.itertuples(index=False)]

    # [3] 청크 단위 적재 --------------------------------------------------------------------------------
    start = time.perf_counter()
    before = row_count()

    conn = connect()
    try:
        # range(시작, 끝, 간격) -> 0, 5000, 10000 ...
        for i in range(0, len(rows), chunk):
            part = rows[i:i + chunk]

            with conn.cursor() as cur:
                cur.executemany(UPSERT, part)
            conn.commit()       # 청크마다 커밋 -> 중간에 실패해도 앞 청크는 저장되어 있음
    except Exception:
        conn.rollback()         # 실패한 청크만 되돌림
        raise
    finally:
        conn.close()

    after = row_count()

    # 신규 = 적재 후 - 적재 전 / 갱신 = 시도 건수 - 신규
    inserted = after - before
    updated = len(rows) - inserted

    return inserted, updated, time.perf_counter() - start


def verify(df):
    """
    DataFrame 과 DB 의 집계값을 비교하여 [(항목, df 값, db 값, 일치 여부), ...] 반환
    """
    conn = connect()
    with conn.cursor() as cur:
        cur.execute(f"""
            SELECT COUNT(*),
                   COUNT(DISTINCT bike_id),
                   COUNT(DISTINCT user_id),
                   SUM(fee),
                   SUM(distance_km),
                   MIN(rent_time),
                   MAX(rent_time)
            FROM {TABLE}
        """)
        n, n_bike, n_user, fee_sum, dist_sum, min_d, max_d = cur.fetchone()
    conn.close()

    # 비교할 값 (df 값, db 값) -> 문자열로 바꿔서 비교
    #   거리 합계 : 둘 다 round(1) / 날짜 : str() 하면 둘 다 'YYYY-MM-DD HH:MM:SS' 형식
    checks = [
        ("행 수", len(df), n),
        ("자전거 수", df['bike_id'].nunique(), n_bike),
        ("이용자 수", df['user_id'].nunique(), n_user),
        ("총 매출", int(df['fee'].sum()), int(fee_sum)),
        ("총 이동 거리", round(df['distance_km'].round(1).sum(), 1), round(float(dist_sum), 1)),
        ("최소 날짜", df['rent_time'].min(), min_d),
        ("최대 날짜", df['rent_time'].max(), max_d),
    ]

    return [(name, exp, act, str(exp) == str(act)) for name, exp, act in checks]

# [5] 검증 ----------------------------------------------------------------------------------------------
if __name__ == "__main__":
    rentals = clean_rentals(rentals_raw)
    bikes = clean_bikes(bikes_raw)
    df4, fail = merge_all(rentals, bikes, stations)
    df5, rules = detect_outliers(df4)
    df, n_fee, n_dist = handle_missing(df5)

    # [8-1] 스키마 ------------------------------------------------------------------------------------------
    created = create_table()
    print(f"[8-1] {TABLE} 테이블 {'생성' if created else '이미 있음 -> 그대로 사용'}")

    # [8-2], [8-3] 적재 + 재실행 검증 ----------------------------------------------------------------------
    # 같은 데이터를 두 번 적재 -> 2회차에 행이 늘지 않아야 함
    reset_table()

    results = []
    for n in (1, 2):
        ins, upd, t = to_db(df)
        results.append((n, ins, upd, row_count(), t))

    print()
    print("[8-3] 재실행 검증")
    print(f"  {'':<6}{'신규':>10}{'갱신':>10}{'최종 행 수':>12}{'시간(초)':>10}")
    for n, ins, upd, total, t in results:
        print(f"  {n}회차{ins:>12,}{upd:>12,}{total:>14,}{t:>12.1f}")

    # [8-4] 적재 검증 ---------------------------------------------------------------------------------------
    print()
    print("[8-4] 적재 검증 (DataFrame / DB)")
    for name, exp, act, ok in verify(df):
        print(f"  {'OK  ' if ok else 'FAIL'} {name:<8} {exp} / {act}")

    checks = [
        ("1회차 신규 13,501",           results[0][1] == 13501),
        ("2회차 신규 0",                results[1][1] == 0),
        ("1, 2회차 최종 행 수 13,501",   results[0][3] == results[1][3] == 13501),
    ]

    print()
    print("[기대 결과 확인]")
    for name, ok in checks:
        print(f"  {'OK  ' if ok else 'FAIL'} {name}")
    print("""
    참고: 2회차 '갱신' 은 수업 방식(시도 건수 - 신규)으로 계산하면 13,501 로 나옴
        -> MERGE 가 2회차에 13,501 행을 같은 값으로 "다시 덮어쓴" 건수
        -> 문제지의 갱신 0 은 "값이 바뀐 행이 없다" 는 의미로 해석 (행 수가 그대로인 것이 핵심)
    """)