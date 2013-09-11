$('.title-row').click(function(){
  $(this).toggleClass('highlight');
  $(this).next('.actions-row').toggle();
});

$('.approve-product').click(function(){
  var product_id = $(this).attr('data-product-id');
  approveProduct(product_id, 'approve');
});

$('.hold-product').click(function(){
  var product_id = $(this).attr('data-product-id');
  approveProduct(product_id, 'hold');
});

$('.delete-product').click(function(){
  if (confirm("Permanently Delete Product?")){
    var product_id = $(this).attr('data-product-id');
    approveProduct(product_id, 'delete');
  }
});

function approveProduct(product_id, action){
  var approve_url = $('#approve-url').val();
  title_row = $('#title-row-'+product_id)
  actions_row = $('#actions-row-'+product_id)

  $.get(approve_url, {product_id:product_id,action:action})
  .done(function(){
    if (action === 'approve' || action === 'delete'){
      //remove actions row
      actions_row.slideUp('slow', function(){
        $(this).remove();
      });
      //remove title row
      title_row.slideUp('slow', function(){
        $(this).remove();
      });
    }else if (action === 'hold'){
      title_row.appendTo('#purgatory');
      actions_row.appendTo('#purgatory');
      title_row.click();
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
