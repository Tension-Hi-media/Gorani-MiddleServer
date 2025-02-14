import httpx
import re
from fastapi import APIRouter, HTTPException
import logging
from app.models.schemas import TranslateRequest, TranslateResponse
from app.services.translation_service import translate_text  # ✅ FastAPI에서 사용 가능하도록 임포트

router = APIRouter()
logger = logging.getLogger(__name__)

# ✅ Runpod Gorani(Llama) 모델 주소 (Runpod Proxy URL 사용)
RUNPOD_MODEL_URL = "https://8309-221-148-97-237.ngrok-free.app/translate/Gorani"

# ✅ **번역을 명확히 요청하는 프롬프트 설정**
TRANSLATION_PROMPT = """
### Instruction:
You are a translation assistant. However, you must NOT introduce yourself or mention that you are an assistant.
- Translate the text provided under 'Input' from {src_lang} to {target_language}.
- Output ONLY the translated text as a plain string.
- Do NOT include explanations, introductions, or formatting.
- Do NOT prefix or suffix the translation with any extra words.
- Ensure that the output does NOT contain the words "assistant", "Translation", "Here is the result:", or similar phrases.

### Target Language:
{target_language}

### Input:
{input_text}

### Response:
"""

async def translate_with_gorani(
    text: str, source_lang: str = "ko", target_lang: str = "en", model: str = "Gorani"
) -> str:
    """
    Runpod의 Gorani(Llama) 모델을 호출하여 번역 수행
    """
    prompt = TRANSLATION_PROMPT.format(
        src_lang=source_lang, target_language=target_lang, input_text=text
    )

    payload = {
        "text": prompt,
        "source_lang": source_lang,
        "target_lang": target_lang,
        "model": model
    }

    logger.info(f"📤 Runpod 요청 Payload: {payload}")  # ✅ 요청 로그 추가

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(RUNPOD_MODEL_URL, json=payload)

            if response.status_code != 200:
                logger.error(f"❌ Runpod 응답 오류: {response.status_code} - {response.text}")
                raise HTTPException(status_code=502, detail=f"Runpod 응답 오류: {response.status_code}")

            try:
                response_data = response.json()
                logger.info(f"✅ Runpod 응답: {response_data}")

                # ✅ `answer` 키에서 번역된 내용만 추출
                raw_text = response_data.get("answer", "").strip()

                # ✅ 패턴을 이용해 불필요한 설명 제거
                match = re.search(r'The text translates to:\s*"(.+?)"', raw_text, re.DOTALL)

                if match:
                    translated_text = match.group(1).strip()
                else:
                    # ✅ 만약 위 패턴이 없으면 전체 응답 중 가장 마지막 따옴표 내부 내용을 가져옴
                    match_alt = re.findall(r'"(.*?)"', raw_text)
                    translated_text = match_alt[-1] if match_alt else raw_text

                if not translated_text:
                    logger.error(f"❌ 번역 실패 - 응답 내용: {response_data}")
                    raise HTTPException(status_code=502, detail="Runpod에서 번역 결과를 받지 못했습니다.")

                return translated_text  # ✅ 번역된 텍스트만 반환

            except ValueError:
                logger.error(f"❌ JSON 파싱 오류 - 응답 내용: {response.text}")
                raise HTTPException(status_code=502, detail="Runpod 응답 JSON 파싱 오류")

        except httpx.RequestError as e:
            logger.error(f"❌ HTTP 통신 오류 발생: {str(e)}")
            raise HTTPException(status_code=502, detail="Runpod 서버 연결 오류")

        except Exception as e:
            logger.error(f"❌ 알 수 없는 오류 발생: {str(e)}")
            raise HTTPException(status_code=500, detail="번역 요청 중 알 수 없는 오류 발생")

@router.post("/translate/onlygpt", response_model=TranslateResponse, tags=["Translation"])
async def translate_with_gpt(request: TranslateRequest):
    """
    GPT 또는 Runpod의 Gorani(Llama) 모델을 사용하여 번역 수행
    """
    try:
        logger.info(f"📥 Received request: {request.dict()}")

        model = request.model if request.model else "OpenAI"

        if model == "OpenAI":
            result = translate_text(request.text, request.source_lang, request.target_lang)
        elif model == "Gorani":
            logger.info("🚀 Runpod Gorani 모델로 요청 중...")
            # ✅ `source_lang`, `target_lang`, `model`도 함께 전달
            result = await translate_with_gorani(request.text, request.source_lang, request.target_lang, request.model)
            logger.info(f"✅ Runpod 응답: {result}")
        else:
            raise HTTPException(status_code=400, detail="지원되지 않는 모델입니다.")

        return TranslateResponse(answer=result)

    except Exception as e:
        logger.error(f"❌ Translation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))