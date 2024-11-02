from core.utils.NvBlogScraper import NvBlogScraper
from core.utils import WebScrpDriverManager
from core.exceptions.scraping_exceptions import ErrorHandler

def render_tmp_html():
    return "<h1>네이버 블로그 스크래핑 시작123<h1>"


def handler_search_naver_blog(manager: WebScrpDriverManager):
    url = "https://www.naver.com"
    try:

        nv_blg_scrper = NvBlogScraper(manager.driver)
        nv_blg_scrper.open_browser(url)
        nv_blg_scrper.search_keyword("재테크 투자", "input[name='query']")
        nv_blg_scrper.go_main_tab(tab_name="블로그")
        nv_blg_scrper.collect_post_links(2)
        
        return nv_blg_scrper.test_render_html()

    except Exception as e:
        return ErrorHandler.generate_error_page(e)