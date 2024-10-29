import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from core.exceptions.route_exceptions import RouteHandlerError
from core.utils.selenium_utils import CrawlingWebDriver, WebScarper

def render_tmp_html():
    return "<h1>네이버 블로그 스크래핑 시작123<h1>"


class NvBlogScraper(WebScarper):
    pass
        
    # _driver = None
    # _wait = None

    # @classmethod
    # def init(self, driver):

    #     try:
    #         self._driver = driver
    #         self._wait = WebDriverWait(self._driver, 3)

    #     except Exception as e:
    #         raise RouteHandlerError(e)

    # @classmethod
    # def wait_loading(self):
    #     try:
    #         self._wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    #     except Exception as e:
    #         print(e)
    #         print("요소를 찾는 데 실패했습니다.")

    # @classmethod
    # def open_browser(self, url):
    #     try:
    #         self._driver.get(url)
    #         self._driver.maximize_window()
    #         self.wait_loading()

    #     except Exception as e:
    #         raise RouteHandlerError(e)
        
    # @classmethod
    # def go_blog_tab(self, tab_name):
    #     tab_name = "블로그"
        
    #     blog_tab = self._driver.find_element(By.XPATH, f"//a[contains(text(),{tab_name})]")

    #     time.sleep(2)  # 페이지 로딩 대기
    #     blog_tab.click()


    # @classmethod
    # def close_browser(self, delay=0):
    #     time.sleep(delay)
    #     self._driver.quit()
