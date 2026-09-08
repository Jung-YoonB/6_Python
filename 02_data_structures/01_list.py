"""
    리스트
"""

# 리스트 데이터 표현: 대괄호 [] 사용
colors = ["black", "red", "blue"]

print(f"colors -> {colors}")

# 첫 번째 요소 출력
print(f"1th : {colors[0]}")

# 마지막 요소 출력
print(f"마지막 : {colors[-1]}")

print(f"{colors[0:2]}")

# 다양한 타입의 데이터를 담을 수 있음
mixed = [100, "Hello", True, [1, 2, 3]]

print(f"mixed : {mixed}")

# 리스트 상태에 따라 bool 타입 확인
temp = []
print(f"mixed --> {bool(mixed)}")
print(f"temp --> {bool(temp)}")

print("=" * 60)

items = ["에이스", "아이비", "코피코"]

print(f"items --> {items}")

# 데이터 추가 : append(), insert(), extend()
items.append("오감자")
print(f"append - 맨뒤에 추가 : {items}")

items.insert(2, "쿠크다스")
print(f"insert - 지정한 위치에 추가 : {items}")

items.extend(["꼬북칩", "허니버터칩"])
print(f"extend - 여러 개의 데이터를 추가 : {items}")

# 수정 / 삭제
print("=" * 60)
items[0] = "ACE"
print(f"특정 인덱스를 지정하여 값을 변경(수정) : {items}")

items.remove("코피코")
print(f"remove - 값으로 삭제 : {items}")

# ValueError: list.remove(x): x not in list --> items.remove("코피코")
#                                           --> 지우려는 데이터가 없을 경우

snack = items.pop()
print(f"pop - 맨 뒤에 데이터를 삭제 후 반환 : {snack} / {items}")

del items[0]
print(f"del - 인덱스로 삭제 : {items}")