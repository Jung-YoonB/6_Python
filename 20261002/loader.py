"""
    데이터 로더
        - train.csv 불러오기
        - 새로운 열을 만들 때 사용할 함수 (나이대 구분, 호칭 추출)
"""
import re           # 정규표현식 모듈

import pandas as pd

from config import TRAIN_PATH, ENCODING


def load_train():
    """
    train.csv 파일을 읽어서 DataFrame 으로 반환
    """
    return pd.read_csv(TRAIN_PATH, encoding=ENCODING)

# ===================================================
#   나이대 구분 기준 (8번 문제)
# ===================================================
AGE_BINS = [
    (0, 10, '아동'),
    (10, 20, '10대'),
    (20, 30, '20대'),
    (30, 40, '30대'),
    (40, 50, '40대'),
    (50, 60, '50대'),
]

# ===================================================
#   호칭 추출 (16번 문제)
# ===================================================
def extract_title(name, default='미확인'):
    """
    이름에서 호칭(Mr, Mrs, Miss, Master 등)을 추출하여 반환
    Args:
        name    : 승객 이름 (예: "Braund, Mr. Owen Harris")
        default : 호칭을 찾지 못했을 때 반환할 값 
    
    정규식 r', ([A-Za-z]+)\.'
        ,           -> 성(Last name) 뒤의 쉼표
        (공백)      -> 쉼표 뒤 공백
        ([A-Za-z]+) -> 영문자 1개 이상 (괄호 = 꺼내고 싶은 부분, 그룹 1)
        \.          -> 마침표 (그냥 . 은 "아무 문자 1개"라는 뜻이라 \ 로 이스케이프)
    """
    m = re.search(r', ([A-Za-z]+)\.', name)

    return m.group(1) if m else default