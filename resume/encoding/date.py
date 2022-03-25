from dateutil.parser import *

def parse_date(dt):
  dt = isoparse(dt)
  return dt.date()
