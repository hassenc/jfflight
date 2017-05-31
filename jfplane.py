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
  start = date
  end = date2
  print date
  print date2.date()
  temp = start
  total = 0
  while temp <= end:
    if (isWorkable(temp) is True):
      total = total + 1
    temp = temp + timedelta(days=1)
  print start.hour
  if ((isWorkable(start) is True) and (start.hour>20)):
    print "yooooooo"
    print start
    total = total - 1
  if ((isWorkable(end) is True) and (start.hour<7)):
    total = total - 1
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
    i = i+1
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
def getbestflights(mylist, options):
  mylist = [x for x in mylist if getDuration(x['depdate'],x['retdate'])>1]
  return nicefy(sorted(mylist, key=lambda k:
    k['contents']['price'] + options["cp_penalty"]*getNbrOfCP(datetime.fromtimestamp(float(k['contents']['outbound']['depDate'])/1000),datetime.fromtimestamp(float(k['contents']['inbound']['depDate'])/1000))
    )[:10])

def nicefy(list):
  nice_list = []
  for flight in list:
    deptime = datetime.fromtimestamp(float(flight['contents']['outbound']['depDate'])/1000)
    rettime = datetime.fromtimestamp(float(flight['contents']['inbound']['depDate'])/1000)
    nice_list.append({
      "price":flight['contents']['price'],
      "depdate": flight['contents']['outbound']['depDate'],
      "retdate": flight['retdate'],
      "deptime": deptime.strftime("%Y-%m-%d %H:%M:%S"),
      "rettime": rettime.strftime("%Y-%m-%d %H:%M:%S"),
      "cp": getNbrOfCP(deptime,rettime),
      "duration": getDuration(flight['depdate'],flight['retdate']),
      "contents": flight['contents']
      })
  return nice_list

def req(options):
  mydates = dates(datetime.strptime(options["last_date"], "%Y-%m-%d").date())
  list_flights = []
  for date in mydates:
    options = {
      "depdate":date["start"],
      "from":options["from"],
      "to":options["to"],
      "direct":"false",
      "range":3,
      "exclude-exact":"false",
      "retdate":date["end"],
    }
    post_response = requests.get(url='http://flights-results.liligo.fr/servlet/flight-cache',headers=headers, params=options)
    items = json.loads(post_response.text)["items"]
    list_flights = list_flights + items
  return list_flights

# print(mydates)
options = {
    "cp_penalty": 90,
    "from":"PAR",
    "to":"MIR",
    "last_date": "2017-06-12"
}
mydates = dates(datetime.strptime(options["last_date"], "%Y-%m-%d").date())
list_flights = req(options)
# getbestflights(json.loads(post_response.text))
bestflights =  getbestflights(list_flights, options)


print "{:<8} {:<25} {:<25} {:<5} {:<5}".format('price','deptime','rettime', 'cp', 'duration')
for flight in bestflights:
    print "{:<8} {:<25} {:<25} {:<5} {:<5}".format(flight['price'],flight['deptime'],flight['rettime'],flight['cp'], flight["duration"])
datetime.now().time()
datetime.now().hour
datetime.strptime(datetime.now(), "%Y-%m-%d")
