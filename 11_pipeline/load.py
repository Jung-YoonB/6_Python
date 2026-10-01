"""
    Load. 데이터를 DB에 적재(저장)
        - 하지 않는 것 : 정제(가공)
        - UPSERT를 사용하여 데이터가 있으면 UPDATE, 없으면 INSERT
        - 대용량을 한 번에 처리하지 않고, CHUNK_SIZE 단위로 나누어서 처리
"""
import time

from config import connect, CHUNK_SIZE

# DB 에 저장 할 컬럼 순서
COLS = ["code","date","open","high","low","close","volume","change","changeRate"]

def _quote(c):
    """
    컬럼명을 큰 따옴표로 감싸서 반환
    - date, change, changeRate

    Args.
        c : 컬럼명
    """
    return f'"{c}"' if c in ("date", "change", "changeRate") else c

# SQL 조각 ================================================================================================
# 컬럼 목록 문자열
#   => code, "date", ..., volume, "change", ...
COL_SQL = ", ".join(_quote(c) for c in COLS)

# 위치 기반 바인드 변수 문자열
#   => :!, :2, ... :8, :9
PH = ", ".join([f":{i + 1}" for i in range(len(COLS))])

# MERGE INTO 사용 시 별칭 지정 문자열
#   => :1 AS code, :2 AS "date", ...
MERGE_USING = ", ".join(f":{i + 1} AS {_quote(c)}" for i, c in enumerate(COLS))

# 실행 할 쿼리문
#   - daily_price 테이블
UPSERT = """
MERGE INTO daily_price dst
USING (SELECT {MERGE_USING} FROM dual) src
ON (dst.code = src.code AND dst."date" = src."date")
WHEN MATCHED THEN
    UPDATE SET dst.open = src.open,
               dst.high = src.high,
               dst.low = src.low,
               dst.close = src.close,
               dst.volume = src.volume,
               dst."change" = src."change",
               dst."changeRate" = src."changeRate" 
WHEN NOT MATCHED THEN
    INSERT ({COL_SQL})
    VALUES (src.code, src."date", src.open, src.high, src.low, src.loase, 
            src.volume, src."change", src."changeRate")
"""

# ---------------------------------------------------------------------------------------------------------
def _row_count(conn):
    """ daily_price 테이블의 전체 행 수를 반환 """
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM daily_price")
        return cur.fetchone()[0]


def to_db(df, logger, chunk=CHUNK_SIZE):
    """
    UPSERT 로 적재하고 (신규 건수, 갱신 건수, 소요 시간)을 반환
    """
    # ------ 데이터 준비 ---------------------------------------------
    #   * 필요한 열(COLS)만 선택 
    #   * Nan --> None 변환
    data = df[COLS].astype(object).where(df[COLS].notna(), None)   
    #           -> astype(cbject) : 모든 열을 파이썬 객체 타입으로 변환
    #           -> where(df[COLS].notna(), None) : NaN --> None
    #                   => oracledb 가 Python None 을 DBMS NULL 로 처리

    #   * list[tuple] 형태로 변환, 인덱스 없이 변환
    rows = [tuple(r) for r in data.itertuples(index=False)]

    # =================================================================
    conn = connect()
    start = time.perf_counter()     # 타이머 시작
    before = _row_count(conn)       # 적재 전 행 수 저장

    try:
        for i in range(0, len(rows), chunk):
            part = rows[i:i+chunk]      # 청크만큼 데이터 추출

            with conn.cursor() as cur:
                cur.executemany(UPSERT, part)
            conn.commit()
    except Exception:
        conn.rollback()
        logger.warning(f"   적재 실패 ({i} ~ {i+chunk-1})")
        raise
    finally:
        conn.close()

    conn2 = connect()
    after = _row_count(conn2)
    conn2.close()

    # 신규 건수, 갱신 겅수 계산 ---------------------------------------------
    #   * 신규 = (적재 후 행 수) - (적재 전 행 수)
    #   * 갱신 = (총 적재 시도 건수) - 신규
    inserted = after - before
    updated = len(rows) - inserted
    t = time.perf_counter() - start

    logger.info(f"  적재 완료 - 신규: {inserted} 건, 갱신: {updated} 건")
    return inserted, updated, t


def verify():
    """
    적재 후 검증 결과를 반환
    [검증 항목 : (df, db)]
        - 전체 행 수
        - 종목 코드 수
        - 종가 총 합
        - 날짜 최소
        - 날짜 최대
    """
    pass
