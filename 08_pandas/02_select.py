"""
    조회하기
"""
import pandas as pd

from utils.loader import load_csv

df = load_csv()
print(df.head())

# nunique()     : 중복 제거한 후 개수
print(f"{len(df)} 행 / {df['code'].nunique()} 종목")

# 마지막 거래일 -> 거래일: date / 최댓값 -> 최근 날짜
last_day = df['date'].max()
print(f"마지막 거래일 : {last_day}")

# 마지막 거래일의 기록 -> 거래일이 마지막 거래일과 일치하는 항목
last_history = df[df['date'] == last_day].reset_index(drop=True)
print(f"기준일: {last_day} / {len(last_history)}개 종목")

# print(type(last_fistory))
print(last_history.head())

# 특정 열을 선택하여 조회하기
# SQL       : SELECT code, close, changeRate FROM prices
# Pandas    : df[['code', 'close', 'changeRate']]
print(last_history[['code', 'close', 'changeRate']].head())

# 대괄호 개수에 따른 결과 타입(하나 vs 둘)
one = last_history['close']
two = last_history[['close']]

print(f"last_history['close'] -> {type(one).__name__} / shape : {one.shape}")
print(f"last_history[['close']] -> {type(two).__name__} / shape : {two.shape}")

"""
    바깥 대괄호는 데이터프레임에서 조회(꺼내기)하기 위해 사용
    안쪽 대괄호는 "목록"을 지정하기 위해 사용
"""

print("=" * 60)

# 조건을 지정하여 조회하기
# SQL       : WHERE close > 100000
# Pandas    : df[df['close'] > 100000]
exps = last_history[last_history['close'] > 100_000]
print(f"결과: {len(exps)} 건")
print(exps[['code', 'close']].to_string(index=False))

result = last_history['close'] > 100_000
print(f"결과 : {result.sum()} 건")
print()

# SQL       : WHERE 조건1 AND 조건2 / WHERE 조건1 OR 조건2
# Pandas    : df[(조건1) & (조건2)] / df[(조건1) | (조건2)]

# 기준 데이터 : 마지막 거래일 기록
#   - 'close'가 50000을 초과하고, 'changeRate' 가 0을 초과하는 데이터
both = last_history[(last_history['close'] > 50_000) & (last_history['changeRate'] > 0)]
print(f"결과 : {len(both)} 건")
print(both[['code', 'close', 'changeRate']].head(3))
print()
"""
    SQL                         |       Pandas
    --------------------------------------------------------------------------------------
    ORDER BY 컬럼               |       df.sort_valuews(컬럼, ascending=T/F)
    LIMIT 개수                  |       df.head(개수)
    DISTINCT 컬럼               |       df[컬럼].unique() 결과 / de[컬럼].nunique() 개수
    COUNT(*) ... GROUP BY ~     |       df[컬럼].value_counts()
    IN(...)                     |       df[컬럼].isin([...]) 
"""
df = last_history
print("------ 가장 비싼 3개 종목 ------")
top = df.sort_values("close", ascending=False).head(3)
print(top[['code', 'close']])
print()

print("------ 가장 많이 오른 3개 종목 ------")      # changeRate
rise = df.sort_values("changeRate", ascending=False).head(3)
print(rise[['code', 'close', 'changeRate']])
print()

print("------ 종가 기준, 1만 ~ 5만 사이의 종목 ------")
result = df[(df['close'] >= 10_000) & (df['close'] <= 50_000)]
print(f"조회 결과 : {len(result)}")
# print(df['close'].between(10_000, 50_000))      # Series
result = df[df['close'].between(10_000, 50_000)]
print(f"조회 결과: {len(result)}")
print()

print("------ 종목 코드가 'G0001', 'G0050', 'G0100' 만 조회 ------")
# print(df['code'].isin(['G0001', 'G0050', 'G0100']))     # Series
result = df[df['code'].isin(['G0001', 'G0050', 'G0100'])]
print(f"조회 결과 : \n{result}")
print()

print("=" * 60)

"""
* loc vs iloc
    - 행/열 선택(인덱싱) 및 범위 선택(슬라이싱)
    - loc (Lable Location)      : 라벨 기반 선택
        => df.loc[행_선택, 열_선택]
            * 행 선택   : 인덱스 라벨 (숫자, 문자열, ...)
            * 열 선택   : 컬럼 라벨 (열 이름, 문자열, ...)
                --> 슬라이싱 시 "끝 라벨" 포함
    - iloc (Integer Location)   : 정수(위치) 기반 선택
        => df.iloc[행_선택, 열_선택]
            * 행 선택   : 0 부터 시작하는 위치 (숫자)
            * 열 선택   : 0 부터 시작하는 위치 (숫자)
                --> 위치 기반으로 기존 슬라이싱과 동일, 끝 위치 미포함(제외) 
"""
print("------ loc ------")
print(df.loc[0:2])      # 3건

print()
print("------ iloc ------")
print(df.iloc[0:2])     # 2건

print()
# loc 방식은 행 조건, 열 선택이 가능
result = df.loc[df['close'] > 200_000, ['code', 'close', 'volume']].head(3)
print(result)

print("=" * 60)

# 인덱스 설정(변경) : df.set_index(컬럼)
indexed = df.set_index('code')
print(indexed.head(3))

# 'G0001' 종목의 'close', 'changeRate' 만 조회
print(indexed.loc['G0001', ['close', 'changeRate']])