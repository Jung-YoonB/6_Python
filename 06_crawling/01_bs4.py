"""
    BeautifulSoup
        - HTML 및 XML 문서에서 원하는 데이터를 쉽게 추출할 수 있도록 해주는 스크래핑 라이브러리
    
        1. requests 로 요청 후 문자열(html, xml)을 응답 받음
        2. bs4의 find, select 를 활용해서 특정 텍스트를 추출
"""
import requests     # ModuleNotFoundError: No module named 'requests' --> 해당 모듈 설치 필요
                    # 모듈 설치 --> pip install 모듈명
                    # pip install requests
from bs4 import BeautifulSoup   # pip install beautifulsoup4

# config 모듈에서 BASE, TIMEOUT, HEADERS 변수만 임포트
from config import BASE, TIMEOUT, HEADERS

resp = requests.get(f"{BASE}/stocks", headers=HEADERS, timeout=TIMEOUT)
resp.raise_for_status()     # 상태코드가 200 이 아니면 예외 발생
html = resp.text

print(f"{BASE}/stock    [{resp.status_code}] {len(html):,}자")

print("=" * 60)

# 문자열 --> 태그 구조

# bs4 은 문자열을 DOM 트리처럼 다룰 수 있게 만들어줌
soup = BeautifulSoup(html, 'lxml')  # pip install lxml

print(f"title --> {soup.title.text if soup.title else '없음'}")

# 기존에 자바스크립트를 통해 DOM 조작한 것처럼 bs 이 같은 역할을 함

# select        : CSS 선택자를 사용하여 해당 요소들을 반환, 없는 경우 [] 반환
# select_one    : CSS 선택자를 사용하여 해당 요소 1개 반환, 없는 경우 None 반환
rows_select = soup.select("tr.stock-row")

print(f"tr.stock-row 개수 : {len(rows_select)} 개")

first = soup.select_one("tr.stock-row")
price_tag = first.select_one("td.col-price")

print(f"td.col-price text : {price_tag.text}")

# f-string 에서 !r 을 사용하면 repr()이 호출되어 숨겨진 공백(\n, \t 등)까지 그대로 출력해줌
print(f"td.col-price text : {price_tag.text!r}")
print(f"td.col-price get_text() : {price_tag.get_text()!r}")

# 속성 값을 추출 --> get()
name_link = first.select_one("td.col-name a")

print (f"name_link['href'] : {name_link['href']}")
print (f"name_link.get('href') : {name_link.get('href')}")

print()
# 첫번째 행의 전체 데이터를 추출
for sel in ["td.col-code", "td.col-name a", "td.col-sector", 
            "td.col-price", "td.col-change", "td.col-volume", 
            "td.col-market span"]:
    tag = first.select_one(sel)
    value = tag.get_text(strip=True) if tag else "없음"
    print(f"{sel:<20} {value}")
