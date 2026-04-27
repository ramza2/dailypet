module.exports = {
  apps: [{
    name: "dailypet",
    script: "main.py",
    interpreter: "C:\\Projects\\Cursor\\dailypet\\venv\\Scripts\\python.exe",
    env: {
      PYTHONUNBUFFERED: "1",
      TRANSFORMERS_OFFLINE: "0",
      TOKENIZERS_PARALLELISM: "false",
      HF_HUB_ENABLE_HF_TRANSFER: "1",
      HF_HUB_DISABLE_TELEMETRY: "1",
      HF_HUB_OFFLINE: "1",
      TESSDATA_PREFIX: "C:\\Program Files\\Tesseract-OCR\\tessdata",
      TESSERACT_OCR_LANG: "kor",
      PATH: "C:\\Program Files\\poppler-24.08.0\\Library\\bin;%PATH%"
    },
    env_production: {
      NODE_ENV: "production"
    },
    max_memory_restart: "4G",
    instances: 1,
    autorestart: true,
    watch: false,
    time: true,
    log_date_format: "YYYY-MM-DD HH:mm:ss",
    error_file: "logs/error.log",
    out_file: "logs/out.log",
    merge_logs: true,
    cwd: "C:\\Projects\\Cursor\\dailypet",
    log_type: "json"
  }]
}; 