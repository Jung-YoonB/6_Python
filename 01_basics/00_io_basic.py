"""
    출력 함수
    - print() 
"""

print("=" * 60)             # "=" 문자열을 60번 반복(곱하기)
print("기본 출력 확인")
print("=" * 60)

# 문자열은 따옴표("", '')로 감싸서 표현
print("hello, python!")
print('반가워, 파이썬!')

# 숫자는 따옴표 생략, 값 그대로 표현
print(100)
print(3.14)
print(10 + 20)

print("=" * 60)
print("여러 값을 동시에 출력")
print("=" * 60)

# 콤마(,)로 구분
print("반세오", 20, "노랑")

# 구분자를 지정하여 출력 : sep 옵션 사용 (기본값 공백 " ")
print("2026", "09", "07", sep="-")

# 마지막 출력 문자 지정: end 옵션 사용 (기본값 줄바꿈(개행) "\n")
print("첫번째 줄", end=" ")
print("두번째 줄")

print("=" * 60)
print("이스케이프 문자")
print("=" * 60)

# \로 이스케이프 문자 사용
print("이번 줄 다음에 출력하겠습니다. \n 한 줄 개행")
print("탭 간격을 주겠습니다. \t 한 탭 처리")
print("속마음 : \"배고프다...\"")

print("=" * 60)
print("문자 형식 지정 (문자 포매팅)")
print("=" * 60)

name = "반세오"
age = 20
height = 5.5

# java 의 printf 와 유사
print("이름: %s, 나이: %d, 키: %.1f" % (name, age, height))

# 문자열.format() 메소드 사용
print("이름: {}, 나이: {}, 키: {}".format(name, age, height))

# f-string : 문자열 표현 방법(형식 지정)
print(f"이름: {name}, 나이: {age}, 키: {height}")
print(f"내년에는 {age + 1}살이 됩니다.")

# - 정렬 기능 ({변수:옵션})
print(f"[{name:<10}]")      # <10 : 10칸 확보, 좌측 정렬
print(f"[{name:>10}]")      # >10 : 10칸 확보, 우측 정렬
print(f"[{name:^10}]")      # ^10 : 10칸 확보, 중앙 정렬

"""
    입력 함수
    - input()
"""

print("=" * 60)
print("입력 받아보기")
print("=" * 60)

age_str = input("나이 입력: ")

# 입력 값은 항상 문자열로 처리
print(f"입력값: {age_str}, 타입: {type(age_str)}")

# 계산이 필요한 경우 형변환 필요!
age = int(age_str)

print(f"입력값: {age}, 타입: {type(age)}")
print(f"내년 나이 : {age + 1}")