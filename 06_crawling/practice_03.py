"""
    실습용 사이트에서
        종목 메뉴 페이지(SSR)의 섹터를 "IT서비스"로 검색한 결과 데이터를 추출

    - 요청 주소: ??
    TODO: 오늘 (09/15) 18시까지 이메일로 제출
"""
import requests, json
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin

from config import BASE, HEADERS, TIMEOUT
from parsers import parse_stocks


# query = "IT서비스"
# encoded_query = quote(query)

# it_service_url = f"{BASE}/stocks?sector={encoded_query}"
# resp = requests.get(it_service_url, headers=HEADERS, timeout=TIMEOUT)

# IT서비스 sector code = S08
resp = requests.get(f"{BASE}/stocks?sector=S08&market=&q=", headers=HEADERS, timeout=TIMEOUT)

resp.raise_for_status()

print(f"▶ [1] 요청된 최종 URL: {resp.url}")

html = resp.text
soup = BeautifulSoup(html, 'lxml')

stocks = parse_stocks(html)

print(f"▶ [2] 파싱된 종목 개수: {len(stocks)}개")
print(f"▶ [3] 파싱 결과 데이터: {stocks}")

def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

save_json(stocks, "practice_03_stocks_it_service.json")