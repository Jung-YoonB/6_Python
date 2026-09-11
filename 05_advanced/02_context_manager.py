"""
    with 문 (컨텍스트 매니저)
    - 자원의 획득과 반납을 자동으로 처리하는 제어 구조
    - 블록을 벗어날 때 자동으로 close 처리를 해줌 (직접 f.close() 불필요)
"""

import os   # 운영체제와 상호작용하여 파일 경로 탐색, 폴더 생성/삭제, 환경 변수 조회 등을 지원하는 모듈
import json # json 관련 변환 기능을 제공하는 모듈 (json <--> dict/list)

print("=" * 60)
print(__file__)
print("=" * 60)

# os.path.abspath() : 절대 경로를 반환
# os.path.dirname() : 디렉토리(폴더) 경로를 반환
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)

TXT_PATH = os.path.join(BASE_DIR, "_sample.txt")
JSON_PATH = os.path.join(BASE_DIR, "_sample.json")

print(f"TXT_PATH : {TXT_PATH}")
print(f"JSON_PATH : {JSON_PATH}")

print("=" * 60)
# 직접 파일을 처리(with x)
"""
f = open(TXT_PATH, "w", encoding="utf-8")
f.write("금요일, 20260911, 졸림\n")
f.close()
"""

# with 문을 사용하여 파일 처리
# mode="w" -> 파일 쓰기
with open(TXT_PATH, "w", encoding="utf-8") as f:
    f.write("금요일, 20260911, 졸립고 배고픔\n")
    f.write("토요일, 20260912, 좀비임\n")

print(f"저장 완료 {os.path.basename(TXT_PATH)}")

# mode="r" -> 파일 읽기
with open(TXT_PATH, "r", encoding="utf-8") as f:
    contents = f.read()

print("------ 파일 내용 ------")
print(contents)

print("=" * 60)

for line in contents.strip().split("\n"):
    print("* * * * * *")
    print(line)

print("=" * 60)

products = [
    {"code": "001123", "name": "iPhone Duo (아이폰 듀오)", "price": 3300000},
    {"code": "004123", "name": "Galaxy Z Flip8 (갤럭시 플립8)", "price": 1680000}        
]

# JSON 으로 저장 (파일 쓰기)
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print(f"저장 완료 {os.path.basename(JSON_PATH)}")

# print(f"ensure_ascii=True --> {json.dumps(products, ensure_ascii=True, indent=2)}")
# print(f"ensure_ascii=False --> {json.dumps(products, ensure_ascii=False, indent=2)}")

# JSON 읽기 (파일 읽기)
with open(JSON_PATH, "r", encoding="utf-8") as f:
    json_contents = json.load(f)

print(f"type -> {type(json_contents)}")
print()
for c in json_contents:
    print(f"data type -> {type(c)}")
    print(" * * * * * * ")
    print(f"{c['name']} : {c['price']}")