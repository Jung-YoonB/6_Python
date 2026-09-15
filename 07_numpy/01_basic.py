"""
    Numpy (넘파이)
    다차원 배열을 다룰 수 있는 기능을 제공하는 라이브러리
    넘파이 배열 : ndarray
"""
import numpy as np

# 파이썬 리스트에는 다양한 타입의 데이터를 담을 수 있음
data_list = [1, "오", 3.0, [4]]
print(f"data_list : {data_list}")
print(f"각 요소 별 타입 : {[type(x).__name__ for x in data_list]}")

data_list2 = [10, 20, 30, 40]

"""
print("=" * 60)
for d1, d2 in zip(data_list, data_list2):
    print(f"{d1} + {d2} = {d1 + d2}")
print("=" * 60)
"""
# 파이썬의 리스트는 데이터를 구분하지 않고 담을 수 있는 점이 편리 할 수 있지만
#   다른 리스트와 연산을 하고자 할 때는 문제가 될 수 있음

# 넘파이 배열 (ndarray) 은 데이터 타입이 하나로 고정된 구조 -> 연산이 쉬움
print("=" * 60)
print("넘파이 배열 ndarray")
print("=" * 60)

arr = np.array([1, 2, 3, 4])

print(f"arr : {arr}")
print(f"배열 타입 : {arr.dtype}")
print()

arr2 = np.array([5, 6, 7, 8])
print(f"arr2 : {arr2}")
print()

"""
for d1, d2 in zip(arr, arr2):
    print(f"{d1} + {d2} = {d1 + d2}")
"""

# 벡터화 연산
print(f"arr + arr2 = {arr + arr2}")
# 넘파이 배열은 자바의 배열과 비슷하지만, 연산 수행 시 반복문을 사용하지 않고 배열 단위의 연산이 가능

print("=" * 60)

# 넘파이 배열의 차원, 형태

# 0 차원 배열 -> 스칼라(단일 값)
arr_0d = np.array(42)
print(f"0 차원 배열: {arr_0d}, 차원: {arr_0d.ndim}, 형태: {arr_0d.shape}")

# 1 차원 -> 벡터 (0차원의 모임)
arr_1d = np.array([1, 2, 3])
print(f"1 차원 배열: {arr_1d}, 차원: {arr_1d.ndim}, 형태: {arr_1d.shape}")

# 2 차원 -> 행렬 (1차원의 모임)
arr_2d = np.array([[1, 2, 3], [4, 5, 6]])
print(f"2 차원 배열: \n{arr_2d}\n, 차원: {arr_2d.ndim}, 형태: {arr_2d.shape}")

print("=" * 60)

n = 100_000     # 숫자 표현시 _로 구분 가능 / 단위가 클 경우 , 대신 사용
print(f"n : {n}")

# 리스트랑 배열을 0 ~ 99_999 데이터로 생성
list_10m = list(range(n))
arr_10m = np.arange(n)

print(f"list_10m : {list_10m[:5]} ... {list_10m[-5:]}")
print(f"arr_10m : {arr_10m[:5]} ... {arr_10m[-5:]}")
print()

# 메모리 크기 비교
import sys

list_container = sys.getsizeof(list_10m)
int_obj = sys.getsizeof(list_10m[0])
list_bytes = list_container + (int_obj * n)

arr_bytes = arr_10m.nbytes

print(f"데이터 {n:,}개 기준 ")
print(f" - 리스트 : {list_bytes / 1024 / 1024:6.2f} MB")
print(f" - 배열 : {arr_bytes / 1024 / 1024:6.2f} MB")

# 10만 개 기준으로 약 2 ~ 3 MB 차이