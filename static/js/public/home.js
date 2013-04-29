$(function(){//on page load

  //header changes
  //$('#scroll-controller').scrollspy();
  //$('#rest-of-page').on('activate', showMiniHeader());
  //$('#top-of-page').on('activate', showFullHeader());

  //bootstrap carousel
  $('.carousel').carousel();

  $('.product').hover(function(){
    $(this).find('.extra').toggle(300);
  });

});

function showFullHeader(){
  $('#full-nav').show();
  $('#mini-nav').hide();
}
function showMiniHeader(){
  $('#full-nav').hide();
  $('#mini-nav').show();
}
