"""
    매서드 : 클래스 내의 함수

    * 종류
        1) 인스턴스 매서드
        2) 클래스 매서드 : @classmethod
        3) 정적 메서드 : @staticmethod
"""

class Account:
    bank_name = "KH 은행"
    MIN_DEPOSIT = 1000

    def __init__(self, owner, balance = 0):
        self.owner = owner
        self.balance = balance

    # 인스턴스 메소드 : 객체의 데이터를 다룸. 첫번째 매개변수 self.
    def deposit(self, amount):
        self.balance += amount
        return self.balance

    # 클래스 메소드 : 클래스 자체를 다룸. 첫번째 매개변수 cls. @classmethod 지정
    @classmethod
    def from_dict(cls, data):
        """
        딕셔너리로부터 객체를 생성하는 메소드
        """
        return cls(data["owner"], data.get("balance", 0))

    # 정적 메소드 : 객체, 클래스와 무관한 기능을 담당하는 메소드(유틸리티). @staticmethod 지정
    @staticmethod
    def is_valid_amount(amount):
        return amount >= Account.MIN_DEPOSIT

acc = Account("부추전", 10000)
print(f"deposit --> {acc.deposit(3000)}")   # 인스턴스 메소드 호출

# 클래스 메소드 호출
acc2 = Account.from_dict({"owner": "낙지볶음", "balance": 10000})
print(f"owner: {acc2.owner}, balance: {acc2.balance}")

# 정적 메소드 호출
print(f"amount: 6000 -> {Account.is_valid_amount(6000)}")
print(f"amount: 500 -> {Account.is_valid_amount(500)}")

"""
정적 메소드 활용 예
amount = 500
if Account.is_valid_amount(amount):
    print(f"deposit --> {acc2.deposit(amount)}")
else:
    print(f"최소 금액을 만족하지 않습니다.")
"""

# from_dict 활용
response  = [
    {"owner": "치즈 쭈꾸미 볶음", "balance": 20000},
    {"owner": "계란찜"},
    {"owner": "낙지 탕탕이", "balance": 55000},
]

accounts = [Account.from_dict(item) for item in response]

for a in accounts:
    print(f"{a.owner} {a.balance}원")

# from_dict 활용 시 딕셔너리 구조를 자연스럽게 클래스에 넘겨 객체 생성 가능
# 데이터 구조가 변경되거나 메소드를 수정하는 경우 새로 정의해서 대응 가능