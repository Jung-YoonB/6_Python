"""
    넘파이 배열의 인덱싱과 슬라이싱

    - 기본 인덱싱을 리스트와 동일
    - 슬라이싱은 리스트와 달리 복사본이 아님
        원본 배열의 뷰(view) 반환
"""
import numpy as np

from load_utils import load_one_stock

arr = np.array([10, 20, 30, 40, 50])
print(f"arr : {arr}")
print()

print(f"첫 번째 위치 : {arr[0]}")
print(f"마지막 위치 : {arr[-1]}")
print()

print(f"1 ~ 2 위치 : {arr[1:3]}")
print(f"0 ~ 2 위치 : {arr[:3]}")
print(f"3 ~ 끝까지 : {arr[3:]}")
print()

print(f"2칸 건너뛰면서 슬라이싱 : {arr[::2]}")
print(f"역순으로 슬라이싱 : {arr[::-1]}")

print("=" * 60)

data_list = [1, 2, 3, 4]
part_list = data_list[1:3]  # [2, 3]
part_list[0] = 999

print(f"원본 : {data_list} \n슬라이싱: {part_list}")
print()

arr = np.array(data_list)
view = arr[1:3]
view[0] = 999

print(f"원본 배열: {arr} \n슬라이싱: {view}")
print()

arr = np.arange(10)
view = arr[2:5]
copy = arr[2:5].copy()

copy[0] = 999
print(f"원본 배열: {arr} \n복사본: {copy}")
print()

# .base 속성
#   -> 이 배열이 다른 배열의 메모리를 참조하고 있는지 여부 확인
print(f"view --> {view.base is arr}")   # True, 메모리를 공유(같은 데이터)
print(f"copy --> {copy.base is arr}")   # False, 메모리에 복사(독립 된 데이터)
print()

rsh = arr.reshape(2, 5)
print(f"reshape --> {rsh.base is arr}") # True

rv = arr.ravel()
print(f"ravel --> {rv.base is arr}")    # True

ft = arr.flatten()
print(f"flatten --> {ft.base is arr}")  # False

print("=" * 60)

def normalize_wrong(arr):
    """
    [비정상 코드]
    마지막 5개의 데이터를 기준으로 최솟값으로 값을 뺀 후 배열을 반환
    """
    last_5 = arr[-5:]   # 뷰 형태로 반환: 원본 메모리 공유
    last_5 -= last_5.min()
    return last_5

def normalize_safe(arr):
    """
    [안전한 코드]
    슬라이싱 단계에서 .copy() 하여 복사본으로 처리
    """
    last_5 = arr[-5:].copy()   # 복사본 반환: 독립 된 메모리
    last_5 -= last_5.min()
    return last_5

prices = load_one_stock(0)[:10].copy()
print(f"prices : {prices}")

backup = prices.copy()
result = normalize_wrong(prices)
print(f"------ normalize_wrong ------")
print(f"원본 : {prices}")
print(f"결과 : {result}")

result = normalize_safe(backup)
print(f"------ normalize_safe ------")
print(f"원본 : {backup}")
print(f"결과 : {result}")

"""
    뷰 (슬라이싱, ravel, reshape)
        메모리  |   원본과 공유 (하나의 데이터)
        수정    |   뷰를 수정하면 원본도 변경 됨
        속도    |   빠름 (복사 과정이 불필요)
    복사 (copy, flatten)
        메모리  |   새로운 메모리 공간에 복제 (독립 된 두개의 데이터)
        수정    |   복시본을 수정해도 원본은 그대로 유지
        속도    |   상대적으로 느림 (복사 과정 필요)
"""