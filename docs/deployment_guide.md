# Dog LLM API Rocky Linux 9 배포 가이드

## 목차
1. [서버 준비](#1-서버-준비)
2. [프로젝트 파일 전송](#2-프로젝트-파일-전송)
3. [Docker 이미지 빌드](#3-docker-이미지-빌드)
4. [Docker 컨테이너 실행](#4-docker-컨테이너-실행)
5. [방화벽 설정](#5-방화벽-설정)
6. [Nginx 설정](#6-nginx-설정-선택사항)
7. [SSL 인증서 설정](#7-ssl-인증서-설정-선택사항)
8. [모니터링 및 로깅](#8-모니터링-및-로깅)
9. [자동 재시작 설정](#9-자동-재시작-설정)
10. [백업 및 복구](#10-백업-및-복구)
11. [업데이트 방법](#11-업데이트-방법)
12. [문제 해결](#12-문제-해결)
13. [배포 테스트](#13-배포-테스트)
14. [Docker 이미지 배포 및 배포 서버 설정](#14-docker-이미지-배포-및-배포-서버-설정)

## 1. 서버 준비

```bash
# Docker 설치
sudo dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
sudo dnf install docker-ce docker-ce-cli containerd.io

# Docker 서비스 시작 및 자동 시작 설정
sudo systemctl start docker
sudo systemctl enable docker
```

## 2. 프로젝트 파일 전송

로컬에서 서버로 다음 파일들을 전송합니다:
- main.py
- requirements.txt
- Dockerfile
- .env (환경 변수 파일)
- repository/ (디렉토리)

## 3. Docker 이미지 빌드

```bash
# 프로젝트 디렉토리로 이동
cd /path/to/project

# Docker 이미지 빌드 (메모리 제한)
# sudo docker buildx build --shm-size 2g --ulimit memlock=-1:-1 --ulimit stack=67108864 --ulimit nofile=1024:1024 t dog-llm-api .
sudo docker buildx build \
  --shm-size 2g \              # 공유 메모리 크기 제한 (2GB)
  --ulimit memlock=-1:-1 \     # 메모리 잠금 제한 해제
  --ulimit stack=67108864 \    # 스택 크기 제한 (64MB)
  --ulimit nofile=1024:1024 \  # 파일 디스크립터 제한
  -t dog-llm-api .
```

## 4. Docker 컨테이너 실행

```bash
# 컨테이너 실행 (CPU 및 메모리 제한 설정)
# sudo docker run -d --name dog-llm-api -p 8000:8000 --env-file .env --cpuset-cpus 0-3 --cpus 2.5 --memory 2g --shm-size 2g dog-llm-api
sudo docker run -d \
  --name dog-llm-api \
  -p 8000:8000 \
  --env-file .env \
  --cpuset-cpus 0-3 \    # 사용할 CPU 코어 지정 (0-3은 모든 코어 사용)
  --cpus 2.5 \           # 최대 CPU 사용량 제한 (2.5 코어)
  --memory 2g \          # 메모리 제한 (2GB)
  --shm-size 2g \        # 공유 메모리 크기 제한 (2GB)
  dog-llm-api
```

## 5. 방화벽 설정

```bash
# 방화벽 포트 열기
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload
```

## 6. Nginx 설정 (선택사항)

```bash
# Nginx 설치
sudo dnf install nginx

# Nginx 설정 파일 생성
sudo nano /etc/nginx/conf.d/dog-llm-api.conf
```

Nginx 설정 파일 내용:
```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 7. SSL 인증서 설정 (선택사항)

```bash
# Certbot 설치
sudo dnf install certbot python3-certbot-nginx

# SSL 인증서 발급
sudo certbot --nginx -d your_domain.com
```

## 8. 모니터링 및 로깅

```bash
# 컨테이너 로그 확인
sudo docker logs -f dog-llm-api

# 시스템 리소스 사용량 확인
top

# 컨테이너 리소스 사용량 확인
sudo docker stats dog-llm-api
```

## 9. 자동 재시작 설정

```bash
# Docker 컨테이너 자동 재시작 설정
sudo docker update --restart=always dog-llm-api
```

## 10. 백업 및 복구

```bash
# 데이터베이스 백업
pg_dump -U postgres dog_llm > backup.sql

# 복구
psql -U postgres dog_llm < backup.sql
```

## 11. 업데이트 방법

```bash
# 새 버전의 코드를 받은 후
git pull origin main

# Docker 이미지 재빌드 (메모리 제한)
sudo docker buildx build \
  --shm-size 2g \
  --ulimit memlock=-1:-1 \
  --ulimit stack=67108864 \
  --ulimit nofile=1024:1024 \
  -t dog-llm-api .

# 컨테이너 재시작 (CPU 및 메모리 제한 유지)
sudo docker stop dog-llm-api
sudo docker rm dog-llm-api
sudo docker run -d \
  --name dog-llm-api \
  -p 8000:8000 \
  --env-file .env \
  --cpuset-cpus 0-3 \
  --cpus 2.5 \
  --memory 2g \
  --shm-size 2g \
  dog-llm-api
```

## 12. 문제 해결

### 일반적인 문제
1. CPU 사용량 과다
   - `docker stats` 명령어로 CPU 사용량 모니터링
   - `--cpus` 옵션으로 CPU 사용량 제한 조정
   - 환경 변수를 통한 스레드 수 제한 확인
   - 동시 요청 수 제한 확인

2. 메모리 사용량 과다
   - `docker stats` 명령어로 메모리 사용량 모니터링
   - `--memory` 옵션으로 메모리 제한 조정
   - 시스템 전체 메모리 사용량 확인

3. 성능 최적화
   - CPU 코어 수 조정: `--cpuset-cpus` 옵션
   - CPU 사용량 제한: `--cpus` 옵션
   - 스레드 수 제한: 환경 변수 조정
   - 동시 요청 수 제한: `--limit-concurrency` 옵션
   - 메모리 제한: `--memory` 옵션

### 모니터링 명령어
```bash
# 컨테이너 리소스 사용량 확인
sudo docker stats dog-llm-api

# CPU 사용량 상세 확인
top -p $(pgrep -f "uvicorn main:app")

# 메모리 사용량 상세 확인
free -h
```

### 로그 확인
```bash
# 컨테이너 로그 확인
sudo docker logs dog-llm-api

# 시스템 로그 확인
journalctl -u docker
```

## 주의사항

1. 환경 변수 파일(.env)은 반드시 보안을 유지해야 합니다.
2. 정기적인 백업을 수행하세요.
3. SSL 인증서는 주기적으로 갱신해야 합니다.
4. 시스템 로그를 모니터링하여 문제를 조기에 발견하세요.
5. CPU와 메모리 사용량을 주기적으로 모니터링하고 필요시 리소스 제한을 조정하세요. 

## 13. 배포 테스트

### 1. 컨테이너 상태 확인
```bash
# 실행 중인 컨테이너 확인
sudo docker ps

# 컨테이너 로그 확인
sudo docker logs dog-llm-api

# 컨테이너 리소스 사용량 확인
sudo docker stats dog-llm-api
```

### 2. API 엔드포인트 테스트
```bash
# API 서버 상태 확인
curl http://localhost:8000/docs

# 강아지 프로필 검색 테스트
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "건강한 골든 리트리버"}'

# 유사 프로필 검색 테스트
curl -X POST http://localhost:8000/similar \
  -H "Content-Type: application/json" \
  -d '{"profile_id": 1}'
```

### 3. 성능 테스트
```bash
# 동시 요청 테스트 (ab 명령어가 필요할 수 있음)
ab -n 100 -c 10 -p test_data.json -T application/json http://localhost:8000/search

# 응답 시간 측정
time curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "건강한 골든 리트리버"}'
```

### 4. 오류 테스트
```bash
# 잘못된 요청 테스트
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"invalid_field": "test"}'

# 존재하지 않는 엔드포인트 테스트
curl http://localhost:8000/nonexistent
```

### 5. 시스템 리소스 모니터링
```bash
# CPU 사용량 모니터링
top -p $(pgrep -f "uvicorn main:app")

# 메모리 사용량 모니터링
free -h

# 디스크 I/O 모니터링
iostat -x 1

# 네트워크 트래픽 모니터링
iftop
```

### 테스트 결과 확인 사항
1. API 응답이 정상적으로 오는지
2. 응답 시간이 적절한지 (일반적으로 1초 이내)
3. CPU 사용량이 설정한 제한 내에 있는지
4. 메모리 사용량이 설정한 제한 내에 있는지
5. 오류 발생 시 적절한 에러 메시지가 반환되는지
6. 로그에 오류나 경고가 없는지 

## 14. Docker 이미지 배포 및 배포 서버 설정

### 1. 개발 환경에서 Docker Hub에 이미지 푸시
```bash
# Docker Hub에 로그인
docker login

# 이미지에 태그 추가
docker tag dog-llm-api [DOCKER_HUB_USERNAME]/dog-llm-api:latest

# 이미지 푸시
docker push [DOCKER_HUB_USERNAME]/dog-llm-api:latest
```

### 2. 배포 서버(Rocky Linux 9)에서 이미지 풀 및 실행
```bash
# Docker Hub에 로그인
sudo docker login

# 이미지 풀
sudo docker pull [DOCKER_HUB_USERNAME]/dog-llm-api:latest

# 이미지에 로컬 태그 추가
sudo docker tag [DOCKER_HUB_USERNAME]/dog-llm-api:latest dog-llm-api:latest

# 컨테이너 실행
sudo docker run -d \
  --name dog-llm-api \
  -p 8000:8000 \
  --env-file .env \
  --cpuset-cpus 0-3 \
  --cpus 2.5 \
  --memory 2g \
  --shm-size 2g \
  dog-llm-api
```

### 3. 이미지 업데이트 방법
```bash
# 개발 환경에서
docker build -t dog-llm-api .
docker tag dog-llm-api [DOCKER_HUB_USERNAME]/dog-llm-api:latest
docker push [DOCKER_HUB_USERNAME]/dog-llm-api:latest

# 배포 서버에서
sudo docker pull [DOCKER_HUB_USERNAME]/dog-llm-api:latest
sudo docker stop dog-llm-api
sudo docker rm dog-llm-api
sudo docker run -d \
  --name dog-llm-api \
  -p 8000:8000 \
  --env-file .env \
  --cpuset-cpus 0-3 \
  --cpus 2.5 \
  --memory 2g \
  --shm-size 2g \
  dog-llm-api
``` 