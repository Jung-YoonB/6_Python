"""
    Matplotlib
"""
import matplotlib

matplotlib.use("Agg")
# Agg (Anti-Grain Geometry)
#   : 화면(GUI 창)을 열지 않고, 메모리 내에서만 차트 표시(렌더링)
#       - 화면에 따로 출력하지 않고 파일로 저장할 때 설정
#       ** pyplot 임포트하기 전에 설정해야 함 **
import matplotlib.pyplot as plt

from chart_config import setup, out
from merged_loader import load_merged

setup()

df = load_merged()

one = df[df['code'] == 'G0001'].sort_values('date')

# Figure, Axes
#       - Figure (도화지)   ->  Axes (그래프 하나)
#           * subplots(행, 열,figsize=(가로, 세로))
#               => 행, 열 생략시 1 * 1
fig, ax = plt.subplots(figsize=(12, 4))
# figsize => 12*4   | dpi(100)  -> 1200 * 400 픽셀

# ax.plot(x, y)
ax.plot(one['date'], one['close'])

ax.set_title("가온전자 주가 추이")
ax.set_xlabel("날짜")
ax.set_ylabel("종가(원)")
ax.grid(alpha=0.3)

fig.savefig(out('01_basic.png'))
# plt.show()
#   => 화면에 띄워서 바로 차트를 확인
#       -> savefig() 와 show() 를 같이 사용하는 경우, savefig() 호출 후 show() 를 호출해야 함
print("------------------ 실습 구분선 1 ------------------")

fig, ax = plt.subplots(figsize=(10, 3))

ax.plot(one['date'].iloc[:60], one['changeRate'].iloc[:60], marker=".")
#   => marker="." : 각 데이터 지점에 작은 점 표시

ax.axhline(0, color="gray", lw=0.8)
#   => axhline(y) : y 위치에 가로 기준선을 표시, lw -> 선 굵기

ax.set_title("가온전자 일간 등락률")
ax.set_ylabel("등락률(%)")

fig.savefig(out('02_minus.png'), dpi=120)

plt.close(fig)

print("------------------ 실습 구분선 2 ------------------")
"""
* 필수 설정 항목 (최소한 이것들을 설정하자)
    - ax.set_title("그래프 제목") 
    - ax.set_xlabel("x 축 제목")
    - ax.set_ylabel("y 축 제목")
    - ax.grid(alpha=0.3)            : 그리드 표시
    - ax.legend()                   : 범례 표시
"""
# 그래프 여러 개 표시
codes = ["G0001", "G0002", "G0003", "G0004"]
fig, axes = plt.subplots(2, 2, figsize=(13, 6), sharex=True)
#   => plt.subplots(2, 2)   : 그래프를 2행 2열 총 4개를 표시
#           --> axes -> (2, 2) 배열로 반환
#   =       --> sharex      : x 축을 모두 공유하겠다는 설정

for ax, code in zip(axes.flat, codes):
    # axes.flat : 2차원 배열을 1차원으로 펼쳐줌
    data = df[df['code'] == code].sort_values("date")

    ax.plot(data['date'], data['close'], lw=1)
    ax.set_title(f"{data['name'].iloc[0]} ({code})", fontsize=10)
    ax.grid(alpha=0.3)

fig.suptitle("종목별 주가 추이")
fig.tight_layout()                  # 제목, 라벨이 서로 겹치지 않게 자동으로 여백 계산

fig.savefig(out("03_subplots.png"), dpi=120)
plt.close(fig)