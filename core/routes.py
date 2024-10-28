from flask import Blueprint, request, jsonify, render_template_string
from core.selenium_utils import WebDriverSingleton
import traceback

# 블루프린트 생성
main = Blueprint("main", __name__)


# 루트 경로
@main.route("/")
def home():
    try:
        driver = WebDriverSingleton.get_driver()  # 싱글턴 driver 인스턴스 가져오기
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
