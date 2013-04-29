$(function(){//on page load

  //header changes
  //$('#scroll-controller').scrollspy();
  //$('#rest-of-page').on('activate', showMiniHeader());
  //$('#top-of-page').on('activate', showFullHeader());

  //bootstrap carousel
  $('.carousel').carousel();



});

function showFullHeader(){
  $('#full-nav').show();
  $('#mini-nav').hide();
}
function showMiniHeader(){
  $('#full-nav').hide();
  $('#mini-nav').show();
}

$('.product').hover(
  function(){ //on mouseenter
    //adjust parent product row
    var neighbor = findNeighbor($(this).closest('.product-area'));
    neighbor.removeClass('span3').hide();
    $(this).closest('.product-area').removeClass('span3').addClass('span6');

    //adjust product right/left sides
    $(this).find('.left-side').removeClass('span12').addClass('span6');
    $(this).find('.right-side').addClass('span6');
    $(this).find('.extra').each(function(){
      $(this).slideDown(500);
    });
  },
  function(){//on mouseleave
    //adjust parent product row
    var neighbor = findNeighbor($(this).closest('.product-area'));
    neighbor.addClass('span3').show();
    $(this).closest('.product-area').removeClass('span6').addClass('span3');

    //adjust product right/left sides
    $(this).find('.left-side').removeClass('span6').addClass('span12');
    $(this).find('.right-side').removeClass('span6');
    $(this).find('.extra').each(function(){
      $(this).slideUp(500);
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
