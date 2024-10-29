from flask import Flask

def create_app():
    app = Flask(__name__)

    # 라우팅 모듈을 import하고 등록
    from core.routes.routes import main
    app.register_blueprint(main)

    return app