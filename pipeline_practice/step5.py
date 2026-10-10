"""
## STEP 5 · 이상치와 논리 검사
**이 단계가 이 문제의 핵심입니다.**
통계 기법만으로는 찾을 수 없는 오류가 섞여 있습니다. 도메인 규칙으로 걸러내세요.

### 파생 컬럼
먼저 **대여 시간(분)** 을 계산합니다.
```
duration_min = (return_time - rent_time) 의 분 단위
```

### 검사 규칙
| 규칙 | 내용 | 근거 |
| --- | --- | --- |
| ① | 반납 시각이 대여 시각보다 앞서면 안 됨 | 물리적으로 불가능 |
| ② | 요금이 음수면 안 됨 | 논리적으로 불가능 |
| ③ | 이동 거리가 물리 상한을 넘으면 안 됨 | 자전거 속도의 한계 |

> 💡 **물리 상한을 어떻게 구합니까**
자전거로 시속 50km 이상을 지속하는 것은 불가능합니다.
`distance_km / (duration_min / 60)` 이 평균 속도(km/h)이고,
이 값이 **50km/h 를 초과**하면 이상치로 판정하세요.

> ⚠️ **왜 IQR 로는 안 됩니까**
전동 자전거(빠름)와 일반 자전거(느림)가 섞여 있습니다.
일반 자전거에서 비정상적으로 부풀려진 거리값이, 전체 분포에서는 전동의 정상값처럼 보일 수 있습니다.

### 기대 결과
| 규칙 | 탐지 건수 |
| --- | --- |
| ① 반납 ≤ 대여 | 50 |
| ② 요금 음수 | 20 |
| ③ 속도 > 50km/h | 650 |
| 합계 (중복 제외) | 719 |
| 제거 후 행 수 | 13,701 |
"""
import pandas as pd

from step2 import bikes_raw, clean_bikes
from step3 import rentals_raw, clean_rentals
from step4 import stations, merge_all

# [1] 데이터 준비 ----------------------------------------------------------------------------------------
MAX_SPEED = 50

def detect_outliers(df):
    """
    도메인 규칙으로 이상치를 찾아 제거하고 (제거 후 결과, 규칙별 마스크) 반환
    Args:
        df : STEP 4 결합 결과

    Return:
        (df, rules)
        rules : { 규칙 이름: 불리언 마스크(True = 이상치) }
    """
    df = df.copy()

    # [2] 파생 컬럼 : 대여 시간(분) ---------------------------------------------------------------------
    df['duration_min'] = ((df['return_time'] - df['rent_time']).dt.total_seconds() / 60).astype('int64')

    # [3] 검사 규칙 -------------------------------------------------------------------------------------
    rule1 = df['return_time'] <= df['rent_time']

    # ② 요금이 음수면 안 됨
    rule2 = df['fee'] < 0

    # ③ 평균 속도 = 거리 / 시간(h) 가 50km/h 초과
    speed = df['distance_km'] / (df['duration_min'] / 60)
    rule3 = speed > MAX_SPEED

    rules = {
        '① 반납 ≤ 대여': rule1,
        '② 요금 음수': rule2,
        f'③ 속도 > {MAX_SPEED}km/h': rule3,
    }

    # [4] 이상치 제거 -----------------------------------------------------------------------------------
    # 셋 중 하나라도 해당하면 이상치 -> | (or) 로 묶기 (중복 제외 합계가 됨)
    outlier = rule1 | rule2 | rule3

    # ~ (not) : 이상치가 아닌 행만 남김
    df = df[~outlier].reset_index(drop=True)

    return df, rules

# [5] 검증 ----------------------------------------------------------------------------------------------
if __name__ == "__main__":
    pd.set_option("display.width", 140)

    # 이전 STEP 순서대로 실행
    rentals = clean_rentals(rentals_raw)
    bikes = clean_bikes(bikes_raw)
    df4, fail = merge_all(rentals, bikes, stations)

    df, rules = detect_outliers(df4)

    print("[규칙별 탐지 건수]")
    for name, mask in rules.items():
        print(f"  - {name:<16} : {mask.sum():>4} 건")

    # 규칙 3개를 | 로 합치기 -> 중복 제외 합계
    masks = list(rules.values())
    total = masks[0] | masks[1] | masks[2]
    print(f"  - {'합계 (중복 제외)':<14} : {total.sum():>4} 건")
    print()
    print(f"[행 수] {len(df4):,} -> {len(df):,} ({len(df) - len(df4):+,} 행)")
    print("-" * 100)

    counts = [m.sum() for m in masks]   # [① 건수, ② 건수, ③ 건수] 리스트 컴프리헨션

    checks = [
        ("① 반납 ≤ 대여 50",       counts[0] == 50),
        ("② 요금 음수 20",          counts[1] == 20),
        ("③ 속도 > 50km/h 650",    counts[2] == 650),
        ("합계 (중복 제외) 719",     total.sum() == 719),
        ("제거 후 행 수 13,701",     len(df) == 13701),
    ]

    print("[기대 결과 확인]")
    for name, ok in checks:
        print(f"  {'OK  ' if ok else 'FAIL'} {name}")

    print()
    print("[왜 IQR 대신 도메인 규칙인가] - 참고용 비교")
    q1, q3 = df4['distance_km'].quantile([0.25, 0.75])
    iqr = q3 - q1
    iqr_out = (df4['distance_km'] < q1 - 1.5 * iqr) | (df4['distance_km'] > q3 + 1.5 * iqr)
    print(f"  - 거리 IQR 정상 범위 : {q1 - 1.5 * iqr:.1f} ~ {q3 + 1.5 * iqr:.1f} km")
    print(f"  - IQR 로 찾은 거리 이상치 : {iqr_out.sum()} 건")
    print(f"  - 속도 규칙(③) 으로 찾은 이상치 : {rules[f'③ 속도 > {MAX_SPEED}km/h'].sum()} 건")
    print("    => 거리값 자체는 정상 범위 안이라 IQR 로는 못 찾음, 시간과 함께 봐야(속도) 드러남")