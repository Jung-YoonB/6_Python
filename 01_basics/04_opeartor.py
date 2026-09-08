"""
    연산자
"""

print("=" * 60)
print("산술 연산자")
print("=" * 60)

print(f"7 + 3 = {7 + 3}")
print(f"7 - 3 = {7 - 3}")
print(f"7 * 3 = {7 * 3}")
print(f"7 / 3 = {7 / 3}")       # 실수 나눗셈
print(f"7 // 3 = {7 // 3}")     # 정수 나눗셈
print(f"7 % 3 = {7 % 3}")       # 나머지 연산
print(f"7 ** 3 = {7 ** 3}")     # 거듭제곱 연산, 7을 3번 곱함

print()

print(f"실수 나눗셈 타입 : {type(7 / 3)}")

print(f"실수 나눗셈 타입 : {type(6 / 3)}")  # 값이 딱 떨어져도 타입은 항상 float

print(f"-7 / 3 = {-7 / 3}")
print(f"-7 // 3 = {-7 // 3}")       # 음수 : java 에서는 버림처리, python 에서는 내림처리

print("=" * 60)
print("비교, 논리 연산자")
print("=" * 60)

a, b = 2, 5
print(f"a, b --> {a}, {b}")
print(f"a == b --> {a == b}")
print(f"a != b --> {a != b}")
print(f"a < b --> {a < b}")
print(f"a >= b --> {a >= b}")

print()

# 논리 연산자 : java 에서 && , || , ! 형태의 연산자가 아닌
#               python 에서는 and, or, not 사용
print(f"and --> {True and True}")
print(f"or --> {True or 0}")
print(f"not --> {not False}")

print()
# a 값이 -5 ~ 5 사이의 값인가?
print("a 값이 -5 <= a <= 5 인가?")
print(f"and 결과 : { -5 <= a and a <= 5}")
print(f"연쇄 비교 결과 : { -5 <= a <= 5}")    # 연쇄 비교 가능

print("=" * 60)
print("멤버십 연산자(in), 식별 연산자(is)")
print("=" * 60)

members = ["반세오", "스프링롤", "팟타이"]
print(f"{members}")
print(f"'반세오' 포함 여부 -> {'반세오' in members}")
print(f"'푸팟퐁커리' 포함 여부 -> {'푸팟퐁커리' in members}")
print(f"'푸팟퐁커리' 포함하지 않는지? -> {'푸팟퐁커리' not in members}")

print(f"hello 에 ll 포함 여부 -> {'ll' in 'hello'}")

print()

x = [1, 2, 3]
y = [1, 2, 3]
z = x
print(f"x : {x} / y : {y} / z : {z}")

print(f"배열 값 비교 x == y : {x == y}")
print(f"객체 주소 비교 x is y : {x is y}")
print(f"객체 주소 비교 x is z : {x is z}")

# None 비교 시 is 사용을 권장
data = None
print(f"data is none? {data is None}")
print(f"data is not none? {data is not None}")

print("=" * 60)
print("복합 대입 연산자")
print("=" * 60)

x = 10
print(f"x : {x}")

# x = x + 5
x += 5
print(f"x += 5 : {x}")

x -= 5
print(f"x -= 5 : {x}")

# 파이썬에서는 증감 연산자가 존재하지 않음 ( ++ -- )

# 증가 연산자 (++) : 1 씩 증가
x += 1

# 감소 연산자 (--) : 1 씩 감소
x -= 1