import traceback
from datetime import datetime
import time
import psutil
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from config import GOOGLE_CHROME_DRIVER_PATH
import config
from core.exceptions.route_exceptions import RouteHandlerError, NoSuchElementError
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

MAX_REQUEST = 10



class WebScarper:
    _driver: webdriver.Chrome = None
    _wait_under_1sec = None
    _wait_under_3sec = None
    _wait_under_5sec = None

    @classmethod
    def init(self, driver):

        try:
            self._driver = driver
            self._wait_under_1sec = WebDriverWait(self._driver, 0.5)
            self._wait_under_3sec = WebDriverWait(self._driver, 2.5)
            self._wait_under_5sec = WebDriverWait(self._driver, 4)

        except Exception as e:
            raise RouteHandlerError(e)

    @classmethod
    def wait_loading(self, delay: int = 0):

        try:
            wait = self._create_wait(self, delay)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        except Exception as e:
            print(e)

            print("요소를 찾는 데 실패했습니다.")

    @classmethod
    def open_browser(self, url):

        try:
            self._driver.get(url)
            self._driver.maximize_window()
            self.wait_loading(delay=0.5)

        except Exception as e:
            raise RouteHandlerError(e)

    @classmethod
    def search_keyword(self, keyword, css_selector_input):

        self._keyword = keyword

        try:
            search_box = self._wait_under_3sec.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector_input))
            )
            search_box.send_keys(self._keyword)
            search_box.submit()

        except (TimeoutException, NoSuchElementException):

            print("시간 초과: 요소를 찾지 못했습니다.")

            raise NoSuchElementError()

    @classmethod
    def render_test_html(self):

        now = datetime.now()

        formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")

        return f"<h1>스크랩 성공 - 현재: {formatted_now}</h1>"

    def _create_wait(self, delay: int = 5):
        return WebDriverWait(self._driver, delay)
