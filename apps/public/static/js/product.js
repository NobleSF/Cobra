$(function(){//on page load

  $('.carousel').carousel({
    interval: false
  })

});

$('#unapprove').click(function(){
  button = $(this)
  $.get($(this).attr('data-approve-url'),
        {product_id:$(this).attr('data-product-id'), action:"hold"}
  ).done(function(){
    button.html('Unapproved.').addClass('disabled');
  });
})

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
    if(! navigator.userAgent.match(/(iPhone|iPod|iPad)/i)){
      $(this).find('.hover-show').each(function(){
        $(this).fadeOut();
      });
    }
  }
);

$('#custom-order-button').click(function(){
  //hide buy button and artisan picture
  $('#buy-button, #custom-order-button, #artisan').hide();
  $('#custom-order').show();
});
$('#cancel-custom-order-button').click(function(){
  //undo above
  $('#custom-order').hide();
  $('#buy-button, #custom-order-button, #artisan').show();
});

$('#custom-order-submit-button').click(function(){
  $.ajax({url: "/seller/ajax/req_cust_order",
          data: { 'product_id': $('#custom-order-product-id').val(),
                  'customer_email': $('#custom-order-customer-email').val(),
                  'message': $('#custom-order-message').val()
                },
          type: "POST"})
  .done(function(){
    $('#custom-order-success').show();// show success
  })
  .fail(function(){
    $('#custom-order-fail').show();// show fail
  })
  .always(function(){
    $('#custom-order-submit-button').hide(); //hide submit button
    $('#cancel-custom-order-button h2').html("Close");
  });
});
