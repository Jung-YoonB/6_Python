"""
    넘파이 배열 생성
"""
import numpy as np

from load_utils import load_one_stock

print(f"리스트를 배열로 생성 : {np.array([1000, 3000, 4500])}")
print(f"0으로 채워서 배열 생성: {np.zeros(5)}")  # float 타입으로 생성
print(f"0으로 채워서 배열 생성: {np.zeros(5, dtype='int64')}")
print(f"1로 채워서 배열 생성: {np.ones(5)}")    # float 타입으로 생성
print(f"특정 값으로 채워서 배열 생성: {np.full(5, 7)}")
print(f"0부터 9까지 정수를 생성하여 배열 생성: {np.arange(10)}")
print(f"0부터 100까지 5등분하여 배열 생성: {np.linspace(0, 100, 5)}")

print("=" * 60)

# --------- 속성 ----------
arr = np.array([12300, 44400, 79000])
print(f"arr : {arr}")

print(f"배열 형태 (shape) : {arr.shape}")  # 튜플
print(f"차원 수 (ndim) : {arr.ndim}")
print(f"데이터 개수 (size) : {arr.size}")
print(f"데이터(요소) 타입 (dtype) : {arr.dtype}")

"""
    shape 해석

    (n,)    -> 1차원 배열, n개
    (n, m)  -> 2차원 배열, n행 m열
        (4, 1) : 4행 1열   / (1, 4) : 1행 4열
    (x, y, z) -> 3차원 배열, x면 y행 z열
    ...
"""

print("=" * 60)

# reshape(shape)
for shape in [(4,), (4,1), (1,4)]:
    # np.arange(4) -> [0 1 2 3]
    a = np.arange(4).reshape(shape)

    print(f" shape: {str(shape)} / ndim: {a.ndim} / {a}")

print("=" * 60)

# 첫 번째 종목의 데이터 불러오기
prices = load_one_stock(0)
print(f" 첫 종목의 750일 종가")
print(f"앞의 5개 데이터 : {prices[:5]}")
print(f"shape : {prices.shape}")
print(f"ndim : {prices.ndim}")
print(f"size : {prices.size}")
print(f"dtype : {prices.dtype}")