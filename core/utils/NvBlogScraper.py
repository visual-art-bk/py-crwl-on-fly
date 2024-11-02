from core.utils.WebScarper import WebScarper


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

    def collect_post_links(self, links_size=10):
        last_height = self._driver.execute_script("return document.body.scrollHeight")
        collected_links = set()

        while len(collected_links) < links_size:
            # 스크롤을 아래로 내림
            self._driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )

            # 새롭게 로드된 링크 수집

            post_links = self._find_elements_by_css(".titlㅐㅐㅐe_link", 0.5)

            for link in post_links:
                collected_links.add(link.get_attribute("href"))

                # 스크롤 높이 업데이트
                new_height = self._driver.execute_script(
                    "return document.body.scrollHeight"
                )
                if new_height == last_height:
                    break  # 더 이상 새로운 콘텐츠가 없을 때 탈출
                last_height = new_height

        print(f"수집된 링크 수: {len(collected_links)}")
        # for link in collected_links:
        #     print(link)

    def test_render_html(self):
        return "<h1>대기중</h1>"
