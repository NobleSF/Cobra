$().ready( function(){
  //assign bootstrap classes
  $('button').addClass('btn');
  $('#asset_tabs').addClass('nav').addClass('nav-tabs');
  $('#asset_tabs').children('li').first().addClass('active');
  $('.file-button').addClass('btn').html('<i class="icon-camera"></i>');
  $('#artisan_tab').trigger('click');//activate first tab
  $('#title').trigger('click');//get out of the way
  addAssetForms();

  $('.image-input').each(function(){
    $(this)
  });//end .each
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

$('.asset-form form').blur(function(){
  alert('ajax update!');
});

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
      new_asset = $('#asset_forms > .asset').first().clone(true);

      //if not product container, hide category element
      ilk = $(this).attr('id').replace('_container','');
      if ( ilk !== 'product'){
        new_asset.find('.asset-category').hide();
      }

      //give it a new unique id
      unique_id = ilk + '_image_' + (num_forms+1).toString();
      image_div = new_asset.find('.image');
      image_div.attr('id', unique_id);

      //tell form the ilk
      new_asset.find('#id_ilk').attr('value', ilk)

      //place it in the container
      new_asset.appendTo($(this));

      asset_form = new_asset.find('.image-input');
      applyFileUploadAction(asset_form, image_div);
    }//end if
  });
}

function applyFileUploadAction(file_input, image_destination){
  this_element = file_input;
  progress_bar = image_destination.siblings('.progress');
  progress_bar.hide();

  file_input.fileupload({
    dataType: 'json',
    url: '/seller/ajax/image_save',

    //progressall: function (e, data) {
    //  var progress = parseInt(data.loaded / data.total * 100, 10);
    //  progress_bar.find('.bar').css('width', (progress*0.9) + '%');
    //},

    done: function (e, data) {
      response_data = data['response']();
      response = response_data.result;
      image_destination.html('<img src="' + response['thumb_url'] + '">');
      image_destination.closest('.asset').find('.image-id')
        .attr('value',response['image_id']);
      addAssetForms();
    }
  });//end fileupload
}
