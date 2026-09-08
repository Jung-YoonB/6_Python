"""
    조건문
"""

print("=" * 60)
print("if / elif / else")
print("=" * 60)

value = 10
# value = 3

if value > 5:
    print("value > 5 조건문 내부입니다.")
    print("value > 5 조건문 내에서 실행하고자 한다면 들여쓰기 필수!!")

print("조건문 외부입니다.")

print()

score = 80      # int(input("점수 입력 : "))

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"

print(f"{score}점 => {grade}")
# 블록은 들여쓰기로 구분, 조건식 옆에는 콜론(:) 지정
# else if 대신에 elif 사용

print()

print("=" * 60)
print("삼항 연산")
print("=" * 60)

# 참일_때_결과값 if 조건식 else 거짓일_때_결과값
age = 15        # int(input("나이 입력 : "))

"""
if age >= 20:
    result = "성인"
else:
    result = "미성년자"
"""

# 삼항 연산자 이용
result = "성인" if age >= 20 else "미성년자"

print(f"{age}세 -> {result}")

print("=" * 60)
print("match-case (java 의 switch)")
print("=" * 60)

status = 200        # int(input("상태 코드 입력 : "))
"""
    switch (status) {
        case 200:
            result = "정상";
            break;
        case 404:
            result = "페이지를 찾을 수 없음";
            break;
        case 500:
            result = "서버 오류";
            break;
        default:
            result = "알 수 없는 코드";
    }
"""
match status:
    case 200:
        result = "정상"
    case 404:
        result = "페이지를 찾을 수 없음"
    case 500:
        result = "서버 오류"
    case _:
        result = "알 수 없음"

print(f"{status} -> {result}")

print("=" * 60)
print("pass")
print("=" * 60)

# 빈 블록을 작성하고자 할 때 사용 (오류 방지)
score = 90

if score > 90:
    pass        # 미구현 부분을 임시로 처리
else:
    print("------ else 입력 ------")