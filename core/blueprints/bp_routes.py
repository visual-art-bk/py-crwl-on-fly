from flask import Blueprint
from core.utils.WebScrpDriverManager import WebScrpDriverManager
from core.route_handlers.home import home_handler
from core.route_handlers.scr_nv_blog import NvBlogScraper, render_tmp_html
from core.exceptions.route_exceptions import RouteHandlerError
import time

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return home_handler()


@main.route("/scr/nv-blog")
def _():
    try:
        # with문이 종료되면 driver.quit() 실행되므로, 추가 콜 필요없음
        with WebScrpDriverManager() as manager:
            manager.inspect_request_count()
            
            nv_blg_scrper = NvBlogScraper()
            
            nv_blg_scrper.init(manager.driver)
            
            nv_blg_scrper.open_browser("https://www.naver.com")
            nv_blg_scrper.search_keyword("강아지 사료", "input[name='query']")
            
            return nv_blg_scrper.render_test_html()
    except Exception as e:
        raise RouteHandlerError(e)
    finally:
        manager.count_request()
