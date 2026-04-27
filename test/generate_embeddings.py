from sentence_transformers import SentenceTransformer
from dog_profile_repository import DogProfileRepository
import json
from datetime import datetime

# 데이터베이스 연결 정보
DB_HOST = "211.110.19.139"
DB_PORT = "5432"
DB_NAME = "dog_llm"
DB_USER = "postgres"
DB_PASSWORD = "active1004"

def create_profile_text(profile):
    """반려견 프로필 정보를 텍스트로 변환합니다."""
    text_parts = [
        f"이름: {profile['name']}",
        f"품종: {profile['breed']}",
        f"성별: {profile['gender']}",
        f"생년월일: {profile['birth_date'].strftime('%Y-%m-%d')}",
        f"체중: {profile['weight']}kg",
        f"체형 점수: {profile['bcs']}"
    ]
    
    # 예방접종 이력
    if profile['vaccination_history']:
        text_parts.append("예방접종 이력:")
        for vaccine, dates in profile['vaccination_history'].items():
            text_parts.append(f"- {vaccine}: {', '.join(dates)}")
    
    # 알레르기
    if profile['allergies']:
        text_parts.append(f"알레르기: {', '.join(profile['allergies'])}")
    
    # 복용 중인 약
    if profile['medications']:
        text_parts.append("복용 중인 약:")
        for med, schedule in profile['medications'].items():
            text_parts.append(f"- {med}: {schedule}")
    
    # 진단받은 질병
    if profile['diagnosed_diseases']:
        text_parts.append(f"진단받은 질병: {', '.join(profile['diagnosed_diseases'])}")
    
    return " ".join(text_parts)

def generate_embeddings():
    """모든 반려견 프로필에 대한 임베딩을 생성하고 저장합니다."""
    # BGE-m3-ko 모델 로드
    print("BGE-m3-ko 모델을 로드하는 중...")
    model = SentenceTransformer('BAAI/bge-m3-ko')
    
    # Repository 인스턴스 생성
    repo = DogProfileRepository(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    
    try:
        # 모든 프로필 가져오기
        print("프로필을 가져오는 중...")
        profiles = repo.search_profiles()  # 모든 프로필 검색
        
        print(f"총 {len(profiles)}개의 프로필에 대한 임베딩을 생성합니다...")
        
        for i, profile in enumerate(profiles, 1):
            # 프로필 텍스트 생성
            profile_text = create_profile_text(profile)
            
            # 임베딩 생성
            embedding = model.encode(profile_text, normalize_embeddings=True)
            
            # 임베딩 저장
            repo.update_profile(profile['id'], profile_embedding=embedding.tolist())
            
            print(f"프로필 {i}/{len(profiles)} 임베딩 생성 및 저장 완료 (ID: {profile['id']})")
        
        print("\n모든 임베딩 생성이 완료되었습니다.")
        
    except Exception as e:
        print(f"오류 발생: {str(e)}")

if __name__ == "__main__":
    generate_embeddings() 