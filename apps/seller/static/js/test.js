$().ready( function(){

  //apply events for photo uploads
  $('.photo-upload-div').each(function(){
    file_input = $(this).find('.photo-input');
    display_div = $(this).find('.photo');
    uploader = new fileUploadAction();
    uploader.apply(file_input, display_div);
  });

});//end .ready

// What we're going to do:
// just use a minimal form for the photo upload html
// when a file is loaded, first make an extra ajax call to our system
// creating a public_id, timestamp, signature, etc.
// add that new data to the form with the file upload
// submit everything to cloudinary
// when upload finishes, load image using the public_id we specified
// if all goes well, autosave the photo url as usual.

function fileUploadAction(){
  this.apply = function(file_input, display_div){
    var this_file_input = file_input;
    var this_display_div = display_div;
    var photo_url = "http://res.cloudinary.com/anou/image/upload/_unique_id_.jpg";

    var progress_div = this_file_input.closest('.photo-upload-div').find('.progress');
    progress_div.hide();
    var progress_bar = progress_div.find('.bar');
    var iframe_fallback = false;

    this_file_input.fileupload({
      //forceIframeTransport: true,
      dataType: 'json',
      url: "http://api.cloudinary.com/v1_1/anou/image/upload",

      submit: function (e, data ){
        //get url for loading gif and replace the image with it.
        loading_img_url = progress_div.closest('.photo-upload-div').find('.loading img').attr('src');
        progress_div.closest('.photo-upload-div').find('.photo img').attr('src', loading_img_url);
        //reset photo_url
        photo_url = "http://res.cloudinary.com/anou/image/upload/_unique_id_.jpg";

        // call server to get signed form data
        var form = progress_bar.closest('.photo-upload-div').find('.data-form');
        data.formData = getFormData(form);

        //save the url we should get back
        photo_url = photo_url.replace("_unique_id_", data.formData['public_id']);
      },

      send: function (e, data) {
        if (data.dataType.indexOf('iframe') >= 0){
          loadPhoto(progress_div, photo_url);
        }else{
          progress_bar.css('width', '0%');
          progress_div.show();
        }
      },

      // 'data' not available in iframe mode from here on
      // and the following callbacks don't even happen on Android 2.3

      progress: function (e, data) {
        var progress = parseInt(data.loaded / data.total * 100, 10);
        progress_bar.css('width', progress + '%');
      },

      done: function (e, data) {},

      always: function (e, data) {
        if (data.dataType.indexOf('iframe') < 0){//if not using iframe
          progress_div.closest('.photo-upload-div').find('.photo img').attr('src', photo_url);
          progress_div.hide();
        }
      },

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
    progress_div.closest('.photo-upload-div').find('.photo img').attr("src", photo_url);
    progress_div.hide();

  }).error(function(){
    //photo doesn't exist yet, wiat 10 sec and try again.
    setTimeout(function(){
      loadPhoto(progress_div, photo_url);
    }, 10000); //wait 10 seconds
  });
}
