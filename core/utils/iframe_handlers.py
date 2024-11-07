from functools import wraps

def switch_to_frame(frame_locator):
    """프레임 전환을 자동으로 처리하는 데코레이터"""
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                # 프레임으로 전환
                self.driver.switch_to.frame(frame_locator)
                result = func(self, *args, **kwargs)
            finally:
                # 기본 콘텐츠로 복귀
                self.driver.switch_to.default_content()
            return result
        return wrapper
    return decorator