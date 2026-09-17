"""
    Pandas 판다스
        Numpy(넘파이) 기반의 데이터 구조를 제공하고,
        SQL처럼 다양한 조작 및 분석 기능을 제공하는 라이브러리
"""
import pandas as pd

from utils.config import RAW_PATH, ENCODING

"""
* Serise (시리즈)
    - 라벨링 된 1차원 배열 구조
    - 인덱스(라벨)를 따로 지정하지 않으면 정수로 자동 생성 됨(0 ~ )
"""
datas = [10, 20, 30, 40]

# 시리즈 생성
s = pd.Series(datas)
print(s)

"""
인덱스  데이터
0       10
1       20
2       30
3       40
dtype: int64
"""

print(f"index : {s.index} / {s.index.to_list()}")   # 인덱스 정보
print(f"values : {s.values} ({type(s.values).__name__})")
print()

# name : 시리즈의 이름, 데이터프레임 생성 시 열 이름으로 사용 됨
s = pd.Series(datas, name="sample")
print(s)
print(f"name : {s.name}")
print(f"index : {s.index}")
print(f"values : {s.values}")
print()

s = pd.Series(datas, index=['a', 'b', 'c', 'd'])
print(s)
print(f"index : {s.index}")
print()

s1 = pd.Series([10, 20, 30], index=['x', 'y', 'z'])
s2 = pd.Series([1, 2, 3], index=['z', 'y', 'x'])
print("------ s1 ------")
print(s1)
print("------ s2 ------")
print(s2)
print()

# 연산이 수행될 때 순서가 아닌 인덱스를 기준으로 연산이 수행 됨
#   -> 인덱스가 같은 것끼리 연산
print(f"s1 + s2 = \n{s1 + s2}")
print()

s3 = pd.Series([1, 2], index=['x', 'w'])
print("------ s3 ------")
print(s3)
print()

print(f"s1 + s3 = \n{s1 + s3}")
# 연산이 수행 될 때, 동일한 인덱스가 없을 경우 NaN이 됨

print("=" * 60)
"""
* DataFrame : 2차원 테이블 구조
    - Series를 여러 개 묶어서 만든 2차원 구조
    - 행(인덱스)과 열(컬럼)로 구성
"""

data = {
    "이름": ["하루견과", "뼈건강비타민", "페레로로쉐"],
    "가격": [2000, 4000, 3500],
    "재고:": [10, 5, 20]
}

# DataFrame 생성
df = pd.DataFrame(data)
print(df)
print()

print(f"dtypes : \n{df.dtypes}")    # 각 열의 데이터 타입
print(f"shape : {df.shape}")        # 행, 열의 개수
print(f"index : {df.index}")        # 행 인덱스
print(f"columns : {df.columns}")    # 열 이름(컬럼명)

print("=" * 60)

# 파일로부터 읽어와서 생성
# * CSV (Comma Seperated Values) : 쉼표로 구분되어 있는 데이터
# pd.read_csv(파일명) => DataFrame
df = pd.read_csv(RAW_PATH, encoding=ENCODING)

print(df.head())        # 위에서부터 5개의 데이터 조회
print(f"close dtype : {df['close'].dtypes}")
print(f"date dtype : {df['date'].dtypes}")
print("=" * 60)

# read_csv 는 열마다 타입을 추론하는데, 한열에 숫자가 아닌 값이 하나라도 있으면
#                                     그 열은 전체를 문자열로 읽음
# 옵션을 추가하면 조금 더 명확하게 타입을 추론해서 가져올 수 있음
df = pd.read_csv(RAW_PATH, 
                 encoding=ENCODING, 
                 parse_dates=["date"],      # 'date' 열은 'datetime'으로 처리
                 na_values=["N/A", "-"],    # 결측으로 취급할 문자들
                 thousands=","              # '1,000,000' 형태를 숫자로 처리
                 )

print(df.head())
print(f"close dtype : {df['close'].dtypes}")
print(f"date dtype : {df['date'].dtypes}")

print(f"date unique : {df['date'].unique()}")   # 중복 제거한 결과
# date 열에는 2026-09-17, 20260917, 2026.09.17 gudxoemffh 섞여있음
#       -> parse_dates 옵션은 해당 열 전체가 같은 형식일 경우에만 적용 됨
#       -> 형식이 섞여있을 경우 별도로 처리를 해줘야 함
print()

df['date'] = pd.to_datetime(df['date'], format='mixed')
print(f"to_datetime dtype : {df['date'].dtypes}")
print("-" * 60)
"""
read_xxx 의 옵션
    - encoding      : utf-8 / utf-8-sig
    - parse_dates   : 특정 열(날짜)을 datetime 으로 변환
    - na_values     : 겉측으로 취급할 문자열 지정
    - thousands     : 천 단위 구분자 제거(천단위 구분자가 있는 데이터를 숫자로 변환)
"""

# 데이터를 불러온 후 점검하기
# df.head(n)    : 위에서부터 n개의 데이터를 조회 (생략 시 5개)
print(df.head(3))
print()
# df.shape      : 불러온 데이터의 행, 열 개수
print(df.shape)
print()
# df.info()     : 불러온 데이터의 컬럼별 데이터 개수, 타입등을 확인
df.info()
print()
# df.dtypes     : 컬럼별 데이터 타입
print(df.dtypes)