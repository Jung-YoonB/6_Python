"""
    공통 항목 설정
"""
import os

# ~/ml_practice/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# ~/ml_practice/data
DATA_DIR = os.path.join(BASE_DIR,"data")
# ~/ml_practice/models
MODEL_DIR = os.path.join(BASE_DIR,"models")

ENCODING = "utf-8-sig"

# ---------------------------------------------------------------------------------------------------
def path(name):
    """ data 폴더 안의 파일 경로 반환 """
    return os.path.join(DATA_DIR, name)