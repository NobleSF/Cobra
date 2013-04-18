$().ready( function(){
  //assign bootstrap classes
  $('button').addClass('btn');
  $('.file-button').addClass('btn').html('<i class="icon-camera"></i>');

  //run on page load
  $('#summary-show-more').bind('click', function(){
    $('.summary-detail').show();
    $('#summary-show-more').hide();
  });

});//end .ready
