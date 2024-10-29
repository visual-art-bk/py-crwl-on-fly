from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from config import GOOGLE_CHROME_DRIVER_PATH

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

    def __exit__(self, exc_type, exc_val, exc_tb):
        # with 블록 종료 시 자동으로 driver.quit() 호출
        self.driver.quit()
        
        if self.driver.service.process is None:
            print("driver.quit() 호출됨: ChromeDriver가 종료되었습니다.")
        else:
            print("driver.quit() 호출 실패: ChromeDriver가 여전히 실행 중입니다.")