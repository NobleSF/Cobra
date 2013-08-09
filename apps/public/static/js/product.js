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

//PRODUCT ANIMATION
$('.product').hover(
  function(){ //on mouseenter
    $(this).find('.hover-show').each(function(){
      $(this).show();
    });
  },
  function(){//on mouseleave
    $(this).find('.hover-show').each(function(){
      $(this).fadeOut();
    });
  }
);
