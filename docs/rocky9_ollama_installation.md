# Rocky9에서 Ollama 및 llama3 설치 가이드

## 1. 시스템 요구사항

### 하드웨어 요구사항
- CPU: 4코어 이상 권장
- RAM: 최소 16GB (llama3 모델 실행을 위해)
- 디스크: 최소 50GB 여유 공간 (모델 저장용)

### 소프트웨어 요구사항
- Rocky Linux 9
- root 또는 sudo 권한이 있는 사용자 계정

## 2. Ollama 설치

### 2.1 시스템 업데이트
```bash
sudo dnf update -y
```

### 2.2 필수 패키지 설치
```bash
sudo dnf install -y curl wget git
```

### 2.3 Ollama 설치
```bash
# Ollama 설치 스크립트 다운로드 및 실행
curl -fsSL https://ollama.com/install.sh | sh
```

### 2.4 Ollama 서비스 활성화 및 시작
```bash
# 서비스 활성화
sudo systemctl enable ollama

# 서비스 시작
sudo systemctl start ollama

# 서비스 상태 확인
sudo systemctl status ollama
```

## 3. llama3 모델 설치

### 3.1 모델 다운로드
```bash
# llama3 모델 다운로드
ollama pull llama3
```

### 3.2 설치 확인
```bash
# 설치된 모델 목록 확인
ollama list
```

## 4. 방화벽 설정 (필요한 경우)

### 4.1 Ollama 포트(11434) 열기
```bash
# firewalld가 실행 중인 경우
sudo firewall-cmd --permanent --add-port=11434/tcp
sudo firewall-cmd --reload
```

## 5. 시스템 최적화

### 5.1 스왑 공간 설정 (선택사항)
```bash
# 스왑 파일 생성 (16GB)
sudo fallocate -l 16G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# 부팅 시 자동 마운트 설정
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### 5.2 시스템 제한 설정
```bash
# /etc/security/limits.conf 파일에 다음 내용 추가
* soft nofile 65535
* hard nofile 65535
* soft nproc 65535
* hard nproc 65535
```

## 6. 문제 해결

### 6.1 일반적인 문제
1. 모델 다운로드 실패
   - 인터넷 연결 확인
   - 디스크 공간 확인
   - `ollama pull llama3` 명령어 재시도

2. 서비스 시작 실패
   - 로그 확인: `journalctl -u ollama`
   - 포트 충돌 확인: `netstat -tulpn | grep 11434`

### 6.2 성능 최적화
1. 모델 실행 속도가 느린 경우
   - CPU 사용량 확인: `top` 또는 `htop`
   - 메모리 사용량 확인: `free -h`
   - 필요한 경우 스왑 공간 추가

## 7. 자동 시작 설정

### 7.1 시스템 재시작 시 자동 시작
```bash
# 서비스가 자동으로 시작되도록 설정되어 있는지 확인
sudo systemctl is-enabled ollama
```

## 8. 모니터링

### 8.1 기본 모니터링 명령어
```bash
# 서비스 상태 확인
sudo systemctl status ollama

# 로그 확인
journalctl -u ollama -f

# 리소스 사용량 확인
top
htop
free -h
```

## 9. 백업 및 복구

### 9.1 모델 백업
```bash
# 모델 파일 위치
~/.ollama/models
```

### 9.2 백업 스크립트 예시
```bash
#!/bin/bash
BACKUP_DIR="/backup/ollama"
DATE=$(date +%Y%m%d)

mkdir -p $BACKUP_DIR
tar -czf $BACKUP_DIR/ollama_models_$DATE.tar.gz ~/.ollama/models
```

## 10. 보안 고려사항

### 10.1 접근 제한
- 필요한 경우 방화벽 규칙으로 특정 IP만 접근 허용
- 내부 네트워크에서만 접근 가능하도록 설정

### 10.2 모니터링
- 시스템 로그 정기적 확인
- 비정상적인 리소스 사용 모니터링

## 참고사항
- Ollama 공식 문서: https://ollama.com/docs
- llama3 모델 정보: https://ollama.com/library/llama3
- Rocky Linux 문서: https://docs.rockylinux.org 