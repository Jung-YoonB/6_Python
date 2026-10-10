"""
    데이터 로드, 피처 생성, 분할, 인코딩 기능 모아두는 모듈
"""
import pandas as pd

from _config import path, ENCODING

SEED = 42

TARGET = "is_overdue_100m"      # 예측 대상 (정답)
OVERDUE_MIN = 100               # 장기 연체 기준 (분)

# 누수 컬럼 : 반납이 끝난 뒤에야 확정되는 값 (STEP 3)
LEAK_COLS = ["return_time", "duration_min", "distance_km", "fee"]

# 피처 : 대여 시점에 알 수 있는 정보만
NUM_FEATURES = ["hour", "dayofweek", "join_days"]                               # 숫자형
CAT_FEATURES = ["membership_type", "payment_method", "bike_type", "district"]   # 범주형 (인코딩 필요)


# 데이터 로드 -----------------------------------------------------------------------------------------
def load_rentals():
    """
    clean_rentals.csv (이전 실습 최종 결과) 를 날짜 타입으로 읽어서 반환
    """
    return pd.read_csv(path("clean_rentals.csv"), encoding=ENCODING, parse_dates=["rent_time", "return_time"])

def load_users():
    """ users.csv (이용자 마스터) 를 날짜 타입으로 읽어서 반환 """
    return pd.read_csv(path("users.csv"), encoding=ENCODING, parse_dates=["join_date"])


# 파생 변수 -------------------------------------------------------------------------------------------
def add_features(df):
    """
    대여 시간(분), 정답(is_overdue_100m), 시간대, 요일을 추가하여 반환 (STEP 1)
    """
    df = df.copy()

    # 대여 시간(분) : 날짜 - 날짜 = 시간 차이 -> 초 단위 -> / 60
    df["duration_min"] = (df["return_time"] - df["rent_time"]).dt.total_seconds() / 60

    # 정답 : 100분 초과면 1, 아니면 0 (True/False -> 1/0)
    df[TARGET] = (df["duration_min"] > OVERDUE_MIN).astype(int)

    # 대여 시점 기준 시간대, 요일 (0: 월 ~ 6: 일)
    df["hour"] = df["rent_time"].dt.hour
    df["dayofweek"] = df["rent_time"].dt.dayofweek

    return df

def merge_users(df, users):
    """
    대여 기록 + 이용자 결합 후, 가입 기간(일) 을 추가하여 반환 (STEP 2)
    """
    # how="left" : 대여 기록은 전부 유지 / validate="many_to_one" : users 의 user_id 가 유일한지 검사
    #   주의: user_id 는 문자열 그대로 결합 ('U0001' / 'U00001' 이 섞여 있어 숫자로 바꾸면 겹침)
    df = df.merge(users, on="user_id", how="left", validate="many_to_one")

    # 가입 기간(일) = 대여 시각 - 가입일 / 음수(가입 전 대여 = 데이터 오류) 는 0 으로 보정
    #   .dt.days : 시간 차이에서 일 수만 꺼냄
    #   clip(lower=0) : 0 보다 작은 값은 0 으로
    df["join_days"] = (df["rent_time"] - df["join_date"]).dt.days.clip(lower=0)

    # district 결측(배치 대여소 없는 자전거) -> '미배치' 범주로
    df["district"] = df["district"].fillna("미배치")

    return df

def build_dataset():
    """ 피처와 정답이 준비 된 데이터를 반환 (STEP 1 + STEP 2) """
    return merge_users(add_features(load_rentals()), load_users())


# 분할 / 인코딩 ---------------------------------------------------------------------------------------
def time_split(df, test_size=0.2):
    """
    시점(rent_time) 기준으로 학습용, 테스트용 분리 (STEP 4)
    Return
        학습용_데이터, 테스트용_데이터, 분리기준값
    """
    cutoff = df["rent_time"].quantile(1 - test_size)

    train = df[df["rent_time"] <= cutoff].reset_index(drop=True)
    test = df[df["rent_time"] > cutoff].reset_index(drop=True)

    return train, test, cutoff

def encode(train, test, extra=None):
    """
    범주형 피처를 원핫 인코딩하고, 테스트 열 구성을 학습에 맞춰서 (X_train, X_test) 반환
    Args
        extra : 추가로 넣을 숫자형 열 목록 (STEP 5 누수 실험용)
    """
    cols = NUM_FEATURES + (extra or []) + CAT_FEATURES

    # 범주형 열만 원핫 인코딩 (True/False -> 1/0)
    X_train = pd.get_dummies(train[cols], columns=CAT_FEATURES).astype(int)
    X_test = pd.get_dummies(test[cols], columns=CAT_FEATURES).astype(int)

    # 테스트 열 구성을 학습에 맞추기
    #   학습에는 있는데 테스트에 없는 열 -> 0 으로 채워서 추가
    for col in X_train.columns:
        if col not in X_test.columns:
            X_test[col] = 0

    # 학습 열 순서대로 선택 (학습에 없던 테스트 전용 열은 이때 빠짐)
    X_test = X_test[X_train.columns]

    return X_train, X_test