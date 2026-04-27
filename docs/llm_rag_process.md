# LLM(RAG) 기반 반려견 영양 전문가 챗봇 시스템

## 1. 시스템 개요

이 시스템은 Ollama의 LLM을 활용하여 반려견의 영양과 건강에 대한 전문적인 상담을 제공하는 챗봇입니다. RAG(Retrieval-Augmented Generation) 기법을 사용하여 관련 문서를 검색하고, 이를 기반으로 정확하고 전문적인 답변을 생성합니다.

## 2. 주요 구성 요소

### 2.1 LLM 모델 설정
```python
self.llm = Ollama(
    model="llama3",
    temperature=0.7,  # 창의성과 일관성의 균형
    top_p=0.9,        # 토큰 선택의 다양성
    repeat_penalty=1.1,  # 반복 패널티
    num_ctx=4096,     # 컨텍스트 윈도우 크기
    num_thread=4      # 병렬 처리 스레드 수
)
```

### 2.2 프롬프트 템플릿
```python
self.prompt_template = PromptTemplate(
    input_variables=["context", "question", "chat_history", "dog_profile"],
    template="""
    당신은 반려견을 대상으로하는 반려견 영양 전문가입니다.

    반려견 정보:
    {dog_profile}

    관련 문서:
    {context}
    
    이전 대화:
    {chat_history}

    반드시 한글로 답변해주세요.
    친근하고 자연스럽게 대화하세요.
    위 정보를 바탕으로 반려견의 성격과 특성을 고려하여 대화하세요.
    
    질문: {question}
    
    답변:
    """
)
```

## 3. 프로세스 흐름

### 3.1 문서 검색 (Retrieval)
```python
async def _get_relevant_docs(self, query: str, k: int = 3) -> List[str]:
    # 질문의 임베딩 생성
    query_embedding = self.embeddings.encode(query, normalize_embeddings=True)
    
    # 데이터베이스에서 유사한 문서 검색
    similar_docs = await self.docs_repo.search_similar_docs(query_embedding, k)
    return [doc.content for doc in similar_docs]
```

### 3.2 채팅 기록 관리
```python
def _format_chat_history(self, chat_history: List[DogChat]) -> str:
    if not chat_history:
        return "이전 대화가 없습니다."
        
    # 시간 순으로 정렬
    sorted_history = sorted(chat_history, key=lambda x: x.created_at)
    
    formatted_history = []
    for chat in sorted_history:
        formatted_history.append(f"사용자: {chat.message}")
        formatted_history.append(f"AI: {chat.response}")
        
    return "\n".join(formatted_history)
```

### 3.3 채팅 처리
```python
async def chat(self, dog_id: int, message: str) -> str:
    # 반려견 프로필 정보 가져오기
    dog_profile = await self.profile_repo.get_profile(dog_id)
    
    # 관련 문서 검색
    relevant_docs = await self._get_relevant_docs(message)
    context = "\n".join(relevant_docs) if relevant_docs else "관련 문서가 없습니다."
    
    # 최근 채팅 기록 가져오기
    chat_history = await self.chats_repo.get_recent_chats(dog_id, llm_provider=self.llm_provider)
    formatted_history = self._format_chat_history(chat_history)
```

## 4. 데이터베이스 연동

시스템은 다음과 같은 데이터베이스 저장소를 사용합니다:
- `DogDocsRepository`: 문서 저장 및 검색
- `DogChatsRepository`: 채팅 기록 관리
- `DogProfileRepository`: 반려견 프로필 정보 관리

## 5. 특징 및 장점

1. **맥락 이해**: 이전 대화 기록을 활용하여 일관된 대화 흐름 유지
2. **개인화**: 반려견의 프로필 정보를 고려한 맞춤형 답변
3. **정확성**: 관련 문서를 검색하여 전문적인 정보 제공
4. **확장성**: 새로운 문서 추가를 통한 지식 기반 확장 가능

## 6. 사용된 주요 라이브러리

### 6.1 LangChain
LangChain은 LLM 애플리케이션 개발을 위한 프레임워크로, 다음과 같은 주요 기능을 제공합니다:

- **LLM 체인 관리**: 여러 LLM 작업을 체인으로 연결하여 복잡한 작업 수행
- **프롬프트 템플릿**: 동적 프롬프트 생성 및 관리
- **메모리 관리**: 대화 기록과 같은 상태 정보 관리
- **문서 로더**: 다양한 형식의 문서 로딩 지원
- **벡터 저장소 통합**: 문서 임베딩 저장 및 검색

```python
# LangChain을 사용한 LLM 체인 예시
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

chain = LLMChain(
    llm=llm,
    prompt=prompt_template,
    verbose=True  # 디버깅을 위한 상세 로그 출력
)
```

### 6.2 LangChain Community
LangChain Community는 다양한 LLM 제공자와의 통합을 위한 확장 패키지입니다:

- **Ollama 통합**: 로컬에서 실행되는 Ollama LLM과의 통합
- **다양한 LLM 제공자 지원**: OpenAI, Anthropic, HuggingFace 등
- **임베딩 모델 통합**: 다양한 임베딩 모델 지원

```python
# Ollama LLM 통합 예시
from langchain_community.llms import Ollama

llm = Ollama(
    model="llama3",
    temperature=0.7,
    num_ctx=4096
)
```

### 6.3 Sentence Transformers
Sentence Transformers는 텍스트 임베딩 생성을 위한 라이브러리입니다:

- **사전 학습된 모델**: 다양한 언어와 도메인에 대한 사전 학습된 모델 제공
- **고품질 임베딩**: 의미론적 유사성을 잘 포착하는 임베딩 생성
- **벡터 검색**: 유사한 문서 검색을 위한 효율적인 벡터 연산

```python
# Sentence Transformers를 사용한 임베딩 생성 예시
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
embeddings = model.encode(
    texts,                    # 텍스트 리스트
    normalize_embeddings=True,  # 정규화 여부
    show_progress_bar=True    # 진행 상태 표시
)
```

### 6.4 기타 주요 라이브러리
- `torch`: 딥러닝 모델 지원
- `transformers`: NLP 모델 지원 