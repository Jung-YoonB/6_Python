"""
    목록 파싱
"""
import requests, json, csv
from bs4 import BeautifulSoup


from config import BASE, TIMEOUT, HEADERS
from parsers import get_text, parse_stocks

resp = requests.get(f"{BASE}/stocks", headers=HEADERS, timeout=TIMEOUT)
resp.raise_for_status()     # 응답 코드 200이 아니면 예외 발생

html = resp.text

soup = BeautifulSoup(html, 'lxml')

row = soup.select_one("tr.stock-row")
try:
    row.select_one("td.test").text    # 해당하는 클래스가 없을 때 None 이므로, text 사용 시 AttributeError
except Exception as e:
    print(f"오류:: {e}")

print(f"td.test -> {get_text(row, 'td.test')} (default 빈 string)")

print("=" * 60)

stocks = parse_stocks(html)

print(f"{'코드':<8}{'종목명':<14}{'섹터':<10}{'현재가':>12}{'등락률':>9}")

for s in stocks:
    print(f"{s['code']:<8}{s['name']:<14}{s['sector']:<10}{s['price']:>12}{s['rate']:>9}")

print("=" * 60)

# 파일로 저장
# - json
# - csv => 상품명, 가격, 재고
#          아이폰, 3000000, 20

# json 저장하기
def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

save_json(stocks, "stocks.json")
# 경로를 따로 지정하지 않을 경우 현재 터미널 위치에 저장 됨(실행하는 위치)

# csv 저장하기
def save_csv(data, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        # fieldnames -> 컬럼 순서

        writer.writeheader()    # csv 파일 맨 첫줄에 컬럼 이름들로 씀
        writer.writerows(data)   # 딕셔너리 리스트 전체를 각각의 행으로 씀(기록)

save_csv(stocks, "stocks.csv")