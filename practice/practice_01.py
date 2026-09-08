# import math
# 1. 이름, 성별, 나이,키를 입력 받은 후 정보를 출력하는 프로그램
name = input("이름 입력: ")
gender = input("성별(M/F) 입력: ")
age = input("나이 입력: ")
height = input("키 입력: ")

print()
print(f"이름: {name}, 성별: {gender}, 나이: {age}, 키: {height}cm")

print()
print("-" * 70)

# 2. 소문자를 대문자로 변환하여 출력하는 프로그램
alp = input("영문 소문자를 입력하세요: ")

print()
print(f"소문자: {alp.lower()}")
print(f"대문자: {alp.upper()}")

# 3. 정수 두 개를 입력받아 산술 연산 결과를 출력하는 프로그램
num1 = int(input("첫 번째 정수를 입력하세요: "))
num2 = int(input("두 번째 정수를 입력하세요: "))

print(f"합: {num1 + num2}")
print(f"차: {num1 - num2}")
print(f"곱: {num1 * num2}")
print(f"몫: {num1 // num2}")
print(f"나머지: {num1 % num2}")

# 4. 두 정수를 입력 받아 제곱과 제곱근을 출력하는 프로그램
num1 = int(input("첫 번째 정수를 입력하세요: "))
num2 = int(input("두 번째 정수를 입력하세요: "))

print(f"{num1}의 제곱: {num1 ** 2}")
print(f"{num2}의 제곱근: {num2 ** 0.5}")
# 함수 사용 : print(f"{num2}의 제곱근: {int(math.sqrt(num2))}")

# 5. 학점 산출 프로그램
score = int(input("점수를 입력하세요(0~100): "))

if (score < 0 or score > 100):
    print("점수를 올바르게 입력해주세요.")
elif score >= 90:
    print("학점: A")
elif score >= 80:
    print("학점: B")
elif score >= 70:
    print("학점: C")
elif score >= 60:
    print("학점: D")
else:
    print("학점: F")

# 6. 1부터 100까지의 숫자 중에서 짝수만 출력하는 프로그램
for i in range(2, 101, 2):
    print(i)

# 7. 1부터 100까지의 숫자 중에서 "3의 배수"이거나 "5의 배수가 아닌 수"의 합을 구하여 출력하는 프로그램
total = 0
for i in range(3, 101, 3):
    if (i % 5 == 0):
        continue
    total += i

print("1부터 100까지의 숫자 중 3의 배수이거나 5의 배수가 아닌 수의 합")
print(f"결과: {total}")