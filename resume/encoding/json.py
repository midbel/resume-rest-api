import datetime
from flask.json import JSONEncoder

class ResumeEncoder(JSONEncoder):

  def default(self, obj):
    if isinstance(obj, datetime.date):
      return obj.isoformat()
    return super().default(obj)
