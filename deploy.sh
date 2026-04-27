#!/bin/bash

set -euo pipefail

# 프로젝트 디렉토리로 이동
cd /home/ramza/dailypet

# 필요한 시스템 패키지 설치 (Ubuntu/Debian)
sudo apt-get update -y && sudo apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-kor \
    poppler-utils \
    python3-dev \
    python3-venv \
    python3-pip \
    build-essential \
    zlib1g-dev \
    libbz2-dev \
    libssl-dev \
    libncurses5-dev \
    libsqlite3-dev \
    libreadline-dev \
    tk-dev \
    libffi-dev \
    liblzma-dev \
    curl

# 가상환경이 없으면 생성
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# 가상환경 활성화
source venv/bin/activate

# pip 업그레이드
pip install --upgrade pip

# Poppler는 Ubuntu에서 기본 경로(/usr/bin) 사용

# Python 패키지 설치
pip install -r requirements.txt

# BGE-m3 모델 다운로드
python3 -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-m3')"

# Ollama 설치 여부 확인 및 설치
if ! command -v ollama &> /dev/null; then
    echo "Ollama 설치 중..."
    curl -fsSL https://ollama.com/install.sh | sh
    
    # Ollama 서비스 시작
    echo "Ollama 서비스 시작 중..."
    sudo systemctl start ollama
    sudo systemctl enable ollama
else
    echo "Ollama가 이미 설치되어 있습니다."
fi

# Ollama 모델 다운로드 여부 확인
if ! ollama list | grep -q "gemma3"; then
    echo "Ollama 모델 다운로드 중..."
    ollama pull gemma3
else
    echo "gemma3 모델이 이미 설치되어 있습니다."
fi

# PM2 설치 여부 확인 및 설치
if ! command -v pm2 &> /dev/null; then
    echo "PM2가 설치되어 있지 않아 설치를 진행합니다..."
    sudo apt-get install -y nodejs npm
    sudo npm install -g pm2
else
    echo "PM2가 이미 설치되어 있습니다."
fi

# 로그 디렉토리 생성
mkdir -p logs

# PM2로 애플리케이션 시작/재시작
pm2 restart ecosystem.config.js || pm2 start ecosystem.config.js

# PM2 자동 시작 설정
pm2 startup
pm2 save

# 상태 확인
pm2 status 