-- ============================================================================
--  [설계 기준]
--  - 금액(fee)      : NUMBER(10)    정수(원). FLOAT 은 소수 오차가 누적될 수 있어 사용하지 않음
--  - 거리(distance) : NUMBER(6, 1)  원본이 소수 첫째 자리까지 기록 -> 자릿수 고정
--  - 날짜·시각      : DATE          오라클 DATE 는 초 단위 시각까지 저장 (문자열 저장 X)
--  - ID             : VARCHAR2      계산하지 않는 값, 'R000001' 처럼 문자 포함
--  - rental_id      : UNIQUE 제약   재실행 시 중복 적재 방지 (MERGE INTO 의 기준)
--  - id             : 자동 증가 대리키 (10_database/02_schema.py 방식)
--  - station_id, station_name, district : B043(배치 대여소 없음) 대여 기록 때문에 NULL 허용
-- ============================================================================
CREATE TABLE rental_log (
    id              NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    rental_id       VARCHAR2(20)    NOT NULL,
    bike_id         VARCHAR2(20)    NOT NULL,
    user_id         VARCHAR2(20)    NOT NULL,
    rent_time       DATE            NOT NULL,
    return_time     DATE            NOT NULL,
    duration_min    NUMBER(5)       NOT NULL,
    distance_km     NUMBER(6, 1)    NOT NULL,
    fee             NUMBER(10)      NOT NULL,
    payment_method  VARCHAR2(20)    NOT NULL,
    bike_type       VARCHAR2(20)    NOT NULL,
    station_id      VARCHAR2(20),
    station_name    VARCHAR2(100),
    district        VARCHAR2(50),
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_rental_id UNIQUE (rental_id)
);