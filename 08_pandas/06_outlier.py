"""
    이상치 탐색
"""
# raw-prices.csv 파일을 읽어와서
#   'close' : int64 / float64
#   'date'  : datetime64
#   'code', 'date' 열을 기준으로 중복 제거 (첫번째 데이터를 남김)
# 위 결과를 df 변수에 저장
import pandas as pd

from utils.config import RAW_PATH, ENCODING, step_path

df = pd.read_csv(RAW_PATH, encoding=ENCODING)
print(df.head())
df.info()

# 숫자 변환 =========================================================
NUM_COLS = ['open', 'high', 'low', 'close', 'volume', 'change', 'changeRate']
for col in NUM_COLS:
    df[col] = pd.to_numeric(
        df[col].astype(str).str.replace(',', '', regex=False),
        errors='coerce'
    )

# 날짜 변환 =========================================================
df['date'] = pd.to_datetime(df['date'], format='mixed')

# 중복 제거 =========================================================
df = df.drop_duplicates(subset=['code', 'date'], keep='first').reset_index(drop=True)

# 결과 개수는 ... 약 90,000 건 정도 예상 ...
print(df.head())
df.info()
print(len(df))
print('-' * 100)

step1_path = step_path('_step1.pkl')

# 파일로 데이터를 저장(.pkl)
#       df.to_pickle(경로)      => 파일로 저장. 반환값 x
# 파일로부터 데이터 읽기 (.pkl)
#       pd.read_pickle(경로)    => 파일에 저장 된 데이터를 DF으로 반환

print("====== 파일로 저장 ======")
df.to_pickle(step1_path)
print("****** 저장 완료 ******")
print("-" * 100)

print("====== 파일 읽어오기 ======")
df = pd.read_pickle(step1_path)
print(f"파일 불러오기 완료 : {len(df)} 행")
print(df.head())
print("-" * 100)

# 이상치 확인하기
print(df['close'].describe().round(0))

# - median      : 중앙값
# - mean        : 평균
med = df.groupby('code')['close'].transform('median')
# print(med)
print(f"""
        [종목 중앙값과 비교]
            - 중앙값의 50배 초과    : {(df['close'] > med * 50).sum()} 건
            - 중앙값의 5% 미만      : {(df['close'] < med * 0.05).sum()} 건

            => 나름의 기준으로 너무 큰 값이나 너무 작은 값을 찾아볼 수 있음
""")

print('-' * 60)
# quantile()        : 값을 크기순으로 나열했을 때 특정 위치의 값을 구해주는 함수
#       => .quantile([0.25, 0.75])
#            -> 값 2개짜리 시리즈가 반환 됨. Q1 (25%), Q3 (75%)
# IQR (사분위 범위)  : Q3 - Q1
#       => 규칙 : Q1 - 1.5 * IQR 보다 작으면 이상치,
#                 Q3 + 1.5 * IQR 보다 크면 이상치
#            -> 평균, 표준편차와 달리 극단값에 흔들리지 않기 때문에 이상치 탐지 사용
q1, q3 = df['close'].quantile([0.25, 0.75])
print(f"q1 : {q1}, q3 : {q3}")
# q1 -> 하위 25%, 1사분위 값 (12061.0)
# q3 -> 상위 25%(75%), 3사분위 값 (55106.25)
iqr = q3 - q1
lo = q1 - 1.5 * iqr
hi = q3 + 1.5 * iqr

out_mask = (df['close'] < lo) | (df['close'] > hi)

print(f"q1: {q1}, q3: {q3}, iqr: {iqr}")
print(f"정상 데이터 범위 : {lo} ~ {hi}")
print(f"이상치 : {out_mask.sum()} 건")
# IQR로 이상치 탐지에 한계가 있음
#   하한선이 음수가 나올 수가 없는데, 규칙을 적용하니 음수 값이 확인 됨
print()

# 중앙값 5% 미만
tiny = df['close'] < med * 0.05
print(f"중앙값 5% 미만 : {tiny.sum()} 건")
print(f"이중에 전체 IQR에도 속하는 건수 : {(tiny & out_mask).sum()} 건")
print(f"중앙 값 5% 미만 또는 IQR에도 속하는 건수 : {(tiny | out_mask).sum()} 건")

def is_outlier(data):
    """
    한 종목의 종가데이터를 받아서 같은 길이의 bool mask(True/False)를 반환
        - True  : 이상치
        - Flase : 정상데이터
    """
    q1, q3 = data.quantile([0.25, 0.75])
    iqr = q3 - q1
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return (data < lo) | (data > hi)

print()

# 종목별 이상치(IQR)
result = df.groupby('code')['close'].transform(is_outlier)
print(f"종목별 : {result.sum()} 건")

# 종가 > 고가 ? 종가 < 저가 ? ...
result2 = (df["close"] > df["high"]) | (df['close'] < df['low'])
result3 = df['volume'] < 0      # 거래량이 음수인 경우 ?

print(f"종가가 최저가, 최고가에서 벗어난 경우 : {result2.sum()}")
print(f"거래량이 음수인 경우 : {result3.sum()}")

# 이상치 처리
#   => 결측치(NaN)로 처리
mask = result | result2

# mask에 해당하는 행 중 종가(close) 데이터의 이상치를 결측으로 변경
#   pd.NA       # 결측 표시값
df.loc[mask, 'close'] = pd.NA

df['close'] = pd.to_numeric(df['close'], errors='coerce')

df.loc[result3, 'volume'] = pd.NA

print()
print(f"이상치 (mask) : {mask.sum()}")
print(f"거래량 음수 (result3) : {result3.sum()}")
print(f"종가 결측수 : {df['close'].isna().sum()}")

print("====== _step2.pkl 저장 ======")
df.to_pickle(step_path('_step2.pkl'))
print("****** 저장 완료 ******")
print("-" * 100)