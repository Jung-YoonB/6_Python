"""
    공통 변수 (설정 항목)
"""
from pathlib import Path

BASE_DIR = Path(__file__).parent    # 상위 폴더
DATA_DIR = BASE_DIR / "data"                   # / => 경로 연결

ENCODING = "utf-8-sig"

def path(name):
    """
        data 폴더 안의 파일 경로를 반환
    """
    return DATA_DIR / name


# ===================================================
#   DB 접속 (STEP 8, solution.py)
# ===================================================
ENV_PATH = BASE_DIR / ".env"
 
 
def connect(autocommit=False):
    """
    오라클에 연결 후 커넥션 객체를 반환
 
    Args:
        autocommit : 자동 커밋 설정 (기본값 False -> commit() 을 직접 호출)
    """
    import os
    import oracledb
    from dotenv import load_dotenv
 
    load_dotenv(ENV_PATH)   # .env 파일 내용을 환경 변수로 읽어옴
 
    conn = oracledb.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dsn=f"{os.getenv('DB_HOST', '127.0.0.1')}:{os.getenv('DB_PORT', 1521)}/{os.getenv('DB_NAME')}"
    )
    conn.autocommit = autocommit
    return conn