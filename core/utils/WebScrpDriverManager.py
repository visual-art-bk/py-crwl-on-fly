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
    _request_count = 0

    def __init__(self):
        self._init_driver()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._count_request()

       
        
        self.inspect_request_count()
        self.driver.quit()

    @classmethod
    def _configure_options(cls):
        cls.options = Options()

        # See ./.env
        if config.HEADLESS:
            cls.options.add_argument("--headless")
        #
        #
        #
        cls.options.add_argument(
            "--no-sandbox"
        )  # 샌드박스 비활성화 (리소스 제한 환경에서 필수)
        cls.options.add_argument("--disable-dev-shm-usage")  # /dev/shm 공간 문제 해결
        cls.options.add_argument("--disable-gpu")  # GPU 비활성화
        cls.options.add_argument(
            "--remote-debugging-port=9222"
        )  # 원격 디버깅 포트 설정
        cls.options.add_argument("--window-size=1920,1080")  # 기본 창 크기 설정

        ### 최근에 추가된 옵션
        cls.options.add_argument(
            "--blink-settings=imagesEnabled=false"
        )  # 이미지 비활성화

        # eager: DOM 콘텐츠가 로드되면 바로 작업을 시작하며, 이미지나 광고 등은 나중에 로드
        cls.options.page_load_strategy = "eager"

        # 속도가 빨라짐에 기여하는 듯함 데스트해봐야함
        cls.options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
        )

    @classmethod
    def _init_driver(cls):

        if cls.driver:
            cls.driver.quit()

        services = Service(GOOGLE_CHROME_DRIVER_PATH)
        cls.options = Options()
        cls._configure_options()

        cls.driver = webdriver.Chrome(service=services, options=cls.options)
        cls._configure_driver()

        return cls.driver

    @classmethod
    def _configure_driver(cls):
        if cls.driver:
            cls.driver.execute_cdp_cmd(
                "Network.setBlockedURLs",
                {
                    "urls": [
                        "*googlesyndication.com/*",
                        "*doubleclick.net/*",
                        "*adservice.google.com/*",
                        "*.jpg",
                        "*.jpeg",
                        "*.png",
                        "*.gif",
                        "*.svg",
                        "*.css",
                        "*.woff",
                        "*.woff2",
                        "*.js",
                    ]
                },
            )
            cls.driver.execute_script(
                """
                var ads = document.querySelectorAll('.ad, .banner, .popup');
                ads.forEach(ad => ad.remove());
                """
            )

    @classmethod
    def _count_request(cls):
        cls._request_count += 1

    @classmethod
    def _regenrate_driver(cls):
        cls.driver.quit()
        cls.driver = cls._init_driver()

    @classmethod
    def inspect_request_count(cls):
        print(f"현재 {cls._request_count}번 요청되었습니다.")
        
        # NOTE todo repair calcurating. self._request_count > MAX_REQUEST
        if cls._request_count >= MAX_REQUEST:
            print(
                f"드라이브 초기화 됩니다 -  총 {cls._request_count} // Max {MAX_REQUEST}"
            )

            cls._regenrate_driver()

            cls._request_count = 0  # 카운트 초기화
