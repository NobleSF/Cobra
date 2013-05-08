$().ready( function(){
  //assign bootstrap classes
  $('button').addClass('btn');
  $('.file-button').addClass('btn').html('<i class="icon-camera"></i>');
  $('.progress').addClass('progress-striped');
  $('.asset-chooser').addClass('btn-group');
  $('.asset').addClass('btn');

  //run on page load
  //only show the first 5 photo upload divs
  num_divs = 0;
  $('.photo-upload-div').each(function(){
    num_divs += 1;
    if (num_divs > 5){
      $(this).hide();
    }
  });

  markAssignedAssetsAsSelected();

  //activate the "show more" link in the summary
  $('#summary-show-more').bind('click', function(){
    $('.summary-detail').show();
    $('#summary-show-more').hide();
  });

  //selection actions for choosing assets, etc
  $('.asset').each( function(){
    $(this).bind('click', function(){
      $(this).toggleClass('active');
      $(this).toggleClass('selected');
      toggleStoreAssetId($(this));
      toggleActiveState($(this));
    });
  });

  //apply events for photo uploads
  $('.photo-upload-div').each(function(){
    file_input = $(this).find('.photo-input');
    display_div = $(this).find('.photo');
    uploader = new fileUploadAction();
    uploader.apply(file_input, display_div);
  });

  applyAutosaveDataToTextAttributes();
  applyAutosaveEvents();

  //set events for updating the summary
  $('#photo1').addClass('updates-summary');
  $('#price').addClass('updates-summary');
  $('#weight').addClass('updates-summary');
  $('#shipping_option').addClass('updates-summary');
  $('.updates-summary').each(function(){$(this).change(updateSummary);});
  updateSummary();

});//end .ready

function markAssignedAssetsAsSelected(){
  //actual assets
  asset_ids = $('#id_assets').val().split(" ");
  $.each(asset_ids, function(index, value){
    if (value !== ""){
      var btn = $('[store-input_id="assets"][store-object_id="'+value+'"]')
      $(btn).addClass("active").addClass("selected");
    }
  });


  //colors
  color_ids = $('#id_colors').val().split(" ");
  $.each(color_ids, function(index, value){
    if (value !== ""){
      var btn = $('[store-input_id="colors"][store-object_id="'+value+'"]')
      $(btn).addClass("active").addClass("selected");
    }
  });

  //shipping options
  shipping_option_ids = $('#id_shipping_options').val().split(" ");
  $.each(shipping_option_ids, function(index, value){
    if (value !== ""){
      var btn = $('[store-input_id="shipping_options"][store-object_id="'+value+'"]')
      $(btn).addClass("active").addClass("selected");
    }
  });
}

function toggleStoreAssetId(asset_element){
  asset_id = asset_element.attr('store-object_id');
  input_element = $('#id_'+asset_element.attr('store-input_id'));
  input_element_value = input_element.attr('value');
  if (input_element_value === undefined){input_element_value=""}

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

function toggleActiveState(asset_element){
  asset_input = asset_element.find('input');
  if (asset_element.hasClass('selected')){ //if selected
    asset_input.attr('data-status', "active");
  }else{
    asset_input.attr('data-status', "");
  }
  asset_input.trigger('change');//for any autosave function watching
}

function applyAutosaveDataToTextAttributes(){
  $('.giveMeData').each(function(){
    $(this).attr('data-product_id', $('#id_product_id').val());
    attribute = $(this).attr('id').replace("id_","");
    $(this).attr('data-attribute', attribute);
  });
}

function applyAutosaveEvents(){
  $('.autosave').each(function(){
    $(this).autosave({
      url:$('#product-ajax-url').attr('value'),
      before:function(){$(this).addClass('updating')},
      success:function(){$(this).removeClass('updating').addClass('saved')},
      error:function(){$(this).removeClass('updating').addClass('error')}
    });
  });
}

function fileUploadAction(){
  this.apply = function(file_input, display_div){
    var this_file_input = file_input;
    var this_display_div = display_div;

    var progress_div = this_file_input.closest('.photo-upload-div').find('.progress');
    progress_div.hide();
    var progress_bar = progress_div.find('.bar');

    this_file_input.fileupload({
      dataType: 'json',
      url: "http://api.cloudinary.com/v1_1/anou/image/upload",

      send: function (e, data) {
        progress_div.show();
      },

      progress: function (e, data) {
        var progress = parseInt(data.loaded / data.total * 100, 10);
        progress_bar.css('width', progress + '%');
      },

      done: function (e, data) {
        response_data = data['response']();
        response = response_data.result;
        //load thumb_url into display div
        thumb_url = response['url'].replace("upload","upload/t_thumb");
        this_display_div.html('<img src="' + thumb_url + '">');
        //save photo_id in form field
        photo_save_input = this_display_div.closest('.photo-upload-div').find('.photo-id-save');
        photo_save_input.attr('value', response['url']);
        photo_save_input.trigger('change');
        //hide progress bar
        progress_bar.css('width', '0%');
        progress_div.hide();
      }
    });//end fileupload
  }
}

function updateSummary(){
  //set photo
  first_photo_url = $('#photo1').closest('.photo-upload-div').find('img').attr('src');
  if(!first_photo_url){/*do nothing*/}else{
    summary_pinky_url = first_photo_url.replace('thumb','pinky');
    $('.summary-photo').find('img').attr('src', summary_pinky_url);
  }
  //set price and Anou fee
  seller_price = parseInt($('#id_price').val());
  if (seller_price !== ""){
    $('#summary-price').attr('value', seller_price);
    anou_fee = parseInt(seller_price * 0.15);
    $('#summary-anou-fee').attr('value', anou_fee);
  }
  //set shipping cost and totals
  weight = $('#id_weight').val();
  shipping_option_id = $('#id_shipping_options').val().trim();
  if ((weight !== "") && (shipping_option_id != "")){
    shipping_cost = parseInt(weight/3);//ajax call to calculate shipping cost
    $('#summary-shipping-cost').attr('value', shipping_cost);
    total = seller_price + anou_fee + shipping_cost;
    $('#summary-total').attr('value', total);
    USD_total = parseInt(total / 8.5);//pull conversion rate from controller
    $('#summary-USD').attr('value', USD_total);
  }
}

//https://github.com/cfurrow/jquery.autosave.js
//example:
//  $("input").autosave({url:"/save",success:function(){},error:function(){}});
//
jQuery.fn.autosave=function(e){function n(e){var n=/^data\-(\w+)$/,r={};r.value=e.value;r.name=e.name;t.each(e.attributes,function(e,t){n.test(t.nodeName)&&(r[n.exec(t.nodeName)[1]]=t.value)});return r}var t=jQuery;t.each(this,function(){var r=t(this),i={data:{},event:"change",success:function(){},error:function(){},before:function(){}};e=t.extend(i,e);var s=n(this),o=s.event||e.event;r.on(o,function(){var r=t(this);s.value=r.val();s=t.extend(s,n(this));var i=s.url?s.url:e.url;e.before&&e.before.call(this,r);t.ajax({url:i,data:s,success:function(t){e.success(t,r)},error:function(t){e.error(t,r)}})})})};
