from core.utils.WebScarper import WebScarper
import time
import json
import inspect

class NvBlogScraper(WebScarper):
    _iframe_hadler = None
    _err_msg = None

    def go_main_tab(self, tab_name):
        has_frame = self.check_iframe_presence()
        xpath = self.make_xpath(tab_name)

        main_tap = self.find_element_by_xpath(xpath)
        if main_tap:
            if has_frame:
                print("아이프레임 존재합니다. 아이프레임 전환을 고려해보세요.")
            else:
                print("아이프레임이 존재하지않습니다.")

        main_tap.click()

    def collect_post_links(self, links_size=100):
        collected_links = set()  # 중복 제거를 위해 set 사용
        scroll_attempt = 0  # 스크롤 시도 횟수
        max_scrolls = int(links_size / 30)  # 최대 스크롤 시도 횟수

        while len(collected_links) < links_size and scroll_attempt < max_scrolls:
            last_height = self._driver.execute_script(
                "return document.body.scrollHeight"
            )

            # 스크롤을 페이지 끝까지 내림
            self._driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(1.5)  # 페이지 로딩을 기다리기 위해 지연 시간 추가 (2초 권장)

            # 새 높이를 확인하여 비교
            new_height = self._driver.execute_script(
                "return document.body.scrollHeight"
            )
            if new_height == last_height:
                print("페이지 끝에 도달했습니다. 더 이상 로드할 내용이 없습니다.")
                break  # 페이지 끝에 도달하면 루프 탈출

            # 링크 수집
            post_links = self._find_elements_by_css(".title_link")
            for link in post_links:
                collected_links.add(link.get_attribute("href"))
                if len(collected_links) >= links_size:
                    break  # 목표 수만큼 수집되면 종료

            scroll_attempt += 1  # 스크롤 횟수 증가

        print(f"수집된 링크 수: {len(collected_links)}")
        result = {"links": list(collected_links)}
        return json.dumps(result, ensure_ascii=False)
    
    def scrape_blog_infos(self):
        current_function = inspect.currentframe().f_code.co_name
        
        has_iframe = self.check_iframe_presence()
        
        if has_iframe:
            self.switch_to_iframe()
            print(f"아이프레임 전환 {current_function}")
            
            self._scrape_nickname()
            
            self.switch_to_default_content()
            
    def _scrape_nickname(self):
        try:
        
            nick = self.find_element_by_xpath('//span[@class="nick"]').text
            print(f"닉네임 - {nick}")
        except:
            nick = "닉네임-결과없음"
            print(f"닉네임 - {nick}")
            
        return nick
            
    def test_render_html(self):
        return "<h1>대기중</h1>"
