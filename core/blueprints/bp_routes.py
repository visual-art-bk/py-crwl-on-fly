from flask import Blueprint, render_template_string
import traceback
from core.utils.selenium_utils import CrawlingWebDriver
from selenium.common.exceptions import WebDriverException
from core.route_handlers.home import home_handler
from core.route_handlers.scr_nv_blog import NvBlogScraper, render_tmp_html
from core.exceptions.route_exceptions import RouteHandlerError


main = Blueprint("main", __name__)


@main.route("/")
def home():
    return home_handler()


@main.route("/scr/nv-blog")
def _():

    try:
        with CrawlingWebDriver() as driver:

            nv_blg_scrper = NvBlogScraper()
            nv_blg_scrper.init(driver)
            nv_blg_scrper.open_browser("https://www.naver.com")
            nv_blg_scrper.close_browser(delay=0)

            return render_tmp_html()
    except Exception as e:
        RouteHandlerError(e)
