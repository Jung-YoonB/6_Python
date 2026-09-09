"""
    함수의 매개변수
"""

print("=" * 60)
print("기본값 매개변수")
print("=" * 60)

# 전달 된 값이 없을 경우 기본 값으로 저장해서 사용
def connect(host, port=8080, charset='utf-8'):
    print(f"전달 된 정보 : {host}:{port} ({charset})")

connect("localhost")
connect("localhost", 1521)
connect("localhost", 1521, "euc-kr")
# 기본 값이 있는 매개변수는 뒤쪽에 배치

print("=" * 60)
print("키워드 매개변수")
print("=" * 60)

connect(port=1521, host='localhost')
# 키워드를 지정하면 순서와 상관없이 값을 전달할 수 있음

print("=" * 60)
print("가변 매개변수")
print("=" * 60)

# 개수가 정해지지 않은 값들을 전달받을 때 사용
def total(*numbers):
        print(f"전달 받은 값: {numbers} ({type(numbers)})")
        return sum(numbers)

print(f"total(1, 3) -> {total(1, 3)}")
print(f"total(1, 3, 5, 7) -> {total(1, 3, 5, 7)}")
print(f"total() -> {total()}")

print("=" * 60)
print("키워드 가변 매개변수")
print("=" * 60)

# 특정 키워드를 지정하여 값들을 전달 받을 때 사용
def create_user(**data):
    print(f"전달 받은 값: {data} ({type(data)})")

    for k, v in data.items():
        print(f"{k} : {v}")

create_user(name="pizze", age=20, address="seoul")

print("=" * 60)

def log(level, *messages, **options):
    print(f"level : {level}")
    print(f"messages : {messages}")
    print(f"options : {options}")

log("INFO", "서버 시작", "포트 8080...", color="green", timestamp=True)
log("ERROR", color="red")