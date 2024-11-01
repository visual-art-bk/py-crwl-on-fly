import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from core.exceptions.route_exceptions import RouteHandlerError
from core.utils.WebScarper import WebScarper

def render_tmp_html():
    return "<h1>네이버 블로그 스크래핑 시작123<h1>"


class NvBlogScraper(WebScarper):
    

    pass