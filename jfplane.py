#!/usr/bin/python
from datetime import datetime
from datetime import timedelta
import requests
import json

HOLIDAYS = ["2017-07-14","2017-08-15","2017-11-01","2017-11-11","2017-12-25","2018-01-01"]

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


def getNbrOfCP(date,date2):
  start = datetime.strptime(date, "%Y-%m-%d")
  end = datetime.strptime(date2, "%Y-%m-%d")
  temp = start
  total = 0
  while temp <= end:
    if (isWorkable(temp) is True):
      total = total + 1
    temp = temp + timedelta(days=1)
  return total

def getDuration(date,date2):
  start = datetime.strptime(date, "%Y-%m-%d")
  end = datetime.strptime(date2, "%Y-%m-%d")
  return (end-start).days

def getEndDates(date):
  endDates = []
  # endDates.append((date + timedelta(days=2)).date())
  endDates.append((date + timedelta(days=0)).date())
  # maxSpan = getMaxSpan(date)
  # if maxSpan > 3:
  #   print "maxSpan superior"
  #   print maxSpan
  #   endDates.append((date + timedelta(days=maxSpan)).date())
  # print "endDates"
  return endDates

def dates(lastDate):
  result = []
  date = {"start":datetime.now(), "end":datetime.now()}
  today = datetime.now() + timedelta(days=2)
  date = today
  i = 0
  while ((date.date() < lastDate) and (i<400)):
    i = i+1;
    print date
    print date.weekday()
    print i
    if (date):
    # if ((isWorkable(date) is False) or (isWorkable(date + timedelta(days=1)) is False)):
      for endDate in getEndDates(date):
        result.append({"start":date.date(), "end":endDate})
    date = date + timedelta(days=6)
  return result






headers = {
    "Host": "flights-results.liligo.fr",
    "Connection": "keep-alive",
    # "Content-Length": "1157",
    # "Origin": "https://www.voyages-sncf.com",
    # "X-VSD-SMART-GUY-GUARD": "SdulvO|rqT3639534:T4QQRZD\\",
    # "X-VSD-LOCALE": "fr_FR",
    "Content-Type": "text/json;charset=ISO-8859-1"
}

        # {
        #     "contents": {
        #         "roundTrip": true,
        #         "providerCode": "OPO",
        #         "arrCityName": "Monastir",
        #         "inbound": {
        #             "supplierName": "Tunisair",
        #             "duration": 150,
        #             "date": "2017-06-15",
        #             "flightCode": "TU440",
        #             "arrDate": 1497536400000,
        #             "arrStation": "ORY",
        #             "supplier": "TU",
        #             "stops": 0,
        #             "depStation": "MIR",
        #             "depDate": 1497527400000
        #         },
        #         "depCityTimeZone": "Europe/Paris",
        #         "priceCurrency": "EUR",
        #         "arrCityTimeZone": "Africa/Tunis",
        #         "provider": "Opodo",
        #         "price": 204,
        #         "outbound": {
        #             "duration": 155,
        #             "supplierName": "Tunisair",
        #             "date": "2017-06-08",
        #             "arrDate": 1496943900000,
        #             "arrStation": "MIR",
        #             "flightCode": "TU441",
        #             "supplier": "TU",
        #             "stops": 0,
        #             "depStation": "ORY",
        #             "depDate": 1496934600000
        #         },
        #         "depCityName": "Paris",
        #         "id": "9146585022626541459",
        #         "providerSite": "www.opodo.fr/",
        #         "timestamp": "2017-05-30 17:17:48.0"
        #     },
        #     "depdate": "2017-06-08",
        #     "retdate": "2017-06-15"
        # }
def getbestflights(mylist):
  mylist = [x for x in mylist if getDuration(x['depdate'],x['retdate'])>1]
  return nicefy(sorted(mylist, key=lambda k: 
    k['contents']['price'] + 90*getNbrOfCP(k['depdate'],k['retdate'])
    )[:10])

def nicefy(list):
  nice_list = []
  for flight in list:
    nice_list.append({
      "price":flight['contents']['price'],
      "depdate": flight['depdate'],
      "retdate": flight['retdate'],
      "pc": getNbrOfCP(flight['depdate'],flight['retdate'])
      })
  return nice_list

def req(mydates):
  list_flights = []
  for date in mydates:
    print date["start"]
    print date["end"]
    options = {
      "depdate":date["start"],
      "from":"PAR",
      "to":"MIR",
      "direct":"false",
      "range":3,
      "exclude-exact":"false",
      "retdate":date["end"],
    }
    post_response = requests.get(url='http://flights-results.liligo.fr/servlet/flight-cache',headers=headers, params=options)
    print json.loads(post_response.text)
    items = json.loads(post_response.text)["items"]
    print len(items)
    list_flights = list_flights + items
  return list_flights

mydates = dates(datetime.strptime("2017-07-15", "%Y-%m-%d").date())
print(mydates)
list_flights = req(mydates)
# getbestflights(json.loads(post_response.text))
print getbestflights(list_flights)
