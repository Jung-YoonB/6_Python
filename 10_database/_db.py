"""
    DB 접속 관련 공통 모듈

    - 접속 정보는 .env 에서만 읽을 것임! (코드 상에 비밀번호를 저장하지 않음)
"""
import os
import oracledb

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()  # .env 파일을 읽어서 os.environ 에 저장(채워줌)

# os.getenv('키값', 기본값) : 환경변수에서 키값에 해당하는 값을 반환
#                           (기본값 제시하는 경우 값이 없을 경우 사용)
HOST = os.getenv("DB_HOST", '127.0.0.1')
PORT = int(os.getenv("DB_PORT", 1521))
NAME = os.getenv("DB_NAME")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")

def connect(autocommit=False):
    """
        오라클에 연결 후 커넥션 객체를 반환하는 함수

        Args:
            autocommit : 자동 커밋 설정(기본값: False)
    """
    # 오라클에 연결. DDL, UPSERT 처럼 세밀한 작업(제어)이 필요할 때 사용.
    conn = oracledb.connect(
        user=USER, password=PASSWORD, dsn=f"{HOST}:{PORT}/{NAME}"
    )
    conn.autocommit = autocommit
    return conn

def get_engine():
    """
        SQLAlchemy 엔진을 반환하는 함수
    """
    url = f"oracle+oracledb://{USER}:{PASSWORD}@{HOST}:{PORT}/?service_name={NAME}"
    # oracle+oracledb://사용자명:비밀번호@호스트:포트/?service_name=서비스명

    # pool_pre_ping : 풀에서 커넥션을 꺼낼 때, 아직 살아있는지를 한번 확인
    return create_engine(url, pool_pre_ping=True)