from flask import Blueprint, request, jsonify, render_template_string
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import traceback

# 블루프린트 생성
main = Blueprint("main", __name__)


# 루트 경로
@main.route("/")
def home():
    try:
        options = Options()
        
        # Fly.io와 같은 서버 환경에서 Selenium을 사용하는 경우, 
        # 실제 디스플레이가 없는 상태에서 Chrome을 실행하게 되므로, 
        # --headless 옵션이 필요합니다. 
        # --headless 옵션 없이 Chrome을 실행하면 디스플레이가 없는 환경에서는 Chrome이 제대로 실행되지 않아 오류가 발생할 수 있습니다.
        # 화면 표시 없이 실행 (서버 환경에서 필수)
        options.add_argument("--headless")  
        # 
        # 
        # 
        options.add_argument(
            "--no-sandbox"
        )  # 샌드박스 비활성화 (리소스 제한 환경에서 필수)
        options.add_argument("--disable-dev-shm-usage")  # /dev/shm 공간 문제 해결
        options.add_argument("--disable-gpu")  # GPU 비활성화
        options.add_argument("--remote-debugging-port=9222")  # 원격 디버깅 포트 설정
        options.add_argument("--window-size=1920,1080")  # 기본 창 크기 설정

        driver_path = "/app/static/drivers/chromedriver/chromedriver"

        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)

        driver.get("https://google.com")
        data = driver.title  # 예시로 페이지 제목 가져오기

        return f"<h1>{data}</h1>"

    except Exception as e:
        # 예외 발생 시 HTML로 출력
        error_message = traceback.format_exc()
        return render_template_string(
            """
            <html>
                <head><title>Error</title></head>
                <body>
                    <h1>An error occurred</h1>
                    <pre>{{ error_message }}</pre>
                </body>
            </html>
            """,
            error_message=error_message,
        )
