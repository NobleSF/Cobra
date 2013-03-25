$().ready( function(){
  //assign bootstrap classes
  $('button').addClass('btn');
  $('#asset_tabs').addClass('nav').addClass('nav-tabs');
  $('#asset_tabs').children('li').first().addClass('active');
  $('.file-button').addClass('btn').html('<i class="icon-camera"></i>');
  $('#artisan_tab').trigger('click');//activate first tab
  $('#title').trigger('click');//get out of the way
  addAssetForms();
});

$('.asset-tab').click(function(){
  //make this tab active
  $('.asset-tab').removeClass('active');
  $(this).addClass('active');
  //hide all asset containers, then show the right one
  $('.asset-container').hide();
  asset_ilk = $(this).attr('id').replace('_tab','');
  $('#'+asset_ilk+'_container').show();
})

$('#title').on('click', function(){
  $('#seller_form').slideToggle();
});

$('input:file').change(function(){
  key_string = createKey($(this))
  full_key = copyKeyToAssetForm($(this), key_string);
  postImage($(this));
  //loadThumbnail($(this), full_key);
  addAssetForms();
})

function postImage(file_element){
  //create progress bar
  file_element.closest('form').submit();
  //remove progress bar
  return true;
}

function loadThumbnail(file_element, full_key){

  $.get('/seller/ajax/image_save', {url:full_key, ilk:asset_ilk})
  .done(function(response){

    if (response.problem){//try again?
    }else if(response.exception){//fail permanently
    }else if(respolse.url){//success!
      //replace img placeholder with thumbnail
      file_element.closest('.asset').find('.placeholder-image')
      .html('<img src="' + response.url + '" width="200">');
    }
  });
}

function createKey(file_element){
  filename = file_element.val().split('/').pop().split('\\').pop();
  //todo: if no file extension, add one

  //add asset ilk and datetime
  asset_ilk = file_element.closest('.asset-container').attr('id').split('_',1).toString();
  key_date = $('#key_date').html()
  return ("_" + asset_ilk + "_" + key_date + "_" + filename);
}

function copyKeyToAssetForm(file_element, key_string){
  key = file_element.closest('.asset').find('#id_key');
  //todo: if no file extension, add one

  //add asset ilk and datetime
  asset_ilk = key.closest('.asset-container').attr('id').split('_',1).toString();
  key_date = $('#key_date').html()
  append_to_key = "_" + asset_ilk + "_" + key_date + "_" + filename;

  //find key and append
  key.val(key.val() + append_to_key);

  //match image input to key
  key.closest('.asset').find('#id_image').attr('value',key.val());

  //return full key
  return key.val();
}

function addAssetForms(){
  //use jquery appendTo function to move blank asset forms
  //to asset containers so there is always at least one fresh one.

  //for each asset container
  $('.asset-container').each(function(){
    num_forms = 0;
    num_empty_forms = 0;

    //for each asset form inside the containter
    $(this).children('.asset').each(function(){
      //count empty forms
      if ($(this).find('#id_image').val() == ''){
        num_empty_forms++;
      }else{
        num_forms++;
      }
    });

    //if there are no empty forms, add one
    if (num_empty_forms == 0){
      //grab an empty form from the hidden .asset_forms div
      new_asset_form = $('#asset_forms > .asset').first().clone(true);
      //if not product container, hide category element
      ilk = $(this).attr('id').replace('_container','');
      if ( ilk !== 'product'){
        new_asset_form.find('.asset-category').hide();
      }
      //give it a new unique id
      unique_id = ilk + '_image_' + (num_forms+1).toString();
      new_asset_form.find('.asset-image').attr('id', unique_id);
      //place it in the container
      new_asset_form.appendTo($(this));
    }
  });
}
