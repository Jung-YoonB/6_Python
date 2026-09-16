"""
    axis : 차원의 축

    axis = 0   행 방향
    axis = 1   열 방향
"""
import numpy as np

from load_utils import load_matrix

# 2행 3열의 2차원 배열 생성
m = np.array([[1,2,3], [4,5,6]])
print(f"m : \n{m}")

print(f" sum : {m.sum()}")
print(f" sum(axis=0) : {m.sum(axis=0)} 열 기준(세로로 더함)")
print(f" sum(axis=1) : {m.sum(axis=1)} 행 기준(가로로 더함)")

print(f" m.shape : {m.shape}")
print(f" sum(axis=0) : {m.sum(axis=0).shape} 행이 사라짐!")
print(f" sum(axis=1) : {m.sum(axis=1).shape} 열이 사라짐!")
# axis 는 사라지는 축!
#    shape : (120, 750)
#       axis=0 => (750,)
#       axis=1 => (120,)
print("=" * 60)

matrix = load_matrix()
print(f"matrix.shape : {matrix.shape}")
print(f" 전체 평균 : {matrix.mean()}")
print(f" 날짜별 평균 : {matrix.mean(axis=0)[:5]} {matrix.mean(axis=0).shape}")
print(f" 종목별 평균 : {matrix.mean(axis=1)[:5]} {matrix.mean(axis=1).shape}")

print('-' * 60)
# 줄인 축을 없애지 않고 유지 (크기를 1로 남겨둠)
#   keepdims=True
a = matrix.mean(axis=1)
b = matrix.mean(axis=1, keepdims=True)

print(f"a : {a.shape}")
print(f"b : {b.shape}")

# 값은 동일함. 축이 사라지지 않고 남아있다는 것만 다름.
# (120,750) 행렬과 연산을 수행하기 위해서 축을 유지시켜야 함!
# (120,) 이면 (120, 750)와 브로드 캐스팅 실패!