import os
from dotenv import load_dotenv

# .env 파일을 로드하여 환경 변수를 설정
load_dotenv()

# 환경 변수 .env에서 GOOGLE_CHROME_DRIVER_PATH 값을 가져옴
# Vs code에서의 ./static/drivers와 서버 Fly.io에서의 /app/static/drivers 분리를 위한 설정 
GOOGLE_CHROME_DRIVER_PATH = os.getenv("GOOGLE_CHROME_DRIVER_PATH")
HEADLESS = os.getenv("HEADLESS", "True").lower() == "true"