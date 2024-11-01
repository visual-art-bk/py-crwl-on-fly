import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from core.exceptions.route_exceptions import RouteHandlerError
from core.utils.WebScarper import WebScarper
from core.utils import WebScrpDriverManager


def render_tmp_html():
    return "<h1>네이버 블로그 스크래핑 시작123<h1>"


class NvBlogScraper(WebScarper):
    pass


def handler_search_naver_blog(manager: WebScrpDriverManager):
    url = "https://www.naver.com"
    nv_blg_scrper = NvBlogScraper()

    nv_blg_scrper.init(manager.driver)
    nv_blg_scrper.open_browser(url)
    nv_blg_scrper.search_keyword("강아지 사료", "input[name='query']")

    return nv_blg_scrper.render_test_html()
