"""
    공통 변수 (설정 항목)
"""
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent     # 상위 폴더
DATA_DIR = BASE_DIR / "data"                   # / => 경로 연결

RAW_PATH = DATA_DIR / "raw-prices.csv"

ENCODING = "utf-8-sig"

# 정제 단계별 중간 결과물 저장 경로
STEP_DIR = DATA_DIR / "steps"
# 폴더가 없으면 생성
STEP_DIR.mkdir(parents=True, exist_ok=True)

def step_path(filename):
    """ 단계별 저장된 파일 경로 반환 """
    return STEP_DIR / filename

def path(name):
    """
        data 폴더 안의 파일 경로를 반환
    """
    return DATA_DIR / name