import time
import pandas as pd
from _db import prices_path, get_engine, ENCODING
from db_utils import reset_table, make_table, count_rows

SAMPLE = 1_000

engine = get_engine()

df = pd.read_csv(prices_path(), encoding=ENCODING, parse_dates=["date"])
sample = df.head(SAMPLE).copy()

# 열 이름 변경 : date -> date_at, change -> change_value, changeRate -> change_rate
sample = sample.rename(columns={'date':'date_at', 
               'change':'change_value', 
               'changeRate':'change_rate'})
print(sample.head())

table_name = "daily_price_v2"
CLEAN_DDL = f"""
    CREATE TABLE {table_name} (
        id      NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        code    VARCHAR2(20)    NOT NULL,
        date_at  DATE            NOT NULL,
        open    NUMBER(20),
        high    NUMBER(20),
        low     NUMBER(20),
        close   NUMBER(20),
        volume  NUMBER(20),
        change_value NUMBER(20),
        change_rate  NUMBER(6, 2),
        -- 수집 시간이나 출처 등 따로 필요한 정보는 자유롭게 추가
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (code, date_at)
    )
"""
make_table(table_name, CLEAN_DDL)
print(f"=== {table_name} 테이블 생성 완료 ===")

results = []

reset_table(table_name)
start = time.perf_counter()

sample.to_sql(table_name, engine, if_exists="append", index=False)
t3 = time.perf_counter() - start

results.append(("3. to_sql", t3, count_rows(table_name)))


#   4. to_sql , method="multi"  -> 원하는 개수만큼 쪼개서(청킹) 데이터를 적재
reset_table(table_name)
start = time.perf_counter()

sample.to_sql(table_name, engine, if_exists="append", index=False,
              chunksize=500)
t4 = time.perf_counter() - start

results.append(("4. to_sql (multi)", t4, count_rows(table_name)))

print('-' * 60)
for name, t, n in results:
    print(f"{name:<20} {t*1000:>8.0}ms {n:>8,}")