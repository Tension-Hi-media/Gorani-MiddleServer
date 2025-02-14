from celery import Celery
import requests

# ✅ Redis 컨테이너와 연결 (Docker Compose에서 설정할 예정)
celery_app = Celery(
    "translation_worker",
    backend="redis://redis:6379/0",
    broker="redis://redis:6379/0"
)

@celery_app.task
def translate_task(text, source_lang, target_lang):
    MODEL_SERVER_URL = "http://로컬모델서버_IP:8000/translate/Gorani"  # 모델 서버 URL

    payload = {
        "text": text,
        "source_lang": source_lang,
        "target_lang": target_lang,
        "model": "Gorani"
    }

    response = requests.post(MODEL_SERVER_URL, json=payload)

    if response.status_code == 200:
        return response.json().get("answer", "번역 실패")
    else:
        return "번역 오류 발생"
