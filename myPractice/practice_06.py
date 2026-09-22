from pathlib import Path
import platform
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1) seaborn 스타일을 먼저 지정 (이 함수가 폰트 설정을 초기화하므로 반드시 폰트보다 먼저!)
sns.set_theme(style='whitegrid')

# 2) 한글 폰트 지정
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'   # 윈도우: 맑은 고딕
elif platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'     # 맥: 애플고딕

# 3) 마이너스(-) 기호가 네모(□)로 깨지는 문제 방지
plt.rcParams['axes.unicode_minus'] = False

# (선택) 출력할 때 컬럼이 ... 으로 생략되지 않게 모두 보여줌
pd.set_option('display.max_columns', None)

# *************************************************************************************************************************

OUTPUT_DIR = Path(__file__).with_name("output")

def out(name):
    """ output/ 폴더 내의 파일 경로 반환 """
    OUTPUT_DIR.mkdir(exist_ok=True)
    # 해당 경로가 존재하지 않으면 생성, 존재하면 넘어감(exist_ok=True)
    return OUTPUT_DIR / name

def saved_files():
    """ output/ 폴더에 저장 된 파일 이름 목록 반환 """
    OUTPUT_DIR.mkdir(exist_ok=True)

    # iterdir() : 폴더 안을 하나씩 돌면서 반환
    return sorted(p.name for p in OUTPUT_DIR.iterdir() if p.is_file())

# *************************************************************************************************************************

np.random.seed(42)   # 매번 같은 데이터가 나오도록 고정
n = 250

# ── 범주형: 직업군, 상품유형 ──
job_types = ['직장인', '공무원', '자영업자', '프리랜서', '무직·주부']
job = np.random.choice(job_types, size=n, p=[0.45, 0.10, 0.20, 0.15, 0.10])
product = np.random.choice(['신용대출', '비상금대출', '대환대출'], size=n, p=[0.5, 0.3, 0.2])

# ── 날짜형: 신청일 (2026년 6~8월) ──
start = pd.Timestamp('2026-06-01')
dates = start + pd.to_timedelta(np.random.randint(0, 92, size=n), unit='D')

# ── 신용점수 (직업군별 평균이 다름, 350~990점) ──
score_mean = {'직장인': 760, '공무원': 820, '자영업자': 700, '프리랜서': 680, '무직·주부': 640}
credit_score = np.array([np.random.normal(score_mean[j], 90) for j in job])
credit_score = np.clip(credit_score, 350, 990).round().astype(int)

# ── 연소득 (단위: 만원, 자영업자·프리랜서는 편차가 큼) ──
income_mean = {'직장인': 4500, '공무원': 5000, '자영업자': 4000, '프리랜서': 3200, '무직·주부': 1200}
income_sd   = {'직장인': 0.3,  '공무원': 0.2,  '자영업자': 0.6,  '프리랜서': 0.6,  '무직·주부': 0.5}
income = np.array([np.random.lognormal(np.log(income_mean[j]), income_sd[j]) for j in job]).round(-1)

# ── 제시금리 (단위: %, 신용점수가 높을수록 낮음) ──
rate = 19.0 - (credit_score - 350) / 640 * 14 + np.random.normal(0, 1.2, n)
rate = rate + np.where(product == '비상금대출', 1.5, 0) + np.where(product == '대환대출', -1.0, 0)
rate = np.clip(rate, 4.5, 19.9).round(1)

# ── 제시한도 (단위: 만원, 소득 기반 / 비상금대출은 최대 300만원) ──
limit_ratio = {'직장인': 0.9, '공무원': 1.1, '자영업자': 0.6, '프리랜서': 0.5, '무직·주부': 0.3}
limit_noise = {'직장인': 0.15, '공무원': 0.1, '자영업자': 0.45, '프리랜서': 0.5, '무직·주부': 0.3}
limit = np.array([income[i] * limit_ratio[j] * np.random.lognormal(0, limit_noise[j])
                  for i, j in enumerate(job)])
limit = np.where(product == '비상금대출', np.minimum(limit, 300), limit)
limit = np.clip(limit, 50, 15000).round(-1)

# ── 승인여부 (1=승인, 0=거절 / 신용점수 650 부근에서 급변) ──
logit = (credit_score - 650) / 35 + np.where(job == '무직·주부', -1.0, 0) + np.where(product == '대환대출', 0.5, 0)
prob = 1 / (1 + np.exp(-logit))
approved = (np.random.rand(n) < prob).astype(int)

df = pd.DataFrame({
    '신청일': dates, '직업군': job, '상품유형': product, '신용점수': credit_score,
    '연소득': income, '제시금리': rate, '제시한도': limit, '승인여부': approved
})
df = df.sort_values('신청일').reset_index(drop=True)

# ── [현업 재현 1] 결측치 주입: 직업군 4%, 연소득 6%, 제시한도 3% ──
for col, ratio in [('직업군', 0.04), ('연소득', 0.06), ('제시한도', 0.03)]:
    idx = np.random.choice(n, size=int(n * ratio), replace=False)
    df.loc[idx, col] = np.nan

# ── [현업 재현 2] 이상치 주입 ──
df.loc[30, '연소득'] = 48000000                 # 만원 단위 컬럼에 '원' 단위로 잘못 입력
df.loc[150, '연소득'] = 0                        # 소득 0원 입력
df.loc[[77, 201], '제시금리'] = [35.0, 42.5]     # 법정최고금리(20%) 초과 → 시스템 오류 의심
df.loc[[77, 201], '승인여부'] = 1
high_idx = df[df['신용점수'] >= 900].index[0]
df.loc[high_idx, '제시금리'] = 19.5              # 초고신용자에게 최고 수준 금리 → 금리 역전

# ── CSV 저장 후 다시 불러오기 ──
df.to_csv(out('business_data.csv'), index=False, encoding='utf-8-sig')   # utf-8-sig: 엑셀에서 한글 안 깨짐
df = pd.read_csv(out('business_data.csv'), parse_dates=['신청일'])       # parse_dates: 해당 컬럼을 날짜형으로 읽음

# 차트 범례용: 0/1을 '거절'/'승인' 글자로 바꾼 컬럼 추가
df['승인결과'] = df['승인여부'].map({1: '승인', 0: '거절'})          # map: 값을 사전에 따라 바꿔줌

print(df.shape)     # (행 수, 열 수)
df.head()           # 위에서 5행 미리보기

# *************************************************************************************************************************
"""
[과제 1] 데이터를 믿어도 되는가? 그리고 승인율은 어느 신용점수에서 꺾이는가?
📌 비즈니스 문제 의도

경영진이 가장 먼저 묻는 건 "우리 제휴 금융사들은 몇 점부터 받아주나?"입니다. 
이게 보여야 마케팅팀이 어느 점수대 고객에게 광고비를 써야 하는지 정할 수 있어요. 
그런데 차트를 그리기 전에, 분석가는 반드시 "이 데이터를 믿어도 되는가?"부터 확인해야 합니다.

질문 1-1. 결측치가 있는 컬럼은 어디이고, 비율은 얼마인가? 요약 통계에서 말이 안 되는 값은 없는가?
질문 1-2. 어느 신용점수 구간에서 승인율이 급격히 꺾이는가?

🔍 분석 포인트 힌트
df.isnull()은 칸마다 결측이면 True, 아니면 False를 돌려줍니다. 
True는 1로 계산되니, 이걸 더하면 컬럼별 결측 개수가 됩니다.
describe() 결과에서 min / max 줄을 유심히 보세요. 
연봉 4,800만"만원"(=4,800억 원)인 사람이 대출 비교 앱을 쓸까요? 금리 42.5%가 합법일까요?
승인여부는 0/1이라서 평균을 내면 곧 승인율입니다. (예: 1,1,0,1 → 평균 0.75 = 승인율 75%)
sns.barplot은 기본적으로 그룹별 평균을 막대 높이로 그려줍니다.

✅ 이렇게 그려지면 성공
결측치는 **직업군 약 4%, 연소득 약 6%, 제시한도 약 3%**로 나오고 나머지 컬럼은 0이어야 합니다.
describe()에서 연소득 max가 48,000,000, min이 0, 제시금리 max가 42.5로 튀는 게 보여야 합니다.
막대 차트는 왼쪽(저신용)에서 오른쪽으로 계단처럼 올라가는 모양입니다. 
600 미만은 10% 남짓, 650~699는 50%대인데 700점을 넘는 순간 90% 이상으로 점프합니다. 
800점 이상은 사실상 100%예요.
"""
# ── 1-1. 결측치 확인 ──
print(df.isnull().sum())                    # TODO ①: 컬럼별 결측치 '개수'를 구하는 함수
print((df.isnull().mean() * 100).round(1))    # 컬럼별 결측 '비율(%)' (mean: 평균 → True 비율)

# ── 1-1. 이상치 확인 ──
print(df.describe())                          # describe: 수치형 컬럼의 개수·평균·최소·최대 등 요약 통계

# ── 1-2. 신용점수를 구간으로 나누기 ──
bins = [300, 600, 650, 700, 750, 800, 850, 1000]
labels = ['600 미만', '600~649', '650~699', '700~749', '750~799', '800~849', '850 이상']
df['신용점수구간'] = pd.cut(df['신용점수'], bins=bins, labels=labels, right=False)  # pd.cut: 연속 숫자를 구간(범주)으로 나눔

# 구간별 승인율과 신청 건수를 숫자로도 확인
print(df.groupby('신용점수구간', observed=True)['승인여부'].agg(['mean', 'count']))
# groupby: 그룹별로 묶기 / agg: 여러 집계(평균, 개수)를 한 번에 계산
# observed=True: 범주형 컬럼(pd.cut 결과)에서 실제 데이터가 있는 그룹만 표시 (빈 그룹 제외, 경고 방지)

# ── 1-2. 막대 차트 ──
fig, ax = plt.subplots(figsize=(10, 5))       # 그림판(fig)과 그 위의 차트 영역(ax)을 만듦
sns.barplot(data=df, x='신용점수구간', y='승인여부',          # TODO ②: x축에 올 구간 컬럼 / TODO ③: 승인율이 될 컬럼
            color='steelblue', errorbar=None, ax=ax)   # barplot: 그룹별 평균을 막대로 / errorbar=None: 오차막대 숨김
ax.axhline(df['승인여부'].mean(), color='red', linestyle='--', label='전체 평균 승인율')  # axhline: 가로 기준선
ax.set_title('신용점수 구간별 대출 승인율')
ax.set_xlabel('신용점수 구간')
ax.set_ylabel('승인율')
ax.legend()
plt.tight_layout()                            # 제목·라벨이 잘리지 않게 여백 자동 조정
fig.savefig(out('self_practice01.png'), dpi=120)
plt.close(fig)

# *************************************************************************************************************************
"""
[과제 2] 제시 금리는 신용점수를 제대로 반영하고 있는가? 이상 징후는 없는가?
📌 비즈니스 문제 의도

대출 비교 서비스의 신뢰는 "내 신용에 맞는 금리를 보여준다"는 데서 나옵니다. 
만약 고신용자에게 고금리가 제시되거나 법정최고금리(20%)를 넘는 금리가 노출됐다면, 
이건 단순 데이터 오류가 아니라 컴플라이언스 이슈라서 즉시 리스크팀·제휴사에 공유해야 합니다.

질문 2. 신용점수와 제시금리는 어떤 관계인가? 그 관계에서 벗어난 "이상한 점"은 몇 건이고, 어떤 고객인가?

🔍 분석 포인트 힌트
산점도는 점 하나가 신청 1건입니다. x축, y축에 연속형 숫자 컬럼 두 개를 놓으세요.
hue에 컬럼을 넣으면 그 값에 따라 점 색깔이 달라집니다. 승인/거절을 색으로 나누면 "승인선"이 보일 거예요.
20% 위치에 빨간 기준선을 그어 두면, 선 위에 있는 점이 곧 문제 건입니다.
상관계수는 이상치를 넣었을 때와 뺐을 때 둘 다 계산해 비교해 보세요. 
이상치 몇 건이 결론을 얼마나 흔드는지 체감할 수 있습니다.

✅ 이렇게 그려지면 성공
점들이 왼쪽 위에서 오른쪽 아래로 내려가는 띠 모양이어야 합니다. (신용점수↑ → 금리↓)
왼쪽(저신용)은 빨간 거절 점, 오른쪽은 파란 승인 점이 몰려 있습니다.
20% 선 위로 튀어나온 점 2개(35.0%, 42.5%)가 보이고, 둘 다 '승인'입니다. 
오른쪽 끝(940점대)에 혼자 19.5%에 떠 있는 점도 하나 보여요. outliers 출력은 3행입니다.
상관계수는 전체 약 -0.59, 이상치 제거 후 약 -0.76. 이상치 단 2건이 관계를 꽤 흐려놓고 있다는 뜻입니다.
"""
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=df, x='신용점수', y='제시금리', hue='승인결과',    # TODO ①②③: x축 컬럼, y축 컬럼, 색 구분 컬럼
                palette={'승인': 'royalblue', '거절': 'tomato'},
                alpha=0.7, ax=ax)                     # scatterplot: 산점도 / alpha: 점 투명도(겹침 확인용)
ax.axhline(20, color='red', linestyle='--', label='법정최고금리 20%')
ax.set_title('신용점수 vs 제시금리 (승인 여부별)')
ax.set_xlabel('신용점수')
ax.set_ylabel('제시금리 (%)')
ax.legend()
plt.tight_layout()
fig.savefig(out('self_practice02.png'), dpi=120)
plt.close(fig)

# ── 이상치 행 뽑아보기 ──
# 조건 1: 금리 20% 초과 / 조건 2: 900점 이상인데 금리 15% 이상 ( | 는 '또는')
outliers = df[(df['제시금리'] > 20) | ((df['신용점수'] >= 900) & (df['제시금리'] >= 15))]
print(outliers)

# ── 상관계수 비교 ──
df_clean = df[df['제시금리'] <= 20]                                 # 대괄호 안 조건: 조건을 만족하는 행만 남김
print('전체      :', df['신용점수'].corr(df['제시금리']).round(2))    # corr: 두 컬럼의 상관계수(-1~1)
print('이상치 제거:', df_clean['신용점수'].corr(df_clean['제시금리']).round(2))

# *************************************************************************************************************************
"""
[과제 3] 직업군별로 한도 산정이 얼마나 "들쭉날쭉"한가?
📌 비즈니스 문제 의도

평균 한도만 보면 "자영업자는 2천만 원쯤 받는다"로 끝나지만, 실제 고객 경험은 분산이 결정합니다. 
같은 직업군인데 누구는 500만 원, 누구는 1억이면 고객은 "비교해 봐야 소용없다"고 느끼고 이탈하죠. 
분산이 큰 세그먼트는 소득 증빙 연동(홈택스, 건보료 등)을 강화할 1순위 후보가 됩니다.

질문 3. 승인된 고객 기준으로, 직업군별 제시한도의 중앙값과 흩어짐은 어떻게 다른가? 
어느 세그먼트의 한도가 가장 예측하기 어려운가?

🔍 분석 포인트 힌트
공정한 비교를 위한 필터링: 거절 건은 한도가 의미 없고, 비상금대출은 최대 300만 원이라 섞으면 분산이 왜곡됩니다. 템플릿에 필터는 미리 넣어 뒀어요.
박스플롯 읽는 법: 상자 가운데 선 = 중앙값, 상자 길이 = 가운데 50% 고객의 범위, 바깥 점 = 튀는 값. 
상자가 길수록 들쭉날쭉합니다.
숫자로는 표준편차(std)를 보세요. 표준편차가 중앙값보다 크다면 상당히 불안정한 세그먼트입니다.

✅ 이렇게 그려지면 성공
**공무원(중앙값 약 5,300만)·직장인(약 4,600만)**은 상자가 높은 곳에 짧고 촘촘하게 있습니다. 
표준편차가 1,000~1,300만 원 수준이에요.
자영업자는 중앙값이 약 2,400만인데 표준편차가 약 2,900만으로 중앙값보다 큽니다. 
상자와 수염이 위로 길게 뻗고 튀는 점도 보입니다.
프리랜서도 중앙값(약 1,600만)보다 표준편차(약 1,800만)가 큽니다.
무직·주부는 바닥에 납작하게 붙어 있고, 건수가 6건뿐이라 해석에 주의가 필요합니다.
"""
# 승인 건 중 비상금대출을 제외 ( != 는 '같지 않다', & 는 '그리고')
df_limit = df[(df['승인여부'] == 1) & (df['상품유형'] != '비상금대출')]

# 직업군별 중앙값·표준편차·건수
print(df_limit.groupby('직업군')['제시한도'].agg(['median', 'std', 'count']).round(0))
# TODO ①: 표준편차를 뜻하는 집계 이름 (median: 중앙값)

order = ['공무원', '직장인', '자영업자', '프리랜서', '무직·주부']   # 차트에 표시할 순서

fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=df_limit, x='직업군', y='제시한도', order=order,   # TODO ②③: 그룹 컬럼, 분포를 볼 수치 컬럼
            palette='Set2', hue='직업군', legend=False, ax=ax)  # boxplot: 그룹별 분포를 상자 모양으로 요약
ax.set_title('직업군별 제시한도 분포 (승인 건, 비상금대출 제외)')
ax.set_xlabel('직업군')
ax.set_ylabel('제시한도 (만원)')
plt.tight_layout()
fig.savefig(out('self_practice03.png'), dpi=120)
plt.close(fig)

# *************************************************************************************************************************
"""
[과제 4 · 보너스] 어떤 "직업군 x 상품" 조합에 전환 병목이 있는가?
📌 비즈니스 문제 의도

과제 1~3은 한 축씩 봤다면, 실무 액션은 보통 두 축의 조합에서 나옵니다. 
예를 들어 "프리랜서가 신용대출에서 유독 승인율이 낮다"면, 
프리랜서에게는 신용대출 대신 승인 가능성이 높은 상품을 먼저 추천하는 식으로 추천 로직을 바꿀 수 있어요.

질문 4. 직업군 x 상품유형 조합별 승인율 중 가장 낮은 곳은 어디인가? 그 숫자는 믿을 만한 표본 크기인가?

🔍 분석 포인트 힌트
pivot_table은 엑셀 피벗과 똑같습니다: 행(index), 열(columns), 채울 값(values), 집계 방식(aggfunc).
승인율이니까 집계 방식은? (과제 1 힌트를 떠올려 보세요.)
표본 수를 꼭 같이 보세요. 1건 신청해서 1건 승인이면 승인율 100%지만, 이걸 경영진 보고서에 쓰면 안 되겠죠.

✅ 이렇게 그려지면 성공
5행(직업군) x 3열(상품유형) 격자에 퍼센트 숫자가 찍혀 있어야 합니다.
무직·주부 줄 전체가 빨간색(27~40%)이고, 특히 무직·주부 x 신용대출이 약 27%로 최저입니다.
**프리랜서 x 신용대출(약 53%)**도 주황색으로 눈에 띕니다. 같은 프리랜서라도 비상금대출은 75%예요.
**공무원 x 대환대출이 100%**로 초록색이지만, pivot_cnt를 보면 단 1건입니다. 이걸 알아채면 진짜 성공입니다.

🚀 시간이 남으면 도전: 
df['신청월'] = df['신청일'].dt.month(.dt.month: 날짜에서 월만 꺼냄)로 
월 컬럼을 만들고, index='신청월', columns='신용점수구간' 히트맵을 그려 보세요. 
승인 기준이 월별로 바뀌었는지 볼 수 있습니다.
"""
# 조합별 승인율 피벗
pivot_rate = df.pivot_table(index='직업군', columns='상품유형',   # TODO ①②: 행에 올 컬럼, 열에 올 컬럼
                            values='승인여부', aggfunc='mean')   # TODO ③: 집계 방식 (문자열로)
# pivot_table: 행×열 조합별로 값을 집계한 표를 만듦

# 조합별 신청 건수 (표본 크기 확인용)
pivot_cnt = df.pivot_table(index='직업군', columns='상품유형', values='승인여부', aggfunc='count')
print(pivot_cnt)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
sns.heatmap(pivot_rate, annot=True, fmt='.0%', cmap='RdYlGn',
            vmin=0, vmax=1, linewidths=0.5, ax=axes[0])
# heatmap: 표의 숫자를 색으로 표시 / annot: 칸에 숫자 표시 / fmt='.0%': 0.75 → 75% 형식
# cmap='RdYlGn': 낮으면 빨강, 높으면 초록 / vmin·vmax: 색 기준 범위 고정
axes[0].set_title('직업군 x 상품유형별 승인율')

# TODO BOUNUS : 승인 기준 월별
df['신청월'] = df['신청일'].dt.month

pivot_rate_mon = df.pivot_table(index='신청월', columns='신용점수구간', values='승인여부', aggfunc='mean', observed=True)
# observed=True: 실제로 신청이 있었던 '월 x 구간' 조합만 표에 포함
pivot_cnt_mon = df.pivot_table(index='신청월', columns='신용점수구간', values='승인여부', aggfunc='count', observed=True)
print(pivot_cnt_mon)

# 신청월 x 신용점수구간 승인율 heatmap 으로 표시해보기
sns.heatmap(pivot_rate_mon, annot=True, fmt='.0%', cmap="RdYlGn", vmin=0, vmax=1, linewidths=0.5, ax=axes[1])
axes[1].set_title('신청월 x 신용점수구간 승인율')

plt.tight_layout()
fig.savefig(out('self_practice04.png'), dpi=120)
plt.close(fig)
