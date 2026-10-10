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