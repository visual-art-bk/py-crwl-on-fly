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
from core.utils.IFrameHandler import IFrameHandler
from core.exceptions.scraping_exceptions import ErrorHandler

MAX_REQUEST = 10


class WebScarper(IFrameHandler):
    _driver: webdriver.Chrome = None
    _keyword: str = None
    _wait_under_1sec = None
    _wait_under_3sec = None
    _wait_under_5sec = None

    def __init__(self, driver):
        super().__init__(driver)
        self._driver = driver

    @classmethod
    def wait_loading(self, delay: int = 0):
        try:
            wait = WebDriverWait(self._driver, delay)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        except Exception as e:
            print(e)
            print("요소를 찾는 데 실패했습니다.")
            

    def open_browser(self, url):
        try:
            self._driver.get(url)
            self._driver.maximize_window()

        except Exception as e:
            print(e)
            

    def search_keyword(self, keyword, css_selector_input):

        self._keyword = keyword
        wait = WebDriverWait(self._driver, 3)

        try:
            search_box = wait.until(
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


    def find_element_by_xpath(self, xpath):
        try:
            element = self._driver.find_element(By.XPATH, xpath)
            return element
        except Exception as e:
            error_message = traceback.format_exc()
            print(f"{xpath} 에  해당하는 엘레멘트가  존재하지 않습니다.")
            print(error_message)


    @classmethod
    def make_xpath(cls, keword):
        return f"//a[contains(text(),'{keword}')]"
    

    def _find_elements_by_css(self, css, delay=0):
        try:
            elements = WebDriverWait(self._driver, delay).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, css))
            )
            return elements
        except Exception as e:
            raise ErrorHandler.ScrapingException(f"css 선택자: {css} 에 일치하는 엘리멘트가 없음.")
