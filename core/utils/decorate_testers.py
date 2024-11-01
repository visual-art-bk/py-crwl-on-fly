from functools import wraps
import time

def test_simulate_multiple_requests(request_count=10, delay=0.1):
    """
    데코레이터 함수: 지정된 request_count만큼 함수를 반복 호출하여 테스트를 지원.
    
    Args:
        request_count (int): 함수 호출 반복 횟수. 기본값은 10.
        delay (float): 각 호출 사이의 지연 시간(초). 기본값은 0.1초.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(request_count):
                result = func(*args, **kwargs)
                time.sleep(delay)  # 지연 시간 설정
            return result
        return wrapper
    return decorator
