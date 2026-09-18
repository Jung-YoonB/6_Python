"""
    그룹화 기초 (groupby)
        - agg / transform
"""
import pandas as pd
from utils.loader import load_csv

# 출력창 크기 설정
pd.set_option("display.width", 130)

# 데이터 불러오기
df = load_csv()


# agg : 그룹 당 한 줄(행)

# 'code' 열을 기준으로 평균 조회
# SQL       : SELECT code, AVG(close) FROM prices GROUP BY code
# Pandas    : df.groupby('code')['close'].mean()
mean_by_code = df.groupby('code')['close'].mean()
print(f"종목 코드별 평균 : {len(mean_by_code)} 행")
print(mean_by_code.head().round())
print()

# 여러개를 한번에 집계
summary = df.groupby('code').agg(
            평균종가=("close", "mean"),
            최고가=("close", "max"),
            거래일수=("date", "count")
        )

print(f"통계 결과 : {len(summary)} 행")
print(summary.head())
print()
"""
.agg(
    새로운_열_이름=("계산할_기존_열_이름", "적용할_함수명"),
    ...
)
"""

# transform : 결과 행이 원본과 같은 길이로 반환
df['code_mean'] = df.groupby('code')['close'].transform('mean')
print(df.head())
print(df.tail())
print()
"""
* agg       : 여러 집계를 한 번에 확인하고자 할 때 사용
                de.groupby(기준_열).agg(새로운_열_이름=(대상_열, 집계함수), ...)
                    => 그룹 수만큼 행 반환
                    => 그룹화 하여 어떤 결과를 요약해서 볼 수 있는
                        --> 요약한 결과 확인 시 사용

* transform : 그룹별로 계산하되, 기존 df와 연산을 하기위해서 결과를 각 행의 원래 자리에 표시해줌
                df.groupby(기준_열)[대상_열].transform(집계함수)
                    => 데이터 개수만큼 행 반환
                    => 결과를 가지고 다음 연산을 수행할 수 있음
                        --> 집계 결과를 통한 다른 연산 수행 시 사용
"""