from selenium import webdriver
import requests
from urllib.parse import quote, urlparse, parse_qs, urlunparse, urlencode
import json

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
