"""
    열(컬럼) 다루기
"""
import pandas as pd

from utils.loader import load_csv

pd.set_option('display.width', 130)     # 출력 창 길이 설정

df = load_csv()

# 마지막 거래일 기록만 조회하여 day 변수에 저장, 인덱스 초기화
day = df[df['date'] == df['date'].max()].reset_index(drop=True)
print(day.head())
print()

# 새로운 열(컬럼) 추가
day['range'] = day['high'] - day['low']    # 최고가 - 최저가
day['range_pct'] = day['range'] / day['low'] * 100
print(day.head())
print()

day['temp'] = 0
print(f"day shape : {day.shape}")
# 열삭제 df.drap(colimns=[...])
day = day.drop(columns=['temp'])
print(f"'temp' 열 삭제 후 day shape : {day.shape}")
print()

# 열 이름 변경 df.rename(columns={기존_열_이름:변경할_열_이름})
renamed = day.rename(columns={'close': '종가'})
print(f"열 이름 변경 : {renamed.columns}")
print()

# .str 접근자
# 문자열 메소드를 모든 행에 일괄적으로 적용하고자 할 때 사용
# print(f"길이 len() -> {day['code'].str.len()}")
print(f"길이 len() -> {day['code'].str.len().unique().tolist()}")
print(f"슬라이싱   -> {day['code'].str[1:].head(3).tolist()}")
print(f"'G00'으로 시작하는 종목 코드 개수 -> {day['code'].str.startswith('G00').sum()} 개")
print()

sample = pd.Series(["    가온전자   ", "해피 바이오", "한빛중공업"])
print(f"공백 제거 --> {sample.str.strip().tolist()}")

sample2 = pd.Series(["52000", "51500", "N/A", "1,240"])
print(f"sample2 : {sample2.tolist()}")

# ValueError: could not convert string to float: 'N/A' # sample2.astype('float64')
converted = pd.to_numeric(sample2, errors='coerce')
print(converted.tolist())
print(f"결측 : {converted.isna().sum()}")

c = pd.to_numeric(sample2.str.replace(',', ''), errors='coerce')
print(c.tolist())
print(f"결측 : {c.isna().sum()}")
"""
astype은 하나라도 값이 이상하면 전체를 변경할 수 없음
    - to_numeric(errors='coerce) 은 오염 된 데이터를 강제로 nan(결측)으로 남기고 나머지는 변경
"""