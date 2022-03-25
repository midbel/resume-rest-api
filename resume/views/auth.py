from flask import request, current_app
from . import handle, create_blueprint
from .. import office
from .. import repo
from ..encoding import jwt

bp = create_blueprint("auth", __name__)

@bp.route("/signin", methods=["POST"])
@handle()
def authenticate():
  p = office.authenticate(
    repo.SaRepository(),
    request.json["email"],
    request.json["pass"],
  )
  return {
    "profile": p,
    "token": jwt.encode_token(
      payload={"email": p.email, "uid": p.id},
      secret=current_app.config["SECRET_KEY"],
    ),
  }
