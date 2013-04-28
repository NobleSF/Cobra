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
