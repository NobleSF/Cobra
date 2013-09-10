$('.title-row').click(function(){
  $(this).toggleClass('highlight');
  $(this).next('.actions-row').toggle();
});

$('.approve-product').click(function(){
  var product_id = $(this).attr('data-product-id');
  var product_row = $(this).closest("tr");
  approveProduct(product_id, 'approve', product_row);
});

$('.hold-product').click(function(){
  var product_id = $(this).attr('data-product-id');
  var product_row = $(this).closest("tr");
  approveProduct(product_id, 'hold', product_row);
});

$('.delete-product').click(function(){
  if (confirm("Permanently Delete Product?")){
    var product_id = $(this).attr('data-product-id');
    var product_row = $(this).closest("tr");
    approveProduct(product_id, 'delete', product_row);
  }
});

function approveProduct(product_id, action, product_row){
  var approve_url = $('#approve-url').val();

  $.get(approve_url, {product_id:product_id,action:action})
  .done(function(){
    if (action === 'approve' || action === 'delete'){
      product_row.slideUp('slow', function(){
        $(this).remove();
      });
    }else if (action === 'hold'){
      product_row.closest('.title-row').appendTo('#purgatory');
      product_row.closest('.actions-row').appendTo('#purgatory');
    }
  });
}

$('.rate').click(function(){
  var product_id  = $(this).attr('data-product-id');
  var subject     = $(this).attr('data-subject');
  var value       = $(this).attr('data-value');
  var rating_span   = $(this).parent('span');

  if (value > 0){
    rateProduct(product_id, subject, value, rating_span);
  }
});

function rateProduct(product_id, subject, value, rating_span){
  var rate_url = $('#rate-url').val();

  $.get(rate_url, {product_id:product_id,
                      subject:subject,
                      value:value
                     })
  .error(function(){
    //show no rating
    rating_span.closest('div').removeClass('chosen');
    rating_span.siblings('span').removeClass('selected');
  })
  .done(function(){
    rating_span.closest('div').addClass('chosen');
    rating_span.siblings('span').removeClass('selected');
    rating_span.addClass('selected');
  });
}
