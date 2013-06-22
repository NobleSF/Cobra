$().ready( function(){

  //$('.extra').hide();

  $('.product-id').click(function(){
    $(this).closest('.product').find('.costs-detail').hide();
    $(this).closest('.product').find('.status').hide();
    $(this).closest('.product').find('.total-cost').toggle();
  });

  $('.total-cost').click(function(){
    $(this).closest('.details').find('.extra').show();
  });

});
