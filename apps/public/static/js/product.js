$(function(){//on page load

  $('.carousel').carousel({
    interval: false
  })

  //CUSTOM ORDER FORM AUTO-SHOW
  if (window.location.hash.split("#")[1] == "custom-order"){
    $('#custom-order').slideDown();
  }

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
  $('#custom-order').slideDown();
});

$('.change-size').click(function(){
  $('.change-size').hide();
  $('#size-form').show();
});
$('.change-quantity').click(function(){
  $('.change-quantity').hide();
  $('#quantity-form').show();
});
$('.change-description').click(function(){
  $('.change-description').hide();
  $('#description-form').show();
});

$('#custom-order-submit-button').click(function(){
  if ($('#custom-order-email').val() == "") {
    $('#custom-order-email').addClass('error');
  }else{
    $('#custom-order-submit-button h2').html("Sending...");
    $('#custom-order-submit-button').attr('disabled', 'True')

    var size = $('#custom-order-length-A').val() + "ft. "
    size += $('#custom-order-length-B').val() + "in. by "
    size += $('#custom-order-width-A').val() + "ft. "
    size += $('#custom-order-width-B').val() + "in."

    $.ajax({url: $('#custom-order-url').val(),
            data: { 'product_id': $('#custom-order-product-id').val(),
                    'email': $('#custom-order-email').val(),
                    'size': size,
                    'quantity': $('#custom-order-quantity').val(),
                    'description': $('#custom-order-description').val()
                  },
            type: "POST"})
    .done(function(){
      $('#custom-order-submit-button').hide();// hide form
      $('#custom-order-success').show();// show success
    })
    .fail(function(){
      $('#custom-order-fail').show();// show fail
      $('#custom-order-submit-button').hide(); //hide submit button
    })
    .always(function(){
      $('#custom-order *').attr('disabled', 'True');
    })
  }
});
