$(function(){//on page load



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