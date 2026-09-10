"""
    클래스와 객체

    -기본 형태-
    class 클래스명:
        # 생성자
        def __init__(self):
            self.필드명 = 값

        # 메소드
        def 메소드명(self):
            # 실행 할 내용
"""

# 기본 형태
class Account:
    # 생성자
    def __init__(self, owner, balance = 0):
        self.owner = owner
        self.balance = balance

    # 메소드
    def deposit(self, amount):
        self.balance += amount
        return self.balance

# 객체 생성
acc = Account("낙지볶음", 10000)

print(f"name : {acc.owner}")
print(f"balance : {acc.balance}")

print(f"deposit : {acc.deposit(7000)}")

print("=" * 60)

# 인스턴스 변수 vs 클래스 변수
class Member:
    # 클래스 변수 : 모든 인스턴스 공유
    team_name = "리센느"
    count = 0

    # 생성자
    def __init__(self, name):
        self.name = name        # 인스턴스 변수
        Member.count += 1       # 클래스 변수는 클래스명으로 접근

m1 = Member("원이")
m2 = Member("미나미")

print(f"m1.name : {m1.name}")
print(f"m2.name : {m2.name}")

print(f"m1.team_name : {m1.team_name}")
print(f"m2.team_name : {m2.team_name}")

print(f"count : {Member.count}")

print()
m1.team_name = "RESCENE"    # 인스턴스에 클래스 변수명으로 값을 대입하는 경우, 새로운 인스턴스 변수 생성
print(f"m1.team_name : {m1.team_name}")
print(f"Member.team_name : {Member.team_name}") # 클래스 변수 자체는 변경되지 않음
Member.team_name = "rescene"
print(f"m1.team_name : {m1.team_name}")
print(f"Member.team_name : {Member.team_name}")