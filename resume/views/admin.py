from flask import Blueprint

bp = Blueprint("admin", __name__)

@bp.route("/")
def index():
    pass
