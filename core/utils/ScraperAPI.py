import requests
import time
import json
import os
from flask import Blueprint, request, url_for
from dotenv import load_dotenv
from core.utils.WebScrpDriverManager import WebScrpDriverManager
from core.route_handlers.home import home_handler
from core.route_handlers.scr_nv_blog import (
    NvBlogScraper,
    render_tmp_html,
    handler_search_naver_blog,
)
from core.route_handlers.scraping import handle_scraping_blog_infos
from core.exceptions.route_exceptions import RouteHandlerError
from core.utils.testers import tester_request_searched_links

# .env 파일 로드 (로컬 개발 환경에서만 필요)
load_dotenv()

# BASE_URL 환경 변수 읽기
base_url = os.getenv("BASE_URL", "https://rchr-micro-ws-7090524482ab.herokuapp.com")

# main = Blueprint("main", __name__)


class ScraperAPI:
    @staticmethod
    def index():
        kmong_data_url = "https://rchr-lab.store/data"
        html_content = (
            f"<h1>안녕하세요 고객님. 크몽의 <a href='{kmong_data_url}'>웹 데이터 수집</a>를 이동해서 테스트 해보세요!</h1>"
        )

        return html_content