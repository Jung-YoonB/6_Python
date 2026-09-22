"""
    상관 히트맵
"""
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np

from chart_config import setup, out
from merged_loader import load_merged

setup()
df = load_merged()

# 종목별 일간 수익률 (%)
df['ret'] = df.groupby('code')['close'].transform(lambda s: s.pct_change())

# 상관 히트맵
#   - 여러 변수들 간의 상관 관계를 계산한 데이터(표)를 색상의 농도와 밝기로 표현한 그래프
pivot = df.pivot_table(index='date', columns='code', values='ret')
# 긴 형식(한 행 = 한 종목의 하루)   -> 넓은 형식(행=날짜, 열=종목)

# 섹터순으로 열을 정렬해야 블록이 제대로 표시 됨
order = df[['code', 'sector']].drop_duplicates().sort_values(['sector', 'code'])['code'].tolist()
pivot = pivot[order]        # 열 순서 정렬 / 데이터 유지, 순서만 변경한 값 대입

# corr() : 열끼리 상관 계수 행렬 (120, 120)
#       => -1 (정반대)  ~ 0 (무관)  ~ 1 (동일하게 움직임), 대각선은 자기 자신과 비교하기 때문에 항상 1
corr = pivot.corr()

print(f"pivot   : {pivot.shape} (행=날짜, 열=종목)")
print(f"corr    : {corr.shape} (종목*종목 상관계수)")

fig, ax = plt.subplots(figsize=(9, 7.5))

sns.heatmap(corr, cmap="coolwarm", center=0, vmin=-1, vmax=1, xticklabels=False, yticklabels=False, ax=ax)
# sns.heatmap(2 차원표, ...)
#       - cmap="coolwarm"   : 발산형 팔레트, 파랑 - 회색 - 빨강색 순으로 표시
#       - center=0          : 팔레트 중앙 값 지정
#       - vmin/vmax         : 색 범위에 양 끝을 고정, 지정하지 않을 경우 데이터의 최소/최대
#       - xticklabels       : 눈금 글자 표시 여부

ax.set_title("종목 간 수익률 상관(섹터순 정렬)")

fig.savefig(out('08_heatmap.png'), dpi=120)
plt.close(fig)
print("------------------ 실습 구분선 1 ------------------")

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

sns.heatmap(corr, cmap="coolwarm", xticklabels=False, yticklabels=False, ax=axes[0])
axes[0].set_title("center 미지정")

sns.heatmap(corr, cmap="coolwarm", center=0, vmin=-1, vmax=1, xticklabels=False, yticklabels=False, ax=axes[1])
axes[1].set_title("center=0, vmin/vmax")

fig.tight_layout()
fig.savefig(out('09_center.png'), dpi=120)
plt.close(fig)
print("------------------ 실습 구분선 2 ------------------")

# 섹터 블록을 숫자로 확인
sector_of = df[['code', 'sector']].drop_duplicates().set_index('code')['sector']
codes = corr.columns

same, diff = [], []
for i in range(len(codes)):
    for j in range(i+1, len(codes)):
        v = corr.iloc[i, j]

        if sector_of[codes[i]] == sector_of[codes[j]]:
            same.append(v)
        else:
            diff.append(v)
# 상관 행렬은 대칭이고 대각선은 항상 1임
#       -> j를 i+1 부터 돌면 위쪽 삼각형만 훑게 되어 같은 쌍을 두번 세거나, 자기 자신을 섞이지 않고 추가
print(f"같은 섹터 쌍 : {len(same)} 개 평균: {np.mean(same):.4f}")
print(f"다른 섹터 쌍 : {len(diff)} 개 평균: {np.mean(diff):.4f}")
"""
수치 상으로 보았을 때, 상관 관계가 섹터별로 존재함  -> 그래프로는 판단하기 어려움
    - 시장 전체가 함께 움직이는 요인이 크다보니,
        섹터 차이가 심하게 발생하지는 않기 때문에 바로 식별할 정도가 되지 않음
"""