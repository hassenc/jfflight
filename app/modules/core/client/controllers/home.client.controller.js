(function () {
  'use strict';

  angular
    .module('core')
    .controller('HomeController', HomeController);

  HomeController.$inject = ['$http'];

  function HomeController($http) {
    var vm = this;

    vm.options = {
      cp_penalty : 40,
      from : "PAR",
      to : "MIR",
      selected_date : moment().add(2,'months').toDate(),
      last_date : null,
    }

    vm.slider = {
      value: 40,
      options: {
        floor: 0,
        ceil: 100
      }
    };

    vm.runScript = runScript;
    runScript();
    function runScript() {
      console.log('yo');
      vm.options.cp_penalty = vm.slider.value;
      vm.options.last_date = moment(vm.options.selected_date).format("YYYY-MM-DD")
      var options = vm.options;
      $http({
        method: 'GET',
        url: '/servelet/go',
        params: options,
      }).then(function successCallback(response) {
        vm.flights = response.data.data;
        console.log(vm.flights)
        console.log(response);
      }, function errorCallback(response) {
        console.log(response);
        // called asynchronously if an error occurs
        // or server returns response with an error status.
      });
    }
  }
}());
