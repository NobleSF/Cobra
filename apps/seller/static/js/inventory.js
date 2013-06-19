$().ready( function(){

  $('.ratings').hide();

  $('.product-id').click(function(){
    $(this).closest('.details').find('.ratings').show();
  });

});

