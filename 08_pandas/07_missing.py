"""
    결측치 처리
"""
import pandas as pd

from utils.config import step_path

# _step2.pkl 파일을 읽어서 df 변수에 저장
df = pd.read_pickle(step_path('_step2.pkl'))
print(f"Step 2 : 이상치 처리 완료 ... {len(df)} 행")

print("====== 현재 결측 ======")
for col in['open', 'high', 'low', 'close', 'volume']:
    n = df[col].isna().sum()

    if n:
        print(f"{col}: {n} 건 ({n / len(df) * 100:.2f} %)")
print("-" * 100)

"""
결측 처리 3가지 방법(전략)
    - 삭제  : dropna(subset=, how=, ...)
        => 삭제할 행 없이도 분석이 가능한지?
    - 대치  : fillna(값/평균/중앙값)
        => 대표값으로 적절한 것이 있는지?
    - 보간  : interpolate()
        => 시계열. 앞뒤 값 사이를 잇는다
"""

# 보간
#   => 종목별로 처리해줘야 함
edge = df.index[df['code'] != df['code'].shift()][1]
print(edge)
print()

demo = df.loc[(edge - 2) : (edge + 2), ['code', 'date', 'close']].copy()
print(demo)
print('-' * 60)

demo.loc[edge, 'close'] = pd.NA
demo['close'] = pd.to_numeric(demo['close'], errors='coerce')
print(demo)
print('-' * 60)

result1 = demo['close'].interpolate()
print(result1)
print('-' * 60)

result2 = demo.groupby('code')['close'].transform(lambda d: d.interpolate())
print(result2)
print('-' * 60)

"""
    groupby 없이 보간처리를 하면 마지막 종가 (G0001)와 뒷 종목의 다음 종가 사이를 이어버림
    groupby 를 사용하여 보간처리를 하면 해당 종목(그룹화 기준열)안에서만 이어줌
"""
# 열 별로 각각 다른 방법을 적용하여 처리
#   open, high, low, close  => 종목 별로 보간(시계열 데이터, 연속성)
#   volume                  => 결측 유지 (0으로 채우면 X)
OHLC = ['open', 'high', 'low', 'close']
before = df[OHLC].isna().sum().sum()
print(f"OHLC 결측 : {before}")

for col in OHLC:
    df[col] = df.groupby('code')[col].transform(lambda s: s.interpolate())

pola = df[OHLC].isna().sum().sum()
print(f"종목 별 보간 처리 후 : {pola}")
#   => 종목의 맨 앞/뒤에 남은 결측 개수
print('-' * 60)

# .ffill()  : 결측을 바로 앞의 값으로 채움
# .bfill()  : 결픅을 바로 뒤의 값으로 채움
for col in OHLC:
    df[col] = df.groupby('code')[col].transform(lambda s: s.ffill().bfill())

fb = df[OHLC].isna().sum().sum()
print(f"ffill; + bfill 처리 후 : {fb}")

# 거래량 (volume)은 결측 유지