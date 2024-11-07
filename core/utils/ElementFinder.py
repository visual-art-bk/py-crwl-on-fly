from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
import logging
from datetime import datetime
from typing import List, Dict, Union, TypedDict
from core.utils.loggers import element_find_logger as ef_logger


def handle_exceptions(func):
    """공통 예외 처리 함수"""

    def wrapper(*args, **kwargs):
        element_description = kwargs.get("element_description", "정의되지않은-엘레멘트")
        expression = kwargs.get("expression", "정의되지않음")
        
        try:
            return func(*args, **kwargs)
        except TimeoutException:
            ef_logger.exception(
                f"{element_description} 요소를 찾는 데 시간이 초과되었습니다. 표현식 {expression}"
            )
        except NoSuchElementException:
            ef_logger.exception(
                f"{element_description} 요소를 찾을 수 없습니다. 표현식 {expression}"
            )
        except Exception as e:
            ef_logger.exception(
                f"{element_description} 요소 검색 중 예기치 않은 오류 발생. 표현식 {expression}: {e}"
            )
        finally:
            ef_logger.debug(msg=f"{element_description} 검색 시도 완료.")
        return None  # 예외 발생 시 None 반환

    return wrapper


class FindingStrategy(TypedDict):
    by: By
    expression: str


class ElementFinder:
    def __init__(self, driver: webdriver.Chrome, timeout=10):
        self.driver = driver
        self.timeout = timeout

    @handle_exceptions
    def find_element(
        self, by, expression="정의되지않음", element_description="정의되지않은-엘레멘트"
    ):
        """공통 예외 처리를 통해 요소를 찾는 함수"""
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((by, expression))
        )
        ef_logger.debug(msg=f"{element_description} 요소를 성공적으로 찾았습니다.")
        return element

    @handle_exceptions
    def find_all_element(
        self,
        by,
        expression="정의되지않음",
        element_description="multiple element정의되지않은-엘레멘트들",
    ):
        elements = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_all_elements_located((by, expression))
        )
        ef_logger.debug(msg=f"{element_description} 요소를 성공적으로 찾았습니다.")
        return elements

    @handle_exceptions
    def find_element_in_list(
        self,
        finding_strategies: List[FindingStrategy],
        element_description="element",
    ):
        """

        finding_strategies는 [{by: By.*, expression: str}] 의 리스트

        """
        for strategy in finding_strategies:
            elem = self.find_element(
                by=strategy["by"],
                expression=strategy["expression"],
                element_description=element_description,
            )
            if not elem == None:
                ef_logger.debug(msg=f"{elem.tag_name}에서 닉네임 발견.")
                return elem
