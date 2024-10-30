import traceback
from flask import render_template_string
from selenium.common.exceptions import NoSuchElementException


class RouteHandlerError(Exception):
    "라우트 핸들러 예외처리. 웹 페이지에 표시됨."
    pass


def route_error_handler(error):
    err_msg = traceback.format_exc()
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Custom Error</title>
    </head>
    <body>
        <h1>{error}</h1>
        <pre>{err_msg}</pre>
    </body>
    </html>
    """.format(
        error=error, err_msg=err_msg
    )
    return render_template_string(html_content), 500


class NoSuchElementError(NoSuchElementException):
    def __init__(
        self, message="XPATH, CSS Selector에 일치하는 HTML 엘리멘트를 찾을 수 없습니다."
    ):
        print("NoSuchElementException: 요소를 찾지 못했습니다.")
        super().__init__(message)
