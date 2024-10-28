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
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # GUI 없이 실행
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")


        driver_path = "/app/static/drivers/chromedriver/chromedriver"
        
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
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
