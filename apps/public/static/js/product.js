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

$('.morocco-price').click(function(){
  $('.morocco-price-details').show();
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

$('#custom-order input').not('#custom-order-email').on('keyup change', function(){
  updateCustomOrderEstimate();
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

    $.ajax({url: $('#custom-order-request-url').val(),
            data: { 'product_id':   $('#custom-order-product-id').val(),
                    'email':        $('#custom-order-email').val(),
                    'size':         size,
                    'quantity':     $('#custom-order-quantity').val(),
                    'description':  $('#custom-order-description').val(),
                    'estimate':     $('#custom-order-estimate').val()
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

function updateCustomOrderEstimate(){

  $('#custom-order-estimate').hide()
  $('#custom-order-estimate-loader').show()

  //pull dimensions
  var length = $('#custom-order-length-A').val()*12*2.54 //feet -> cm
  length += $('#custom-order-length-B').val()*2.54 //inches -> cm
  var width = $('#custom-order-width-A').val()*12*2.54 //feet -> cm
  width += $('#custom-order-width-B').val()*2.54 //inches -> cm

  $.ajax({url: $('#custom-order-estimate-url').val(),
          data: { 'product_id': $('#custom-order-product-id').val(),
                  'length':     parseInt(length),
                  'width':      parseInt(width),
                  'quantity':   $('#custom-order-quantity').val()
                },
          type: 'GET'})
  .done(function(data){
    $('#custom-order-estimate').val("$"+data.display_price_estimate)
    $('#custom-order-estimate').show()
    $('#custom-order-estimate-loader').hide()
  })
  .fail(function(){
$('#custom-order-estimate').val("error")
    $('#custom-order-estimate').show()
    $('#custom-order-estimate-loader').hide()
  });
}
