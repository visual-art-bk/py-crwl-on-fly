# Python 3.9 slim 베이스 이미지 사용
FROM python:3.9-slim

# 필수 패키지 설치
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && apt-get clean

# Google Chrome 설치
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    google-chrome --version  # 설치된 Google Chrome 버전 출력

# 작업 디렉토리 설정
WORKDIR /app

# 환경 변수 설정
# 이곳은 서버를 위한 변수설정이며, 로컬을 위한 설정은 .env에서 정의
ENV GOOGLE_CHROME_DRIVER_PATH=/app/static/drivers/chromedriver/chromedriver
ENV HEADLESS=True

# Python 패키지 설치
COPY requirements.txt .
RUN pip install -r requirements.txt

# 애플리케이션 소스 복사
COPY . . 

# 앱 실행
CMD ["python", "app.py"]
