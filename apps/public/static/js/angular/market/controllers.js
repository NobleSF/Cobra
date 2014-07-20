(function(){
  var controllers = angular.module('market-controllers', []);

  controllers.controller('MarketController', ['$http', function($http){

    var market = this;
    market.blocks = [];

    function big_or_small(){
      if (Math.floor(Math.random() * 2) == 1){
        return 'double';
      }else{
        return 'single';
      }
    }

    //get some blocks
    market.blocks = [
                      {type:"category", id:"11"}
                    ];

    //get 3 listing and append them to the blocks array
    $http.get('/api/listings/?limit=3')
    .success(function(data){
      for( listing=0; listing < data.results.length; listing++){
        market.blocks.push({
          type: 'listing',
          size: 'single',
          data: data.results[listing]
        });
      };
    });

    //get parent categories and append them to the blocks array
    $http.get('/api/categories/?is_parent=True')
    .success(function(data){
      for( category=0; category < data.results.length; category++){
        market.blocks.push({
          type: 'category',
          size: 'single',
          data: data.results[category]
        });
      };
    });

    //size them

    //order them

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

  controllers.controller('OldMarketController', ['$http', function($http){

    var market = this;
    market.categories = [];
    $http.get('/api/categories/?is_parent=True') //todo: load urls in with a constant
    //http://django-angular.readthedocs.org/en/latest/manage-urls.html
    .success(function(data){
      market.categories = data.results;
    });

  }]);
