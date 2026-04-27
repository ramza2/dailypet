-- 반려견 프로필 테이블
CREATE TABLE dog_profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    breed TEXT NOT NULL,
    gender TEXT NOT NULL,
    is_neutered BOOLEAN NOT NULL DEFAULT 0,
    birth_date DATE,
    adoption_date DATE,
    weight REAL,
    size_type TEXT,
    bcs_score INTEGER,
    bcs_type TEXT,
    health_status TEXT NOT NULL DEFAULT '건강함',
    health_issues TEXT,
    last_checkup_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 반려견 대화 테이블
CREATE TABLE dog_chat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT,
    response TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    dog_id INTEGER,
    message_embedding TEXT,  -- JSON 배열로 저장
    llm_provider TEXT NOT NULL DEFAULT 'ollama',
    prompt_template_text TEXT,
    FOREIGN KEY (dog_id) REFERENCES dog_profile(id)
);

-- 프롬프트 템플릿 테이블
CREATE TABLE prompt_template (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- 반려견 문서 테이블
CREATE TABLE dog_doc (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    embedding TEXT NOT NULL,  -- JSON 배열로 저장
    source TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    loader_type TEXT
);

-- 반려견 체온 테이블
CREATE TABLE dog_temperature (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dog_id INTEGER NOT NULL,
    temperature REAL NOT NULL,
    measured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dog_id) REFERENCES dog_profile(id)
);

-- 반려견 심박수 테이블
CREATE TABLE dog_heart_rate (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dog_id INTEGER NOT NULL,
    heart_rate INTEGER NOT NULL,
    measured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dog_id) REFERENCES dog_profile(id)
);

-- 반려견 호흡수 테이블
CREATE TABLE dog_respiratory_rate (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dog_id INTEGER NOT NULL,
    respiratory_rate INTEGER NOT NULL,
    measured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dog_id) REFERENCES dog_profile(id)
);

-- 반려견 산책 테이블
CREATE TABLE dog_walk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dog_id INTEGER NOT NULL,
    duration INTEGER NOT NULL,  -- 분 단위
    distance REAL,  -- km 단위
    started_at TIMESTAMP NOT NULL,
    ended_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dog_id) REFERENCES dog_profile(id)
);

-- 반려견 간식 테이블
CREATE TABLE dog_snack (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dog_id INTEGER NOT NULL,
    snack_name TEXT NOT NULL,
    amount REAL NOT NULL,  -- g 단위
    given_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dog_id) REFERENCES dog_profile(id)
);

-- 반려견 식사 테이블
CREATE TABLE dog_meal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dog_id INTEGER NOT NULL,
    meal_name TEXT NOT NULL,
    amount REAL NOT NULL,  -- g 단위
    given_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dog_id) REFERENCES dog_profile(id)
); 