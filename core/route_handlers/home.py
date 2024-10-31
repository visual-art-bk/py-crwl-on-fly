from core.utils.selenium_utils import CrawlingWebDriver
from core.exceptions.route_exceptions import RouteHandlerError

def home_handler():
    try:
        with CrawlingWebDriver() as manager:
            manager.driver.get("https://google.com")

            print(manager.driver.title)  
            data = manager.driver.title  
            
        return f"<h1>{data} - CrawlingWebDriver Test OK 123 </h1>"

    except Exception as e:
        raise RouteHandlerError(e)
        
