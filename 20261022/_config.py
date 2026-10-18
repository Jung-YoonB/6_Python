"""
    공통 항목 설정
"""
import os
 
# ~/20261022/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# ~/20261022/data
DATA_DIR = os.path.join(BASE_DIR, "data")
 
ENCODING = "utf-8-sig"
 
# ---------------------------------------------------------------------------------------------------
def path(name):
    """ data 폴더 안의 파일 경로 반환 """
    return os.path.join(DATA_DIR, name)
 