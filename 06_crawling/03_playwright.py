import requests

from config import BASE, TIMEOUT, HEADERS
from parsers import parse_stocks

# ssr : server side rendering, 서버에서 완성 된 화면을 응답
# csr : client side rendering, 빈 HTML을 서버로부터 응답받고, 
#                              자바스크립트를 통해 데이터를 화면에 표시

ssr = requests.get(f"{BASE}/stocks", headers=HEADERS, timeout=TIMEOUT)
csr = requests.get(f"{BASE}/csr/stocks", headers=HEADERS, timeout=TIMEOUT)

print(f"{'경로':<20}{'상태':<8}{'본문 길이':>12}")
print(f"{'/stocks (SSR)':<20}{ssr.status_code:<8}{len(ssr.text):>12}")
print(f"{'/csr/stocks (CSR)':<20}{csr.status_code:<8}{len(csr.text):>12}")

# 렌더링 방식에 따라서 <body>가 비어있을 수 있음
# csr 일 때는 bs으로 파싱할 수 없음

# csr 본문 확인
for line in csr.text.strip().split("\n"):
    print(f"{line}")

KEYWORD = '가온전자'
print(f"ssr --> {KEYWORD in ssr.text}")
print(f"csr --> {KEYWORD in csr.text}")

print("=" * 60)

"""
    Playwright
    브라우저 자동화를 통해 동적페이지 데이터를 수집을 지원하는 도구

    기본 구조
        Browser     브라우저(프로세스)
        Context     쿠키, 캐시 공간
        Page        탭
"""

# Platwright 동기 방식 API
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # browser : 크롬을 실행
    browser = p.chromium.launch(headless=True)  # headless=True => 창이 보이지 않음

    # context : 시크릿 창 하나, 쿠키/캐시가 독립적으로 보관
    context = browser.new_context(locale="ko-KR", viewport={"width": 1280, "height": 720}) # 한국어 설정 값, 뷰포트

    # page    : 실제로 조작하기 위한 탭 하나
    page = context.new_page()

    # page.route(패턴, 처리함수) : 특정 패턴의 요청을 가로채서 직접 처리하는 함수
    # route.abort()             : 요청을 취소
    # route.continew_()         : 요청을 그대로 진행
    page.route(
        "**/*",   # 모든 요청
        lambda route: route.abort() if route.request.resource_type in {"image", "font", "media"}
                                    else route.continue_()
    )

    page.goto(f"{BASE}/csr/stocks", wait_until='domcontentloaded')
    # wait_until
    #   - domcontentloaded : HTML을 다 읽고 DOM트리가 만들어진 시점 (JS 실행 전)
    #   - load             : 이미지를 포함한 모든 리소스가 로드 된 시점(기본값), 느림

    page.wait_for_selector("tr.stock-row")
    # 해당 선택자가 DOM에 그려질 때까지 대기(기다림)

    count = page.locator("tr.stock-row").count()
    print(f"렌더링 후 가져온 행의 개수: {count}")

    # content() : DOM을 문자열로 반환
    html = page.content()
    # print(f"page.content : {html}")

    items = parse_stocks(html)

    # ...

    browser.close()

for data in items[:5]:
    print(f"{data.get('code')} : {data.get('name')} : {data.get('price')}")


"""
    * headless=False, slow_mo=1000
        화면을 직접 보면서 확인할 수 있음

    * 스크린샷, HTML 저장
        page.scrennshot(path="..../screnntshot.png, full_page=True)
        open("capture.html', "w", encoding="utf-8).write(page.content())

    * 브라우저 콘솔
        page.on("console", lamda m: print(f"[BROWSER] {m.text}"))
"""

# 섹터가 IT서비스인 데이터만 크롤링
