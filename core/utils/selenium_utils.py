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


class CrawlingWebDriver:
    _driver: webdriver.Chrome = None
    _service: Service = None

    @classmethod
    def _init_serive_options(self, options: Options):
        

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

        ### 최근에 추가된 옵션
        options.add_argument("--blink-settings=imagesEnabled=false")  # 이미지 비활성화

        # eager: DOM 콘텐츠가 로드되면 바로 작업을 시작하며, 이미지나 광고 등은 나중에 로드
        options.page_load_strategy = "eager"

        # 속도가 빨라짐에 기여하는 듯함 데스트해봐야함
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
        )

        return options

    @classmethod
    def _init_driver_execute_cdp_dmd(self, global_driver: webdriver.Chrome):
        # 이미지, 광고, 외부 스크립트 차단
        global_driver.execute_cdp_cmd(
            "Network.setBlockedURLs",
            {
                "urls": [
                    "*googlesyndication.com/*",  # Google 광고
                    "*doubleclick.net/*",  # DoubleClick 광고
                    "*adservice.google.com/*",  # Google 광고 서비스
                    "*.jpg",
                    "*.jpeg",
                    "*.png",  # 이미지 파일
                    "*.gif",
                    "*.svg",  # 이미지 파일
                    "*.css",  # CSS 파일
                    "*.woff",
                    "*.woff2",  # 웹 폰트
                    "*.js",  # 외부 스크립트
                ]
            },
        )
        # 불필요한 요소 제거 (예: 광고 배너, 동적 콘텐츠 등)
        global_driver.execute_script(
            """
            var ads = document.querySelectorAll('.ad, .banner, .popup');
            ads.forEach(ad => ad.remove());
        """
        )

    def __init__(self):
        global driver

        # See .env, config.py and Dockerfile.
        self._service = Service(GOOGLE_CHROME_DRIVER_PATH)
        
        options = Options()
        self._init_serive_options(options)

        driver = webdriver.Chrome(service=self._service, options=options)
        self._init_driver_execute_cdp_dmd(driver)
        
        self._driver = driver

    def __enter__(self):
        return self._driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._driver.quit()

        # 서비스 종료 및 자식 프로세스 강제 종료
        if self._service.process:
            try:
                # 부모 프로세스 (ChromeDriver) PID 가져오기
                parent_pid = self._service.process.pid
                parent = psutil.Process(parent_pid)

                # 자식 프로세스 순회 및 종료
                for child in parent.children(recursive=True):
                    child.kill()
                parent.kill()
            except psutil.NoSuchProcess:
                print("프로세스가 이미 종료되었습니다.")
            except Exception as e:
                print(f"프로세스 종료 중 오류 발생: {e}")


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
