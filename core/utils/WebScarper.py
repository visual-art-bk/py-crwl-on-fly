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
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from core.exceptions.scraping_exceptions import ErrorHandler
from core.utils.ElementFinder import ElementFinder

MAX_REQUEST = 10


class WebScarper(ElementFinder):

    def __init__(self, driver, timeout):
        super().__init__(driver, timeout)

    def open_browser(self, url):

        self.driver.get(url)
        self.driver.maximize_window()

    def search_keyword(self, keyword):

        search_box = self.find_element(
            by=By.CSS_SELECTOR,
            expression="input[name='query']",
            element_description="검색창",
        )
        if not search_box == None:
            search_box.send_keys(keyword)
            search_box.submit()
            return

    @classmethod
    def render_test_html(self):

        now = datetime.now()

        formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")

        return f"<h1>스크랩 성공 - 현재: {formatted_now}</h1>"

    @classmethod
    def make_xpath(cls, keword):
        return f"//a[contains(text(),'{keword}')]"

    def find_element_by_css(self, css, delay=0):
        try:
            element = WebDriverWait(self._driver, delay).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css))
            )
            return element
        except Exception as e:
            raise ErrorHandler.ScrapingException(
                f"css 선택자: {css} 에 일치하는 엘리멘트가 없음."
            )

    def _find_elements_by_css(self, css, delay=0):
        try:
            elements = WebDriverWait(self._driver, delay).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, css))
            )
            return elements
        except Exception as e:
            raise ErrorHandler.ScrapingException(
                f"css 선택자: {css} 에 일치하는 엘리멘트가 없음."
            )
