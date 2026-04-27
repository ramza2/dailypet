# Windows 배포 가이드

## 필수 요구사항

1. Python 3.8 이상
2. Node.js 및 npm
3. Windows PowerShell
4. 관리자 권한
5. Poppler 24.08.0 (PDF 처리용)
6. Tesseract OCR (이미지 텍스트 인식용)

## 수동 설치 가이드

### Poppler 수동 설치
1. [Poppler Windows 릴리스 페이지](https://github.com/oschwartz10612/poppler-windows/releases)에서 24.08.0 버전 다운로드
2. 다운로드한 ZIP 파일을 `C:\Program Files`에 압축 해제
3. 환경 변수 설정:
   ```powershell
   setx POPPLER_PATH_WINDOWS "C:\Program Files\poppler-24.08.0\Library\bin"
   ```

### Tesseract 수동 설치
1. [Tesseract Windows 설치 프로그램](https://github.com/UB-Mannheim/tesseract/wiki)에서 최신 버전 다운로드
2. 설치 프로그램 실행
3. 설치 시 "Additional language data"에서 한국어(kor) 선택
4. 환경 변수 설정:
   ```powershell
   setx TESSERACT_PATH_WINDOWS "C:\Program Files\Tesseract-OCR"
   ```

## 배포 단계

### 1. 저장소 클론
```powershell
git clone [저장소 URL]
cd [프로젝트 디렉토리]
```

### 2. 배포 스크립트 실행
```powershell
.\deploy.bat
```

### 3. PM2 프로세스 관리

#### 프로세스 상태 확인
```powershell
pm2 list
```

#### 로그 확인
```powershell
pm2 logs
```

#### 프로세스 재시작
```powershell
pm2 restart all
```

#### 프로세스 중지
```powershell
pm2 stop all
```

#### 프로세스 삭제
```powershell
pm2 delete all
```

## 문제 해결

### 1. PM2 설치 오류
- Node.js가 제대로 설치되어 있는지 확인
- 관리자 권한으로 PowerShell 실행

### 2. Ollama 설치 오류
- Windows Defender 또는 바이러스 백신이 설치를 차단할 수 있음
- 관리자 권한으로 설치 시도

### 3. Python 패키지 설치 오류
- 가상환경이 제대로 활성화되었는지 확인
- pip 업그레이드 시도: `python -m pip install --upgrade pip`

### 4. Poppler 관련 오류
- `POPPLER_PATH_WINDOWS` 환경 변수가 올바르게 설정되었는지 확인
- Poppler 24.08.0이 `C:\Program Files`에 설치되어 있는지 확인

### 5. Tesseract 관련 오류
- `TESSERACT_PATH_WINDOWS` 환경 변수가 올바르게 설정되었는지 확인
- Tesseract가 `C:\Program Files`에 설치되어 있는지 확인
- 한국어 데이터 파일이 설치되어 있는지 확인

### 6. 메모리 부족 오류
- `ecosystem.config.windows.js`의 `max_memory_restart` 값을 조정
- Windows 시스템의 가상 메모리 설정 확인

### 7.만약 "pip install psycopg2" 실행 시 오류가 발생한다면?

- 우분투의 경우) "libpq-dev" 구성 요소를 설치하지 않았기 때문입니다. Windows 환경이라면 PostgreSQL 구성 요소가 필요한데,

- Windows installers - Interactive installer by EDB
; https://www.postgresql.org/download/windows/
; https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

- 설치까지 할 필요는 없고 압축 해제 후,

c:\temp> postgresql-14.3-1-windows-x64.exe --extract-only yes

- pg_config.exe가 있는 "C:\Program Files\PostgreSQL\14\bin\" 경로를 PATH 환경 변수를 이용해 연결하면 됩니다.

## 자주 묻는 질문

### Q: PM2가 Windows에서 제대로 작동하지 않습니다.
A: Windows용 PM2는 Linux 버전과 약간 다르게 작동합니다. 관리자 권한으로 실행하고, Windows 서비스로 등록하는 것을 고려해보세요.

### Q: Ollama 모델이 메모리 부족 오류를 발생시킵니다.
A: `ecosystem.config.windows.js`에서 메모리 제한을 조정하거나, 더 작은 모델을 사용해보세요.

### Q: Python 가상환경이 활성화되지 않습니다.
A: PowerShell에서 `Set-ExecutionPolicy RemoteSigned` 명령을 실행하여 스크립트 실행 정책을 변경해보세요.

### Q: Poppler나 Tesseract가 제대로 작동하지 않습니다.
A: 환경 변수가 올바르게 설정되었는지 확인하고, 필요한 경우 수동으로 설치해보세요.

## 추가 설정

### Windows 서비스로 등록
```powershell
pm2 startup
pm2 save
```

### 자동 재시작 설정
`ecosystem.config.windows.js`에서 `autorestart: true` 확인

### 로그 관리
```powershell
pm2 install pm2-logrotate
pm2 set pm2-logrotate:max_size 10M
pm2 set pm2-logrotate:retain 7
```

## 지원 및 문의

문제가 발생하면 다음 정보를 포함하여 문의해주세요:
- Windows 버전
- Python 버전
- Node.js 버전
- Poppler 버전 (24.08.0)
- Tesseract 버전
- 발생한 오류 메시지
- PM2 로그 