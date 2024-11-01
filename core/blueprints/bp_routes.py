from flask import Blueprint
from core.utils.WebScrpDriverManager import WebScrpDriverManager
from core.route_handlers.home import home_handler
from core.route_handlers.scr_nv_blog import (
    NvBlogScraper,
    render_tmp_html,
    handler_search_naver_blog,
)
from core.exceptions.route_exceptions import RouteHandlerError
import time
from core.utils.decorate_testers import test_simulate_multiple_requests
from core.utils.testers import request_tester

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return home_handler()


@main.route("/scr/nv-blog")
@test_simulate_multiple_requests(request_count=11, delay=0.2)
def _():

    try:
        # with문이 종료되면 driver.quit() 실행되므로, 추가 콜 필요없음
        with WebScrpDriverManager() as manager:
            return handler_search_naver_blog(manager)

    except Exception as e:
        raise RouteHandlerError(e)
