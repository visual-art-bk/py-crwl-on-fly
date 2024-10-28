from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class WebDriverSingleton:
    _driver = None  # 클래스 변수로 driver 인스턴스를 저장
    _google_chrome_driver_path = "/static/drivers/chromedriver/chromedriver"

    @classmethod
    def get_driver(cls):
        # driver 인스턴스가 없으면 생성
        if cls._driver is None:
            service = Service(cls._google_chrome_driver_path)

            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")

            # ChromeDriver를 설정하고 인스턴스 생성
            cls._driver = webdriver.Chrome(service=service, options=chrome_options)
        return cls._driver

    @classmethod
    def quit_driver(cls):
        # driver 인스턴스가 있으면 종료
        if cls._driver is not None:
            cls._driver.quit()
            cls._driver = None  # driver를 종료하고 None으로 설정
