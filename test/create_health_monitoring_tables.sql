-- 식사 기록 테이블
CREATE TABLE IF NOT EXISTS dog_meals (
    id SERIAL PRIMARY KEY,
    dog_id INTEGER NOT NULL REFERENCES dog_profiles(id),
    meal_type VARCHAR(10) NOT NULL CHECK (meal_type IN ('건식', '습식', '화식', '생식')),
    amount INTEGER NOT NULL, -- 단위: g
    meal_time TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 간식 기록 테이블
CREATE TABLE IF NOT EXISTS dog_snacks (
    id SERIAL PRIMARY KEY,
    dog_id INTEGER NOT NULL REFERENCES dog_profiles(id),
    snack_type VARCHAR(20) NOT NULL CHECK (snack_type IN ('쿠키', '덴탈껌', '육포', '고구마', '치즈', '황태포', '트릿', '과일')),
    amount INTEGER NOT NULL, -- 단위: 개수
    snack_time TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 산책 기록 테이블
CREATE TABLE IF NOT EXISTS dog_walks (
    id SERIAL PRIMARY KEY,
    dog_id INTEGER NOT NULL REFERENCES dog_profiles(id),
    duration INTEGER NOT NULL, -- 단위: 분
    distance NUMERIC(4,2), -- 단위: km
    walk_time TIMESTAMP NOT NULL,
    activity_level VARCHAR(20) CHECK (activity_level IN ('과다 흥분', '공격성', '불안 행동', '목줄 잡아당김', '산책 거부')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 호흡수 측정 테이블
CREATE TABLE IF NOT EXISTS dog_respiratory_rates (
    id SERIAL PRIMARY KEY,
    dog_id INTEGER NOT NULL REFERENCES dog_profiles(id),
    rate INTEGER NOT NULL, -- 단위: 회/분
    measured_at TIMESTAMP NOT NULL,
    measurement_duration INTEGER NOT NULL, -- 단위: 초
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 심박수 측정 테이블
CREATE TABLE IF NOT EXISTS dog_heart_rates (
    id SERIAL PRIMARY KEY,
    dog_id INTEGER NOT NULL REFERENCES dog_profiles(id),
    rate INTEGER NOT NULL, -- 단위: bpm
    measured_at TIMESTAMP NOT NULL,
    measurement_duration INTEGER NOT NULL, -- 단위: 초
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 체온 측정 테이블
CREATE TABLE IF NOT EXISTS dog_temperatures (
    id SERIAL PRIMARY KEY,
    dog_id INTEGER NOT NULL REFERENCES dog_profiles(id),
    temperature NUMERIC(3,1) NOT NULL, -- 단위: °C
    measurement_method VARCHAR(10) NOT NULL CHECK (measurement_method IN ('직접입력', '간편입력')),
    measured_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 각 테이블에 인덱스 추가
CREATE INDEX IF NOT EXISTS idx_dog_meals_dog_id_meal_time ON dog_meals(dog_id, meal_time);
CREATE INDEX IF NOT EXISTS idx_dog_snacks_dog_id_snack_time ON dog_snacks(dog_id, snack_time);
CREATE INDEX IF NOT EXISTS idx_dog_walks_dog_id_walk_time ON dog_walks(dog_id, walk_time);
CREATE INDEX IF NOT EXISTS idx_dog_respiratory_rates_dog_id_measured_at ON dog_respiratory_rates(dog_id, measured_at);
CREATE INDEX IF NOT EXISTS idx_dog_heart_rates_dog_id_measured_at ON dog_heart_rates(dog_id, measured_at);
CREATE INDEX IF NOT EXISTS idx_dog_temperatures_dog_id_measured_at ON dog_temperatures(dog_id, measured_at); 