"""
    데이터 파이프라인, 재실행 검증
"""
from etl._db import connect
from etl.pipeline import run

# daily_price 테이블 초기화
conn = connect()

with conn.cursor() as cur:
    cur.execute("TRUNCATE TABLE daily_price")

# daily_price 테이블 행 수 조회
def row_count():
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM daily_price")
        return cur.fetchone()[0]

print("--- 1회차 실행 ---")
print("-" * 100)
ok1 = run()
n1 = row_count()
print("-" * 100)

print("--- 2회차 실행 ---")
ok2 = run()
n2 = row_count()
print("-" * 100)

print("--- 검증 ---")
print("-" * 100)

# 재실행 검증
checks = [
    ("1회차 성공", ok1),
    ("2회차 성공", ok2),
    ("행수 비교", n1 == n2),
    ("종목 수", None)
            
]

with conn.cursor() as cur:
    cur.execute("SELECT COUNT(DISTINCT code) FROM daily_price")
    codes = cur.fetchone()[0]
checks[3] = ("종목 수", codes == 120)

print(f"1회차 적재: {n1:,} 행")
print(f"2회차 적재: {n2:,} 행")
print(f"종목 수 : {codes}")
print()

for name, ok in checks:
    print(f"{name} : {'통과' if ok else '실패'}")

conn.close()