import random

# 1. 몸무게(kg)와 키(cm)를 입력받아 BMI 지수를 계산하는 함수를 정의
def bmi():
    weight = int(input("몸무게를 입력하세요(kg): "))
    height = float(input("키를 입력하세요(cm): ")) / 100
    bmi = weight / (height * height)
    print(f"BMI: {weight / (height * height):.2f}")

# bmi()

# 2. 여러 개의 숫자를 입력받아 평균을 계산하는 함수를 정의
def avg_num():
    print("========== 평균 계산기 ==========")

    numbers = []

    while True:
        num = input("숫자 입력 (q 입력 시 종료) : ")
        if num == 'q':
            break
        numbers.append(float(num))

    if len(numbers) == 0:
        print("---> 값이 없습니다.")
    else:
        avg = round(sum(numbers)/len(numbers), 2)
        print(f"---> 평균: {avg}")

# avg_num()

# 3. 단어 빈도수 분석 함수 정의
def word_used():
    sentence = input("문장을 입력하세요: ")
    words = sentence.lower().split()

    word_count = {w: words.count(w) for w in words}

    print("단어 빈도수 결과")
    for word, count in word_count.items():
        print(f"- {word}: {count}회")
    

#word_used()

# 4. 로또 번호 자동 생성 함수 정의
def lotto():
    game_round = int(input("구매할 로또 게임 수를 입력하세요: "))

    print("\n[로또 번호 발급 결과]")
    for i in range(1, game_round+1):
        numbers = []
        while len(numbers) < 6:
            num = random.randint(1, 45)

            # 중복 번호 방지
            if num not in numbers:
                numbers.append(num)
        
        print(f"{i}게임: {sorted(numbers)}")

# lotto()

# 5. 학생 성적 통계 분석 함수 정의
def analyze_scores(scores):
    if not scores:
        return None, None, 0.0
    
    # 최고 득점자 및 최저 득점자 계산
    max_student = max(scores.items(), key=lambda x: x[1])
    min_student = min(scores.items(), key=lambda x: x[1])
    avg_score = sum(scores.values()) / len(scores)
    
    return max_student, min_student, round(avg_score, 2)

student_scores = {
    "홍길동": 85,
    "이순신": 96,
    "강감찬": 72,
    "유관순": 91
}
top_scorer, low_scorer, average = analyze_scores(student_scores)

print("========== 학생 성적 분석 결과 ==========")
print(f"- 최고 득점자: {top_scorer[0]} ({top_scorer[1]}점)")
print(f"- 최저 득점자: {low_scorer[0]} ({low_scorer[1]}점)")
print(f"- 전체 평균: {average}점")