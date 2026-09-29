"""
    환경 설정 확인
    (실습 시작 시 실행하여 결과를 확인)

    1. 패키지 설치 확인
    2. .env 파일 (파일 존재, 설정 항목 여부)
    3. 오라클 접속
    4. 문자셋 확인
    5. 권한 (테이블 생성, 삭제)
"""
import os

def step1_packages():
    """ 패키지 설치 여부 확인 """
    need = {
        "oracledb": "Oracle 드라이버",
        "sqlalchemy": "DB 추상화 계층 (Pandas 연동)",
        "dotenv": "환경 변수 로딩",
        "pandas": "데이터 처리",
        "requests": "API 호출"
    }

    missing = []
    for mod, desc in need.items():
        try:
            m = __import__(mod)
            ver = getattr(m, '__version__', '')
            print(f"[ OK ] {mod:<14}{ver:<12}{desc}")
        except ImportError:
            print(f"[ 실패 ] {mod:<14}{'':<12}{desc}")
            missing.append(mod)

    if missing:
        raise RuntimeError(
            f"설치되지 않은 항목 : {missing}\n"
            "   해결: pip install -r requirements.txt\n"
            " requirements.txt 파일이 없는 경우, 직접 설치\n"
            f"  해결: pip install oracledb sqlalchemy dotenv pandas requests"
        )

def step2_env():
    """ .env 파일 확인 """
    from dotenv import load_dotenv

    if not os.path.exists(".env"):
        raise FileNotFoundError(
            ".env 파일이 없습니다.\n"
            "   해결: copy .env.example .env\n"
            "        그다음 설정 항목에 값을 채워주세요."
        )

    load_dotenv()

    required = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]
    for key in required:
        value = os.getenv(key)

        if not value:
            raise ValueError(f"{key} 가 비어 있습니다.")

        show = "*"*len(value) if "PASSWORD" in key else value
        print(f"[ OK ] {key:<14} {show}")

    if "write" in os.getenv("DB_PASSWORD", ""):
        raise ValueError(
            "DB_PASSWORD 가 예시 그대로입니다.\n"
            ".env 파일을 열어 값을 변경해주세요."
            )

    # .gitignore : 깃에서 관리하지 않을 항목 관리하는 파일
    for gitign in (".gitignore", os.path.join("..", ".gitignore")):
        if os.path.exists(gitign):
            with open(gitign, encoding="UTF-8") as f:
                if ".env" in f.read():
                    print(f"[ OK ] .gitignore에 .env 파일이 등록됨 ({gitign})")
                else:
                    print(f"[ 실패 ] {gitign} 에 .env 파일이 없음! 추가 필요!")
            break
    else:
        # for문이 break 없이 끝났을 때 실행되는 부분! => 제시한 경로에서 파일을 찾지 못했을 때
        print(f"[ 실패 ] .gitignore 파일을 찾지 못했습니다. 파일을 추가해주세요.")

def step3_connect():
    """ 오라클 접속 확인 """
    import oracledb
    from dotenv import load_dotenv

    load_dotenv()

    try:
        conn = oracledb.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            dsn=f'{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'
        )
    except oracledb.Error as e:
        err_obj, = e.args
        code = err_obj.code

        message = {
            1017: "비밀번호나 사용자명이 잘못되었습니다. .env 파일을 확인하세요.",
            12154: "접속 식별자를 해석하지 못했습니다. HOST, NAME을 확인하세요.",
            12541: "TNS 리스너가 없습니다. 포트 번호, 서버 실행 여부를 확인하세요."
        }.get(code, "해당 코드를 관리자에게 문의하세요. (검색)")

        raise RuntimeError(f"{e}\n --> {message}")
    except UnicodeEncodeError:
        # 비밀번호에 한글이 포함된 경우 해당 예외가 발생!
        raise RuntimeError(
            "접속 정보에 한글이 포함되어 있습니다.\n"
            "   --> DB 비밀번호, 사용자명은 영문, 숫자, 기호로만 사용해주세요."
        )

    # ... 서버 버전, DB 정보 출력
    with conn.cursor() as cur:
        cur.execute("SELECT banner FROM v$version WHERE ROWNUM <= 1")
        print(f"[ OK ] 서버 버전    {cur.fetchone()[0]}")

        cur.execute("SELECT sys_context('USERENV', 'DB_NAME') FROM dual")
        print(f"[ OK ] 현재 DB    {cur.fetchone()[0]}")
    conn.close()

    # SQLAlchemy 확인
    from sqlalchemy import create_engine, text

    url = (f"oracle+oracledb://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
           f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/?service_name={os.getenv('DB_NAME')}")
    engine = create_engine(url)

    with engine.connect() as c:
        c.execute(text("SELECT 1 FROM dual"))

    print("[ OK ] SQLAlchemy 엔진 생성 및 접속 성공")

def step4_charset():
    """ 문자셋 확인 """
    import oracledb
    from dotenv import load_dotenv

    load_dotenv()
    conn = oracledb.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dsn=f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

    with conn.cursor() as cur:
        cur.execute("SELECT value FROM v$nls_parameters WHERE parameter = 'NLS_CHARACTERSET'")

        charset = cur.fetchone()[0]
        print(f"[ OK ] 문자셋 {charset}")

        if charset not in ("AL32UTF8", "UTF8"):
            conn.close()
            raise ValueError(
                f"문자셋 {charset} 으로 설정되어 있습니다. AL32UTF8 또는 UTF8이어야 합니다.\n"
                "   오라클 DB 문자셋 설정을 변경해주세요."
            )

        cur.execute("CREATE TABLE charset_test (txt VARCHAR2(100))")
        cur.execute("INSERT INTO charset_test VALUES (:1)", ("가온전자 🎶",))
        conn.commit()

        cur.execute("SELECT txt FROM charset_test")
        result = cur.fetchone()[0]

        cur.execute("DROP TABLE charset_test")
    conn.close()

    if result == "가온전자 🎶":
        print(f"[ OK ] 한글, 이모지 저장/조회 확인 ({result})")
    else:
        raise ValueError(f"[ 실패 ] 문자가 깨졌습니다. ({result})")

def step5_privileges():
    """ 테이블 처리 권한 확인 """
    import oracledb
    from dotenv import load_dotenv

    load_dotenv()
    conn = oracledb.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dsn=f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE perm_test (
                id NUMBER PRIMARY KEY,
                code VARCHAR2(10),
                note VARCHAR2(10),

                CONSTRAINT uk_perm_code UNIQUE (code)
            )
        """)
        print(f"[ OK ] CREATE TABLE 성공 (제약조건 포함)")

        cur.execute("INSERT INTO perm_test (id, code) VALUES (:1, :2)", (1, "G0001"))
        conn.commit()

        print(f"[ OK ] INSERT, COMMIT 성공")

        cur.execute("""
            MERGE INTO perm_test dst
            USING (SELECT :1 AS code FROM dual) src
            ON (dst.code = src.code)
            WHEN MATCHED THEN
                UPDATE SET dst.note = 'test'
            WHEN NOT MATCHED THEN
                INSERT (id, code) VALUES (2, src.code)
        """, ("G0001", ))
        conn.commit()

        cur.execute("SELECT COUNT(*) FROM perm_test")
        n = cur.fetchone()[0]
        print(f"[ OK ] UPSERT 동작 확인 (결과: {n})")

        cur.execute("DROP TABLE perm_test")
        print(f"[ OK ] DROP TABLE 완료")

    conn.close()

    if n != 1:
        raise ValueError(f"UPSERT 후 결과가 {n}행 입니다. 1개여야 합니다.")

# ======================================================
results = []
def check(name, fn):
    """ 점검 항목을 실행하고 결과를 기록 """
    print(f"\n{'=' * 60}")
    print(f" {name}")
    print('=' * 60)

    try:
        fn()
        results.append((name, True))
    except Exception as e:
        print(f"[ 실패 ] {type(e).__name__}: {e}")
        results.append((name, False))
# ======================================================

if __name__ == "__main__":
    print("=" * 60)
    print(" 실습 환경 점검 ")
    print("=" * 60)

    check("1. 패키지 설치", step1_packages)
    check("2. .env 파일", step2_env)
    check("3. 오라클 접속", step3_connect)
    check("4. 문자셋 확인", step4_charset)
    check("5. 권한 확인", step5_privileges)

    print("=" * 60)
    print(" 결과 ")
    print("=" * 60)

    for name, ok in results:
        print(f" {'통과' if ok else '실패'}  {name}")

    passed = sum(ok for _, ok in results)
    print(f"\n {passed} / {len(results)} 항목 통과")

    if passed == len(results):
        print("모든 준비가 끝났습니다.")
    else:
        print("실패한 항목에 대해서 처리 후 다시 점검해주세요.")
    