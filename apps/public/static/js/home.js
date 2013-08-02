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

$('.product').click(function(){
  window.location.href = $(this).attr('data-url');
});

$('.product').hover(
  function(){ //on mouseenter
    $(this).find('.hover-show').each(function(){
      $(this).fadeIn();
      //$(this).attr('style','opacity:1');
    });
  },
  function(){//on mouseleave
    $(this).find('.hover-show').each(function(){
      $(this).fadeOut();
      //$(this).attr('style','opacity:0.01');
    });
  }
);