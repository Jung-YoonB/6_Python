"""
    수집 데이터를 위한 스키마 설계
"""
import pandas as pd

from _db import connect, raw_prices_path, ENCODING

conn = connect()

def drop_table(cur, name):
    """ 전달된 테이블을 삭제하는 함수 """
    try:
        cur.execute(f"DROP TABLE {name}")
    except Exception as e:
        if "ORA-00942" not in str(e):
            pass

# ==================================

# 원본 데이터 저장 -> 원본 테이블
#    대리키(데이터가 아닌 별도의 키를 추가)
#    자동 증가 기본키 - oracle 12c 버전부터 지원!
#    - ALWAYS AS : INSERT 시 별도의 값을 지정 불가
#    - BY DEFAULT AS : 값을 지정하지 않았을 때만 자동 증가

RAW_DDL = """
    CREATE TABLE raw_daily_price (
        id      NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        code    VARCHAR2(20),
        "date"  VARCHAR2(20),
        open    VARCHAR2(20),
        high    VARCHAR2(20),
        low     VARCHAR2(20),
        close   VARCHAR2(20),
        volume  VARCHAR2(20),
        "change" VARCHAR2(20),
        "changeRate"  VARCHAR2(20),
        -- 수집 시간이나 출처 등 따로 필요한 정보는 자유롭게 추가
        collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        source  VARCHAR2(100)
    )
"""

with conn.cursor() as cur:
    drop_table(cur, "raw_daily_price")
    cur.execute(RAW_DDL)

print("=== raw_daily_price 테이블 생성 완료 ===")
"""
    원본 데이터를 저장할 테이블 생성 시
    - 모든 컬럼의 데이터 타입은 "문자열"로 지정
      (어떤 값이든 저장할 수 있도록)
    - 제약조건을 설정하지 않음
    - 수집 시간, 출처도 함께 기록하기 위해 컬럼 추가

    원본 데이터를 저장해야 하는 이유
    - 정제 로직이 잘못된 경우 원본이 없다면 되돌릴 수 없음!
"""

raw_sample = pd.read_csv(raw_prices_path(), 
                         encoding=ENCODING, dtype=str,
                         keep_default_na=False)

# print(raw_sample.head())
bad = raw_sample[raw_sample["close"].isin(["N/A","-"])].head(2)
good = raw_sample[~raw_sample["close"].isin(["N/A","-"])].head(2)

mix = pd.concat([good, bad])
print(mix[["code", "date", "close"]])

print('-' * 60)

# 제약 조건을 설정한 테이블 추가
with conn.cursor() as cur:
    drop_table(cur, "demo_strict")
    cur.execute("""
        CREATE TABLE demo_strict (
            code VARCHAR2(20), 
            "date" DATE, 
            close NUMBER NOT NULL
        )
    """)

succ_cnt = 0
for _, r in mix.iterrows():
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO demo_strict VALUES (:1, TO_DATE(:2, 'YYYY-MM-DD'), :3)",
                        (r['code'], r['date'], r['close']))
        conn.commit()
        succ_cnt += 1
    except Exception as e:
        conn.rollback()
        print(f"close ({r['close']}) ... {type(e).__name__}")

print(f"demo_strict 데이터 추가: {succ_cnt} / 4 성공")

# 제약 없이 만든 테이블에 추가
with conn.cursor() as cur:
    cur.executemany(
        'INSERT INTO raw_daily_price (code, "date", close, source) VALUES (:1, :2, :3, :4)',
        [ (r['code'], r['date'], r['close'], '실습데이터') for _, r in mix.iterrows() ]
    )
conn.commit()

with conn.cursor() as cur:
    cur.execute("SELECT COUNT(*) FROM raw_daily_price")
    print(f"raw_daily_price 데이터 추가: {cur.fetchone()[0]} / 4 성공")

"""
    원본 테이블은 데이터를 그대로 저장하는 것이 목적이고, 
    결측 또는 이상치 등은 정제 단계에서 판단해야 함!
"""
# =====================================================

CLEAN_DDL = """
    CREATE TABLE daily_price (
        id      NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        code    VARCHAR2(20)    NOT NULL,
        "date"  DATE            NOT NULL,
        open    NUMBER(20),
        high    NUMBER(20),
        low     NUMBER(20),
        close   NUMBER(20),
        volume  NUMBER(20),
        "change" NUMBER(20),
        "changeRate"  NUMBER(6, 2),
        -- 수집 시간이나 출처 등 따로 필요한 정보는 자유롭게 추가
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT uk_code_date UNIQUE (code, "date")
    )
"""

with conn.cursor() as cur:
    drop_table(cur, "daily_price")
    cur.execute(CLEAN_DDL)

print("=== daily_price 테이블 생성 완료 ===")

"""
    - 금액: 실수 타입 금지 - 부동소수점(float). 오차가 누적될 수 있음! NUMBER 사용
    - 비율: NUMBER(6,2) => 자릿수 고정. 오차를 줄일 수 있음!
    - 날짜: DATE => 문자열 저장하게 되면, 날짜 계산이나 정렬이 어려워질 수 있음
    - 코드: VARCHAR2 => 0부터 시작하는 값인 경우 0을 보존하기 위함
"""

with conn.cursor() as cur:
    for t in ["demo_strict"]:
        drop_table(cur, t)
conn.close()

print("**** 테이블 정리 완료 ****")