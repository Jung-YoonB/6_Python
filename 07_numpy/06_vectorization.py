"""
    벡터화 연산

    넘파이의 핵심 특징.
    반복문 없이 연산 수행 가능. (빠름)
"""
import numpy as np
from load_utils import load_dates, load_codes, load_one_stock

dates = load_dates()        # 거래일
codes = load_codes()        # 종목 코드
prices = load_one_stock(0)  # 첫 종목의 750일 종가


a = np.array([10,20,30,40])
b = np.array([1,2,3,4])
print(f"a : {a}\nb : {b}")
print(f"a * 2 = {a * 2}")   # [20 40 60 80]
print(f"a + b = {a + b}")   # [11 22 33 44]
print(f"a > 25 = {a > 25}") # [False False True True]

# 유니버설 함수 (ufunc) : 배열의 모든 요소에 하나씩 적용되는 함수
x = np.array([1,4,9,16])
print(f"x : {x}\nsqrt : {np.sqrt(x)}")  # sqrt() : 제곱근

x = np.array([1.123423, 4.23423, 9.25234, 16.2356234])
print(f"x: {x}\nround : {np.round(x, 3)}") # round() : 반올림
# round(배열, n) : 소수점 n+1번째 자리에서 반올림

x = np.array([-1, 4, -9, 16])
print(f"x: {x}\nabs : {np.abs(x)}")    # abs() : 절대값
print("=" * 60)

# 집계 함수
print(f"==== {codes[0]} 750일 종가 ====")
print(f" 전체 합 : {prices.sum():,}")
print(f" 전체 평균 : {prices.mean():,.0f}")
print(f" 전체 표준편차 : {prices.std():,.0f}")
print(f" 최저가 : {prices.min():,.0f}")
print(f" 최고가 : {prices.max():,.0f}")

max_idx = prices.argmax()   # 가장 큰 값이 있는 위치
min_idx = prices.argmin()   # 가장 작은 값이 있는 위치

print(f"최고가 : {prices[max_idx]:,}원 ({dates[max_idx]})")
print(f"최저가 : {prices[min_idx]:,}원 ({dates[min_idx]})")

"""
    수익률 = (오늘 - 어제) / 어제

    prices[1:] 둘째날부터 끝까지 (오늘)
    prices[:-1] 첫날부터 끝에서 두번째까지 (어제)
"""

result = (prices[1:] - prices[:-1]) / prices[:-1]  # 전일 대비 변화량

print(f"== 일간 수익률 {len(result)} ==")
print(f" 평균 : {result.mean() * 100:.4f}")
print(f" 표준편차 : {result.std() * 100:.4f}")
print(f" 최대 상승 : {result.max() * 100:.4f} ({dates[result.argmax() + 1]})")
print(f" 최대 하락 : {result.min() * 100:.4f} ({dates[result.argmin() + 1]})")