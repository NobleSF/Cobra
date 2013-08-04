$(function(){//on page load

  $(this).find('.extra').find('div').find('*').each(function(){
    $(this).hide();
  });

});

//bootstrap carousel

$('#video-image').on('click', function(){
  $('#video-image').hide();
  $('#video').show();
});

$('.product').hover(
  function(){ //on mouseenter
    $(this).find('.hover-show').each(function(){
      $(this).show();
    });
    $(this).find('.title h3').addClass('underline')
  },
  function(){//on mouseleave
    $(this).find('.hover-show').each(function(){
      $(this).fadeOut();
    });
    $(this).find('.title h3').removeClass('underline')
  }
);