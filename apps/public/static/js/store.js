$(function(){//on page load



});

//activate the 'show more' buttons
$('[data-show]').one('click', function(){
  $(this).next().removeClass('hidden')
                .removeClass('hidden-phone')
                .removeClass('visible-phone');
  $(this).removeClass('visible-phone');
  $('#'+$(this).attr('data-show')).slideDown();
  $(this).hide();
});
