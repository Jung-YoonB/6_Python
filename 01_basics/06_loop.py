"""
    반복문
"""

print("=" * 60)
print("for문 --> 항상 for-each")
print("=" * 60)

members = ["반세오", "스프링롤", "짜조"]

for m in members:
    print(f"{m} 맛있겠다...")

for c in "Happy":
    print(c, end=" ")

print()

print("=" * 60)
print("range 내장 함수 사용")
print("=" * 60)

# range(시작, 끝, 간격)
print(f"range(5) -> {list(range(5))}")      # 끝값: 5로 지정, 시작: 초기값 0, 간격: 초기값 1
print(f"range(1, 6) -> {list(range(1, 6))}")    # 시작값: 1, 끝값 : 6, 간격: 1

# [0, 2, 4, 6, 8] -> 시작: 0 / 간격: 2 / 끝: 9 or 10
print(f"range(0, 10, 2) -> {list(range(0, 10, 2))}")
# [-5, -4, -3, -2, -1] -> 시작: -5 / 끝: 0 / 간격: 1
print(f"range(-5, 0, 1) -> {list(range(-5, 0, 1))}")
#[5, 4, 3, 2, 1] -> 시작: 5/ 끝: 0 / 간격: -1
print(f"range(5, 0, -1) -> {list(range(5, 0, -1))}")

for i in range(5):
    print(f"i : {i}")

print()

for i in range(len(members)):   #range(3)
    print(f"{i} : {members[i]}")

print("=" * 60)
print("enumerate() -> 번호와 값을 함께")
print("=" * 60)

for i, m in enumerate(members):
    print(f"[{i}] : {m}")

print()

for i, m in enumerate(members, start=1): # start=시작 번호 지정
    print(f"<{i}> : {m}")

print("=" * 60)
print("zip() -> 여러 리스트를 동시에")
print("=" * 60)

names = ["삼땡전자", "kk하이닉스", "타타오"]
today = [275000, 1845000, 35850]
yesterday = [175000, 1945000, 34850]

for name, now, prev in zip(names, today, yesterday):
    diff = now - prev
    print(f"{name:<10} : {now:<8}원 ({diff})")

print("=" * 60)
print("while")
print("=" * 60)

count = 0

while count < 5:
    print(f"count : {count}")
    count += 1  # count 값을 1씩 증가

print()

n = 1
# 반복문 종료 조건: n이 3보다 클 때
while True:
    if n > 3:
        break   # 반복문 종료
    print(f"n : {n}")
    n += 1

print("=" * 60)
print("break / continue / for-else")
print("=" * 60)

print("1~10 범위에서 홀수만 출력, 단, 7을 넘으면 중단")
for n in range(1, 11):
    # 짝수인 경우 다음 루프로 이동
    if n % 2 == 0:
        continue

    # 7 보다 큰 경우 반복문 종료(중단)
    if n > 7:
        break

    print(n, end=" ")

print()
# for-else : 반복문 정상 종료 시 else 블록 실행
print(f"{members}")

for m in members:
    if m == "반세오":
        print("반세오를 찾았습니다!")
        break
else:
    print("찾는 음식이 없습니다.")

for m in members:
    if m == "푸팟퐁커리":
        print("푸팟퐁커리를 찾았습니다!")
        break
else:
    print("찾는 음식이 없습니다.")