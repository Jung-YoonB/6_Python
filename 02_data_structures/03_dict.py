"""
    딕셔너리 (dict)
"""

# JSON 형식과 유사한 구조
# key-value 형태로 데이터를 관리

user = {
    "name": "pizza",
    "age": 20,
    "skills": ["java", "sql", "html/css", "js", "python"]
}

print(f"user : {user}")

print()

# 딕셔너리 내의 데이터 접근 -> 키값 사용
print(f"이름 : {user['name']}")
print(f"스킬 : {user['skills']}")

# KeyError: 'phone' --> print(f"연락처 : {user['phone']}")
#                   --> 직접 접근 시 존재하지 않는 키 값은 오류 발생
print()
# get() 사용하여 접근
print("get() 로 key 접근")
print(f"이름 : {user.get('name')}")
print(f"스킬 : {user.get('skills')}")

print(f"연락처 : {user.get('phone')}")  # 존재하지 않는 키 값인 경우 오류가 아닌 None 반환
print(f"연락처 : {user.get('phone', '없음')}")  # 기본값 지정 가능
print()

# 변경 (추가/수정/삭제)
user['email'] = 'pizza@gmail.com'
print(f"user 이메일 추가 : {user}")

user['age'] = 80        # 기존의 키 값을 지정하면 변경
print(f"user 나이 변경 : {user}")

del user['age']
print(f"user 나이 삭제 : {user}")

# KeyError: 'phone' --> del user['phone']

print()
print("=" * 60)

# 탐색
for key in user:
    print(f"key: {key} / value: {user[key]}")

print()

for k, v in user.items():
    print(f"key: {k} / value{v}")

print()

print(f"키 목록 : {list(user.keys())}")
print(f"밸류 목록 : {list(user.values())}")
print(f"items() : {list(user.items())}")