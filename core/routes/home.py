from core.utils.selenium_utils import CrawlingWebDriver
from core.exceptions.route_exceptions import RouteHandlerError

def home_handler():
    try:
        with CrawlingWebDriver() as driver:
            driver.get("https://google.com")

            print(driver.title)  
            data = driver.title  
            
        return f"<h1>{data} - CrawlingWebDriver Test OK </h1>"

    except Exception as e:
        raise RouteHandlerError(e)
        
