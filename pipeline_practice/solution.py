"""
    공공 자전거 대여 데이터 파이프라인 - 전체 실행

    [실행 흐름]
        Extract   ->  Transform (STEP 2 ~ 6)  ->  Summary (STEP 7)  ->  Load (STEP 8)  ->  Verify
        원본 읽기      정제 / 결합 / 이상치 / 결측     집계 확인             DB 적재            적재 검증

    - 각 STEP 파일의 함수를 import 해서 순서대로 실행
    - 단계별 건수는 logging 으로 화면 + 파일(logs/YYYYMMDD.log) 에 동시 기록
    - 재실행 검증 : 테이블을 비운 뒤 run() 을 두 번 실행 -> 2회차 신규 0 건, 행 수 그대로
"""
import logging
import time
from datetime import datetime

from config import BASE_DIR
from step2 import bikes_raw, clean_bikes
from step3 import rentals_raw, clean_rentals
from step4 import stations, merge_all
from step5 import detect_outliers
from step6 import handle_missing
from step7 import summarize
from step8 import TABLE, create_table, reset_table, row_count, to_db, verify

LOG_DIR = BASE_DIR / "logs"


# ===================================================================================================
#   로거 설정
# ===================================================================================================
def setup_logger(name="bikecity", level=logging.INFO):
    """
    화면과 파일에 동시에 기록하는 로거를 만들어서 반환
        - Logger    : logger.info(...) 로 기록하는 객체
        - Handler   : 어디에 출력할지 (StreamHandler = 화면 / FileHandler = 파일)
        - Formatter : 출력 형식 (시간 / 레벨 / 내용)
    """
    LOG_DIR.mkdir(exist_ok=True)                            # 폴더가 없으면 생성
    log_path = LOG_DIR / f"{datetime.now():%Y%m%d}.log"     # 예) logs/20261010.log

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers.clear()     # 여러 번 호출돼도 같은 메시지가 중복 출력되지 않게

    fmt = logging.Formatter("%(asctime)s [%(levelname)-7s] %(message)s", "%H:%M:%S")

    console = logging.StreamHandler()
    console.setFormatter(fmt)
    logger.addHandler(console)

    file = logging.FileHandler(log_path, encoding="utf-8")
    file.setFormatter(fmt)
    logger.addHandler(file)

    return logger


# ===================================================================================================
#   정제 결과 검증 -> 실패하면 적재하지 않음
# ===================================================================================================
def validate(df, logger):
    """
    정제가 끝난 데이터를 검사하고, 하나라도 실패하면 ValueError 발생 (적재 단계로 넘어가지 않음)
    """
    speed = df['distance_km'] / (df['duration_min'] / 60)

    checks = [
        ("rental_id 중복 0",            df['rental_id'].duplicated().sum() == 0),
        ("반납 시각 > 대여 시각",        bool((df['return_time'] > df['rent_time']).all())),
        ("요금 음수 0",                 bool((df['fee'] >= 0).all())),
        ("속도 50km/h 이하",            bool((speed <= 50).all())),
        ("fee 결측 0",                  df['fee'].isna().sum() == 0),
        ("distance_km 결측 0",          df['distance_km'].isna().sum() == 0),
        ("bike_type 일반/전동",          sorted(df['bike_type'].unique().tolist()) == ['일반', '전동']),
    ]

    for name, ok in checks:
        logger.info(f"    {'OK  ' if ok else 'FAIL'} {name}")

    failed = [name for name, ok in checks if not ok]
    if failed:
        raise ValueError(f"검증 실패: {failed}")


# ===================================================================================================
#   파이프라인
# ===================================================================================================
def run(logger):
    """ 파이프라인을 한 번 실행하고 성공 여부(True/False)를 반환 """
    t0 = time.perf_counter()

    logger.info("-" * 80)
    logger.info("파이프라인 시작")
    logger.info("-" * 80)

    # [1] Extract ----------------------------------------------------------------------------------
    # 원본은 step2, step3, step4 를 import 할 때 이미 읽혀 있음 (dtype=str, keep_default_na=False)
    logger.info("[Extract]")
    logger.info(f"  raw-bikes.csv     {len(bikes_raw):>8,} 행")
    logger.info(f"  raw-rentals.csv   {len(rentals_raw):>8,} 행")
    logger.info(f"  stations.csv      {len(stations):>8,} 행")

    # [2] Transform --------------------------------------------------------------------------------
    logger.info("[Transform]")

    bikes = clean_bikes(bikes_raw)
    logger.info(f"  STEP 2 자전거 정제   {len(bikes_raw):>8,} -> {len(bikes):>8,} 행 (중복 {len(bikes_raw) - len(bikes)} 건 제거)")

    rentals = clean_rentals(rentals_raw)
    logger.info(f"  STEP 3 대여 정제     {len(rentals_raw):>8,} -> {len(rentals):>8,} 행 (중복 {len(rentals_raw) - len(rentals)} 건 제거)")
    logger.info(f"         distance_km 결측 {rentals['distance_km'].isna().sum()} 건 / fee 결측 {rentals['fee'].isna().sum()} 건")

    df4, fail = merge_all(rentals, bikes, stations)
    logger.info(f"  STEP 4 결합         {len(rentals):>8,} -> {len(df4):>8,} 행 (매칭 실패 {len(fail)} 건 제외)")
    if len(fail) > 0:
        # 고아 레코드는 경고(WARNING) 레벨로 기록 -> 운영팀 확인이 필요한 항목
        logger.warning(f"         매칭 실패 bike_id : {fail['bike_id'].value_counts().to_dict()}")
    logger.info(f"         자치구 결측 {df4['district'].isna().sum()} 건 (배치 대여소 없는 자전거)")

    df5, rules = detect_outliers(df4)
    logger.info(f"  STEP 5 이상치       {len(df4):>8,} -> {len(df5):>8,} 행 ({len(df4) - len(df5)} 건 제거)")
    for name, mask in rules.items():
        logger.info(f"         {name} : {mask.sum()} 건")

    df, n_fee, n_dist = handle_missing(df5)
    logger.info(f"  STEP 6 결측         {len(df5):>8,} -> {len(df):>8,} 행 (요금 복원 {n_fee} 건 / 거리 결측 {n_dist} 건 제거)")

    logger.info("  [정제 검증]")
    try:
        validate(df, logger)
    except ValueError as e:
        logger.error(f"  {e} -> 적재하지 않고 중단")
        return False

    # [3] Summary (STEP 7) -------------------------------------------------------------------------
    logger.info("[Summary]")
    overall, by_district, by_type, by_payment = summarize(df)
    for name, value in overall.items():
        logger.info(f"  {name:<12} {value:>14,}")

    # 타입별 검산 : 결과만 기록 (데이터 특성상 FAIL 이어도 정제 오류는 아님)
    e, g = by_type.loc['전동'], by_type.loc['일반']
    ok = (e['평균이동거리'] > g['평균이동거리']) and (e['평균대여시간'] < g['평균대여시간'])
    logger.info(f"  검산 (전동이 짧은 시간에 더 긴 거리) : {'OK' if ok else 'FAIL'} "
                f"/ 거리 {e['평균이동거리']} vs {g['평균이동거리']}, 시간 {e['평균대여시간']} vs {g['평균대여시간']}")

    # [4] Load (STEP 8) ----------------------------------------------------------------------------
    logger.info("[Load]")
    try:
        ins, upd, t = to_db(df)
    except Exception as e:
        logger.error(f"  적재 실패: {type(e).__name__}: {e}")
        return False

    logger.info(f"  입력: {len(df):>8,} 행")
    logger.info(f"  신규: {ins:>8,} 행")
    logger.info(f"  갱신: {upd:>8,} 행")
    logger.info(f"  소요: {t:>8.1f} 초")

    # [5] Verify -----------------------------------------------------------------------------------
    logger.info("[Verify]")
    results = verify(df)
    for name, exp, act, ok in results:
        logger.info(f"  {'OK  ' if ok else 'FAIL'} {name:<8} {exp} / {act}")

    all_ok = all(ok for _, _, _, ok in results)

    logger.info("-" * 80)
    logger.info(f"  {'완료' if all_ok else '검증 실패'} 총 {time.perf_counter() - t0:.1f} 초")
    logger.info("-" * 80)
    return all_ok


if __name__ == "__main__":
    logger = setup_logger()

    # 테이블 준비 -> 비우기 (재실행 검증을 깨끗한 상태에서 시작)
    created = create_table()
    logger.info(f"{TABLE} 테이블 {'생성' if created else '이미 있음'} -> TRUNCATE 후 시작")
    reset_table()

    # 같은 파이프라인을 두 번 실행
    logger.info("=" * 80)
    logger.info("1회차 실행")
    ok1 = run(logger)
    n1 = row_count()

    logger.info("=" * 80)
    logger.info("2회차 실행")
    ok2 = run(logger)
    n2 = row_count()

    # 재실행 검증
    logger.info("=" * 80)
    logger.info("[재실행 검증]")
    checks = [
        ("1회차 성공", ok1),
        ("2회차 성공", ok2),
        (f"행 수 비교 ({n1:,} / {n2:,})", n1 == n2),
    ]
    for name, ok in checks:
        logger.info(f"  {'통과' if ok else '실패'} {name}")