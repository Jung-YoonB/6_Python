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