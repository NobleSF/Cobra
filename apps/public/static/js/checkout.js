$(function(){//on page load



});

$('#checkout').on('click', function(){
  $("#cart #items").slideUp();
  $("#cart #summary").slideUp();
  $("#cart-sentance").slideUp();
  $("#cart-paragraph").removeClass('hidden');
  $("#cart-form").removeClass('hidden');
});

//use mailcheck on email field
//https://github.com/kicksend/mailcheck
