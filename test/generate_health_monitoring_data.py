import psycopg2
from psycopg2.extras import RealDictCursor
import random
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 데이터베이스 연결 설정
db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "dog_llm"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "active1004")
}

# 식사 타입 목록
MEAL_TYPES = ['건식', '습식', '화식', '생식']
# 간식 타입 목록
SNACK_TYPES = ['쿠키', '덴탈껌', '육포', '고구마', '치즈', '황태포', '트릿', '과일']
# 산책 활동 수준 목록
ACTIVITY_LEVELS = ['과다 흥분', '공격성', '불안 행동', '목줄 잡아당김', '산책 거부', None, None, None, None, None]  # None이 더 많게 설정
# 체온 측정 방법 목록
TEMPERATURE_METHODS = ['직접입력', '간편입력']

def get_random_datetime(date):
    """주어진 날짜의 랜덤한 시간을 반환"""
    random_seconds = random.randint(0, 24*60*60)
    return date + timedelta(seconds=random_seconds)

def create_meal_data(cursor, dog_id, start_date):
    """식사 데이터 생성"""
    current_date = datetime.now()
    date = start_date
    
    while date <= current_date:
        records_count = random.randint(0, 3)  # 하루 0~3개의 기록
        for _ in range(records_count):
            meal_time = get_random_datetime(date)
            meal_type = random.choice(MEAL_TYPES)
            amount = random.randint(100, 500)  # 100g ~ 500g
            
            cursor.execute("""
                INSERT INTO dog_meals (dog_id, meal_type, amount, meal_time)
                VALUES (%s, %s, %s, %s)
            """, (dog_id, meal_type, amount, meal_time))
        date += timedelta(days=1)

def create_snack_data(cursor, dog_id, start_date):
    """간식 데이터 생성"""
    current_date = datetime.now()
    date = start_date
    
    while date <= current_date:
        records_count = random.randint(0, 3)
        for _ in range(records_count):
            snack_time = get_random_datetime(date)
            snack_type = random.choice(SNACK_TYPES)
            amount = random.randint(1, 5)  # 1~5개
            
            cursor.execute("""
                INSERT INTO dog_snacks (dog_id, snack_type, amount, snack_time)
                VALUES (%s, %s, %s, %s)
            """, (dog_id, snack_type, amount, snack_time))
        date += timedelta(days=1)

def create_walk_data(cursor, dog_id, start_date):
    """산책 데이터 생성"""
    current_date = datetime.now()
    date = start_date
    
    while date <= current_date:
        records_count = random.randint(0, 3)
        for _ in range(records_count):
            walk_time = get_random_datetime(date)
            duration = random.randint(15, 60)  # 15분 ~ 60분
            distance = round(random.uniform(0.5, 5.0), 2)  # 0.5km ~ 5.0km
            activity_level = random.choice(ACTIVITY_LEVELS)
            
            cursor.execute("""
                INSERT INTO dog_walks (dog_id, duration, distance, walk_time, activity_level)
                VALUES (%s, %s, %s, %s, %s)
            """, (dog_id, duration, distance, walk_time, activity_level))
        date += timedelta(days=1)

def create_respiratory_rate_data(cursor, dog_id, start_date):
    """호흡수 데이터 생성"""
    current_date = datetime.now()
    date = start_date
    
    while date <= current_date:
        records_count = random.randint(0, 3)
        for _ in range(records_count):
            measured_at = get_random_datetime(date)
            rate = random.randint(10, 30)  # 10~30회/분
            measurement_duration = random.choice([30, 60])  # 30초 또는 60초
            
            cursor.execute("""
                INSERT INTO dog_respiratory_rates (dog_id, rate, measured_at, measurement_duration)
                VALUES (%s, %s, %s, %s)
            """, (dog_id, rate, measured_at, measurement_duration))
        date += timedelta(days=1)

def create_heart_rate_data(cursor, dog_id, start_date):
    """심박수 데이터 생성"""
    current_date = datetime.now()
    date = start_date
    
    while date <= current_date:
        records_count = random.randint(0, 3)
        for _ in range(records_count):
            measured_at = get_random_datetime(date)
            rate = random.randint(60, 120)  # 60~120bpm
            measurement_duration = random.choice([30, 60])  # 30초 또는 60초
            
            cursor.execute("""
                INSERT INTO dog_heart_rates (dog_id, rate, measured_at, measurement_duration)
                VALUES (%s, %s, %s, %s)
            """, (dog_id, rate, measured_at, measurement_duration))
        date += timedelta(days=1)

def create_temperature_data(cursor, dog_id, start_date):
    """체온 데이터 생성"""
    current_date = datetime.now()
    date = start_date
    
    while date <= current_date:
        records_count = random.randint(0, 3)
        for _ in range(records_count):
            measured_at = get_random_datetime(date)
            temperature = round(random.uniform(37.5, 39.5), 1)  # 37.5°C ~ 39.5°C
            measurement_method = random.choice(TEMPERATURE_METHODS)
            
            cursor.execute("""
                INSERT INTO dog_temperatures (dog_id, temperature, measurement_method, measured_at)
                VALUES (%s, %s, %s, %s)
            """, (dog_id, temperature, measurement_method, measured_at))
        date += timedelta(days=1)

def main():
    # 데이터베이스 연결
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # 한 달 전 날짜 계산
        start_date = datetime.now() - timedelta(days=30)
        
        # 모든 강아지 ID 가져오기
        cursor.execute("SELECT id FROM dog_profiles")
        dog_ids = [row['id'] for row in cursor.fetchall()]
        
        # 각 강아지에 대해 데이터 생성
        for dog_id in dog_ids:
            print(f"강아지 ID {dog_id}의 데이터 생성 중...")
            
            create_meal_data(cursor, dog_id, start_date)
            create_snack_data(cursor, dog_id, start_date)
            create_walk_data(cursor, dog_id, start_date)
            create_respiratory_rate_data(cursor, dog_id, start_date)
            create_heart_rate_data(cursor, dog_id, start_date)
            create_temperature_data(cursor, dog_id, start_date)
            
            conn.commit()
            print(f"강아지 ID {dog_id}의 데이터 생성 완료")
        
        print("모든 데이터 생성이 완료되었습니다.")
        
    except Exception as e:
        conn.rollback()
        print(f"오류 발생: {str(e)}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main() 