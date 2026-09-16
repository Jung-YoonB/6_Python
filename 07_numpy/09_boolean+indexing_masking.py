"""
    불리언 인덱싱과 마스킹
"""
import numpy as np

from load_utils import load_matrix, load_column

arr = np.array([10, 25, 30, 15, 40])
mask = arr > 20

print(f" arr : {arr}")
print(f" arr > 20 : {mask}")

print(f" arr[mask] : {arr[mask]}")
# 대괄호 안에 mask를 넣으면 True에 해당하는 위치 값들만 배열로 만들어줌
print(f" True 개수 : {mask.sum()}")
print('-' * 60)

matrix = load_matrix()

big = matrix > 500_000
print(f"matrix > 500_000  :: shape {big.shape}, dtype {big.dtype}")
print(f"True의 개수 : {big.sum()} 개 / 전체: {matrix.size} 개")

print(f"{matrix[big].shape}")   # 2차원 배열에 불리언 인덱싱 -> 1차원 배열 추출

print('-' * 60)

# np.diff(배열, axis=1) : 인접한 두 요소의 차를 계산 (오른쪽 - 왼쪽)
#   axis=1 이면 같은 행에서 열 방향으로 차(-)를 구함
#   결과: (120, 749)
result = np.diff(matrix, axis=1) / matrix[:,:-1]    # 일간 수익률
print(result)

cond1 = result > 0.03    # 3% 넘게 오른 경우

# 거래량(volume)
volumes = load_column("volume")[:,1:]   # (120,750) -> (120,749) 첫날 제외
cond2 = volumes > 2_000_000     # 거래량이 200만주(건) 초과

# and --> &     /   or  --> |   / not  --> ~
both = cond1 & cond2
print(f" 수익률이 3% 이상이고, 거래량이 200만주 이상 : {both.sum()}")
print(f" 수익률이 3%가 되지 않는 건수 : {(~cond1).sum()}")

print('-' * 60)

sample = np.array([0.05, -0.02, 0.0, 0.12, -0.15])
sample2 = np.where(sample > 0, "up",
         np.where(sample < 0, "down", "keep"))
print(sample2)