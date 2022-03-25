import datetime
import jwt

class InvalidTokenException(Exception):

  def __str__(self):
    return "invalid token provided"

token_ttl = 86400

def encode_token(payload, secret="", issuer="resume", ttl=token_ttl, alg="HS256"):
  data = {
    'iat': datetime.datetime.now(),
    'exp': datetime.datetime.now() + datetime.timedelta(seconds=ttl),
    'iss': issuer,
  }
  payload = {**payload, **data}
  return jwt.encode(payload, secret, algorithm=alg)

def decode_token(token, secret="", issuer="", ttl=token_ttl, alg="HS256"):
  try:
    return jwt.decode(token, secret, algorithms=alg)
  except Exception as e:
    raise InvalidTokenException()
