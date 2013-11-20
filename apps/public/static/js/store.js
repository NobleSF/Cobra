$(function(){//on page load

  //LAZY PRODUCT LOADING
  $('.lazy-load').lazyload(800);

  //HOVER ANIMATION
  addHoverAnimation($('.product'));

  //LOAD MORE PRODUCTS
  if ($('.product-area.load-me-later').length > 0){
    loadMoreProducts();
  }

});

//activate the 'show more' buttons on mobile version
$('[data-show]').one('click', function(){
  $(this).next().removeClass('hidden')
                .removeClass('hidden-phone')
                .removeClass('visible-phone');
  $(this).removeClass('visible-phone');
  $('#'+$(this).attr('data-show')).slideDown();
  $(this).hide();
});

$('.read-more').on('click', function(){
  $(this).prev('.short-description').hide();
  $(this).hide();
  $(this).next('.long-description').show();
});

//PRODUCT ANIMATION
function addHoverAnimation(selection){
  $(selection).hover(
    function(){ //on mouseenter
      if(! navigator.userAgent.match(/(iPhone|iPod|iPad)/i)){
        $(this).find('.hover-show').each(function(){
          $(this).show();
        });
      }
    },
    function(){//on mouseleave
      if(! navigator.userAgent.match(/(iPhone|iPod|iPad)/i)){
        $(this).find('.hover-show').each(function(){
          $(this).fadeOut();
        });
      }
    }
  );
}

// Lazy Load products based on jQuery Unveil at http://luis-almeida.github.com/unveil
;(function($) {
  $.fn.lazyload = function(given_threshold) {

    var $w = $(window),
        threshold = given_threshold || 0, //default visibility threshold of 0 pixels
        containers = this,
        url = $('#load-products-url').val(),
        loaded, inview, product_areas, product_ids;

    this.on("loadnow", function() {
      //get unloaded products
      product_areas = $(this).children('.unloaded').removeClass('unloaded');

      if (product_areas.length){ //if any products, load them
        product_ids = product_areas.map(function(){ //get id list
          return $(this).attr('data-product-id');
        }).get();

        $.ajax({type:"GET", url:url, data:{product_ids:product_ids.join()}})
        .done(function(response){
          for (var key in response){ //for each (id, html) in response
            if (response.hasOwnProperty(key)){
              var product_area = $(".product-area[data-product-id='"+key+"']")
              $(product_area).html(response[key]);
              $(product_area).addClass('loaded'); //mark loaded
              addHoverAnimation($(product_area).find('.product'));
            }
          }
        })
        .fail(function(){
          product_areas.addClass('unloaded');
        });
      }
    }); //end loading function

    function lazyload(){ //find objects within range that need loading
      inview = containers.filter(function() {
        var $e = $(this),
            wt = $w.scrollTop(),
            wb = wt + $w.height(),
            et = $e.offset().top,
            eb = et + $e.height();
        return eb >= wt - threshold && et <= wb + threshold;
      });
      inview.trigger("loadnow"); //always keep triggering, products can hop in and out
    }

    $w.scroll(lazyload); //run on window scroll
    $w.resize(lazyload); //run on window resize
    lazyload(); //run right now
    return this;
  };
})(window.jQuery);
