# 정적 프롬프트와 동적 프롬프트를 반영한 반려견 식단 추천 AI 구성 방안

## 1. 로컬 LLM 방식 구성 방안
- PostgreSQL pgvector(VectorDB)
- LangChain
- Ollama(LLaMA 3)

## 2. 기능 구현 위치
- `/llm/ollama` 패키지에 구현

## 3. 전체 플로우
1. 사용자 질의
2. LangChain PromptTemplate (정적 + 동적 프롬프트 구성)
3. 문서 기반 RAG 검색 (FAISS + 한국어 문서 벡터화)
4. 한글 튜닝 LLM (Ollama 기반 KoAlpaca 또는 Yi6B)
5. PromptLayer 로깅 및 분석
6. 최종 응답 → 사용자에게 식단 정보 전달

## 4. 현재 DB 테이블 정보

### dog_docs 테이블
```sql
CREATE TABLE IF NOT EXISTS public.dog_docs
(
    id integer NOT NULL DEFAULT nextval('dog_docs_id_seq'::regclass),
    content text COLLATE pg_catalog."default",
    embedding vector(1024),
    CONSTRAINT dog_docs_pkey PRIMARY KEY (id)
)
```

- 이미 생성된 테이블
- 반려견 관련 전문 지식을 담고 있는 임베팅 벡터 테이블
- `entity` 디렉토리 밑의 `dog_chat.py`와 `dog_profile.py`처럼 entity 파일 생성 필요
- `repository` 디렉토리 밑에 `dog_chats_repository.py`와 `dog_profile_repository.py`처럼 BaseRepository를 상속받은 기본적인 CRUD 기능 구현 필요

### dog_chats 테이블
- 채팅 이력 테이블
- `/entity/dog_chat.py`와 `/repository/dog_chats_repository.py` 정보 참고

### dog_profiles 테이블
- 반려견 건강 정보 테이블
- `/entity/dog_profile.py`와 `/repository/dog_profile_repository.py` 정보 참고

## 5. 상세 기능 정의

### 문서 업로드 및 처리
- 반려견에 대한 전문지식이 기재되어 있는 PDF나 TXT 등의 문서파일을 업로드
- 파일 내용을 읽어 적절하게 chunking
- `dog_docs` 테이블에 등록

### 로컬 LLM 채팅 구현
- 기존 `/llm/openai/chat.py`의 `chat_with_dog`과 같은 기능을 로컬 LLM 모델인 Ollama(LLaMA 3)를 사용해 `/llm/ollama/chat.py`에 구현
- 임베딩 모델이 필요하면 기존 `main.py`에 있는 `_model` ('BAAI/bge-m3') 재사용

### 채팅 기능 상세
- `/llm/ollama/chat.py`의 `chat_with_dog` 함수:
  - 파라미터로 받은 `dog_id`의 반려견에 대한 전문지식(`dog_docs` 테이블)과 이전 채팅 이력(`dog_chat` 테이블) 조회
  - LangChain을 사용해 `map_prompt`와 `combine_prompty` 연동
  - Ollama 모델(한글에 최적화)을 사용한 채팅 응답 생성
  - 채팅 이력 테이블(`dog_chats`)에 등록

### API 구현
- `main.py`에 `/ollama/chat` POST API 추가
- 구현된 `/llm/ollama/chat.py`를 사용하여 응답 