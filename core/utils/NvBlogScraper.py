from core.utils.WebScarper import WebScarper
from core.utils.WebScrpDriverManager import WebScrpDriverManager
from core.exceptions.scraping_exceptions import ErrorHandler
import time
import json
import inspect
from urllib.parse import urlparse, parse_qs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.utils.ElementFinder import ElementFinder
from core.utils.iframe_handlers import switch_to_frame
import logging
from datetime import datetime
from core.utils.loggers import element_find_logger as e_finder_logger


class NvBlogScraper(WebScarper):

    def __init__(self, driver, timeout):
        super().__init__(driver, timeout)

    def go_main_tab(self, tab_name):
        main_tab = self.find_element(
            by=By.XPATH,
            expression=f"//a[contains(text(),'{tab_name}')]",
            element_description="네이버 탭-블로그",
        )
        if not main_tab == None:
            main_tab.click()
        print("대기중")

    def collect_post_links(self, link_css_selector, links_size=100):

        collected_links = list()  # 중복 제거를 위해 set 사용
        scroll_attempt = 0  # 스크롤 시도 횟수
        max_scrolls = int(links_size / 30)  # 최대 스크롤 시도 횟수

        while len(collected_links) < links_size or scroll_attempt < max_scrolls:
            last_height = self.driver.execute_script(
                "return document.body.scrollHeight"
            )

            # 스크롤을 페이지 끝까지 내림
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(1.5)  # 페이지 로딩을 기다리기 위해 지연 시간 추가 (2초 권장)

            # 새 높이를 확인하여 비교
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("페이지 끝에 도달했습니다. 더 이상 로드할 내용이 없습니다.")
                break  # 페이지 끝에 도달하면 루프 탈출

            post_links = self.find_all_element(
                by=By.CSS_SELECTOR,
                expression=link_css_selector,
                element_description="네이버블로그-게시물링크들",
            )

            if post_links == None or post_links.__len__() == 0:
                e_finder_logger.debug("네이버블로그-게시물링크의 css 선택자를 체크필요")
                scraped_links = {
                    "links": [
                        {
                            "error_message": "수집된 링크가 없습니다.",
                            "info": "네이버블로그-게시물링크의 css 선택자를 체크필요",
                        }
                    ]
                }

                return json.dumps(scraped_links, ensure_ascii=False)

            for link in post_links:
                link_info = {"href": link.get_attribute("href"), "title": link.text}

                collected_links.append(link_info)

                if len(collected_links) >= links_size:
                    break  # 목표 수만큼 수집되면 종료

            scroll_attempt += 1  # 스크롤 횟수 증가

        scraped_links = {"links": collected_links}

        return json.dumps(scraped_links, ensure_ascii=False)

    def scrape_blog_post_links(self, element_finder: ElementFinder):
        post_links = None

        post_links = element_finder.find_all_element(
            by=By.CSS_SELECTOR,
            expression=".title_link",
            elements_description="블로그 링크",
        )
        if not post_links == None:
            return post_links
        return post_links

    def scrape_infos_from_blogs(self, link_info_list):
        blogs_infos = list()

        with WebScrpDriverManager.create_driver_manager() as driver_manager:
            self.driver = driver_manager.driver
            elem_finder = ElementFinder(driver_manager.driver, 3)

            for link_info in link_info_list:
                href = link_info["href"]
                title = link_info["title"]

                # #  추후 아래의 post 포함하는 페이지 완전히 고쳐야만 함.
                if href.startswith("https://post.naver.com/"):
                    e_finder_logger.debug(f"https://post.naver.com 도메인은 스크래핑 건너뜁니다. - {href}")
                    continue

                driver_manager.driver.get(href)

                iframe = elem_finder.find_element(
                    By.TAG_NAME,
                    expression="iframe",
                    element_description=f"아이프레임 in {href}",
                )

                if not iframe == None:

                    # 아이프레임 진입
                    driver_manager.driver.switch_to.frame(iframe)

                    infos = self.scrape_blog_infos(
                        element_finder=elem_finder, blog_link=href, link_title=title
                    )

                    driver_manager.driver.switch_to.default_content()

                    blogs_infos.append(infos)

        return blogs_infos

    def scrape_blog_infos(
        self, element_finder: ElementFinder, blog_link, link_title="정의되지않음"
    ):
        infos = {}
        nick = self._scrape_nickname(
            scrape_link=blog_link, element_finder=element_finder
        )

        blog_id = self._scrape_id(scrape_link=blog_link)

        email = self._scrape_email(blog_id=blog_id)

        visitors_count = self._scrpe_visitor_count(
            blog_id=blog_id, element_finder=element_finder
        )

        infos["nickname"] = nick
        infos["blog_id"] = blog_id
        infos["email"] = email
        infos["visitors_count"] = visitors_count
        infos["link"] = blog_link
        infos["blog_post_title"] = link_title

        return infos

    def _scrape_email(self, blog_id):
        if blog_id == None:
            return None
        return f"{blog_id}@naver.com"

    def _scrape_nickname(self, scrape_link, element_finder: ElementFinder):
        nick = None

        element = element_finder.find_element(
            by=By.XPATH,
            expression='//span[@class="nick"]',
            element_description="블로그 닉네임",
        )
        if not element == None:
            nick = element.text

            return nick

        strategies = [
            {"by": By.XPATH, "expression": "//p[@class='nick']"},
            {"by": By.XPATH, "expression": "//strong[@class='nick']"},
            {"by": By.CLASS_NAME, "expression": "span.se_author"},
        ]
        element_by_strategies = element_finder.find_element_in_list(
            finding_strategies=strategies, element_description="닉네임"
        )

        if not element_by_strategies == None:
            return element_by_strategies.text

        return nick

    def _scrape_id(self, scrape_link):
        parsed_url = urlparse(scrape_link)

        if "blog.naver.com" in parsed_url.netloc:

            path_parts = parsed_url.path.split("/")

            if len(path_parts) > 1 and path_parts[1]:
                return path_parts[1]
        return None

    def _scrpe_visitor_count(self, blog_id, element_finder: ElementFinder):
        count = None

        naver_api = f"https://blog.naver.com/NVisitorgp4Ajax.nhn?blogId={blog_id}"
        self.driver.get(naver_api)

        current_date = datetime.now().strftime("%Y%m%d")
        element = element_finder.find_element(
            by=By.ID, expression=current_date, element_description="방문자 수"
        )
        if not element == None:
            count = element_finder.find_element(
                by=By.ID, expression=current_date, element_description="블로그-방문자수"
            ).get_attribute("cnt")
            return int(count)

        return count
