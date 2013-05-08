$().ready( function(){
  COUNTER = 1;
  //assign bootstrap classes
  $('button').addClass('btn');
  $('#asset_tabs').addClass('nav').addClass('nav-tabs');
  $('#asset_tabs').children('li').first().addClass('active');
  $('.file-button').addClass('btn').html('<i class="icon-camera"></i>');

  //run on page load
  $('#artisan_tab').trigger('click');//activate first tab
  arrangeAssetForms();
  addAssetForms();

});//end .ready

$('.asset-tab').click(function(){
  //make this tab active
  $('.asset-tab').removeClass('active');
  $(this).addClass('active');
  //hide all asset containers, then show the right one
  $('.asset-container').hide();
  asset_ilk = $(this).attr('id').replace('_tab','');
  $('#'+asset_ilk+'_container').show();
});

$('#acct-details').on('click', function(){
  $('#seller_form').slideToggle();
});

function arrangeAssetForms(){
  $('#asset_forms .asset').each(function(){
    //move to proper asset container
    var ilk = $(this).find('#id_ilk').val();
    var asset_id = $(this).find('#id_asset_id').val();
    applyData($(this), asset_id, ilk)
    applyEvents($(this));
    if (ilk != ''){
      $(this).appendTo('#'+ilk+'_container');
    }
  });
}

function addAssetForms(){
  //copy blank asset forms to asset containers so there is always an extra new one.

  //for each asset container
  $('.asset-container').each(function(){
    num_forms = 0;
    num_empty_forms = 0;

    //for each asset form inside the containter
    $(this).children('.asset').each(function(){
      //count empty forms
      if ($(this).find('#id_asset_id').val() == 'none'){
        num_empty_forms++;
      }else{
        num_forms++;
      }
    });

    //if there are no empty forms, add one
    if (num_empty_forms == 0){

      //grab an empty form from the hidden .asset_forms div
      new_asset = $('#asset_forms .asset').first().clone(false);
      var ilk = $(this).attr('id').replace('_container','');
      var asset_id = new_asset.find('#id_asset_id').val();

      //place it in the container
      new_asset.appendTo($(this));
      applyData(new_asset, asset_id, ilk);
      applyEvents(new_asset);

    }//end if
  });//end for each asset-container
}

function applyData(asset_div, asset_id, ilk){
  //if not product container, hide category element
  if ( ilk !== 'product'){
    asset_div.find('.asset-category').hide();
  }else{
    asset_div.find('.asset-category').show();
  }

  //give the image div and input a new unique id
  unique_div_id = ilk + '_image_' + COUNTER.toString();
  unique_input_id = ilk + '_image_' + COUNTER.toString();
  image_div = asset_div.find('.image');
  image_div.attr('id', unique_div_id);
  image_input = asset_div.find('.image-input');
  image_input.attr('id', unique_input_id);

  //tell form and autosave elements the asset_id and ilk
  asset_div.find('.autosave').attr('data-asset_id', asset_id);
  asset_div.find('#id_ilk').attr('value', ilk);
  asset_div.find('.autosave').attr('data-ilk', ilk);

  COUNTER++;
}

function applyEvents(asset_div){
  //for images uploader
  image_input = asset_div.find('.image-input');
  image_div = asset_div.find('.image');
  uploader = new fileUploadAction();
  uploader.apply(image_input, image_div);

  //for input fields
  applyAutosave();
}
