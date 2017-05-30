#!/usr/bin/python
from datetime import datetime
from datetime import timedelta
print (datetime.now()).weekday()
print (datetime.now() + timedelta(days=2)).weekday()
#Add 1 day
print (datetime.now() + timedelta(days=1)).date()
print (datetime.now() + timedelta(days=2) - timedelta(days=1)).date()
print (datetime.now() + timedelta(days=1)).date() == (datetime.now() + timedelta(days=2) - timedelta(days=1)).date()

import time

now = time.strftime("%c")
print now
time.strftime("%w")
time +



def dates(endDate):
  result = []
  date = {"start":datetime.now(), "end":datetime.now()}
  today = datetime.now()
  date = today
  while (date.date() != endDate):
    date = date + timedelta(days=1)
    result.append(date)
  return result


dates("2017-06-01")
