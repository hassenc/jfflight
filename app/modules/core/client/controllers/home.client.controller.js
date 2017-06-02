(function () {
  'use strict';

  angular
    .module('core')
    .controller('HomeController', HomeController);

  HomeController.$inject = ['$http']

  function HomeController($http) {
    var vm = this;

    vm.runScript = runScript;

    function runScript() {
      console.log('yo');
      $http({
        method: 'GET',
        url: '/servelet/go'
      }).then(function successCallback(response) {
          console.log(response)
        }, function errorCallback(response) {
          console.log(response)
          // called asynchronously if an error occurs
          // or server returns response with an error status.
        });
    }
  }
}());
