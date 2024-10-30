import traceback
from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from config import GOOGLE_CHROME_DRIVER_PATH
import config
import os
import signal
from core.exceptions.route_exceptions import RouteHandlerError, NoSuchElementError
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class CrawlingWebDriver:
    def __init__(self):
        # See .env, config.py and Dockerfile.
        service = Service(GOOGLE_CHROME_DRIVER_PATH)

        options = Options()

        # Fly.io와 같은 서버 환경에서 Selenium을 사용하는 경우,
        # 실제 디스플레이가 없는 상태에서 Chrome을 실행하게 되므로,
        # --headless 옵션이 필요합니다.
        # --headless 옵션 없이 Chrome을 실행하면 디스플레이가 없는 환경에서는 Chrome이 제대로 실행되지 않아 오류가 발생할 수 있습니다.
        # 화면 표시 없이 실행 (서버 환경에서 필수)
        if config.HEADLESS:
            options.add_argument("--headless")
        #
        #
        #
        options.add_argument(
            "--no-sandbox"
        )  # 샌드박스 비활성화 (리소스 제한 환경에서 필수)
        options.add_argument("--disable-dev-shm-usage")  # /dev/shm 공간 문제 해결
        options.add_argument("--disable-gpu")  # GPU 비활성화
        options.add_argument("--remote-debugging-port=9222")  # 원격 디버깅 포트 설정
        options.add_argument("--window-size=1920,1080")  # 기본 창 크기 설정

        # ChromeDriver 설정 및 생성
        self.driver = webdriver.Chrome(service=service, options=options)

    def __enter__(self):
        # with 블록 시작 시 driver 객체 반환
        return self.driver

    # TODO [f342] 여기 에러처리가 안되고 있음 해결해야 합니다.
    def __exit__(self, exc_type, exc_val, exc_tb):
        # with 블록 종료 시 자동으로 driver.quit() 호출
        self.driver.quit()

        # ChromeDriver 프로세스 상태 확인 및 강제 종료
        if self.driver.service.process is None:
            print("driver.quit() 호출됨: ChromeDriver가 종료되었습니다.")
        else:
            print("driver.quit() 호출 실패: ChromeDriver가 여전히 실행 중입니다.")

            # 프로세스 ID를 가져와 강제 종료 시도
            try:
                pid = self.driver.service.process.pid
                os.kill(pid, signal.SIGTERM)
                print("프로세스 강제 종료됨: ChromeDriver가 종료되었습니다.")
            except Exception as e:
                print("프로세스 강제 종료 실패:", e)


class WebScarper:
    _driver = None
    _wait = None

    @classmethod
    def init(self, driver):

        try:
            self._driver = driver
            self._wait = WebDriverWait(self._driver, 5)

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
            self.wait_loading(delay=3)

        except Exception as e:
            raise RouteHandlerError(e)

    @classmethod
    def close_browser(self, delay=0):

        time.sleep(delay)

        print("현재 드라이브를 닫습니다.")

        self._driver.quit()

    @classmethod
    def search_keyword(self, keyword, css_selector_input):

        self._keyword = keyword

        try:
            wait = self._create_wait(self, delay=3)
            search_box = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector_input))
            )

            search_box.send_keys(self._keyword)
            search_box.submit()

        except (TimeoutException, NoSuchElementException):

            self.close_browser()

            print("시간 초과: 요소를 찾지 못했습니다.")

            raise NoSuchElementError()

    @classmethod
    def render_test_html(self):

        now = datetime.now()

        formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")

        return f"<h1>스크랩 성공 - 현재: {formatted_now}</h1>"

    def _create_wait(self, delay: int = 5):
        return WebDriverWait(self._driver, delay)
