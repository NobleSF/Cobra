$().ready( function(){
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
  $('#id_price').addClass('updates-summary');
  $('#id_weight').addClass('updates-summary');
  $('#id_shipping_option').addClass('updates-summary');
  $('.updates-summary').each(function(){
    $(this).change(updateSummary());
  });
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
      before:function(){$(this).addClass('updating');},
      success:function(){$(this).removeClass('updating').addClass('saved');},
      error:function(){$(this).removeClass('updating').addClass('error');}
    });
  });
}

function fileUploadAction(){
  this.apply = function(file_input, display_div){
    var this_file_input = file_input;
    var this_display_div = display_div;
    var photo_url = "http://res.cloudinary.com/anou/image/upload/_unique_id_.jpg";

    var progress_div = this_file_input.closest('.photo-upload-div').find('.progress');
    var button_div = this_file_input.closest('.photo-upload-div').find('.photo-form');
    progress_div.hide();
    button_div.show();
    var progress_bar = progress_div.find('.bar');
    var iframe_fallback = false;

    this_file_input.fileupload({
      //forceIframeTransport: true,
      dataType: 'json',
      url: "http://api.cloudinary.com/v1_1/anou/image/upload",

      submit: function(e, data){
        //get url for loading gif and replace the image with it.
        loading_img_url = progress_div.closest('.photo-upload-div').find('.loading img').attr('src');
        progress_div.closest('.photo-upload-div').find('.photo img').attr('src', loading_img_url);

        // call server to get signed form data
        var form = progress_bar.closest('.photo-upload-div').find('.data-form');
        data.formData = getFormData(form);

        //reset and save the url we should get back
        photo_url = "http://res.cloudinary.com/anou/image/upload/_unique_id_.jpg";
        photo_url = photo_url.replace("_unique_id_", data.formData['public_id']);
      },

      send: function (e, data) {
        if (data.dataType.indexOf('iframe') >= 0){
          //using iframe fallback, so use loadPhoto to bring it back later
          iframe_fallback = true;
          loadPhoto(progress_div, photo_url);
        }else{
          //not using iframe, so we can show a progress bar
          progress_bar.css('width', '0%');
          progress_div.show();
          button_div.hide();
        }
      },

      //'data' not available in iframe mode from here on
      //and the following callbacks don't even happen on Android 2.3

      progress: function (e, data) {
        var progress = parseInt(data.loaded / data.total * 100, 10);
        progress_bar.css('width', progress + '%');
      },

      done: function (e, data) {
        response_data = data['response']();
        response = response_data.result;

        loadThumb(response['url'], this_display_div);
        storePhotoURL(response['url'], this_display_div);
      },

      always: function (e, data) {
        //we're done here, hide the progress bar
        progress_bar.css('width', '0%');
        progress_div.hide();
        button_div.show();
      }

    });//end fileupload
  }
}

function getFormData(form){
  var form_data = {};
  $.ajax({
    async: false,
    cache: false,
    type: form.attr('method'),
    url: form.attr('action'),
    data: form.serialize(),
    success: function(data){
      form_data = data
      //form_data['api_key'] = data.api_key;
    },
  });
  return form_data;
}

function loadPhoto(progress_div, photo_url){
  $.ajax({
      url: photo_url,
      //cache: true, // i don't think this is possible, it should be a new image
      processData: false,

  }).success(function(){
    //photo exists, so load it up and and hide the loading animation
    display_div = progress_div.closest('.photo-upload-div').find('.photo');
    loadThumb(photo_url, display_div);
    storePhotoURL(photo_url, display_div);
    progress_div.hide();


  }).error(function(){
    //photo doesn't exist yet, wiat 10 sec and try again.
    setTimeout(function(){
      loadPhoto(progress_div, photo_url);
    }, 10000); //wait 10 seconds
  });
}

function loadThumb(url, display_div){ //load thumb_url into display div
  thumb_url = url.replace("upload","upload/t_thumb");
  display_div.html('<img src="' + thumb_url + '">');
  //progress_div.closest('.photo-upload-div').find('.photo img').attr('src', photo_url);
}

function storePhotoURL(url, display_div){
  photo_save_input = display_div.closest('.photo-upload-div').find('.photo-id-save');
  photo_save_input.attr('value', response['url']);
  photo_save_input.trigger('change');
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
