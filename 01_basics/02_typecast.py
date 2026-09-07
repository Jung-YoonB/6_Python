"""
    형변환
"""

print("=" * 60)
print("문자열 --> 숫자")
print("=" * 60)

print(f"'100' --> {int('100')}")
print(f"'6.28' --> {float('6.28')}")

# ValueError : print(f"'6.28' --> {int('6.28')}")
print(f"'6.28' --> {int(float('6.28'))}")
# 실수 형태의 문자열은 바로 int 변환이 불가
#       -> float 변환 후 int 변환

print("=" * 60)
print("숫자 --> 문자열")
print("=" * 60)

print(f"{str(1000)}")
# 숫자와 문자열은 더하기(+) 연상 불가 : print(1000 + "원")
print(str(1000) + "원")
print(f"{1000}원")

print("=" * 60)
print("bool 타입 변환")
print("=" * 60)

falsy_values = [0, 0.0, "", [], {}, (), set(), None, False]
truthy_values = [1, -1, "0", "False", [0], " "]
print("== falsy (거짓으로 취급되는 값) ==")
for v in falsy_values:
    print(f"{str(v):<10} -> {bool(v)}")

print("== truthy (참으로 취급되는 값) ==")
for v in truthy_values:
    print(f"{str(v):<10} -> {bool(v)}")
