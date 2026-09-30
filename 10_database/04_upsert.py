"""
    멱등성과 upsert
"""
import time
import pandas as pd

from _db import connect, get_engine, prices_path, ENCODING

N = 2_000
conn = connect()
engine = get_engine()

df = pd.read_csv(prices_path(), encoding=ENCODING, parse_dates=["date"])
cols = ["code","date","open","high","low","close","volume","change","changeRate"]

sample = df.head(N)[cols].copy()   # 2000개 데이터 복제

# rows 변수에 df -> list(tuple) 변환하여 저장
rows = [tuple(c) for c in sample.itertuples(index=False)]

def quote(c):
    return f'"{c}"' if c in ("date", "change", "changeRate") else c

COL_SQL = ", ".join(quote(c) for c in cols)
PH = ", ".join([f":{i+1}" for i in range(len(cols))])

def make_table(name, unique=False):
    """
        실습용 테이블을 생성하는 함수
        - name : 테이블명
        - unique : UNIQUE(code, date) 설정 여부
    """
    def drop_table(cur, name):
        try:
            cur.execute(f"DROP TABLE {name}")
        except Exception as e:
            if "ORA-00942" not in str(e):
                raise

    with conn.cursor() as cur:
        drop_table(cur, name)

        uk = ', UNIQUE (code, "date")' if unique else ''
        cur.execute(f"""
            CREATE TABLE {name} (
                id      NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                code    VARCHAR2(20)    NOT NULL,
                "date"  DATE            NOT NULL,
                open    NUMBER(20), high    NUMBER(20), low     NUMBER(20),close   NUMBER(20),
                volume  NUMBER(20), "change" NUMBER(20), "changeRate"  NUMBER(6, 2)
                {uk}           
            )
        """)

def count(name):
    """ 전달받은 테이블의 행 개수를 조회하여 반환 """
    with conn.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) FROM {name}")
        return cur.fetchone()[0]

"""
    * UPSERT (Update or Insert)
      => 데이터가 없으면 추가, 있으면 수정(갱신)
    - MERGE INTO 구문

    데이터의 중복을 방지하기 위해, 추가하기 전에 SELECT로 값이 있는 지 확인할 수는 있으나
    조회(SELECT, 1번) 후 추가 또는 갱신(INSERT/UPDATE, 2번) ..SQL 2배로 사용해야함..

    추가/갱신을 동시에 진행하기 위해 UPSERT 를 적용함(사용)!
"""

PLAIN = f"INSERT INTO {{t}} ({COL_SQL}) VALUES ({PH})"
# {t} 는 이후에 .format(t="테이블명") 를 적용할 예정임!

MERGE_USING_SQL = ", ".join(f":{i+1} AS {quote(c)}" for i, c in enumerate(cols))
UPSERT = f"""
    MERGE INTO {{t}} dst
    USING (SELECT {MERGE_USING_SQL} FROM dual) src
    ON (dst.code = src.code AND dst."date" = src."date")
    WHEN MATCHED THEN
        UPDATE SET dst.open = src.open, dst.high = src.high, dst.low = src.low,
                   dst.close = src.close, dst.volume = src.volume, 
                   dst."change" = src."change", dst."changeRate" = src."changeRate"
    WHEN NOT MATCHED THEN
        INSERT ({COL_SQL})
        VALUES (src.code, src."date", src.open, src.high, src.low, src.close, src.volume, src."change", src."changeRate")
"""

# ==============================================
cases = []

# 1. 유니크 제약 없이 실행
make_table("t_noconstraint", unique=False)

for i in (1,2):     # 두번 반복하기 위해 작성
    with conn.cursor() as cur:
        cur.executemany(PLAIN.format(t="t_noconstraint"), rows)
    conn.commit()

n1 = count("t_noconstraint")
# print(f"CASE 1. 제약조건없이 실행 : {n1} 행 추가")

cases.append(("CASE 1. 제약조건없이 INSERT", "성공", n1, "데이터가 두배"))


# 2. 제약조건 설정(unique), INSERT 반복
make_table("t_unique", unique=True)

with conn.cursor() as cur:
    cur.executemany(PLAIN.format(t="t_unique"), rows)
conn.commit()

try:
    with conn.cursor() as cur:
        cur.executemany(PLAIN.format(t="t_unique"), rows)
    conn.commit()
    r2 = "성공"
except Exception as e:
    conn.rollback()
    r2 = type(e).__name__

n2 = count("t_unique")
cases.append(("CASE 2. 제약조건 설정 + INSERT", r2, n2, "두번째 실행 시 오류 발생!"))


# 3. 제약 조건 설정(unique) + UPSERT (MERGE INTO)
make_table("t_upsert", unique=True)

for i in (1,2):
    with conn.cursor() as cur:
        cur.executemany(UPSERT.format(t="t_upsert"), rows)
    conn.commit()
n3 = count("t_upsert")
cases.append(("CASE 3. 제약조건 설정 + UPSERT", "성공", n3, "데이터 추가 후 재실행 시 갱신됨"))

print(f"{'방식':<25}{'결과':<10}{'행수':>10} - 설명")
for name, res, n, desc in cases:
    print(f"{name:<25}{res:<10}{n:>10} {desc}")

"""
    CASE 1. 제약 조건이 없을 경우, 오류도 없음!
    --> 중복해서 무한하게 데이터가 추가될 수 있음..
    나중에 집계 시 이상한 결과를 도출할 수 있고, 되돌리고 싶어도.. 쉽지 않음

    CASE 2. 제약 조건을 설정하는 경우, 중복은 막을 수 있음. 재실행 불가함!

    CASE 3. UPSERT 를 사용하면 위의 문제들을 해결할 수 있음!
    --> 데이터가 있으면 갱신, 없으면 새로 추가!
"""
# ===================================
print('=' * 60)
"""
    신규/갱신 건수를 실행 전, 후의 전체 행수를 비교해서 기록
    * 실행 후 행수 - 실행 전 행수 => 신규 건수
"""

def upsert_with_stats(table, data, chunk=1000):
    """ 청크마다 커밋하면서 신규, 갱신 건수를 집계하는 함수 """
    start = time.perf_counter()

    before_count = count(table)

    for i in range(0, len(data), chunk):
        part = data[i:i+chunk]

        with conn.cursor() as cur:
            cur.executemany(UPSERT.format(t=table), part)
        conn.commit()

    after_count = count(table)

    add_count = after_count - before_count
    update_count = len(data) - add_count

    # (추가 건수, 갱신 건수, 실행 시간) 반환
    return add_count, update_count, time.perf_counter() - start

make_table("t_stats", unique=True)

a1, u1, t1 = upsert_with_stats("t_stats", rows)
print(f"\n [적재] t_stats (1회차)")
print(f"   입력    {len(rows)}행")
print(f"   신규    {a1}행")
print(f"   갱신    {u1}행")
print(f"   시간    {t1:.2f}")

a2, u2, t2 = upsert_with_stats("t_stats", rows)
print(f"\n [적재] t_stats (2회차 - 동일데이터)")
print(f"   입력    {len(rows)}행")
print(f"   신규    {a2}행")
print(f"   갱신    {u2}행")
print(f"   시간    {t2:.2f}")

"""
    기록(로그, 출력)을 남기는 것은 중요함!
    재실행 시 전부 갱신으로 확인되면 멱등하게 동작했다고 볼 수 있음!
             전부 신규로 확인되면.. 중복데이터가 쌓이고 있다고 볼 수 있음!
    위 데이터 기준으로 2회차 실행 시 신규 0, 갱신 (데이터길이)으로 확인된 것은 정상적임!
"""
# =====================================================
print('=' * 60)

expected = sample
actual = pd.read_sql(f"SELECT {COL_SQL} FROM t_stats", engine)

# print(actual.head())

checks = [
    ("행 수", len(expected), len(actual)),
    ("종목 수", expected["code"].nunique(), actual["code"].nunique()),
    ("종가 합계", expected["close"].sum(), actual["close"].sum()),
    ("종가 평균", expected["close"].mean(), actual["close"].mean()),
    ("거래량 합계", expected["volume"].sum(), actual["volume"].sum()),
    ("최소 날짜", expected["date"].min().date(), actual["date"].min().date()),
    ("최대 날짜", expected["date"].max().date(), actual["date"].max().date()),
]

all_ok = True
for name, exp, act in checks:
    ok = str(exp) == str(act)
    all_ok &= ok
    print(f" {name:<14}{str(exp):>20}{str(act):>20} {'O' if ok else 'X'}")

print(f"모든 항목 일치 : {all_ok}")

# 테스트 테이블 삭제
def drop_table(cur, name):
    """ 전달된 테이블을 삭제하는 함수 """
    try:
        cur.execute(f"DROP TABLE {name}")
    except Exception as e:
        if "ORA-00942" not in str(e):
            pass

with conn.cursor() as cur:
    for t in ["t_noconstraint", "t_unique", "t_upsert", "t_stats"]:
        drop_table(cur, t)
conn.close()