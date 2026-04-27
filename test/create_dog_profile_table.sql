-- 반려견 프로필 테이블 생성
CREATE TABLE dog_profiles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,                    -- 반려견 이름
    breed VARCHAR(100) NOT NULL,                   -- 품종
    gender VARCHAR(10) NOT NULL,                   -- 성별 (수컷/암컷)
    is_neutered BOOLEAN DEFAULT false,            -- 중성화 여부
    birth_date DATE,                              -- 생년월일
    adoption_date DATE,                           -- 입양일
    weight DECIMAL(5,2),                          -- 체중 (kg)
    size_type VARCHAR(10),                        -- 체형 (소형/중형/대형)
    bcs_score INTEGER CHECK (bcs_score BETWEEN 1 AND 9), -- 체형 점수 (1-9)
    bcs_type VARCHAR(20),                         -- BCS 유형 (마름/적정/비만/고도비만)
    health_status VARCHAR(20) DEFAULT '건강함',    -- 현재 상태
    health_issues TEXT,                           -- 질병 정보
    last_checkup_date DATE,                       -- 최근 진단일
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 제약조건 추가
ALTER TABLE dog_profiles
    ADD CONSTRAINT chk_gender CHECK (gender IN ('수컷', '암컷')),
    ADD CONSTRAINT chk_size_type CHECK (size_type IN ('소형', '중형', '대형')),
    ADD CONSTRAINT chk_bcs_type CHECK (bcs_type IN ('마름', '적정', '비만', '고도비만')),
    ADD CONSTRAINT chk_health_status CHECK (health_status IN ('건강함', '주의필요', '질병있음'));

-- updated_at 자동 업데이트를 위한 트리거 함수
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 트리거 생성
CREATE TRIGGER update_dog_profiles_updated_at
    BEFORE UPDATE ON dog_profiles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 인덱스 생성
CREATE INDEX idx_dog_profiles_name ON dog_profiles(name);
CREATE INDEX idx_dog_profiles_breed ON dog_profiles(breed); 