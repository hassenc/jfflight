'use strict';

var request = require("request");
var path = require('path'),
  config = require(path.resolve('./config/config'));

/**
 * Run Script
 */
exports.runScript = function (req, res) {
	var result;
  var date = {
  start:"2017-08-31",
  end:"2017-08-31"
  }
  var params = {
      "depdate":date["start"],
      "from":"PAR",
      // "from":options["from"],
      "to":"MIR",
      // "to":options["to"],
      "direct":"false",
      "range":3,
      "exclude-exact":"false",
      "retdate":date["end"],
    }
  request.get({url: "http://flights-results.liligo.fr/servlet/flight-cache", 
             qs: params},
            function(error, response, body){
            	if (error) {
            		console.log("Error")
            		console.log(error)
            		return res.status(404).send({
								    data: error,
								    message: 'Error'
								  });
            	}
            	if (body) {
            		result = body
            		  return res.status(200).send({
								    data: JSON.parse(body),
								    message: 'Script running'
								  });
            	}
            });


  // return res.status(404).send({
  //   message: 'Script Failed'
  // });
};



var HOLIDAYS = ["2017-07-14","2017-08-15","2017-11-01","2017-11-11","2017-12-25","2018-01-01"];

var isWeekend = function(date) {	
  if ((date.weekday() == 5) || (date.weekday() == 6)) {
    return True
  }
  else {
    return False
  }
}

var isHoliday = function(date) {
  for (var i = 0; i < HOLIDAYS.length; i++) {
    if (date.date() == datetime.strptime(HOLIDAYS[i], "%Y-%m-%d").date()) {
      return True
    }
  }
  return False
}

var isWorkable = function(date) {
  if (isHoliday(date) || isWeekend(date)){
    return False
  } else {
    return True
  }
}

var getMaxSpan = function(date) {
  var span = 0
  var nextDay = date
  while (isWorkable(nextDay) == False) {
    span = span + 1
    nextDay = nextDay + timedelta(days=1)
  	return span
  }
}


// var getNbrOfCP = function(date,date2) {
//   start = date
//   end = date2
//   print date
//   print date2.date()
//   temp = start
//   total = 0
//   while temp <= end:
//     if (isWorkable(temp) is True):
//       total = total + 1
//     temp = temp + timedelta(days=1)
//   print start.hour
//   if ((isWorkable(start) is True) and (start.hour>20)):
//     print "yooooooo"
//     print start
//     total = total - 1
//   if ((isWorkable(end) is True) and (start.hour<7)):
//     total = total - 1
//   return total
// }


// var getDuration = function(date,date2):
//   start = datetime.strptime(date, "%Y-%m-%d")
//   end = datetime.strptime(date2, "%Y-%m-%d")
//   return (end-start).days

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
  return date
}



var dates = function(lastDate) {

  var result = []
  var date = {"start":datetime.now(), "end":datetime.now()}
  var today = datetime.now() + timedelta(days=2)
  var date = today
  var i = 0
  while ((date.date() < lastDate) && (i<400)) {
  	i = i+1
    if (date) {
    // if ((isWorkable(date) is False) or (isWorkable(date + timedelta(days=1)) is False)):
      var endDates = getEndDates(date)
      for (var i = 0; i < endDates.length; i++) {
        result.append({"start":date.date(), "end":endDates[i]})
      };
    }
    date = date + timedelta(days=6)
  }
  return result
}
