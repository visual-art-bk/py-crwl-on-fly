from flask import Flask, Blueprint, render_template_string
from core.exceptions.route_exceptions import RouteHandlerError, route_error_handler

app = Flask(__name__)

errors_bp = Blueprint("errors", __name__)


@errors_bp.app_errorhandler(RouteHandlerError)
def _(error):
    return route_error_handler(error)
