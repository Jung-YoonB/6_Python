from _db import connect

conn = connect()

def make_table(name, ddl_sql=None):
    """ 
        테이블이 존재하면 삭제 후 생성하는 함수 
        - name : 테이블명
        - ddl_sql : 실행할 쿼리문
    """
    def drop_table(cur, name):
        try:
            cur.execute(f"DROP TABLE {name}")
        except Exception as e:
            if "ORA-00942" not in str(e):
                raise
    if not ddl_sql:
        raise ValueError("실행할 쿼리문이 전달되지 않았습니다.")
    
    with conn.cursor() as cur:
        drop_table(cur, name)
        cur.execute(ddl_sql)

def reset_table(name):
    """ 테이블을 비워주는 함수 """
    with conn.cursor() as cur:
        cur.execute(f"TRUNCATE TABLE {name}")

def count_rows(name):
    """ 테이블의 행 개수를 반환하는 함수 """
    with conn.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) FROM {name}")
        return cur.fetchone()[0]