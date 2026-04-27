import random
from datetime import date, timedelta
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

# 환경 변수 로드
load_dotenv()

# 데이터베이스 연결 정보
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'dog_llm')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'active1004')

# 샘플 데이터 생성 함수
def generate_sample_data():
    # 품종 목록
    breeds = [
        "골든 리트리버", "래브라도 리트리버", "시베리안 허스키", "푸들", "시츄",
        "비숑 프리제", "말티즈", "요크셔 테리어", "포메라니안", "웰시 코기",
        "보더 콜리", "진도개", "불독", "치와와", "비글"
    ]
    
    # 체형 크기
    size_types = ["소형", "중형", "대형"]
    
    # BCS 유형
    bcs_types = ["마름", "적정", "비만", "고도비만"]
    
    # 건강 상태
    health_statuses = ["건강함", "주의필요", "질병있음"]
    
    # 질병 목록
    health_issues = [
        "피부염", "관절염", "심장병", "신장병", "간질",
        "당뇨병", "알레르기", "치주질환", "비만", "암"
    ]
    
    # 성별
    genders = ["수컷", "암컷"]
    
    # 샘플 데이터 생성
    samples = []
    for i in range(100):
        # 랜덤 생년월일 (1-10세 사이)
        age = random.randint(1, 10)
        birth_date = date.today() - timedelta(days=365*age)
        
        # 랜덤 입양일 (생일 이후)
        adoption_age = random.randint(2, age*12)  # 2개월에서 현재 나이까지
        adoption_date = birth_date + timedelta(days=30*adoption_age)
        
        # 랜덤 체중 (2-40kg 사이)
        weight = round(random.uniform(2, 40), 1)
        
        # 체형 크기 결정 (체중 기반)
        if weight < 10:
            size_type = "소형"
        elif weight < 25:
            size_type = "중형"
        else:
            size_type = "대형"
        
        # 랜덤 BCS (1-9)
        bcs_score = random.randint(1, 9)
        
        # BCS 유형 결정 (점수 기반)
        if bcs_score <= 3:
            bcs_type = "마름"
        elif bcs_score <= 6:
            bcs_type = "적정"
        elif bcs_score <= 8:
            bcs_type = "비만"
        else:
            bcs_type = "고도비만"
        
        # 건강 상태와 이슈
        health_status = random.choices(
            health_statuses, 
            weights=[0.7, 0.2, 0.1]  # 70% 건강함, 20% 주의필요, 10% 질병있음
        )[0]
        
        # 건강 이슈 (상태에 따라 다르게)
        if health_status == "건강함":
            health_issues_text = None
        elif health_status == "주의필요":
            num_issues = random.randint(1, 2)
            health_issues_text = ", ".join(random.sample(health_issues, num_issues))
        else:
            num_issues = random.randint(2, 3)
            health_issues_text = ", ".join(random.sample(health_issues, num_issues))
        
        # 최근 진단일 (현재 날짜로부터 0-6개월 전)
        last_checkup_date = date.today() - timedelta(days=random.randint(0, 180))
        
        sample = {
            "name": f"강아지{i+1}",
            "breed": random.choice(breeds),
            "gender": random.choice(genders),
            "is_neutered": random.choice([True, False]),
            "birth_date": birth_date,
            "adoption_date": adoption_date,
            "weight": weight,
            "size_type": size_type,
            "bcs_score": bcs_score,
            "bcs_type": bcs_type,
            "health_status": health_status,
            "health_issues": health_issues_text,
            "last_checkup_date": last_checkup_date
        }
        samples.append(sample)
    
    return samples

def insert_profile(cursor, profile):
    sql = """
    INSERT INTO dog_profiles (
        name, breed, gender, is_neutered, birth_date, adoption_date,
        weight, size_type, bcs_score, bcs_type, health_status,
        health_issues, last_checkup_date
    ) VALUES (
        %(name)s, %(breed)s, %(gender)s, %(is_neutered)s, %(birth_date)s,
        %(adoption_date)s, %(weight)s, %(size_type)s, %(bcs_score)s,
        %(bcs_type)s, %(health_status)s, %(health_issues)s, %(last_checkup_date)s
    ) RETURNING id;
    """
    cursor.execute(sql, profile)
    return cursor.fetchone()[0]

def main():
    try:
        # 데이터베이스 연결
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        
        # 샘플 데이터 생성
        print("샘플 데이터 생성 중...")
        samples = generate_sample_data()
        
        # 데이터베이스에 저장
        print("데이터베이스에 저장 중...")
        for i, sample in enumerate(samples, 1):
            profile_id = insert_profile(cursor, sample)
            print(f"프로필 {i}/100 생성 완료 (ID: {profile_id})")
            conn.commit()  # 각 프로필마다 커밋
        
        print("\n모든 샘플 데이터 생성 완료!")
        
    except Exception as e:
        print(f"\n에러 발생: {str(e)}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    main() 