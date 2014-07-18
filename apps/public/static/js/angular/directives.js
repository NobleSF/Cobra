(function(){
  var app = angular.module('market-directives', []);


  app.directive("component", function() {

    function link(scope, element, attrs) {

    }

    return {
      link: link,
      restrict: 'E',
    }
  });

  app.directive("listing", function() {
    return {
      restrict: 'E',
      templateUrl: "/listing"
    };
  });

  app.directive("store", function() {
    return {
      restrict: 'E',
      templateUrl: "/store"
    };
  });

  app.directive("category", function() {
    return {
      restrict: 'E',
      templateUrl: "/category"
    };
  });

  app.directive("listingGrid", function() {
    return {
      restrict: 'E',
      templateUrl: "/listing-grid"
    };
  });

  app.directive("categoryGrid", function() {
    return {
      restrict: 'E',
      templateUrl: "/category-grid"
    };
  });

  //app.directive("productSpecs", function() {
  //  return {
  //    restrict:"A",
  //    templateUrl: "product-specs.html"
  //  };
  //});
  //
  //app.directive("productTabs", function() {
  //  return {
  //    restrict: "E",
  //    templateUrl: "product-tabs.html",
  //    controller: function() {
  //      this.tab = 1;
  //
  //      this.isSet = function(checkTab) {
  //        return this.tab === checkTab;
  //      };
  //
  //      this.setTab = function(activeTab) {
  //        this.tab = activeTab;
  //      };
  //    },
  //    controllerAs: "tab"
  //  };
  //});
  //
  //app.directive("productGallery", function() {
  //  return {
  //    restrict: "E",
  //    templateUrl: "product-gallery.html",
  //    controller: function() {
  //      this.current = 0;
  //      this.setCurrent = function(imageNumber){
  //        this.current = imageNumber || 0;
  //      };
  //    },
  //    controllerAs: "gallery"
  //  };
  //});

})();
