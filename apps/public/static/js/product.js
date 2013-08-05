$(function(){//on page load

  $('.carousel').carousel({
    interval: false
  })

});


$('.read-more').on('click', function(){
  $(this).prev('.short-description').hide();
  $(this).hide();
  $(this).next('.long-description').show();
});

//$('.product').click(function(){
//  window.location.href = $(this).attr('data-url');
//});

$('.product').hover(
  function(){ //on mouseenter
    $(this).find('.title h3').addClass('underline')
  },
  function(){//on mouseleave
    $(this).find('.title h3').removeClass('underline')
  }
);
