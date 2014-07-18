(function(){
  var controllers = angular.module('market-controllers', []);


  controllers.controller('MarketController', ['$http', function($http){

    var market = this;
    market.components = [];

    function big_or_small(){
      if (Math.floor(Math.random() * 2) == 1){
        return 'big';
      }else{
        return 'small';
      }
    }

    //get some components
    market.components = [{type:"listing", id:"1"},
                         {type:"listing", id:"6"},
                         {type:"category", id:"11"}];


    //size them


    //order them


  }]);



  controllers.controller('OldMarketController', ['$http', function($http){

    var market = this;
    market.categories = [];
    $http.get('/api/categories/?is_parent=True') //todo: load urls in with a constant
    //http://django-angular.readthedocs.org/en/latest/manage-urls.html
    .success(function(data){
      market.categories = data.results;
    });

  }]);

  controllers.controller('CategoryController', ['$http', function($http){

    var category = this;
    category.pages = 1;
    category.listings = [];
    $http.get('/api/listings/') //todo: load urls in with a constant
    //http://django-angular.readthedocs.org/en/latest/manage-urls.html
    .success(function(data){
      var page_size = 24;
      category.pages = parseInt((data.count+(page_size-1))/page_size);
      category.listings = data.results;
    });

  }]);

  controllers.controller('ListingController', ['$http', '$routeParams',
    function ($http, $routeParams) {
      var phone = this;

      $http.get('/api/listings/'+$routeParams.listingId)
      .success(function(data) {
        phone.detail = data;
      });

    }
  ]);

})();
