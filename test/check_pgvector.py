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

def check_pgvector():
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
        
        with conn.cursor() as cur:
            # pgvector 확장 확인
            print("\npgvector 확장 상태 확인 중...")
            cur.execute("SELECT * FROM pg_extension WHERE extname = 'vector';")
            result = cur.fetchone()
            if result:
                print("pgvector 확장이 설치되어 있습니다.")
            else:
                print("pgvector 확장이 설치되어 있지 않습니다.")
                
            # 벡터 연산자 확인
            print("\n벡터 연산자 확인 중...")
            cur.execute("""
                SELECT oprname, oprleft::regtype, oprright::regtype, oprresult::regtype
                FROM pg_operator
                WHERE oprname = '<=>'
                AND oprleft::regtype = 'vector'::regtype;
            """)
            operators = cur.fetchall()
            if operators:
                print("벡터 연산자 (<=>)가 정의되어 있습니다:")
                for op in operators:
                    print(f"- 연산자: {op[0]}, 왼쪽 타입: {op[1]}, 오른쪽 타입: {op[2]}, 결과 타입: {op[3]}")
            else:
                print("벡터 연산자 (<=>)가 정의되어 있지 않습니다.")
            
        conn.close()
        
    except Exception as e:
        print(f"\n에러 발생: {str(e)}")

if __name__ == "__main__":
    check_pgvector() 