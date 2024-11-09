import requests
import time
from core.utils.loggers import element_find_logger
from flask import Blueprint, request
from core.utils.WebScrpDriverManager import WebScrpDriverManager
from core.route_handlers.home import home_handler
from core.route_handlers.scr_nv_blog import (
    NvBlogScraper,
    render_tmp_html,
    handler_search_naver_blog,
)
from core.route_handlers.scraping import handle_scraping_blog_infos
from core.exceptions.route_exceptions import RouteHandlerError
from core.utils.testers import request_tester, tester_request_searched_links
import json
import os
from dotenv import load_dotenv

# .env 파일 로드 (로컬 개발 환경에서만 필요)
load_dotenv()

# BASE_URL 환경 변수 읽기 (설정이 없으면 기본값으로 로컬 호스트 URL 사용)
base_url = os.getenv("BASE_URL", "https://py-crwl-on-hero-6a1a5129f69c.herokuapp.com")


main = Blueprint("main", __name__)


@main.route("/")
def home():
    return home_handler()


@main.route("/scr/nv-blog", methods=["GET"])
def _():

    try:
        # with문이 종료되면 driver.quit() 실행되므로, 추가 콜 필요없음
        search_keyword = request.args.get("search_keyword")
        keywords_size = request.args.get("keywords_size")
        with WebScrpDriverManager.create_driver_manager() as driver_manager:
            return handler_search_naver_blog(
                driver_manager,
                search_keyword=search_keyword,
                links_size=int(keywords_size),
            )

    except Exception as e:
        raise RouteHandlerError(e)


@main.route("/scr/nv-blog/scraping")
def blog_scraping():

    try:
        search_keyword = request.args.get("search_keyword", type=str, default='가을%20러닝')
        keywords_size = request.args.get("keywords_size", type=int, default=10)
        start_index = request.args.get("start", type=int, default=0)
        end_index = request.args.get("end", type=int, default=5)
        
        max_retries = 5  # 최대 재시도 횟수
        retry_count = 0  # 현재 재시도 횟수
        delay_between_retries = 1  # 각 재시도 사이의 대기 시간 (초)
        
        # 지속적으로 JSON 응답이 올 때까지 요청을 반복
        while retry_count < max_retries:
            try:
                searched_blog_post_links = tester_request_searched_links(
                    f"{base_url}/scr/nv-blog?search_keyword={search_keyword}&keywords_size={keywords_size}"
                )

                # JSON 파싱 시도
                links = json.loads(searched_blog_post_links.text)["links"]
                
                # 파싱 성공 시 루프 탈출
                break

            except json.JSONDecodeError as e:
                print(f"JSONDecodeError 발생: {e} - 재시도 중 ({retry_count + 1}/{max_retries})")
                retry_count += 1
                time.sleep(delay_between_retries)  # 재시도 전 대기 시간

            except Exception as e:
                raise RouteHandlerError(f"예상치 못한 오류: {e}")

        # 최대 재시도 횟수 초과 시 예외 발생
        if retry_count == max_retries:
            raise RouteHandlerError("JSON 데이터를 파싱할 수 없습니다. 최대 재시도 횟수를 초과했습니다.")

        # 링크 슬라이싱 및 스크래핑 시작
        links_len = len(links)
        if start_index >= links_len:
            start_index = 0
        if end_index >= links_len:
            end_index = links_len

        links_to_scrape = links[start_index:end_index]

        # with문이 종료되면 driver.quit() 실행되므로, 추가 콜 필요없음
        with WebScrpDriverManager.create_driver_manager() as driver_manager:
            return handle_scraping_blog_infos(driver_manager, links_to_scrape)

    except Exception as e:
        raise RouteHandlerError(e)
@main.route("/test")
def test():
    return '<h1>테스트 페이지입니다.</h1>'