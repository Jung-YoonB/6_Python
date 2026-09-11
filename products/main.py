"""
    사용자 메뉴 루프 진입점
"""
from datetime import date
import inventory

c = inventory.ProductController()

def start():
    while True:
        print("<상품 재고 관리를 시작합니다.>")
        print("-" * 70)
        print("[진행 할 메뉴를 선택해주세요.]")
        print()
        print("[1] 상품 등록 (일반/신선)")
        print("[2] 등록 된 상품 조회(ALL)")
        print("[3] 긴급 발주 필요 상품 조회")
        print("[4] 전체 재고의 총 금액 확인")
        print("[5] 입/출고 수량 변경")
        print("[6] 상품 단가 변경")
        print("[7] 단종 된 품목 제거")
        print("[8] 프로그램 종료")
        print("-" * 70)

        select_num = input("번호 선택 (1~8): ")

        print("-" * 70)
        match select_num:
            case '1':
                add_product()
            case '2':
                search_all()
            case '3':
                search_red()
            case '4':
                check_total()
            case '5':
                update_stock()
            case '6':
                update_price()
            case '7':
                delete_product()
            case '8':
                print("프로그램을 종료합니다.")
                return
            case _:
                print("1 ~ 8 중의 번호를 입력해 주세요...\n")
                print("-" * 70)


def add_product():
    print("[등록할 상품 종류를 선택해주세요.]")
    print()
    print("[1] 일반 상품")
    print("[2] 신선 상품") 
    print("-" * 70)

    p_type = input("번호 선택 (1 or 2): ")

    code = input("상품 코드: ")
    name = input("상품명: ")
    price = int(input("단가: "))
    stock = int(input("재고: "))

    match p_type:
        case '1':
            dangerous = input("위험물 여부 (y/n): ")
            is_danger = True if (dangerous == 'y') else False

            result = c.add_normal(code, name, price, stock, is_danger)

            print(result)

        case '2':
            exp_year = int(input("유통기한 년 (예: 2006): "))
            exp_month = int(input("유통기한 월 (예: 9): "))
            exp_day = int(input("유통기한 일 (예: 2): "))
            expiration = date(exp_year, exp_month, exp_day)

            result = c.add_fresh(code, name, price, stock, expiration)

            print(result)

        case _:
            print("잘못 된 입력입니다.")
            return

def search_all():
    result = c.all_products()

    if len(result) == 0:
        print("상품이 없습니다. 등록을 진행해주세요.")
        return

    for p in result:
        print(p)

def search_red():
    result = c.red_products()

    if len(result) == 0:
        print("긴급 발주가 필요한 상품이 없습니다.")
        return

    for p in result:
        print(p)

def check_total():
    total = c.total_price()
    print(f"전체 재고의 총 금액: {total:,}원")

def update_stock():
    print("[변경할 재고 방식을 선택해주세요.]")
    print()
    print("[1] 입고")
    print("[2] 출고")
    print("-" * 70)

    s_type = input("번호 선택 (1 or 2): ")
    code = input("상품 코드: ")
    stock = int(input("변경할 수량: "))

    match s_type:
        case '1':
            result = c.add_stock(code, stock)
            print(result)

        case '2':
            result = c.out_stock(code, stock)
            print(result)

        case _:
            print("잘못 된 입력입니다.")
            return

def update_price():
    code = input("상품 코드: ")
    price = int(input("변경할 단가: "))

    result = c.update_price(code, price)
    print(result)

def delete_product():
    code = input("삭제할 상품 코드: ")

    result = c.del_product(code)
    print(result)


start()