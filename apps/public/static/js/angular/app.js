(function(){

  var app = angular.module('marketplace', ['ngRoute', 'market-directives']);

  app.controller('MarketController', ['$http', function($http){

    var market = this;
    market.listings = [];
    $http.get('/api/listings/') //todo: load urls in with a constant
    //http://django-angular.readthedocs.org/en/latest/manage-urls.html
    .success(function(data){
      market.listings = data;
    });

  }]);

})();
