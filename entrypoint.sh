#!/bin/bash

# ✅ 환경 변수 로드
export $(grep -v '^#' .env | xargs)

# ✅ FastAPI 실행
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# ✅ Celery Worker 실행 (백그라운드)
celery -A app.services.celery_worker:celery_app worker --loglevel=info --pool=solo &

# ✅ 프로세스를 유지
wait -n
