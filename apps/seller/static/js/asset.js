$().ready( function(){
  //run on page load
});

function applyAssetAutosave(asset_div) {
  asset_div.find('.autosave').autosave({
    url:$('#save-asset-url').val(),
    before:saveAssetBefore,
    success:saveAssetSuccess,
    error:saveAssetError
  });
}

function saveAssetBefore($this_element){
  var this_asset = $this_element.closest('.asset');
  //set to 'saving'
  this_asset.removeClass('empty');
  this_asset.removeClass('error');
  this_asset.removeClass('saved');
  this_asset.addClass('saving');

  //check if we need a new asset form
  addAssetForms();
}

function saveAssetSuccess(data, $this_element){
  var this_asset = $this_element.closest('.asset');
  //set to 'saved'
  this_asset.removeClass('saving');
  this_asset.addClass('saved');
}

function saveAssetError(error,$this_element){
  var this_asset = $this_element.closest('.asset');
  //set to 'saving'
  this_asset.removeClass('saving');
  this_asset.addClass('error');
}

function applyAssetDeleteAction(asset_div){
  asset_div.find('.delete-asset').click(function(){
    var asset = $(this).closest('.asset');

    //set asset to 'soon-dead'
    asset.addClass('soon-dead');

    $.ajax({
      url:$('#delete-asset-url').val(),
      data:{'ilk':  asset.find('input#id_ilk').val(),
            'rank': asset.find('input#id_rank').val()}
    })
    .success(function(data){
      //slideUp animation and delete element and events from DOM
      asset.slideUp(500, function(){asset.remove();});
    });
  });
}

function fileUploadAction(){
  this.apply = function(file_input, display_div){
    var this_file_input = file_input;
    var this_display_div = display_div;
    //prepare to predict the url in advance
    var image_url = $('#download-url').val() + "_unique_id_.jpg";

    var progress_div = this_file_input.closest('.asset-media').find('.progress');
    var button_div = this_file_input.closest('.image-upload-div').find('.image-form');
    progress_div.hide();
    button_div.show();
    var progress_bar = progress_div.find('.bar');
    var iframe_fallback = false;

    var spinner_id = progress_div.closest('.image-upload-div').find('.spinner-div').attr('id');
    var spinner_target = document.getElementById(spinner_id);
    var spinner = new Spinner()

    this_file_input.fileupload({
      //forceIframeTransport: true,
      dataType: 'json',
      url: $('#upload-url').val(),

      submit: function(e, data){
        var spinner_id = progress_div.closest('.image-upload-div').find('.spinner-div').attr('id');
        var spinner_target = document.getElementById(spinner_id);
        spinner.spin(spinner_target);

        // call server to get signed form data
        var form = progress_bar.closest('.image-upload-div').find('.data-form');
        data.formData = getFormData(form);

        //reset and save the url we should get back
        image_url = image_url.replace("_unique_id_", data.formData['public_id']);
      },

      send: function (e, data) {
        if (data.dataType.indexOf('iframe') >= 0){
          //using iframe fallback, so use loadImage to bring it back later
          iframe_fallback = true;
          //download the image afterwards
          setTimeout(function(){
            loadImage(progress_div, image_url, spinner);
          }, 20000); //wait 20 seconds

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

        //load thumb_url into display div
        if (!iframe_fallback){
          loadThumb(response['url'], this_display_div);
          storeImageURL(response['url'], this_display_div);
          spinner.stop();
        }
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

function loadImage(progress_div, image_url, spinner){
  $.ajax({
      url: image_url,
      type:'HEAD',
      cache: false, //in case it caches a 404 before the image is ready to download
      processData: false,

  }).success(function(){
    //image exists, so load it up and and hide the loading animation
    display_div = progress_div.closest('.image-upload-div').find('.image');
    loadThumb(image_url, display_div);
    storeImageURL(image_url, display_div);
    spinner.stop();

  }).error(function(){
    //image doesn't exist yet, wiat 10 sec and try again.
    setTimeout(function(){
      loadImage(progress_div, image_url, spinner);
    }, 5000); //wait 5 seconds and try again
  });
}

function loadThumb(url, display_div){ //load thumb_url into display div
  thumb_url = url.replace("upload","upload/c_fill,g_center,h_225,q_85,w_300");
  display_div.html('<img src="' + thumb_url + '">');
  //progress_div.closest('.image-upload-div').find('.image img').attr('src', image_url);
}

function storeImageURL(url, display_div){
  image_save_input = display_div.closest('.asset').find('#id_image_url');
  image_save_input.attr('value', url);
  image_save_input.trigger('change');
}
