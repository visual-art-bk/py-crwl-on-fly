from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.DEBUG,  # 로그 레벨 설정 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        # logging.StreamHandler(),  # 콘솔에 로그 출력
        logging.FileHandler("__logs__/iframe_switch.log"),  # 파일에 로그 출력
    ],
)

logger = logging.getLogger(__name__)


class IFrameHandler:
    def __init__(self, driver: webdriver.Chrome):
        self._driver: webdriver.Chrome = driver
        self._iframe = None

    def check_iframe_presence(self):
        try:
            iframes = self._driver.find_elements(By.TAG_NAME, "iframe")
            for ifrm in iframes:
                if self._driver.find_elements(By.TAG_NAME, "body"):
                    self._iframe = ifrm
                    
            return self._iframe != None
        except NoSuchElementException:
            return False
       
    def switch_to_iframe(self):
        try:
            if not self._iframe:
                raise ValueError("전환될 아이프레임이 존재하지 않습니다.")

            # 아이프레임 전환 시도
            self._driver.switch_to.frame(self._iframe)
            logger.info("아이프레임으로 전환되었습니다.")

        except ValueError as e:
            # 아이프레임이 없을 경우의 에러 로그 기록
            logger.error(f"에러: {e}")

        except Exception as e:
            # 일반적인 예외 처리 추가 (예: WebDriver의 예외 처리)
            logger.exception(f"예상치 못한 오류 발생: {e}")

        finally:
            # 로그 출력 또는 기타 후속 작업을 여기에 추가 가능
            logger.debug("아이프레임 전환 시도 완료.")

    def switch_to_default_content(self):
        try:
            if not self._iframe:
                raise ValueError("복귀할 아이프레임이 존재하지 않습니다.")

            # 아이프레임 전환 시도
            self._driver.switch_to.default_content()
            logger.info("아이프레임을 나왔습니다.")

        except ValueError as e:
            # 아이프레임이 없을 경우의 에러 로그 기록
            logger.error(f"에러: {e}")

        except Exception as e:
            # 일반적인 예외 처리 추가 (예: WebDriver의 예외 처리)
            logger.exception(f"예상치 못한 오류 발생: {e}")

        finally:
            # 로그 출력 또는 기타 후속 작업을 여기에 추가 가능
            logger.debug("아이프레임 복귀 시도 완료.")
