(function(){

  var app = angular.module('marketplace', ['ngRoute', 'market-directives']);

  app.controller('MarketController', ['$http', function($http){

    var market = this;
    market.listings = [];
    $http.get('/api/listings/')
    .success(function(data){
      market.listings = data;
    });

  }]);

})();
