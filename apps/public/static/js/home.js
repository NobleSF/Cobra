$(function(){//on page load

  $(this).find('.extra').find('div').find('*').each(function(){
    $(this).hide();
  });

});

//bootstrap carousel
$('.carousel').carousel();

$('.product').click(function(){
  window.location.href = $(this).attr('data-url');
});

$('.product').hover(
  function(){ //on mouseenter
    $(this).find('.extra').find('div').find('*').each(function(){
      $(this).show();
    });
  },
  function(){//on mouseleave
    $(this).find('.extra').find('div').find('*').each(function(){
      $(this).hide();
    });
  }
);

function findNeighbor(product_area){
  if ($(product_area).hasClass('pos1') || $(product_area).hasClass('pos2')){
    return $(product_area).next('.product-area');
  }else{
    return $(product_area).prev('.product-area');
  }
}
