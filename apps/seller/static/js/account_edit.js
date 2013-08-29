$().ready( function(){
  COUNTER = 1;//for creating unique id numbers
  //assign bootstrap classes
  $('#asset-tabs').children('li').first().addClass('active');//first tab active
  $('#artisan_tab').trigger('click');//activate first tab

  //run on page load for seller form
  applyData($('#seller-account'), 'seller', 'seller');//add data- attributes
  applyEvents($('#seller-account'), to_assets=false);//for seller image
  applySellerAutosave();//autosave seller form elements

  //run on page load for assets
  arrangeAssetForms();//move assets to their respective tab
  addAssetForms();//create blank assets as needed

});//end .ready

$('.asset-tab').click(function(){//when an asset tab is clicked
  //make this tab active
  $('.asset-tab').removeClass('active');
  $(this).addClass('active');
  //hide all asset containers, then show the right one
  $('.asset-container').hide();
  asset_ilk = $(this).attr('id').replace('_tab','');
  $('#'+asset_ilk+'_container').show();
});

function applySellerAutosave() {
  $('#seller-account').find('.autosave').autosave({
    url:$('#save-seller-url').val(),
    before:saveSellerBefore,
    success:saveSellerSuccess,
    error:saveSellerError
  });
}

function saveSellerBefore($this_element){
  //start 'updating' visual
  $this_element.closest('#seller-account').removeClass('error').removeClass('saved').addClass('updating');
}
function saveSellerSuccess(data,$this_element){
  //finished visual
  $this_element.closest('.asset').removeClass('updating').addClass('saved');
}
function saveSellerError(error,$this_element){
  //error visual
  $this_element.closest('.asset').removeClass('updating').addClass('error');
}

function arrangeAssetForms(){
  $('#asset-forms .asset').each(function(){
    //move to proper asset container
    var ilk = $(this).find('#id_ilk').val();
    var asset_id = $(this).find('#id_asset_id').val();
    applyData($(this), asset_id, ilk);
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

      //grab an empty form from the hidden .asset-forms div
      new_asset = $('#asset-forms .asset').first().clone(false);
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

  if (ilk !=='artisan'){
    asset_div.find('.asset-phone').hide();
  }else{
    asset_div.find('.asset-phone').show();
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

function applyEvents(asset_div, to_assets){
  //for images uploader
  image_input = asset_div.find('.image-input');
  image_div = asset_div.find('.image');
  uploader = new fileUploadAction();
  uploader.apply(image_input, image_div);

  //for input fields
  to_assets = to_assets || true;//parameter defaults to true
  if (to_assets){
    applyAssetAutosave(asset_div);
    applyAssetDeleteAction(asset_div);
  }
}
