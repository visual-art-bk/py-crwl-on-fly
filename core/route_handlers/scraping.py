from core.utils import WebScrpDriverManager
from core.utils.NvBlogScraper import NvBlogScraper
from core.exceptions.scraping_exceptions import ErrorHandler
import time


def handle_scraping_blog_infos(manager: WebScrpDriverManager):

    url = "https://blog.naver.com/gogh_jing/223642226777"
    try:
        nv_blg_scrper = NvBlogScraper(manager.driver)

        nv_blg_scrper.open_browser(url)
        nv_blg_scrper.scrape_blog_infos()

        
        time.sleep(3)
        
        return "<h1>준비중</h1>"
    except Exception as e:
        return ErrorHandler.generate_error_page(e)
