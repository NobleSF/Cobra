$().ready( function(){
  //assign bootstrap classes
  $('button').addClass('btn');

  //run on page load
  $('#summary-show-more').bind('click', function(){
    $('.summary-detail').show();
    $('#summary-show-more').hide();
  });

});//end .ready
