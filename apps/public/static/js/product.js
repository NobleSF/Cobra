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
  $('#custom-order').show();
  //scrollTo #custom-order
});

$('#custom-order-submit-button').click(function(){
  if ($('#custom-order-message').val() == "") {
    $('#custom-order-message').addClass('error');
  }else if ($('#custom-order-email').val() == "") {
    $('#custom-order-email').addClass('error');
  }else{
    $('#custom-order-submit-button h2').html("Sending...");
    $('#custom-order-submit-button').attr('disabled', 'True')

    $.ajax({url: $('#custom-order-url').val(),
            data: { 'product_id': $('#custom-order-product-id').val(),
                    'email': $('#custom-order-email').val(),
                    'length': $('#custom-order-width').val(),
                    'width': $('#custom-order-length').val(),
                    'message': $('#custom-order-message').val()
                  },
            type: "POST"})
    .done(function(){
      $('#custom-order-form').hide();// hide form
      $('#custom-order-success').css('display', 'block');// show success
    })
    .fail(function(){
      $('#custom-order-fail').css('display', 'block');// show fail
      $('#custom-order-submit-button').hide(); //h ide submit button
    })
  }
});
