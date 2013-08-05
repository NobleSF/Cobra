$().ready( function(){

  $('.ratings').hide();

  $('.product-id').click(function(){
    $(this).hide();
    $(this).closest('.details').find('.ratings').show();
  });

  $('.ratings').click(function(){
    $(this).hide();
    $(this).closest('.details').find('.product-id').show();
  });

});
