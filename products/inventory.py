"""
    재고 관리 클래스(등록 / 조회 / 수정 / 삭제)
    <공통>
    - 전체 재고 확인
    - 긴급 발주 목록 확인(재고 수량이 10개 미만 품목)
    - 전체 재고의 총 금액 확인
    - 입고 수량을 증가시키거나 출고 수량 감소
        - 출고 수량이 현재 재고를 초과하는 경우 예외 발생
    - 상품 단가 수정
    - 단종된 품목은 상품 코드를 통해 제거
    - 예외 클래스를 최소 2개 정의하여 활용
        - 예 : OutOfStockError (출고량이 재고 초과 시), 
               ProductNotFoundError (존재하지 않는 상품 코드 조회 시)
    ----------------------------------------------------------------------------------
    <신선 식품>
    -> 유통기한이 오늘로부터 3일 이내인 경우, 단가를 50% 할인한 가격을 반환 / get_price()
"""

import models as m

class ProductController:
    # ------ 상품 데이터 저장 ------
    def __init__(self):
        self.products = {}

    # ------ 상품 등록(일반) ------
    def add_normal(self, code, name, price, stock, is_danger):
        if code in self.products:
            return "[실패] 이미 존재하는 상품 코드입니다."
        
        product = m.NormalProduct(code, name, price, stock, is_danger)
        self.products[code] = product

        return "[성공] 일반 상품 등록 완료"

    # ------ 상품 등록(신선) ------
    def add_fresh(self, code, name, price, stock, expiration):
        if code in self.products:
            return "[실패] 이미 존재하는 상품 코드입니다."
        
        product = m.FreshProduct(code, name, price, stock, expiration)
        self.products[code] = product
        return "[성공] 신선 상품 등록 완료"

    # ------ 상품 조회 (ALL) ------
    def all_products(self):
        p_list = []

        for p in self.products.values():
            p_list.append(p)

        return p_list

    # ------ 긴급 발주 목록 ------
    def red_products(self):
        p_list = []

        for p in self.products.values():
            if p.stock < 10:
                p_list.append(p)

        return p_list

    # ------ 총금액 ------
    def total_price(self):
        total = 0

        for p in self.products.values():
            total += p.get_price() * p.stock
        
        return total

    # ------ 입/출고 수량 변경 ------ 
    # 입고 수량을 증가시키거나 출고 수량 감소
    #   - 출고 수량이 현재 재고를 초과하는 경우 예외 발생
    # *** 입고 ***
    def add_stock(self, code, stock):
        if code not in self.products:
            raise m.ProductNotFoundError(code)

        product = self.products[code]
        product.stock += stock
        return f"[성공] 상품의 재고가 {stock}개 추가되어 {product.stock:,}개로 변경되었습니다."

    # *** 출고 ***
    def out_stock(self, code, stock):
        if code not in self.products:
            raise m.ProductNotFoundError(code)

        product = self.products[code]

        if stock > product.stock:
            raise m.OutOfStockError(product.stock)

        product.stock -= stock
        return f"[성공] 상품의 재고가 {stock}개 감소되어 {product.stock:,}개로 변경되었습니다."        
    
    # ----- 상품 단가 수정 ------
    def update_price(self, code, price):
        if code not in self.products:
            raise m.ProductNotFoundError(code)

        product = self.products[code]
        product.price = price
        return f"[성공] 상품의 가격이 {price:,}원으로 변경되었습니다."

    # ------ 단종된 품목 상품 코드를 통해 제거 ------
    def del_product(self, code):
        if code not in self.products:
            raise m.ProductNotFoundError(code)
        
        del self.products[code]
        return f"[성공] {code} 상품이 삭제되었습니다."