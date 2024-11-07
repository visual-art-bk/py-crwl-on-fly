from core.utils import WebScrpDriverManager
from core.utils.NvBlogScraper import NvBlogScraper
from core.exceptions.scraping_exceptions import ErrorHandler
import time
from flask import jsonify


def handle_scraping_blog_infos(manager: WebScrpDriverManager, blog_links):

    # url = "https://blog.naver.com/gogh_jing/223642226777"

    try:
        nv_blg_scrper = NvBlogScraper(manager.driver, timeout=10)

        # nv_blg_scrper.open_browser(url)
        blog_infos = nv_blg_scrper.scrape_infos_from_blogs(blog_links)
        # infos = nv_blg_scrper.scrape_blog_infos()
        return jsonify(blog_infos)
    except Exception as e:
        return ErrorHandler.generate_error_page(e)
