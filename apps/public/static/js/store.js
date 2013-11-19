$(function(){//on page load

  //LAZY PHOTO LOADING
  $("img").unveil();
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

//LOAD MORE PRODUCTS
function loadMoreProducts(){
  var product_ids = $('.product-area.load-me-later')
        .map(function(){return $(this).attr('data-product-id');}).get();

  var url = $('#load-products-url').val();
  $.ajax({
    type: "GET",
    url: url,
    data: {product_ids:product_ids.join()},
    async: true
  })
  .done(function(response){
    for (var key in response) {
      if (response.hasOwnProperty(key)){
        var product_area = $(".product-area[data-product-id='"+key+"']")
        $(product_area).html(response[key]);
        $(product_area).find('img').unveil(400);
        addHoverAnimation($(product_area).find('.product'));
        $(product_area).removeClass('load-me-later');
      }
    }
  })
}
