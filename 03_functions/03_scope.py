"""
    스코프
    - 전역 변수 : 함수 외부에 선언 된 변수
    - 지역 변수 : 함수 내부에 선언 된 변수, 해당 함수 내에서만 접근 가능
"""

print("=" * 60)
print("지역 변수 - 함수 안에서 만든 변수는 함수 밖에서 안 보임")
print("=" * 60)

count = 0                    # 전역 변수

def increase1():
    count = 10               # 지역 변수 생성
    print(f"count 함수1에서 출력 : {count}")

increase1()
print(f"count 함수1 수행 후 전역에서 출력: {count}")    # 0

def increase2():
    global count             # global : 전역변수 사용 명시 / 누락 시 전역 변수 인지 X UnboundLocalError
    count += 1               # count = count + 1

increase2()
print(f"count 함수2 수행 후 전역에서 출력: {count}")

print()

# 스코프 검색 순서 : Local -> Enclosing -> Global
data = "-- 전역 --"

def outer():
    data = '-- 바깥 함수 (outer) --'

    def inner():
        data = '-- 안쪽 함수 (inner) --'
        print(f"** inner :: data - {data}")

    inner()
    print(f"** outer :: data - {data}")

outer()
print(f"** global :: data - {data}")