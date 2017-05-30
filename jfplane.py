#!/usr/bin/python
from datetime import datetime
from datetime import timedelta


print (datetime.now()).weekday()
print (datetime.now() + timedelta(days=2)).weekday()

HOLIDAYS = ["2017-07-14"]

def isWeekend(date):
  if (date.weekday() == 5) or (date.weekday() == 6):
    return True
  else:
    return False

def isHoliday(date):
  for holiday in HOLIDAYS:
    if date.date() == datetime.strptime(holiday, "%Y-%m-%d").date():
      return True
  return False

def isWorkable(date):
  if (isHoliday(date) or isWeekend(date)):
    return False
  else:
    return True

def getMaxSpan(date):
  span = 0
  nextDay = date
  while isWorkable(nextDay) is False:
    span = span + 1
    nextDay = nextDay + timedelta(days=1)
  return span

def getEndDates(date):
  endDates = []
  endDates.append((date + timedelta(days=2)).date())
  endDates.append((date + timedelta(days=3)).date())
  maxSpan = getMaxSpan(date)
  if maxSpan > 3:
    print "maxSpan superior"
    print maxSpan
    endDates.append((date + timedelta(days=maxSpan)).date())
  print "endDates"
  print endDates
  return endDates

def dates(endDate):
  result = []
  date = {"start":datetime.now(), "end":datetime.now()}
  today = datetime.now()
  date = today
  i = 0
  while ((date.date() != endDate) and (i<3)):
    i = i+1
    print type(date.date())
    for endDate in getEndDates(date):
      result.append({"start":date.date(), "end":endDate})
    date = date + timedelta(days=1)
  return result


print dates(datetime.strptime("2017-07-15", "%Y-%m-%d").date())
