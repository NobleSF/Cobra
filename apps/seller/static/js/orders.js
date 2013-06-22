$().ready( function(){

  //$('.extra').hide();

  $('.product-id').click(function(){
    $(this).closest('.product').find('.total-cost').show();
  });

  $('.total-cost').click(function(){
    $(this).closest('.details').find('.extra').show();
  });

});
