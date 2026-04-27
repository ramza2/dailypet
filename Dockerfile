# Python 3.8 기반 이미지 사용
FROM python:3.8-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    postgresql-client \
    tesseract-ocr \
    tesseract-ocr-kor \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# pip 업그레이드
RUN pip install --upgrade pip

# Python 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# BGE-m3 모델 다운로드
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-m3')"

# 애플리케이션 코드 복사
COPY . .

# 환경 변수 설정
ENV PYTHONUNBUFFERED=1
ENV TRANSFORMERS_OFFLINE=0
ENV TOKENIZERS_PARALLELISM=false
ENV HF_HUB_ENABLE_HF_TRANSFER=1
ENV HF_HUB_DISABLE_TELEMETRY=1
ENV HF_HUB_OFFLINE=1

# 포트 노출
EXPOSE 8000

# 애플리케이션 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"] 