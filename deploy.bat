@echo off
setlocal enabledelayedexpansion

echo ===== Windows 배포 스크립트 시작 =====

:: Python 가상환경 설정
echo [1/5] Python 가상환경 설정
if not exist "venv" (
    echo Python 가상환경 생성
    python -m venv venv
    call venv\Scripts\activate
    python -m pip install --upgrade pip
) else (
    call venv\Scripts\activate
)

:: Poppler 설치 확인
echo [2/5] Poppler 설치 확인
if not exist "C:\Program Files\poppler-24.08.0" (
    echo Poppler가 설치되어 있지 않습니다.
    echo Poppler를 설치하시겠습니까? (Y/N)
    set /p install_poppler=
    if /i "!install_poppler!"=="Y" (
        echo Poppler 설치를 시작합니다...
        powershell -Command "Invoke-WebRequest -Uri https://github.com/oschwartz10612/poppler-windows/releases/download/v24.08.0-0/Release-24.08.0-0.zip -OutFile poppler.zip"
        powershell -Command "Expand-Archive -Path poppler.zip -DestinationPath 'C:\Program Files'"
        del poppler.zip
        setx POPPLER_PATH_WINDOWS "C:\Program Files\poppler-24.08.0\Library\bin"
    ) else (
        echo Poppler 설치가 취소되었습니다.
        exit /b 1
    )
)

:: Tesseract 설치 확인
echo [3/5] Tesseract 설치 확인
if not exist "C:\Program Files\Tesseract-OCR" (
    echo Tesseract가 설치되어 있지 않습니다.
    echo Tesseract를 설치하시겠습니까? (Y/N)
    set /p install_tesseract=
    if /i "!install_tesseract!"=="Y" (
        echo Tesseract 설치를 시작합니다...
        powershell -Command "Invoke-WebRequest -Uri https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.3.3.20231005.exe -OutFile tesseract-setup.exe"
        start /wait tesseract-setup.exe
        del tesseract-setup.exe
        setx TESSERACT_PATH_WINDOWS "C:\Program Files\Tesseract-OCR"
    ) else (
        echo Tesseract 설치가 취소되었습니다.
        exit /b 1
    )
)

:: Ollama 설치 확인
echo [4/5] Ollama 설치 확인
where ollama >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Ollama가 설치되어 있지 않습니다.
    echo Ollama를 설치하시겠습니까? (Y/N)
    set /p install_ollama=
    if /i "!install_ollama!"=="Y" (
        echo Ollama 설치를 시작합니다...
        powershell -Command "Invoke-WebRequest -Uri https://ollama.ai/download/windows -OutFile ollama-setup.exe"
        start /wait ollama-setup.exe
        del ollama-setup.exe
    ) else (
        echo Ollama 설치가 취소되었습니다.
        exit /b 1
    )
)

:: Ollama 모델 확인 및 다운로드
echo [5/5] Ollama 모델 확인
ollama list | findstr "llama3" >nul
if %ERRORLEVEL% NEQ 0 (
    echo llama3 모델을 다운로드합니다...
    ollama pull llama3
)

:: Python 패키지 설치
echo [6/6] Python 패키지 설치
pip install -r requirements.txt

:: PM2 설치 및 설정
echo [7/7] PM2 설정
where pm2 >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo PM2를 설치합니다...
    npm install -g pm2
)

:: PM2 프로세스 시작
echo PM2 프로세스를 시작합니다...
pm2 start ecosystem.config.windows.js

echo ===== 배포 완료 =====
echo 다음 명령어로 PM2 상태를 확인할 수 있습니다:
echo pm2 list
echo pm2 logs

endlocal 