import os
import glob
from datetime import datetime
import logging
from dotenv import load_dotenv

# 로컬 환경에서 .env 파일 로드
load_dotenv()

# 환경 변수에서 로그 경로 읽기 (기본값: /app/logs)
log_path = os.getenv("LOG_PATH", "/app/logs")

now = datetime.now()
formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")

# Logger 생성
element_find_logger = logging.getLogger("element_finder")
element_find_logger.setLevel(logging.DEBUG)  # 로그 레벨 설정

# 파일 핸들러 설정
file_handler = logging.FileHandler(f"{log_path}/element_finder_{formatted_now}.log")
file_handler.setLevel(logging.DEBUG)

# 콘솔 핸들러 설정
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# 핸들러에 포맷터 설정
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 핸들러 추가
element_find_logger.addHandler(file_handler)
element_find_logger.addHandler(console_handler)

# 로그 파일 디렉토리와 파일명 패턴 지정
log_file_pattern = os.path.join(log_path, "element_finder_*.log")


# 로그 파일 갯수를 10개로 제한하는 함수
def limit_log_files(directory: str, pattern: str, max_files: int = 10):
    # 로그 파일 목록을 최신 순으로 정렬
    log_files = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)

    # 파일이 max_files를 초과하는 경우 삭제
    if len(log_files) > max_files:
        for file_path in log_files[max_files:]:
            os.remove(file_path)
            element_find_logger.info(f"Old log file deleted: {file_path}")


# 로그 파일 수 제한 함수 호출
limit_log_files(log_path, log_file_pattern)
