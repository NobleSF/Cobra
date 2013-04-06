$().ready( function(){
  COUNTER = 1;
  //assign bootstrap classes
  $('button').addClass('btn');
  $('#asset_tabs').addClass('nav').addClass('nav-tabs');
  $('#asset_tabs').children('li').first().addClass('active');
  $('.file-button').addClass('btn').html('<i class="icon-camera"></i>');

  //run on page load
  $('#artisan_tab').trigger('click');//activate first tab
  $('#title').trigger('click');//get out of the way
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

$('#title').on('click', function(){
  $('#seller_form').slideToggle();
});

function arrangeAssetForms(){
  $('#asset_forms .asset').each(function(){
    //move to proper asset container
    var ilk = $(this).find('#id_ilk').val();
    var asset_id = $(this).find('#id_asset_id').val();
    applyDataAndEvents($(this), asset_id, ilk)
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
      new_asset = $('#asset_forms .asset').first().clone(true);

      var ilk = $(this).attr('id').replace('_container','');
      var asset_id = new_asset.find('#id_asset_id').val();
      applyDataAndEvents(new_asset, asset_id, ilk);

      //place it in the container
      new_asset.appendTo($(this));

    }//end if
  });
}

function applyDataAndEvents(asset_form, asset_id, ilk){
      //if not product container, hide category element
      if ( ilk !== 'product'){
        asset_form.find('.asset-category').hide();
      }

      //give the image div a new unique id
      unique_id = ilk + '_image_' + COUNTER.toString();
      image_div = asset_form.find('.image');
      image_div.attr('id', unique_id);

      //tell form and autosave elements the asset_id and ilk
      asset_form.find('.autosave').attr('data-asset_id', asset_id);
      asset_form.find('#id_ilk').attr('value', ilk);
      asset_form.find('.autosave').attr('data-ilk', ilk);

      image_input = asset_form.find('.image-input');
      applyFileUploadAction(image_input, image_div);

      COUNTER++;
}
