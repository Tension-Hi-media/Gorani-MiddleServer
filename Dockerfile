# 1. Python 이미지를 기반으로 시작
FROM python:3.9-slim

# 2. 앱 디렉토리 생성
WORKDIR /app

# 3. 의존성 파일 복사 (requirements.txt 가 있는 경우)
COPY requirements.txt .

# 4. 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 5. 앱 코드 복사
COPY . .

# 6. FastAPI 서버 실행 (uvicorn 사용)
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
