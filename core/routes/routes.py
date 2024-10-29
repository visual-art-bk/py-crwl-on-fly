from flask import Blueprint, render_template_string
import traceback
from core.utils.selenium_utils import CrawlingWebDriver
from selenium.common.exceptions import WebDriverException

# 블루프린트 생성
main = Blueprint("main", __name__)

# 루트 경로
@main.route("/")
def home():
    try:
        # 사용 예제
        with CrawlingWebDriver() as driver:
            driver.get("https://google.com")

            print(driver.title)  # 페이지 타이틀 출력
            data = driver.title  # 예시로 페이지 제목 가져오기
        return f"<h1>{data} - CrawlingWebDriver Test OK </h1>"
            # driver.quit() 후 세션 종료 여부를 확인하기 위해 Selenium 메서드 호출
            
    # except WebDriverException as e:
    #     return f"<h1>{e}</h1>"
        
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
