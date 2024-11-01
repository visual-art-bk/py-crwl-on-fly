from core.utils.WebScrpManager import WebScrpManager
from core.exceptions.route_exceptions import RouteHandlerError

def home_handler():
    try:
        with WebScrpManager() as manager:
            manager.driver.get("https://google.com")

            print(manager.driver.title)  
            data = manager.driver.title  
            
        return f"<h1>{data} - CrawlingWebDriver Test OK 123 </h1>"

    except Exception as e:
        raise RouteHandlerError(e)
        
