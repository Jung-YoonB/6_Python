"""
    집합 set
"""

# 중복 불가, 순서 X, 수정 O
nums = {1, 2, 3, 3, 3, 4, 2}
print(f"nums : {nums}")

# 비어 있는 상태 표현
empty1 = {}     # 딕셔너리
empty2 = set()

print(f"empty1: {type(empty1)}")
print(f"empty2 set() : {type(empty2)}")

nums = [1, 2, 3, 3, 3, 4, 2]
print(f"원본 데이터 : {nums}")
print(f"중복 제거 : {set(nums)}")
print(f"중복 제거 후 리스트화 : {list(set(nums))}")

print()

# 집합 연산
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

print(f"합집합 | : {a | b}")
print(f"교집합 & : {a & b}")
print(f"차집합 - : {a - b}")
print()

# 데이터 변경
data = {1, 2}
print(f"data: {data}")

# 추가 : add
data.add(3)
print(f"data 3 추가 : {data}")

data.add(3)
print(f"data 3 추가 리트 : {data}")

# update
data.update([4, 5])
print(f"data 리스트로 업데이트 : {data}")

data.update([4, 5, 6, 7])
print(f"data 리스트로 중복 포함 업데이트 : {data}")

# 삭제 discard
data.discard(1)
print(f"data 1 제거 : {data}")

data.discard(99)
print(f"data 없는 숫자 제거 : {data}")