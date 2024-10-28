from flask import Blueprint, request, jsonify
from core.selenium_utils import WebDriverSingleton

# 블루프린트 생성
main = Blueprint('main', __name__)

# 루트 경로
@main.route('/')
def home():
    driver = WebDriverSingleton.get_driver()  # 싱글턴 driver 인스턴스 가져오기
    driver.get("https://google.com")
    data = driver.title  # 예시로 페이지 제목 가져오기
  
    return f'<h1>{data}</h1>'

