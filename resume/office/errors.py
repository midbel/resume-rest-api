class NotFoundException(Exception):

  def __init__(self, message):
    self.message = message

  def __str__(self):
    return self.message

class AuthenticationException(Exception):

  def __str__(self):
    return "invalid credentials provided"

class InvalidIntervalException(Exception):

  def __init__(self, start, end):
    self.start = start
    self.end = end

  def __str__(self):
    return f"invalid interval provided: {self.start} > {self.end}"
