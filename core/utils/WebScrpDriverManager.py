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

class WebScrpDriverManager:
    driver: webdriver.Chrome = None
    _service: Service = (None,)
    _options: Options = None
    _request_count = 0

    @classmethod
    def _init_serive_options(self, options: Options):

        # See ./.env
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
    def _init_driver(self, service: Service, options: Options):
        self.driver = webdriver.Chrome(service=service, options=options)

        # 이미지, 광고, 외부 스크립트 차단
        self.driver.execute_cdp_cmd(
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
        self.driver.execute_script(
            """
            var ads = document.querySelectorAll('.ad, .banner, .popup');
            ads.forEach(ad => ad.remove());
        """
        )

    def __init__(self):

        # See .env, config.py and Dockerfile.
        self._service = Service(GOOGLE_CHROME_DRIVER_PATH)
        self._options = Options()

        self._init_serive_options(options=self._options)

        self._init_driver(service=self._service, options=self._options)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._request_count += 1
        print(f"현재 {self._request_count}번 요청되었습니다.")
        self.driver.quit()

    @classmethod
    def count_request(self):
        self._request_count += 1

    @classmethod
    def _regenrate_driver(cls):

        cls.driver.quit()

        cls.__init__(cls)

    @classmethod
    def inspect_request_count(self):
        # NOTE todo repair calcurating. self._request_count > MAX_REQUEST
        if self._request_count > MAX_REQUEST:
            print(
                f"드라이브 초기화 됩니다 -  총 {self._request_count} // Max {MAX_REQUEST}"
            )

            self._regenrate_driver()

            self._request_count = 0  # 카운트 초기화
