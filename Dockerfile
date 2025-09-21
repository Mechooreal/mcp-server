# Dockerfile
FROM python:3.13.2

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사
COPY requirements.txt .

RUN ls -l

# 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY .env .env

CMD ["python", "my_server.py"]