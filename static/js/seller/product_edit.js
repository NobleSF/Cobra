$().ready( function(){
  //assign bootstrap classes
  $('button').addClass('btn');
  $('.file-button').addClass('btn').html('<i class="icon-camera"></i>');

  //run on page load
  $('#summary-show-more').bind('click', function(){
    $('.summary-detail').show();
    $('#summary-show-more').hide();
  });

  $('.asset').each( function(){
    $(this).bind('click', function(){
      $(this).toggleClass('selected');
      toggleSaveAssetId($(this));
    });
  });

});//end .ready

function toggleSaveAssetId(asset_element){
  asset_id = asset_element.attr('data-object-id');
  input_element = $('#'+asset_element.attr('data-input-id'));
  input_element_value = input_element.attr('value');

  if (asset_element.hasClass('selected')){ //if selected
    if (!input_element_value.match(asset_id)){ //if does not already contain id
      input_element_value = input_element_value + ' ' + asset_id;
      input_element.attr('value', input_element_value);
    }
  }else{ //remove id
    input_element_value = input_element_value.replace(asset_id, '');
    input_element.attr('value', input_element_value);
  }
}
