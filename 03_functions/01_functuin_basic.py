"""
    함수
    - 정의 시 사용하는 키워드 : def
"""

print("=" * 60)

# 함수 정의
def hello(name):
    return f"{name}님 안녕하세요."

# 함수 사용 (호출)
print(hello("피자"))
result = hello("비빔밥")
print(result)

# hello 함수 : 매개변수 O, 반환값 O

print()

def hello_print(name):
    print(f"{name}님 반갑습니다.")
    # return 없음 (생략)

hello_print("피자")
print(hello_print("비빔밥"))        # 반환값이 없는 함수는 None 반환
result = hello_print("불고기")
print(f"result : {result}")

print()
# 여러 값을 반환
def calc(a, b):
    return a + b, a - b, a * b

result = calc(5, 7)
print(f"결과 : {result}")

#언패킹 => 여러 변수로 나누어 저장
add, sub, mul = calc(5, 7)
print(f"언패킹 결과 : {add} {sub} {mul}")

print("=" * 60)
print("docstring (함수 설명)")
print("=" * 60)

def calc_tax(price, rate = 0.1):
    """
    부가세를 포함한 최종 금액을 반환하는 함수
    """
    return int(price * (1 + rate))

print(f"10000원 --> {calc_tax(10000):,}")

# 주의 할 점 .. 
# 파이썬은 호이스팅이라는 개념이 없기 때문에 함수를 정의하기 전에는 호출 불가
# print(test())  --> 정의 전에는 호출 불가

def test():
    return "테스트 함수입니다"