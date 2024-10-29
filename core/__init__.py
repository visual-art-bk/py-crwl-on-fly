from flask import Flask


def create_app():
    app = Flask(__name__)

    # 라우팅 모듈을 import하고 등록
    from core.blueprints.bp_routes import main
    from core.blueprints.bp_exceptions import errors_bp

    app.register_blueprint(main)
    app.register_blueprint(errors_bp)

    return app
