import os
from core import create_app
from dotenv import load_dotenv

load_dotenv()

app = create_app()

# APP_ENV로 호스팅 플랫폼 구분
app_env = os.getenv('APP_ENV', 'heroku')  # 기본값은 'heroku'

# 각 환경에 맞는 포트번호 선택
if app_env == 'gcp':
    port = int(os.getenv('GCP_PORT', 8080))
elif app_env == 'fly':
    port = int(os.getenv('FLY_PORT', 8080))
else:
    port = int(os.getenv('PORT', 5000))
    
if __name__ == "__main__":

    # DYNAMIC PORT
    # - Hero PORT   - 5000, THE DEFAULT
    # - Fly.io PORT - 8080, SEE ./fly.toml CHECK [env] - PORT
    port = int(os.environ.get('PORT', 5000)) 
    app.run(host="0.0.0.0", port=port)
