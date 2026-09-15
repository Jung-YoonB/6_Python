"""
    공통 파서 모듈
"""
import re       # 정규표현식 관련 된 모듈
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from config import BASE

# 텍스트 추출
def get_text(node, selector, default = ""):
    """
    HTML 태그 안에서 '텍스트(글자)'만 안전하게 추출하는 함수
    Args:
        node        : 찾을 범위가 되는 HTML
        selector    : 찾고 싶은 요소의 CSS 선택자
        default     : 요소를 못 찾았을 때 사용할 기본 값("")
    """
    tag = node.select_one(selector)
    return tag.get_text(strip=True) if tag else default

# 속성 추출
def get_attr(node, selector, attr, default = ""):
    """
    HTML 태그 안에서 '속성값(hred, src 등)'을 안전하게 추출하는 함수
    Args:
        node        : 찾을 범위 (HTML 요소)
        selector    : CSS 선택자
        attr        : 속성명
        default     : 찾지 못했을 때 사용할 기본 값("")
    """
    tag = node.select_one(selector)

    if not tag:
        return default

    return tag.get(attr, default)

# 숫자 추출
def get_number(node, selector, default = 0):
    """
    추출 된 데이터에서 '숫자'만 깔끔하게 뽑아서 반환하는 함수
    Args:
        node        : 찾을 범위 (HTML 요소)
        selector    : CSS 선택자
        default     : 찾지 못했을 때 사용할 기본 값(0)
    """
    text = get_text(node, selector)

    numbers = re.sub(r"[^\d]", "", text)    # 숫자가 아닌 문자를 모두 제거
    return int(numbers) if numbers else default

# 실수 추출
def parse_rate(text, default = None):
    """
    '+3.5%', '-1.08' 처럼 부호(+, -)와 소숫점이 포함 된 텍스트에서 
    숫자 부분만 실수(float) 형태로 추출하는 함수
    Args:
    text        : 변환 할 text 값
    default     : 찾지 못했을 때 사용할 기본 값(None)
    """
    if not text:
        return default

    m = re.search(r"-?[\d.]+", text)
    return float(m.group()) if m else default

# stock 목록 파서
def parse_stocks(html):
    """
    주식 목록 전체 HTML 문자열을 통해,
    필요한 데이터만 추출하여 딕셔너리 리스트로 반환해주는 함수
    
    동작 순서
        1. 텍스트 형태의 HTML을 BeautifulSoup을 이용하여 DOM 구조로 변환
        2. 목록에 해당하는 컨테이너(tr.stock-row) 단위로 먼저 추출
        3. 해당 컨테이너에서 이름, 가격, 링크 등을 안전하게 추출하여 리스트로 담아서 반환
    """

    soup = BeautifulSoup(html, 'lxml')

    results = []
    for row in soup.select("tr.stock-row"):
        results.append({
            "code": get_text(row, "td.col-code"), 
            "name": get_text(row, "td.col-name a"), 
            "sector": get_text(row, "td.col-sector"), 
            "price": get_number(row, "td.col-price"), 
            "rate": parse_rate(get_text(row, "td.col-change")),
            "volume": get_number(row, "td.col-volume"),
            "market": get_text(row, "td.col-market span"),
            "link": urljoin(BASE, get_attr(row, "td.col-name a", "href"))
        })

    return results