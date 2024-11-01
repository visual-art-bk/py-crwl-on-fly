from selenium import webdriver


def request_tester(driver: webdriver.Chrome, url="https://www.google.com"):
    driver.get(url)
    driver.quit()
    return "<h1>test 성공</h1>"
