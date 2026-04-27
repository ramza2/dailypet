import psycopg2
import logging
from dotenv import load_dotenv
import os

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 환경 변수 로드
load_dotenv()

# 데이터베이스 연결 설정
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "dog_llm")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "active1004")

def create_tables():
    """필요한 모든 테이블을 생성합니다."""
    try:
        # 데이터베이스 연결
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
        with conn.cursor() as cur:
            # dog_chats 테이블 생성
            cur.execute("""
                CREATE TABLE IF NOT EXISTS dog_chats (
                    id SERIAL PRIMARY KEY,
                    dog_id INTEGER NOT NULL REFERENCES dog_profiles(id),
                    message TEXT NOT NULL,
                    response TEXT NOT NULL,
                    message_embedding vector(1024),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            logger.info("dog_chats 테이블 생성 완료")
            
            # 변경사항 커밋
            conn.commit()
            
    except Exception as e:
        logger.error(f"테이블 생성 중 오류 발생: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()
            logger.info("데이터베이스 연결 종료")

if __name__ == "__main__":
    create_tables() 