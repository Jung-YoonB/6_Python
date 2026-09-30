"""
    대량 적재
"""
import time
import pandas as pd
from _db import connect, get_engine, prices_path, ENCODING

SAMPLE = 1_000
TOTAL = 90_000

conn = connect()
engine = get_engine()

df = pd.read_csv(prices_path(), encoding=ENCODING, parse_dates=["date"])
sample = df.head(SAMPLE).copy()

cols = ["code","date","open","high","low","close","volume","change","changeRate"]
sample = sample[cols]

print(sample.head())

def reset_table():
    """ 테이블을 비워주는 함수 """
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE daily_price")

def count_rows():
    """ 테이블의 행 개수를 반환하는 함수 """
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM daily_price")
        return cur.fetchone()[0]

INSERT_SQL = f"""
    INSERT INTO daily_price (code,"date",open,high,low,close,volume,"change","changeRate")
    VALUES ({','.join([':%d' % i for i in range(1, 10)])})
"""

# * itertuples() -> 행 단위로 데이터를 가져옴. 속도가 좀더 빠름!
rows = [tuple(r) for r in sample.itertuples(index=False)]


# ===========================================
#   적재 방식 
results = []

#   1. execute 반복. -> 한 행씩 SQL을 실행. 가장 느림!
reset_table()
start = time.perf_counter()

with conn.cursor() as cur:
    for r in rows:
        cur.execute(INSERT_SQL, r)
conn.commit()
t1 = time.perf_counter() - start

results.append(("1. execute 반복", t1, count_rows()))


#   2. executemany -> 같은 SQL을 한 문장으로 한번에 실행.
reset_table()
start = time.perf_counter()

with conn.cursor() as cur:
    cur.executemany(INSERT_SQL, rows)
conn.commit()
t2 = time.perf_counter() - start

results.append(("2. executemany", t2, count_rows()))


#   3. to_sql -> 내부적으로 executemany를 사용하여 적재.
"""
    df.to_sql(테이블명, engine, if_exists="append", index=False)
    - if_exists : "append" - 데이터 추가 / "replace" - 테이블을 지우고 새로 만듬 / "fail" - 실패처리
    - INSERT 문을 작성하지 않아도 됨!
"""
# reset_table()
# start = time.perf_counter()

# sample.to_sql("daily_price", engine, if_exists="append", index=False)
# t3 = time.perf_counter() - start

# results.append(("3. to_sql", t3, count_rows()))


# #   4. to_sql , method="multi"  -> 원하는 개수만큼 쪼개서(청킹) 데이터를 적재
# reset_table()
# start = time.perf_counter()

# sample.to_sql("daily_price", engine, if_exists="append", index=False,
#               chunksize=500)
# --> method="multi" 옵션은 오라클 지원 x
# t4 = time.perf_counter() - start

# results.append(("4. to_sql (multi)", t4, count_rows()))

# =====================================================
print('-' * 60)
for name, t, n in results:
    print(f"{name:<20} {t*1000:>8.0}ms {n:>8,}")