from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time


class IFrameHandler:
    def __init__(self, driver):
        self._driver: webdriver.Chrome = driver

    def check_iframe_presence(self):
        try:
            iframes = self._driver.find_elements(By.TAG_NAME, "iframe")
            return len(iframes) > 0
        except NoSuchElementException:
            return False

    def switch_to_iframe(self, iframe_index=0):
        iframe = self._driver.find_element(By.TAG_NAME, "iframe")
        self._driver.switch_to.frame(iframe)
        print('아이프레임으로 전환되었습니다.')
        
    def switch_to_default_content(self):
        self._driver.switch_to.default_content()
        print("Switched back to default content.")

    def scrape_content_from_iframe(self, iframe_index=0, element_xpath="//body"):
        try:
            self._switch_to_iframe(iframe_index)
            element = WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.XPATH, element_xpath))
            )
            content = element.text
            print(
                f"Scraped content: {content[:100]}..."
            )  # 출력 내용은 100자까지만 미리보기
            return 
        except TimeoutException:
            print("Element not found in the iframe.")
            return ""
        finally:
            self._switch_to_default_content()


# # 예제 코드 실행 부분
# if __name__ == "__main__":
#     # ChromeDriver 경로 지정
#     service = Service(executable_path="/path/to/chromedriver")
#     _driver = webdriver.Chrome(service=service)

#     try:
#         _driver.get("https://example.com")  # 원하는 URL로 변경
#         time.sleep(2)  # 페이지 로딩 대기

#         iframe_handler = IFrameHandler(_driver)

#         # iframe이 있는지 확인
#         has_iframe = iframe_handler.check_iframe_presence()
#         print(f"Is there an iframe on the page? {'Yes' if has_iframe else 'No'}")

#         # iframe이 있으면 첫 번째 iframe에서 스크래핑 실행
#         if has_iframe:
#             content = iframe_handler.scrape_content_from_iframe(
#                 iframe_index=0, element_xpath="//h1"
#             )
#             print("Scraped content from iframe:", content)

#     finally:
#         _driver.quit()
