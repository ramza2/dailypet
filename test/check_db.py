import psycopg2
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 데이터베이스 연결 정보
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'dog_llm')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'active1004')

def check_database():
    try:
        # 데이터베이스 연결
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
        with conn.cursor() as cur:
            # 설치된 확장 확인
            print("=== 설치된 확장 ===")
            cur.execute("SELECT * FROM pg_extension;")
            extensions = cur.fetchall()
            for ext in extensions:
                print(f"확장: {ext[1]}")
            
            # dog_profiles 테이블 스키마 확인
            print("\n=== dog_profiles 테이블 스키마 ===")
            cur.execute("""
                SELECT column_name, data_type, character_maximum_length
                FROM information_schema.columns
                WHERE table_name = 'dog_profiles';
            """)
            columns = cur.fetchall()
            for col in columns:
                print(f"컬럼: {col[0]}, 타입: {col[1]}, 길이: {col[2]}")
            
            # 데이터 개수 확인
            print("\n=== 데이터 개수 ===")
            cur.execute("SELECT COUNT(*) FROM dog_profiles;")
            count = cur.fetchone()[0]
            print(f"총 프로필 수: {count}")
            
            # 샘플 데이터 확인
            print("\n=== 샘플 데이터 ===")
            cur.execute("""
                SELECT id, name, breed, gender, 
                       CASE WHEN profile_embedding IS NULL THEN 'NULL' ELSE 'NOT NULL' END as has_embedding
                FROM dog_profiles
                LIMIT 5;
            """)
            samples = cur.fetchall()
            for sample in samples:
                print(f"\nID: {sample[0]}")
                print(f"이름: {sample[1]}")
                print(f"품종: {sample[2]}")
                print(f"성별: {sample[3]}")
                print(f"임베딩: {sample[4]}")
            
    except Exception as e:
        print(f"에러 발생: {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    check_database() 