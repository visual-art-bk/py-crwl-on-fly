from flask import Blueprint, request, jsonify

# 블루프린트 생성
main = Blueprint('main', __name__)

# 루트 경로
@main.route('/')
def home():
    return '<h1>Hello bk!</h1>'

