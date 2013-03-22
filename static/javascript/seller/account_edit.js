$().ready( function(){
  //assign bootstrap classes
  $('button').addClass('btn');
  $('#asset_tabs').addClass('nav').addClass('nav-tabs');
  $('#asset_tabs').children('li').first().addClass('active');
  $('#artisan_tab').trigger('click');//activate first tab
  $('#title').trigger('click');//get out of the way
  addAssetForms();
});

$('.asset_tab').click(function(){
  //make this tab active
  $('.asset_tab').removeClass('active');
  $(this).addClass('active');
  //hide all asset containers, then show the right one
  $('.asset_container').hide();
  asset_ilk = $(this).attr('id').replace('_tab','');
  $('#'+asset_ilk+'_container').show();
})

$('#title').click(function(){
  $('#seller_form').slideToggle();
});

$('.asset_image').click(function(){
  $(this).closest('form').find('.hidden_fields > .image_text').attr('value', 'tings');
  addAssetForms();
});

function addAssetForms(){
  //use jquery appendTo function to move blank asset forms
  //to asset containers so there is always at least one fresh one.

  //for each asset container
  $('.asset_container').each(function(){
    num_forms = 0;
    num_empty_forms = 0;

    //for each asset form inside the containter
    $(this).children('.asset').each(function(){
      //count empty forms
      image_text_element = $(this).find('form > .hidden_fields > .image_text').first();
      if (image_text_element.val() == ''){
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
        new_asset_form.find('.asset_category').hide();
      }
      //give it a new unique id
      unique_id = ilk + '_image_' + (num_forms+1).toString();
      new_asset_form.find('.asset_image').attr('id', unique_id);
      //place it in the container
      new_asset_form.appendTo($(this));
      initializeFileUploader(unique_id);
    }
  });
}

function initializeFileUploader(element_id){
  csrf_token = $('#csrf_token').attr('value');
  image_ajax_url = $('#image_ajax_url').attr('value');
  var uploader = new qq.FileUploader({
    action: image_ajax_url,
    element: $('#'+element_id)[0],
    multiple: false,
    onComplete: function(id, fileName, responseJSON) {
      if(responseJSON.success) {
        alert("success!");
      } else {
        alert("upload failed!");
      }
      alert(JSON.parse(responseJSON));
    },
    params: {
      'csrf_token': csrf_token,
      'csrf_name': 'csrfmiddlewaretoken',
      'csrf_xname': 'X-CSRFToken',
    },
  });
}
