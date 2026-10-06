"""
    공통 항목 설정
"""
import os

# ~/12_ml/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# ~/12_ml/data
DATA_DIR = os.path.join(BASE_DIR,"data")
# ~/12_ml/models
MODEL_DIR = os.path.join(BASE_DIR,"models")

BASE_URL = "https://kh-lab.rockua.ai.kr"

ENCODING = "utf-8-sig"

# ---------------------------------------------------------------------------------------------------
def path(name):
    """ data 폴더 안의 파일 경로 반환 """
    return os.path.join(DATA_DIR, name)

def prices_path():
    """ 일별 시세 데이터(prices.csv) 파일 경로 또는 URL 반환 """
    local = path("prices.csv")

    if os.path.exists(local):
        return local

    return f"{BASE_URL}/datasets/prices.csv"

def model_path(name="model_bundle.pkl"):
    """ models 폴더 안의 파일 경로 반환 """
    os.makedirs(MODEL_DIR, exist_ok=True)

    return os.path.join(MODEL_DIR, name)