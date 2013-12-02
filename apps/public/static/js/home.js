$(function(){//on page load

  //LAZY PRODUCT LOADING
  $('.lazy-load').lazyload(800);

  //HOVER ANIMATION
  addHoverAnimation($('.product'));

  $('.flexslider').flexslider({
    animation: "slide"
    ,slideshow: false
  });

});

//BOOTSTRAP CAROUSEL
//$('#video-image').on('click', function(){
//  $('#video-image').hide();
//  $('#video').show();
//});

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

//SEARCH AND SORTING FUNCTIONS
$('#search-toolbar .category').on('click', function(){
  parent_category = $(this).attr('data-parent-category');
  //remove all selected
  $('#search-toolbar .category').removeClass('selected');

  child_category = $(this).attr('data-child-category');
  //select the clicked one
  $(this).addClass('selected');
  //hide all child categories
  $('#search-toolbar .category.child').hide()
  //show relevent child categories
  $('#search-toolbar .category.child[data-parent-category='+parent_category+']').show()
  //selecte clicked child category
  if ($(this).hasClass('child')){
    $('#search-toolbar .category.parent[data-child-category='+parent_category+']').addClass('selected');
  }
  //sort products according to chosen cateogories
  sortProductsBy(parent_category, child_category)
});

function sortProductsBy(parent_category, child_category){
  // everything, everything shows all
  // parent, parent shows all in parent category
  // parent, child shows all in child category
  // parent, other shows all where child == parent

  //hide all products
  $('.product-area').hide();

  //move the category products first
  if (parent_category == "everything"){
    //nothing to do here

  }else if (parent_category == child_category){//all in parent
    $('#product-container .product-area').each(function(){
      if ($(this).attr('data-parent-category') == parent_category){
        $(this).appendTo($('#product-sorting-container'))
      }
    });

  }else if(child_category == "other"){//all child == parent
    $('#product-container .product-area').each(function(){
      if ($(this).attr('data-parent-category') == parent_category &&
          $(this).attr('data-child-category') == parent_category){
        $(this).appendTo($('#product-sorting-container'))
      }
    });

  }else if(parent_category != child_category){//child only
    $('#product-container .product-area').each(function(){
      if ($(this).attr('data-parent-category') == parent_category &&
          $(this).attr('data-child-category') == child_category){
        $(this).appendTo($('#product-sorting-container'))
      }
    });
  }

  //then move all the rest to follow behind
  $('#product-container .product-area').each(function(){
    $(this).appendTo($('#product-sorting-container'))
  });
  //all products should be in the sorting container now

  //move all products back into rows
  if (child_category == 'everything'){
    $('#product-sorting-container .product-area').each(function(){
      //find the row it originally belonged to and put it there
      row_number = Math.floor($(this).attr('data-order')/3)
      $(this).appendTo($('#product-container .product-row')[row_number])
    });
  }else{
    var next_position = 0;
    //now put them all back into rows - they are already in order
    $('#product-sorting-container .product-area').each(function(){
      row_number = Math.floor(next_position/3);
      $(this).appendTo($('#product-container .product-row')[row_number])
      next_position++;
    });
  }
  $('.lazy-load:lt(5)').trigger('loadnow');

  //this_category = $(this).attr('data-category');
  //this_position = $(this).attr('data-order');

  if (parent_category == 'everything'){//everything
    $('.product-area').show();

  }else if (parent_category == child_category){//all in parent
    $('.product-area[data-parent-category='+parent_category+']').show();

  }else if(child_category == "other"){//all child == parent
    $('.product-area[data-child-category='+parent_category+']').show();

  }else if(parent_category != child_category){//child only
    $('.product-area[data-parent-category='+parent_category+'][data-child-category='+child_category+']').show();
  }
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
