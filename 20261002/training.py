"""
    해결 과제
"""
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from chart_config import setup, out, saved_files
from loader import load_train, AGE_BINS, extract_title

pd.set_option("display.width", 140)     # 출력창 가로길이

setup() # 한글 폰트, 마이너스 기호 설정
# 1 =====================================================================================================
print("-" * 140)
print("1. train.csv 파일을 DataFrame 으로 저장")
print("-" * 140)

df = load_train()
print("저장 완료")

# 2 =====================================================================================================
print("-" * 140)
print("2. 상위 5개 행 출력")
print("-" * 140)

print(df.head())

# 3 =====================================================================================================
print("-" * 140)
print("3. 열 이름, 결측치 여부, 데이터 타입 확인")
print("-" * 140)
"""
    df.info()를 실행한 후, 출력 결과를 바탕으로 다음을 기술하시오.

    - 결측치가 존재하는 열과 결측 개수
    - dtype이 예상과 다르거나 주의가 필요한 열
"""
df.info()   # 열 이름, non-null 개수, dtype 을 한번에 출력

print("*" * 70)
print("[결측치가 존재하는 열] (전체 891 행 - non-null 개수)")
na = df.isna().sum()

for col in df.columns:
    if na[col] > 0:
        print(f" [{col:<10}] (결측 개수 : {na[col]:>4} 개)")

print("*" * 70)
print("<dtype이 예상과 다르거나 주의가 필요한 열>")
print("""
1. Age          : int64 가 아닌 float64 로 실수형 / 영아의 경우 0.42 처럼 소수로 기록
2. Survived     : int64 지만 0 = 사망 / 1 = 생존으로 의미 없는 범주형
3. Pclass       : int64 지만 1/2/3 등급의 등급구분 범주형, 1 < 3 이 더 작은 값 X, 더 좋은 등급 O
4. Sex          : 문자열이므로 상관관계, 수치 계산에 바로 사용 불가
5. Cabin        : 문자열 + 결측 개수가 많아 분석에 그대로 사용키 어려움
6. Ticket       : A/5 21171 처럼 문자가 섞여있어 문자열
"""
)

# 4 =====================================================================================================
print("-" * 140)
print("4. Age, Fare 의 평균값, 최솟값, 최댓값")
print("-" * 140)
stats = df[['Age', 'Fare']].agg(['mean', 'min', 'max']).round(2)
print(stats)

# 5 =====================================================================================================
print("-" * 140)
print("5. 생존자 / 사망자 수")
print("-" * 140)

survived_cnt = df['Survived'].value_counts()

print(f"사망자 (Servived = 0) : {survived_cnt.loc[0]} 명")
print(f"생존자 (Servived = 1) : {survived_cnt.loc[1]} 명")

# 6 =====================================================================================================
print("-" * 140)
print("6. 객실 등급(Pclass)별 탑승객 수")
print("-" * 140)

pclass_cnt = df['Pclass'].value_counts().sort_index()

for pclass, cnt in pclass_cnt.items():
    print(f"{pclass}등급 : {cnt:>4} 명")

# 7 =====================================================================================================
print("-" * 140)
print("7. 나이 50세 이상 탑승객 추출")
print("-" * 140)

over_50 = df[df['Age'] >= 50].copy()

print(f"50세 이상 : {len(over_50)} 명")
print("*" * 70)
print(over_50[['Name', 'Age', 'Pclass', 'Survived']].head())

# 8 =====================================================================================================
print("-" * 140)
print("8. 나이대(AgeGroup) 열 추가")
print("-" * 140)

# 1) AgeGroup 기본 결측치 미확인으로 세팅
df['AgeGroup'] = '미확인'

# 2) 구간별 값 입력
for start, end, label in AGE_BINS:
    mask = (df['Age'] >= start) & (df['Age'] < end)
    df.loc[mask, 'AgeGroup'] = label

# 3) 60세 이상
df.loc[df['Age'] >= 60, 'AgeGroup'] = '60대 이상'

print(df[['Name', 'Age', 'AgeGroup']].head())

# 9 =====================================================================================================
print("-" * 140)
print("9. 성별(Sex) + 객실 등급(Pclass)별 평균 생존율")
print("-" * 140)
 
# Survived 는 0/1 이므로 평균 = 생존자 비율(생존율)
#   예) [1, 0, 1, 1] -> 합/개수 (3/4) = 0.75 -> 75% 생존
sex_pclass = df.groupby(['Sex', 'Pclass'])['Survived'].mean().round(2)
print(sex_pclass)

# 10 =====================================================================================================
print("-" * 140)
print("10. 나이대(AgeGroup)별 평균 생존율")
print("-" * 140)
"""
8번에서 생성한 AgeGroup 열을 기준으로 그룹화하여 계산하시오.
"""
age_rate = df.groupby('AgeGroup')['Survived'].mean().round(2)

order = [label for start, end, label in AGE_BINS] + ['60대 이상', '미확인']
age_rate = age_rate.loc[order]
 
for group, rate in age_rate.items():
    print(f"{group:<8} : {rate:.2f}")


# 11 =====================================================================================================
print("-" * 140)
print("11. 열별 결측치 개수와 비율 (내림차순)")
print("-" * 140)
 
# 결측 개수 / 전체 행 수 * 100 = 결측 비율(%)
na_cnt = df.isna().sum()
na_ratio = (na_cnt / len(df) * 100).round(2)
 
na_df = pd.DataFrame({'결측수': na_cnt, '비율(%)': na_ratio})
 
na_df = na_df.sort_values('결측수', ascending=False)
print(na_df)
# 참고: 8번에서 결측을 '미확인'으로 채웠기 때문에 AgeGroup 의 결측은 0


# 12 =====================================================================================================
print("-" * 140)
print("12. Sex -> Gender_Encoded (male: 0, female: 1)")
print("-" * 140)
 
# map(함수) : 시리즈 값 하나하나에 함수를 적용한 결과로 새 시리즈 반환
df['Gender_Encoded'] = df['Sex'].map(lambda s: 1 if s == 'female' else 0)
# 주의: 'female' 이 아닌 값은 전부 0 이 됨 (오타·결측이 있어도 0 으로 바뀌어 남자로 처리)

print(df[['Sex', 'Gender_Encoded']].head())


# 13 =====================================================================================================
print("-" * 140)
print("13. 탑승지(Embarked)별 평균 요금(Fare)")
print("-" * 140)
 
# C = Cherbourg, Q = Queenstown, S = Southampton
embarked_fare = df.groupby('Embarked')['Fare'].mean().round(2)
 
for port, fare in embarked_fare.items():
    print(f"{port} : {fare:>7.2f}")

# 14 =====================================================================================================
print("-" * 140)
print("14. 피벗 테이블 (인덱스(행): Pclass, 컬럼(열): Sex, 값: Fare 평균)")
print("-" * 140)

# pivot_table(index=행, columns=열, values=셀_값, aggfunc=집계함수)
pv = df.pivot_table(index='Pclass', columns='Sex', values='Fare', aggfunc='mean').round(2)
print(pv)

# 15 =====================================================================================================
print("-" * 140)
print("15. FamilySize (SibSp + Parch) 열 추가 + 요약 통계")
print("-" * 140)
 
# 열 + 열 (형제/배우자 수) + (부모/자녀 수)
df['FamilySize'] = df['SibSp'] + df['Parch']
 
# describe() : 개수, 평균, 표준편차, 최솟값, 사분위수(25/50/75%), 최댓값
print(df['FamilySize'].describe().round(2))

# 16 =====================================================================================================
print("-" * 140)
print("16. 이름에서 호칭(Title) 추출 + 가장 흔한 호칭 5개")
print("-" * 140)
 
df['Title'] = df['Name'].map(extract_title)
 
print(df[['Name', 'Title']].head())
 
print("*" * 70)
print("[가장 흔한 호칭 5개]")
# value_counts() 는 개수가 많은 순으로 정렬 -> head(5) 로 상위 5개
print(df['Title'].value_counts().head(5))

# 17 =====================================================================================================
print("-" * 140)
print("17. 호칭(Title)별 승객 수, 평균 나이, 평균 생존율")
print("-" * 140)
 
# Named Aggregation : 새로운_열_이름=(대상_열, 집계함수)
#       count 는 결측을 제외하고 세므로 결측이 없는 PassengerId 로 승객 수 카운트
title_summary = df.groupby('Title').agg(
                    승객수=('PassengerId', 'count'),
                    평균나이=('Age', 'mean'),
                    평균생존율=('Survived', 'mean')
                ).round(2)

title_summary = title_summary.sort_values('승객수', ascending=False)
print(title_summary)

# 18 =====================================================================================================
print("-" * 140)
print("18. 생존/사망자 나이(Age) 분포 비교 (히스토그램)")
print("-" * 140)
"""
- 히스토그램 또는 KDE(밀도) 플롯 중 하나를 사용하시오.
- 그래프에는 다음 요소를 반드시 포함하시오.
    - 제목 (set_title)
    - x축·y축 라벨 (set_xlabel, set_ylabel)
    - 생존/사망 구분 범례 (legend)
- 결과를 화면에 출력하지 않고 **이미지 파일로 저장**하시오. (savefig 사용)
"""
# 주의: 19번(결측 대치)보다 먼저 그려야 함
#       대치 후에 그리면 중앙값 위치에 막대가 비정상적으로 솟아서 실제 분포가 왜곡됨
# 생존/사망 나누기 (불리언 인덱싱) + 결측 제거
# hist 는 NaN 을 만나면 범위 계산이 깨짐 -> dropna() 선행
dead_age = df[df['Survived'] == 0]['Age'].dropna()
alive_age = df[df['Survived'] == 1]['Age'].dropna()

# subplots(행, 열) : 1행 2열 -> 그래프 칸 2개 (axes[0], axes[1])
# sharey=True : 두 그래프의 y축 눈금을 똑같이 맞춤
#   -> 맞추지 않으면 각자 최댓값 기준으로 그려져서 인원 수 비교가 왜곡됨
fig, axes = plt.subplots(1, 2, figsize=(13, 5), sharey=True)

# 두 그래프에 들어갈 값들을 순서대로 묶어서 반복
#   zip : 여러 목록을 같은 순서끼리 묶어서 하나씩 꺼냄
datas = [dead_age, alive_age]
labels = ["사망", "생존"]
colors = ["indianred", "steelblue"]

for ax, data, label, color in zip(axes, datas, labels, colors):
    # bins=range(0, 85, 5) : 0~5, 5~10, ... 5살 간격 -> 두 그래프의 구간을 똑같이 맞춤
    ax.hist(data, bins=range(0, 85, 5), color=color, label=label)

    # 제목 / 축 라벨 / 범례 -> 칸(ax)마다 따로 지정
    #   주의: axes.set_title() 처럼 묶음 전체에 호출하면 오류 -> 반드시 칸 하나(ax)에 호출
    ax.set_title(f"{label}자 나이 분포 ({len(data)}명)")
    ax.set_xlabel("나이(세)")
    ax.set_ylabel("인원(명)")
    ax.legend()     # 주의: label 을 지정해도 legend() 를 호출해야 범례가 표시됨
    ax.grid(alpha=0.3)

# 전체 그래프의 큰 제목
fig.suptitle("생존 여부에 따른 나이 분포")

# 화면 출력 없이 파일로 저장 -> 닫기
fig.tight_layout()      # 그래프끼리 제목·라벨이 겹치지 않게 간격 자동 조정
fig.savefig(out("18_age_hist.png"), dpi=120)
plt.close(fig)
print(f"저장 완료 : {out('18_age_hist.png').name}")

# 19 =====================================================================================================
print("-" * 140)
print("19. Title + Pclass 그룹 나이 중앙값으로 Age 결측 대치")
print("-" * 140)
"""
- ex. 'Master' 타이틀을 가진 1등급 승객 그룹의 나이 중앙값으로 해당 그룹의 결측치를 채운다.
- `groupby().transform("median")`을 활용하면 그룹별 중앙값을 원본과 같은 길이로 얻을 수 있다.

> ⚠️ 이 문제는 반드시 **16번 완료 후** 진행하시오. `Title` 열이 존재해야 그룹 기준으로 사용할 수 있습니다.
"""
print(f"대치 전 Age 결측 : {df['Age'].isna().sum()} 개")
 
# transform('median') : 그룹별 중앙값을 원본과 같은 길이(891행)로 반환
#   -> 각 행 자리에 "그 행이 속한 그룹의 중앙값"이 들어감
#   => agg 를 쓰면 그룹 수만큼의 행만 나와서 원본과 바로 맞출 수 없음
group_median = df.groupby(['Title', 'Pclass'])['Age'].transform('median')
 
# fillna(시리즈) : 결측인 자리만, 같은 인덱스 위치의 값으로 채움 (기존 값은 그대로)
#   주의: fillna 는 새 시리즈를 반환 -> df['Age'] 에 다시 대입해야 원본에 적용
df['Age'] = df['Age'].fillna(group_median)
 
print(f"대치 후 Age 결측 : {df['Age'].isna().sum()} 개")

# 20 =====================================================================================================
print("-" * 140)
print("20. 수치형 변수 상관관계 히트맵")
print("-" * 140)
"""
- corr() : 상관관계 행렬 계산 함수
- sns.heatmap(..., annot=True, cmap="coolwarm", center=0) 형식으로 작성하면 값이 셀 안에 표시됩니다.
- 결과를 화면에 출력하지 않고 **이미지 파일로 저장**하시오. (savefig 사용)
"""
num_cols = ['Survived', 'Pclass', 'Age', 'SibSp', 'Parch', 'Fare', 'Gender_Encoded', 'FamilySize']

# corr() : 열끼리 상관계수 (-1 반대 ~ 0 무관 ~ 1 같이 움직임), 대각선은 항상 1
#   주의: 문자열 열이 섞이면 오류 -> 수치형 열만 골라서 계산
corr = df[num_cols].corr().round(2)
print(corr)
 
fig, ax = plt.subplots(figsize=(9, 7))
 
#   annot=True : 셀 안에 값 표시
#   fmt=".2f"  : 셀 값 소수 둘째 자리까지
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, vmin=-1, vmax=1, ax=ax)
ax.set_title("타이타닉 수치형 변수 상관관계")
 
fig.savefig(out("20_corr_heatmap.png"), dpi=120)
plt.close(fig)
print(f"저장 완료 : {out('20_corr_heatmap.png').name}")