from core.utils.selenium_utils import CrawlingWebDriver
from core.exceptions.route_exceptions import RouteHandlerError

def home_handler():
    try:
        # 사용 예제
        with CrawlingWebDriver() as driver:
            driver.get("https://google.com")

            print(driver.title)  # 페이지 타이틀 출력
            data = driver.title  # 예시로 페이지 제목 가져오기
            
        return f"<h1>{data} - CrawlingWebDriver Test OK </h1>"

    except Exception as e:
        raise RouteHandlerError(e)
        
