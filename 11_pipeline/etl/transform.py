"""
    Transform : 데이터 정제,계산,검증

    - 하지 않은 것: 저장(적재)

    Extract 단계에서 전달된 원본 데이터를
        DB에 저장할 수 있는 상태로 만듬
    - 타입 변환 (문자열 -> 숫자/날짜)
    - 중복 제거
    - 이상치 탐지 / 결측치 처리 (제거/대치/보간)
    - 파생 컬럼(등락,등락률,..) 계산(재계산)
    - 검증
"""
import pandas as pd

# 수치형(숫자)으로 변환할 열 목록
NUM_COLS = ["open","high","low","close","volume","change","changeRate"]

# 보간 대상 목록 (OHLC - 시가,고가,저가,종가)
OHLC = ["open","high","low","close"]


def clean_prices(records, logger):
    """
        정제 함수. 단계마다 건수를 로그로 기록.

        [처리 순서]
        1. list[dict] -> DataFrame 변환
        2. 숫자 타입 정제
        3. 날짜 타입 정제
        4. 종목 코드 정규화 (대문자, 공백 제거, ...)
        5. 중복 제거 (code,date 기준)
        6. 이상치 탐지 -> NaN 처리
        7. 결측 보간 (interpolate -> ffill -> bfill)
        8. OHLC 정합성
        9. 소수점 -> 정수 (반올림)
        10. 등락, 등락률 재계산
    """

    # 1. DataFrame 변환
    df = pd.DataFrame(records)
    logger.info(f"   입력    {len(df):,}행")

    # 2. 숫자 타입 정제
    #    -콤마 제거: "1,000" -> "1000" -> 1000
    #    -변환 실패 시 NaN 처리
    for col in NUM_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(",","",regex=False),
                errors="coerce"
            )

    # 3. 날짜 타입 정제
    #    -날짜 형식이 다르더라도 변환될 수 있어야 함
    #    -변환 실패 시 NaN 처리
    df["date"] = pd.to_datetime(df["date"], format='mixed', errors='coerce')

    # 4. 종목코드 정규화
    #    "G0001"  / " G0001" / "G0001 " / "g0001" ...
    #    --> 대문자로 변경. 공백 제거.
    df["code"] = df["code"].astype(str).str.upper().str.strip()

    logger.info(f"  타입 정제    {len(df):,}행")

    # 5. 중복 제거
    #    -> 타입 정제 후에 중복 데이터 체크해야 함!
    before = len(df)

    df = df.drop_duplicates(subset=["code", "date"], keep="first")
    logger.info(f"  중복 제거   {len(df):,}행  ({len(df) - before:+,})")


    # 6. 이상치 탐지

    # 종목별 날짜순으로 정렬
    df = df.sort_values(["code","date"]).reset_index(drop=True)

    def is_outlier(s):
        """
            s : 한 종목의 종가 Series

            [IQR 방식]
                Q1(25 분위수)와 Q3(75 분위수)를 구하고,
                IQR = Q3 - Q1로 정의

                Q1 - 1.5 * IQR 미만이거나, Q3 + 1.5 * IQR 초과면 이상치로 판단함
        """
        q1, q3 = s.quantile([0.25, 0.75])
        iqr = q3 - q1

        return (s < q1 - 1.5 * iqr) | (s > q3 + 1.5 * iqr)

    stat = df.groupby("code")["close"].transform(is_outlier) # 통계적 이상치

    logic = (df['close'] > df['high']) | (df['close'] < df['low']) # 논리적 이상치

    n_out = int((stat | logic).sum())  # 통계적 이상치 또는 논리적 이상치에 해당하는 건수

    # 이상치로 판단된 종가 데이터를 NaN 으로 변경
    df.loc[stat | logic, "close"] = pd.NA
    df["close"] = pd.to_numeric(df["close"], errors="coerce")  # pd.NA --> float NaN (명시적 변환)

    # 거래량(volume)이 음수인 경우 NaN으로 변경
    df.loc[df["volume"] < 0, "volume"] = pd.NA
    df["volume"] = pd.to_numeric(df["volume"], errors="coerce")

    logger.info(f"  이상치 탐지/처리   {len(df):,}행  ({n_out:,}건 -> NaN)")

    # 7. 결측 보간
    #    - interpolate()   : 선형 보간. 앞 뒤 값의 중간값으로 채워줌.
    #    - ffill()         : 직전 값으로 채워줌.  (forward fill)
    #    - bfill()         : 직후 값으로 채워줌.  (backward fill)
    for col in OHLC:
        df[col] = df.groupby("code")[col].transform(
            lambda s: s.interpolate().ffill().bfill()
        )

    # 8. OHLC 정합성 - clip
    #    clip(lower=..., upper=...)
    #    => lower 미만이면 lower값으로, upper 초과면 upper값으로 변경
    logger.info(f"  OHLC 정합성 처리 전 (종가 결측: {df['close'].isna().sum():,})")
    df["close"] = df["close"].clip(lower=df["low"], upper=df["high"])

    logger.info(f"  OHLC 정합성 처리 후 (종가 결측: {df['close'].isna().sum():,})")

    # 9. 반올림
    #    OHLC => 실수 타입으로 처리(결측, 보간, ...)
    #    DB(Oracle)에 해당 컬럼들이 NUMBER(20) 정수 형태이므로 반올림 처리
    n_round = int((df[OHLC] % 1 != 0).sum().sum())
    for col in OHLC:
        df[col] = df[col].round(0)
    logger.info(f"  정수 반올림 처리  {len(df):,}행 (처리 대상: {n_round:,}개)")

    # 10. 등락, 등락률 재계산
    #     종가 보간, 반올림 처리를 하면서 데이터가 변경되었으므로 원본의 change, changeRate 를 그대로 사용할 수 없음!
    prev = df.groupby("code")["close"].shift(1)   # 종목별 직전(전일) 종가를 구해줌.

    df["change"]     = (df["close"] - prev).round(0)
    df["changeRate"] = ((df["close"] - prev) / prev * 100).round(2)

    return df
    

def validate(df, logger):
    """
        정제 작업 완료 후 검증 결과를 확인하는 함수
        검증 실패 시 파이프라인 멈춤!

        [검증 항목]
        - 날짜 타입 열이 datetime 타입인지
        - 중복 데이터가 없는지 (code,date 기준)
        - 종가 데이터에 결측이 없는지
        - OHLC 논리 정합성 : 저가 <= 시가,종가 <= 고가
        - 거래량이 음수가 아닌지
    """
    # [(항목이름, 검증결과),....]
    checks = [
        ("날짜 타입 (datetime)", pd.api.types.is_datetime64_any_dtype(df["date"])),
        ("중복 데이터 (0 / code,date)", df.duplicated(subset=["code", "date"]).sum() == 0),
        ("종가 데이터 결측 (0)", df["close"].isna().sum() == 0),
        ("OHLC 정합성", bool( ((df["low"] <= df["close"]) & (df["close"] <= df["high"])).all() ) ),
        ("거래량 음수 (0)", bool( (df["volume"].dropna() >= 0).all() )  ),
    ]

    # 실패한 항목의 이름(첫번째)만 리스트로 저장
    failed = [n for n, ok in checks if not ok]

    for name, ok in checks:
        logger.info(f"   {'OK  ' if ok else 'FAIL'} {name}")

    if failed:
        raise ValueError(f"검증 실패: {failed}")

    return True