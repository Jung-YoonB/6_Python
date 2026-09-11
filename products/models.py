"""
    Product, FreshProduct 등 도메인 클래스 정의
    [상품 정보]
    <공통>
    - 상품 코드. 품명, 단가, 재고수량
    - 예외 클래스를 최소 2개 정의하여 활용
        - 예 : OutOfStockError (출고량이 재고 초과 시), 
               ProductNotFoundError (존재하지 않는 상품 코드 조회 시)
    ----------------------------------------------------------------------------------
    <일반 물품>
    - 위험물 여부
    ----------------------------------------------------------------------------------
    <신선 식품>
    - 유통기한(날짜)
        -> 유통기한이 오늘로부터 3일 이내인 경우, 단가를 50% 할인한 가격을 반환 / get_price()
"""

from datetime import date


# ------ 사용자 정의 예외 ------
class OutOfStockError(Exception):
    """ 출고량 재고 초과 시 """
    def __init__(self, stock):
        super().__init__(f"재고 수량을 넘어서는 출고입니다. 재고 확인 후 다시 시도해주세요.")
        self.stock = stock
    
class ProductNotFoundError(Exception):
    """ 존재하지 않는 상품 코드 조회 시 """
    def __init__(self, code):
        super().__init__(f"존재하지 않는 상품입니다. 상품 코드를 재확인 해주세요.")
        self.code = code


# ------ 공통 상품 -------
class Product:
    def __init__(self, code, name, price=0, stock=0):
        self.__code = code      # 상품 코드
        self.__name = name      # 품명
        self.__price = price    # 단가
        self.__stock = stock    # 재고수량

    # 가격 정보(오버 라이딩용)
    def get_price(self):
        return self.__price

    # *** getter ***
    @property
    def code(self):
        return self.__code
    
    @property
    def name(self):
        return self.__name
    
    @property
    def price(self):
        return self.__price
    
    @property
    def stock(self):
        return self.__stock

    # *** setter ***
    @name.setter
    def name(self, value):
        self.__name = value
    
    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("가격은 0원 이상이여야 합니다.")
        self.__price = value

    @stock.setter
    def stock(self, value):
        if value < 0:
            raise ValueError("재고는 0개 이상이여야 합니다.")
        self.__stock = value

    # *** 정보 출력 ***
    def __str__(self):
        """ 상품 정보 출력 """
        return f"[상품코드] {self.__code} | [상품명] {self.__name} | [단가] {self.__price:,}원 | [재고] {self.__stock:,}개"

    
# ------ 일반 물품 ------
class NormalProduct(Product):
    def __init__(self, code, name, price=0, stock=0, is_danger=False):
        super().__init__(code, name, price, stock)
        self.__is_danger = is_danger    # 위험물 여부

    # *** getter ***
    @property
    def is_danger(self):
        return self.__is_danger

    # *** setter ***
    @is_danger.setter
    def is_danger(self, value):
        self.__is_danger = value

    # *** 정보 출력 ***
    def __str__(self):
        return f"{super().__str__()} | [위험물 여부] {'위험' if self.__is_danger == True else '안전'}"

# ------ 신선 식품 ------
class FreshProduct(Product):
    def __init__(self, code, name, price=0, stock=0, expiration=None):
        super().__init__(code, name, price, stock)
        self.__expiration = expiration if expiration is not None else date.today()  # 유통기한(날짜)

    # 유통기한 <= 3 인 상품 50% 할인 금액 반환
    """ 날짜 관련 함수
        today = date.today()
        expiration = date(2026, 9, 15)
        print((expiration - today))         # 4 days, 0:00:00
        print((expiration - today).days)    # 4
    """
    def get_price(self):
        today = date.today()
        # 남은 기간 : (유통기한 - 오늘).days 
        left_days = (self.__expiration - today).days

        if left_days < 0:
            # 유통 기한이 지난 상품은 폐기 -> 가격 0
            return 0
        elif 0 <= left_days <= 3:
            return int(self.price * 0.5)
        else:
            return self.price

    # *** getter ***
    @property
    def expiration(self):
        return self.__expiration

    # *** setter ***
    @expiration.setter
    def expiration(self, value):
        self.__expiration = value

    # *** 정보 출력 ***
    def __str__(self):
        return f"{super().__str__()} | [유통기한] {self.__expiration}"
