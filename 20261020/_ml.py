"""
    데이터 로드, 결측 처리, 인코딩, 혼동행렬 기능을 모아두는 모듈
"""
import pandas as pd

from _config import path, ENCODING

# 공통 규칙------------------------------------------------------------------------------------
SEED = 42           # random_state=42
TEST_SIZE = 0.2     # test_size=0.2

# 식별용 컬럼 (피처 사용 X)
ID_COLS = ["Number", "Name"]

# 능력치 6개 (합계 = Total)
STATS = ["HP", "Attack", "Defense", "Sp_Atk", "Sp_Def", "Speed"]

# 범주형 피처 (categorical 범주형 문자열, 원핫 인코딩 필요)
CAT_FEATURES = ["Type_1", "Type_2", "Color", "Egg_Group_1", "Egg_Group_2", "Body_Style"]


# 문제 [1] 회귀 -------------------------------------------------------------------------------
# 정답(y)
REG_TARGET = "Total"
 
# 능력치 6개, Total, 식별용 컬럼 제외 회귀 모델에 넣을 피처 전체 list
#   -> encode()에 전달 후, 범주형(CAT_FEATURES) 만 원핫으로 숫자 변환 후 모델에 들어감
REG_FEATURES = ["Type_1", "Type_2", "Generation", "isLegendary", "Color", "hasGender", "Pr_Male",
                "Egg_Group_1", "Egg_Group_2", "hasMegaEvolution", "Height_m", "Weight_kg",
                "Catch_Rate", "Body_Style"]
 
# [1-3] 상관계수를 구할 수치형 변수
REG_NUM_COLS = ["Generation", "Height_m", "Weight_kg", "Catch_Rate", "Pr_Male"]


# 문제 [2] 분류 -------------------------------------------------------------------------------
# 정답(y)
CLS_TARGET = "isLegendary"

# Total 제외 분류 모델에 넣을 피처 전체 list
CLS_FEATURES = STATS + ["Type_1", "Type_2", "Generation", "Color", "hasGender", "Pr_Male",
                        "Egg_Group_1", "Egg_Group_2", "hasMegaEvolution", "Height_m", "Weight_kg",
                        "Catch_Rate", "Body_Style"]


# 데이터 로드 ---------------------------------------------------------------------------------
def load_pokemon():
    """ pokemon_alopez247.csv 를 읽어서 DataFrame 으로 반환 """
    return pd.read_csv(path("pokemon_alopez247.csv"), encoding=ENCODING)


# 결측 처리 -----------------------------------------------------------------------------------
def fill_missing(df):
    """
    결측치를 채워서 반환 (공통 과제 4)
        - Type_2, Egg_Group_2 : 결측 = "보조 타입/두 번째 알 그룹이 없음" -> 'None' 범주로
        - Pr_Male             : 결측 = "성별이 없는 포켓몬" (hasGender=False) -> -1 로
                                * 0 은 "수컷 확률 0% = 전부 암컷" 이라는 다른 뜻이 되므로 사용 X
    """
    df = df.copy()
 
    df["Type_2"] = df["Type_2"].fillna("None")
    df["Egg_Group_2"] = df["Egg_Group_2"].fillna("None")
    df["Pr_Male"] = df["Pr_Male"].fillna(-1)
 
    return df
 
 
def build_dataset():
    """ 결측 처리까지 끝난 데이터를 반환 """
    return fill_missing(load_pokemon())
 
 
# 인코딩 --------------------------------------------------------------------------------------
def encode(df, features):
    """
    피처만 골라서 범주형 열을 원핫 인코딩한 X 를 반환
    """
    cats = [c for c in CAT_FEATURES if c in features]   # features 안에 있는 범주형 열만
 
    # 범주형 -> 원핫 (True/False), bool 열(isLegendary 등) 포함 전부 숫자(0.0/1.0)로
    return pd.get_dummies(df[features], columns=cats).astype(float)
 
 
# 평가 ----------------------------------------------------------------------------------------
def confusion_table(y_true, pred):
    """
    혼동행렬을 DataFrame 으로 반환 (행 = 실제, 열 = 예측)
    """
    tp = ((pred == 1) & (y_true == 1)).sum()    # 전설 예측 + 실제 전설
    fn = ((pred == 0) & (y_true == 1)).sum()    # 일반 예측 + 실제 전설   -> 놓침
    fp = ((pred == 1) & (y_true == 0)).sum()    # 전설 예측 + 실제 일반   -> 헛경보
    tn = ((pred == 0) & (y_true == 0)).sum()    # 일반 예측 + 실제 일반
 
    return pd.DataFrame([[tn, fp], [fn, tp]],
                        index=["실제 일반(0)", "실제 전설(1)"],
                        columns=["예측 일반(0)", "예측 전설(1)"])