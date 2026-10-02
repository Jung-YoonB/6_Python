"""
    파이프라인 : 전체 흐름 관리
        - 이 파일만 읽어도 어떤 작업이 수행되는 지 알 수 있어야 함
    
    [ETL 파이프라인 구조]
        Extract  ->  Transform  ->  Load  ->     Verify
         (수집)  ->  (정제/검증) -> (적재) -> (최종 검증, 확인)
"""
import time
from . import extract, transform, load

from .config import SOURCE
from .logger import setup

def run(source=SOURCE):
    """
        파이프라인 전체를 실행하고 성공 여부를 반환
        Args.
            source : 데이터 수집 방식("api" 또는 "csv")
    """
    logger = setup()
    t0 = time.perf_counter() # 전체 소요시간 측정을 위해 시작 시간 저장

    logger.info("-" * 100)
    logger.info(f"파이프라인 시작 (source={source})")
    logger.info("-" * 100)

    # [1] Extract --------------------------------------------------------------------------------------------
    logger.info("[Extract]")
    t = time.perf_counter() # 단계별 소요시간 측정을 위함

    # source 값에 따라 데이터 수집 함수 호출
    # from_api, from_csv 함수 모두 (rows, failed) 튜플을 반환함(인터페이스 통일)
    if source == "api":
        records, failed = extract.from_api(logger)
    else:
        records, failed = extract.from_csv(logger)

    # 수집 결과가 비어있을 경우, 오류 메시지 기록 후 False 반환
    if not records:
        logger.error("  수집 결과가 비어있습니다. 파이프라인을 중단합니다.")
        return False

    logger.info(f"  {len(records):,} 건 수집 ({time.perf_counter() - t:.1f} 초)")

    if failed:
        logger.warning(f"   실패 {len(failed):,} 건 : {failed}")

    # [2] Transform --------------------------------------------------------------------------------------------
    logger.info("[Transfrom]")
    t- time.perf_counter()

    # 정제 처리
    df = transform.clean_prices(records, logger)
    # 정제 검증
    transform.validate(df, logger)

    logger.info(f"  완료    ({time.perf_counter() - t:.1f} 초)")

    # [3] Load -------------------------------------------------------------------------------------------------
    logger.info("[Load]")
    try:
        ins, upd, lt = load.to_db(df, logger)
    except Exception as e:
        logger.error(f"    적재 실패: {type(e).__name__}: {e}")
        return False

    logger.info(f"  입력: {len(df):>8,} 행")
    logger.info(f"  신규: {ins:>8,} 행")
    logger.info(f"  갱신: {upd:>8,} 행")
    logger.info(f"  소요: {lt:>8.1f} 초")

    # Verify ---------------------------------------------------------------------------------------------------
    logger.info("[Verify]")

    ok = load.verify(df, logger)
            
    logger.info("-" * 100)
    logger.info(f"  {'완료' if ok else '검증 실패'} 총 {time.perf_counter() - t0:.1f} 초")
    logger.info("-" * 100)
    return ok

if __name__ == "__main__":
    run()