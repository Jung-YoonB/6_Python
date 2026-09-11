"""
    예외 처리
    try / except / else / finally
"""

# 함수 정의 : divide
#   데이터를 하나 전달받아 정수로 변환하고
#   변환된 값으로 100을 나눈 결과를 출력
def divide(text):
    try:
        num = int(text)
        result = int(100 / num)
        # print(f"결과 : {result}")
    except ValueError:
        print(f"{text} : 숫자가 아님")
    except ZeroDivisionError:
        print(f"{text} : 0 으로 나눌 수 없음")
    except Exception as e:
        print(f"{text} : {e}")
    else:       # 예외가 없을 때 실행
        print(f"결과 : {result}")
    finally:
        print("finally - 예외가 있던 없던 항상 실행")


for t in ["100", "-5", "abc", "0"]:
    divide(t)

print("=" * 60)

# 사용자 정의 예외 / 예외 발생 (raise)
class NoBalanceError(Exception):
    """ 잔액 부족 예외 """
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(f"잔액 부족: 현재 {balance}, 요청: {amount}")

class InvalidAmountError(ValueError):
    """ 금액이 잘못 된 경우 예외 """

class Account:
    """ 은행 계좌를 나타내는 클래스 """
    def __init__(self, owner, balance = 0):
        self.owner = owner
        self.balance = balance

    def withdraw(self, amount):
        """ 
            계좌에서 출금하는 메소드

            Args:
                amount (int): 출금할 금액
        """

        if amount <= 0:
            raise InvalidAmountError("출금액은 0보다 커야합니다.")

        if amount >self.balance:
            raise NoBalanceError(self.balance, amount)
        
        self.balance -= amount
        return amount

    def __str__(self):
        return f"[{self.owner}] 잔액: {self.balance:,}원"

acc = Account("돈가스", 30000)
print(acc)

for amount in [5000, 50000, -1000]:
    try:
        acc.withdraw(amount)
    except NoBalanceError as e:
        print(e)
    except InvalidAmountError as e:
        print(e)
    else:
        print(f"출금 성공 : {amount}원")

# TODO: 마지막 반복문에 발생되는 예외를 처리 ( ~ 18:00 이메일 제출)