from flask import Blueprint, render_template_string
import traceback
from core.utils.selenium_utils import CrawlingWebDriver
from selenium.common.exceptions import WebDriverException
from core.routes.home import home_handler
from core.exceptions.route_exceptions import RouteHandlerError
# 블루프린트 생성
main = Blueprint("main", __name__)


# 루트 경로
@main.route("/")
def home():
    return home_handler()