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

def install_pgvector():
    try:
        # 데이터베이스 연결
        print(f"데이터베이스 연결 중... (Host: {DB_HOST}, Port: {DB_PORT}, DB: {DB_NAME})")
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
        # pgvector 확장 설치
        with conn.cursor() as cur:
            print("pgvector 확장 설치 중...")
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            conn.commit()
            print("pgvector 확장 설치 완료!")
            
        conn.close()
        
    except Exception as e:
        print(f"\n에러 발생: {str(e)}")

if __name__ == "__main__":
    install_pgvector() 