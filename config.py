import os
from dotenv import load_dotenv

# .env 파일을 로드하여 환경 변수를 설정
load_dotenv()

# 환경 변수에서 GOOGLE_CHROME_DRIVER_PATH 값을 가져옴
GOOGLE_CHROME_DRIVER_PATH = os.getenv("GOOGLE_CHROME_DRIVER_PATH")
