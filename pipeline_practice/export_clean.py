"""
    파이프라인 최종 결과(STEP 6)를 clean_rentals.csv 로 저장
        -> 머신러닝 실습(ml_practice) 에서 사용

    문제지 안내 : "파이프라인 코드의 최종 데이터프레임을 CSV로 저장하여 사용"
    실행 : pipeline_practice 폴더에서  python export_clean.py
"""
from config import BASE_DIR
from step2 import bikes_raw, clean_bikes
from step3 import rentals_raw, clean_rentals
from step4 import stations, merge_all
from step5 import detect_outliers
from step6 import handle_missing
from step8 import COLS

# 저장 위치 : ~/ml_practice/data/clean_rentals.csv
#   BASE_DIR.parent : pipeline_practice 의 상위 폴더 (6_Python)
SAVE_PATH = BASE_DIR.parent / "ml_practice" / "data" / "clean_rentals.csv"

# STEP 2 ~ 6 순서대로 실행
rentals = clean_rentals(rentals_raw)
bikes = clean_bikes(bikes_raw)
df, fail = merge_all(rentals, bikes, stations)
df, rules = detect_outliers(df)
df, n_fee, n_dist = handle_missing(df)

# DB 에 적재한 rental_log 와 같은 컬럼 (STEP 8 의 COLS)
cols = [c for c in COLS if c != "duration_min"]

# index=False : 0, 1, 2 ... 인덱스는 저장하지 않음
df[cols].to_csv(SAVE_PATH, index=False, encoding="utf-8-sig")

print(f"저장 완료 : {SAVE_PATH}")
print(f"  - {len(df):,} 행 / {len(cols)} 열")
print(f"  - 열 : {cols}")