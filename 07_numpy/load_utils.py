"""
    실습 데이터 불러오는 기능을 담은 모듈
"""
import numpy as np

from pathlib import Path

CSV_PATH = Path(__file__).with_name("prices.csv")
# 현재 파일의 경로를 가져온 후, 이름만 제시한 값으로 변경
# print(CSV_PATH)

N_DAYS = 750    # 거래일수

_COLUMNS = { 
    "code": 0,
    "date": 1,
    "open": 2,
    "high": 3,
    "low": 4,
    "close": 5,
    "volume": 6,
    "change": 7,
    "changeRate": 8
}

# 한번 읽은 열(데이터)을 저장하는 용도
_cache = {}

def _read(col, dtype):
    """
    csv에서 하나의 열만 읽어서 1차원 배열로 리턴
    """
    key = (col, str(dtype))

    if key not in _cache:
        if not CSV_PATH.exists():   # 파일이 존재하지 않으면 예외 발생
            raise FileNotFoundError(f"{CSV_PATH} 파일을 찾을 수 없습니다.")

    _cache[key] = np.loadtxt(
        CSV_PATH, 
        dtype=dtype,
        delimiter=",",          # 구분자(CSV는 콤마로 데이터 구분)
        usecols=_COLUMNS[col],  # 필요한 열 하나만 읽음
        skiprows=1,             # 첫 줄 생략(건너뜀)
        encoding="utf-8-sig"    # CSV 는 눈에 안보이는 값을 포함하고 있어 해당부분 제외
    )

    return _cache[key].copy()   # 원본이 아닌 복사본을 반환

def load_close_flat():
    """
    종가(종료가) 데이터만 1차원 배열로 리턴
    """
    return _read("close", "int64")

def load_one_stock(idx = 0):
    """
    한 종목의 종가만 1차원 배열로 리턴

    종목 하나당 750개(줄), 그 다음 종목 750줄 ...
    """
    close_arr = load_close_flat()
    start = idx * N_DAYS
    end = start + N_DAYS

    # close_arr[0:750] # 0 ~ 749
    # close_arr[750:...]

    return close_arr[start:end]

def load_dates():
    """
    거래일 정보를 날짜형식으로 리턴(1차원 배열)
    
        .astype("datetime64[D]")    => 물자열을 날짜로 변경
                        -> [D]      => Day 단위로 다루겠다
    """
    dates = _read("date", str)

    return dates[:N_DAYS].astype("datetime64[D]")

def load_codes():
    """
    종목 코드 배열 리턴
    """
    codes = _read("code", str)
    return codes[::N_DAYS]

def load_matrix():
    """
    종가 행렬을 반환
    행 : 종목 (120)
    열 : 날짜 (750)
        -> (120, 750)
    """
    close = load_close_flat()   # 1차원 배열
    return close.reshape(120, 750)     # 2차원 배열

def load_column(name):
    """
    열 데이터를 행렬(120, 750)로 반환
    """
    if name in ("code", "date"):
        raise KeyError("기존 함수를 사용하세요.")

    if name not in _COLUMNS:
        raise KeyError("찾을 수 없는 열입니다.")

    dtype = "float64" if name == "changeRate" else "int64"

    return _read(name, dtype).reshape(120, 750)