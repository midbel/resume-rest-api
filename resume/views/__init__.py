import functools
from collections.abc import Sized
from flask import (
  jsonify,
  request,
  make_response,
  Blueprint,
  current_app,
  Response,
)
from ..repo import NotFoundException, CredentialsException
from ..encoding import jwt

def create_blueprint(name, pkg):
  bp = Blueprint(name, pkg)
  bp.before_request(preflight)
  bp.after_request(postflight)
  return bp

def postflight(r):
  return set_cors_headers(r)

def preflight():
  if request.method != "OPTIONS":
    return None
  r = make_response()
  return set_cors_headers(r)

def set_cors_headers(r):
  r.headers["Access-Control-Allow-Methods"] = 'GET, POST, DELETE, PUT, OPTIONS'
  r.headers["Access-Control-Allow-Origin"] = "*"
  r.headers["Access-Control-Allow-Headers"] = 'Accept, Accept-language, Content-Language, Content-Type, Origin, Authorization'
  r.headers["Access-Control-Expose-Headers"] = 'Authorization'
  return r


def token_required(fn):
  @functools.wraps(fn)
  def wrapper(*args, **kwargs):
    auth = request.headers.get("Authorization", "")
    if not auth or not auth.startswith('Bearer '):
      return '', 401

    try:
      _, token = auth.split(' ')
      payload = jwt.decode_token(token, current_app.config["SECRET_KEY"])
    except jwt.InvalidTokenException as e:
      return str(e), 403
    except Exception as e:
      return '', 401
    else:
      resp = fn(*args, **kwargs)
      if isinstance(resp, Response):
        resp.headers["Authorization"] = f"Bearer {jwt.encode_token(payload)}"
      return resp

  return wrapper

def handle(status_code=200):
  def decorator(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
      nonlocal status_code
      if (request.method == "POST" or request.method == "PUT") and not request.is_json:
        return Response(status=406)

      try:
        ret = fn(*args, **kwargs)
      except NotFoundException as e:
        resp = jsonify(str(e)), 404
        return make_response(resp)
      except CredentialsException as e:
        resp = jsonify(str(e)), 401
        return make_response(resp)
      except Exception as e:
        resp = jsonify(str(e)), 400
        return make_response(resp)

      if isEmpty(ret):
        status_code = 204
        ret = ''

      resp = jsonify(ret), status_code
      return make_response(resp)
    return wrapper
  return decorator

def isEmpty(obj):
  if obj is None:
    return True
  return isinstance(obj, Sized) and len(obj) == 0
