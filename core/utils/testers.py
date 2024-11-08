from functools import wraps
from selenium import webdriver
import requests
from urllib.parse import quote, urlparse, parse_qs, urlunparse, urlencode
import time

def request_tester(driver: webdriver.Chrome, url="https://www.google.com"):
    driver.get(url)
    driver.quit()
    return "<h1>test 성공</h1>"


def tester_request_searched_links(url):
    # # URL 파싱
    # # URL 파싱
    # parsed_url = urlparse(url)

    # # 쿼리 파라미터 파싱 및 인코딩
    # query_params = parse_qs(parsed_url.query)
    # encoded_query_params = {key: quote(value[0]) for key, value in query_params.items()}

    # # 인코딩된 쿼리 문자열 생성
    # encoded_query = urlencode(encoded_query_params)

    # # 인코딩된 URL 재구성
    # encoded_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path,
    #                         parsed_url.params, encoded_query, parsed_url.fragment))

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Failed to fetch blog links")

    return response

def test_simulate_multiple_requests(request_count=10, delay=0.1):
    """
    데코레이터 함수: 지정된 request_count만큼 함수를 반복 호출하여 테스트를 지원.
    
    Args:
        request_count (int): 함수 호출 반복 횟수. 기본값은 10.
        delay (float): 각 호출 사이의 지연 시간(초). 기본값은 0.1초.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(request_count):
                result = func(*args, **kwargs)
                time.sleep(delay)  # 지연 시간 설정
            return result
        return wrapper
    return decorator
