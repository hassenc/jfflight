"use strict";

var moment = require("moment");
var request = require("request");
var path = require("path"),
  config = require(path.resolve("./config/config"));

/**
 * Run Script
 */
exports.runScript = function (req, res) {
  var options = {
      "nbr_results": 20,
      "cp_penalty": 0,
      "from":"PAR",
      "to":"GOA",
      "last_date": "2017-08-31"
  }
  var dates = getQueryDates("2017-08-31")
	var result = [];
  var completed_requests = 0;
  for (var i = 0; i < dates.length; i++) {
    var params = {
        "depdate":dates[i]["start"],
        "from":"PAR",
        // "from":options["from"],
        "to":"MIR",
        // "to":options["to"],
        "direct":"false",
        "range":3,
        "exclude-exact":"false",
        "retdate":dates[i]["end"],
      }
    request.get({url: "http://flights-results.liligo.fr/servlet/flight-cache", 
               qs: params},
      function(error, response, body){
        if (error) {
          console.log("Error")
          console.log(error)
          return res.status(404).send({
              data: error,
              message: "Error"
            });
        }
        if (body) {
          var newResults = JSON.parse(body)["items"];
          result = result.concat(newResults)
          console.log(newResults.length)
          completed_requests ++;
          if (completed_requests == dates.length) {
            return res.status(200).send({
              data: getbestflights(result,options) ,
              message: "Script running"
            });
          }
      	}
      });
  };


  // return res.status(200).send({
  //    data: dates,
  //    message: "Script running"
  //  });
};



var HOLIDAYS = ["2017-07-14","2017-08-15","2017-11-01","2017-11-11","2017-12-25","2018-01-01"];

var isWeekend = function(date) {	
  if ((date.day() == 6) || (date.day() == 7)) {
    return true
  }
  else {
    return false
  }
}

var isHoliday = function(date) {
  for (var i = 0; i < HOLIDAYS.length; i++) {
    if (date.format("YYYY-MM-DD") == HOLIDAYS[i]) {
      return true
    }
  }
  return false
}

var isWorkable = function(date) {
  if (isHoliday(date) || isWeekend(date)){
    return false
  } else {
    return true
  }
}

var getMaxSpan = function(date) {
  var span = 0
  var nextDay = date
  while (isWorkable(nextDay) == false) {
    span = span + 1
    var nextDay = nextDay + timedelta(days=1)
  	return span
  }
}


var getNbrOfCP = function(date,date2) {
  var start = date;
  var end = date2;
  console.log(start)
  var temp = start.clone();
  var total = 0;
  while (temp <= end) {
    if (isWorkable(temp) == true) {
      total = total + 1;
    }
    temp = temp.add(1,"days");
  }
  if ((isWorkable(start) == true) && (start.hour()>20)) {

    total = total - 1
  }
  if ((isWorkable(end) == true) && (start.hour()<7)) {
    
    total = total - 1
  }
  return total
}

var getKPI = function(flight, options) {
    return flight['contents']['price'] + options["cp_penalty"]*flight.cp
}

var getbestflights = function(mylist, options) {
  //TODO compute parseInt here/ compute getNbr of CP && then pass it for kpi
  var mylist = mylist.filter(function(el) {
    return getDuration(el.depdate,el.retdate) > 1;
  });
  for (var i = 0; i < mylist.length; i++) {
    mylist[i].cp = getNbrOfCP(moment(parseInt(mylist[i]['contents']['outbound']['depDate'])),moment(parseInt(mylist[i]['contents']['inbound']['depDate'])))
    mylist[i].kpi = getKPI(mylist[i],options)
    mylist[i].duration = getDuration(mylist[i]['depdate'],mylist[i]['retdate'])
  };
  console.log("filter")
  console.log(mylist.length)
  mylist.sort(function(a,b) {
    return a.kpi - b.kpi;
  })
  console.log(mylist.length)
  return mylist.slice(0,options["nbr_results"]);
  // return nicefy(sorted(mylist, key=lambda k:
  // k['contents']['price'] + options["cp_penalty"]*getNbrOfCP(datetime.fromtimestamp(float(k['contents']['outbound']['depDate'])/1000),datetime.fromtimestamp(float(k['contents']['inbound']['depDate'])/1000))
  // )[:options["nbr_results"]])
}

var getDuration = function(date,date2) {
  var start = moment(date)
  var end = moment(date2)
  return end.diff(start, 'days')
}

var getEndDates = function(date) {
  // var endDates = []
  // endDates.append((date + timedelta(days=2)).date())
  // endDates.append((date + timedelta(days=0)).date())
  // maxSpan = getMaxSpan(date)
  // if maxSpan > 3:
  //   print "maxSpan superior"
  //   print maxSpan
  //   endDates.append((date + timedelta(days=maxSpan)).date())
  // print "endDates"
  // return endDates
  return [date.clone()]
}



var getQueryDates = function(lastDate) {
  var result = []
  // var date = {"start":datetime.now(), "end":datetime.now()}
  var today = moment().add(2, "days");
  var date = today;
  var i = 0;
  while ((date < moment(lastDate)) && (i<400)) {
  	i = i+1;
    if (date) {
    // if ((isWorkable(date) is false) or (isWorkable(date + timedelta(days=1)) is false)):
      var endDates = getEndDates(date);
      for (var i = 0; i < endDates.length; i++) {
        result.push({"start":date.format("YYYY-MM-DD"), "end":endDates[i].format("YYYY-MM-DD")})
      };
    }
    date = date.add(6, "days");
  }
  return result
}
