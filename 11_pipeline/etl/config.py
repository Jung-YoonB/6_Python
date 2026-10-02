"""
    설정 - 환경변수, 상수

    공통으로 사용되는 값을 정의하기 위한 용도
"""
import os

from ._db import connect, get_engine, ENCODING, KHLAB_BASE, data_path, prices_path, raw_prices_path

# ---- 환경 변수 기반 설정 ----
SOURCE = os.getenv("PIPELINE_SOURCE", "csv")  # Extract 방식: "api" 또는 "csv"

MAX_PAGES = int(os.getenv("PIPELINE_MAX_PAGES", 5))     # API 페이지 상한

# ---- 고정 상수 ----
PAGE_SIZE = 100     # 한 페이지에 요청할 데이터 수

CHUNK_SIZE = 5_000  # DB에 적재 시 청크 개수(쪼개서 실행할 개수)

TIMEOUT = 5         # 서버 응답에 대한 타임아웃 시간(초)

DELAY = 1.0         # 요청 간에 대기 시간(초)

# ---- 로그 경로 ----
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
# => ~/11_pipeline/logs/