(function () {
  'use strict';

  // Focus the element on page load
  // Unless the user is on a small device, because this could obscure the page with a keyboard

  angular.module('core')
    .directive('tileFlight', tileFlight);

  tileFlight.$inject = ['$timeout', '$window'];

  function tileFlight($timeout, $window) {
    var directive = {
      replace: true,
      restrict: 'E',
      link: link
    };

    return directive;

    function link(scope, element, attrs) {
      console.log(scope.flight)
      var element = angular.element(element[0]);
      var deptime = moment(scope.flight.deptime).tz(scope.flight.contents.depCityTimeZone);
      var rettime = moment(scope.flight.rettime).tz(scope.flight.contents.arrCityTimeZone);
      scope.flight.local_deptime = deptime.format('MMMM Do YYYY, h:mm:ss a')
      scope.flight.local_rettime = rettime.format('MMMM Do YYYY, h:mm:ss a')
      activate();

      function activate() {
        for (var i = 0; i < scope.flight.duration; i++) {
          var tile = angular.element('<div class="tile"></div>');
          var tileInner = angular.element('<div class="tile-inner"></div>');
          var day = angular.element('<span class="tile-day"></span>');
          if (i==0) {
            tileInner.css('width',getPercentEndOfDay(deptime)*100+"%")
            tileInner.css('float','right')
            day.append(getDay(deptime))
            tile.append(day);
          } else if (i == scope.flight.duration -1) {
            tileInner.css('width',getPercentOfDay(rettime)*100+"%")
            day.append(getDay(rettime))
            tile.append(day);
          } else {
            tileInner.css('width',100+"%")
          }
          element.append(tile);
          tile.append(tileInner);
        };
        element.addClass("tileContainer")
      }

      function getPercentOfDay(date1) {
        var hours = date1.hours();
        return hours/parseFloat(24);
      }
      function getPercentEndOfDay(date1) {
        var hours = date1.hours();
        return (24-hours)/parseFloat(24);
      }
      function getDay(date1) {
        return date1.format('ddd');
      }
      // console.log(angular.element(element[0]))
    }
  }
}());
