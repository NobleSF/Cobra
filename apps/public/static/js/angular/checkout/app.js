(function(){

  var app = angular.module('checkout', [
                                           'ngRoute',
                                           'cloudinary',
                                           'checkout-directives',
                                           'checkout-controllers'
                                          ]);

  app.config(['$routeProvider',
    function($routeProvider) {
      $routeProvider.
        when('/checkout/cart', {
          templateUrl: 'partials/cart.html',
          controller: 'CartController'
        }).
        otherwise({
          redirectTo: '/'
        });
    }
  ]);

})();
