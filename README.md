# Dog LLM API

FastAPI 기반의 OpenAI API 래퍼 서비스입니다.

## 설치 방법

1. Conda 환경 활성화:
```bash
conda activate dog_llm
```

2. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

3. `.env` 파일에 OpenAI API 키 설정:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## 실행 방법

```bash
python main.py
```

서버는 기본적으로 http://localhost:8000 에서 실행됩니다.

## API 엔드포인트

### POST /openai/chat

채팅 메시지를 받아 OpenAI API를 통해 응답을 반환합니다.

요청 예시:
```json
{
    "message": "안녕하세요!"
}
```

응답 예시:
```json
{
    "response": "안녕하세요! 무엇을 도와드릴까요?"
}
```

## API 문서

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc 