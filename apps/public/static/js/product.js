$(function(){//on page load

  $('.carousel').carousel({
    interval: false
  })

  //PRODUCT PHOTO LOADING
  $("img").unveil();

});

$('.read-more').on('click', function(){
  $(this).prev('.short-description').hide();
  $(this).hide();
  $(this).next('.long-description').show();
});

//PRODUCT ANIMATION
$('.product').hover(
  function(){ //on mouseenter
    if(! navigator.userAgent.match(/(iPhone|iPod|iPad)/i)){
      $(this).find('.hover-show').each(function(){
        $(this).show();
      });
    }
  },
  function(){//on mouseleave
    $(this).find('.hover-show').each(function(){
      $(this).fadeOut();
    });
  }
);
