(function(){

  var app = angular.module('marketplace', [
                                           'ngRoute',
                                           'cloudinary',
                                           'market-directives'
                                          ]);

  app.controller('MarketController', ['$http', function($http){

    var market = this;
    market.pages = 1;
    market.listings = [];
    $http.get('/api/listings/') //todo: load urls in with a constant
    //http://django-angular.readthedocs.org/en/latest/manage-urls.html
    .success(function(data){
      var page_size = 24;
      market.pages = parseInt((data.count+(page_size-1))/page_size);
      market.listings = data.results;
    });

  }]);

})();
