module.exports = {
  apps: [{
    name: "dailypet",
    script: "main.py",
    interpreter: "/home/ramza/dailypet/venv/bin/python",  // 절대 경로 사용
    env: {
      PYTHONUNBUFFERED: "1",
      TRANSFORMERS_OFFLINE: "0",
      TOKENIZERS_PARALLELISM: "false",
      HF_HUB_ENABLE_HF_TRANSFER: "1",
      HF_HUB_DISABLE_TELEMETRY: "1",
      HF_HUB_OFFLINE: "1",
      TESSDATA_PREFIX: "/usr/share/tesseract-ocr/4.00/tessdata",  // Tesseract 데이터 경로
      TESSERACT_OCR_LANG: "kor",  // 기본 OCR 언어 설정
      PATH: "/usr/bin/poppler:$PATH"  // Poppler PATH 설정
    },
    env_production: {
      NODE_ENV: "production"
    },
    max_memory_restart: "4G",  // 메모리 제한 증가
    instances: 1,
    autorestart: true,
    watch: false,
    time: true,
    log_date_format: "YYYY-MM-DD HH:mm:ss",
    error_file: "/home/ramza/dailypet/logs/error.log",
    out_file: "/home/ramza/dailypet/logs/out.log",
    merge_logs: true,
    cwd: "/home/ramza/dailypet",  // 작업 디렉토리 설정
    log_type: "json"  // JSON 형식 로그 사용
  }]
} 