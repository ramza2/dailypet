import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# 데이터베이스 연결 정보
DB_HOST = "211.110.19.139"
DB_PORT = "5432"
DB_NAME = "dog_llm"
DB_USER = "postgres"
DB_PASSWORD = "active1004"

def create_table():
    try:
        # 데이터베이스 연결
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
        # 커서 생성
        cur = conn.cursor()
        
        # 기존 테이블 삭제
        cur.execute("DROP TABLE IF EXISTS dog_profiles CASCADE;")
        print("기존 테이블이 삭제되었습니다.")
        
        # SQL 파일 읽기 (UTF-8 인코딩 지정)
        with open('create_dog_profile_table.sql', 'r', encoding='utf-8') as file:
            sql_commands = file.read()
        
        # SQL 명령 실행
        cur.execute(sql_commands)
        
        # 변경사항 커밋
        conn.commit()
        
        print("테이블이 성공적으로 생성되었습니다.")
        
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        
    finally:
        # 연결 종료
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    create_table() 