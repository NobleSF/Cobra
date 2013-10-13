$().ready( function(){

  //apply events for photo uploads
  $('.photo-upload-div').each(function(){
    var file_input = $(this).find('.photo-input');
    uploader = new fileUploadAction();
    uploader.apply(file_input);
  });

});//end .ready

function fileUploadAction(){
  this.apply = function(file_input){
    var iframe_fallback = false; //not the uploader plugin's default method

    var this_file_input = file_input;
    var photo_data = {}
    var spinner = new Spinner();
    var spinner_div = this_file_input.closest('.photo-upload-div').find('.spinner-div');
    var forms_div = this_file_input.closest('.photo-upload-div').find('.photo-forms');

    //hide progress
    this_file_input.closest('.photo-upload-div').find('.progress').hide();
    //show user actionable items
    this_file_input.closest('.photo-upload-div').find('.photo-forms').show();

    //apply upload action and callbacks
    this_file_input.fileupload({
      //forceIframeTransport: true,
      dataType: 'json',
      url: $('#upload-url').val(),

      submit: function(e, data){
        // call server to get signed form data
        var data_form = forms_div.find('.data-form');
        data.formData = getFormData(data_form);

        photo_data = data.formData;
        photo_data['product_id'] = $(forms_div).find('.product').val();
        photo_data['rank'] = $(forms_div).find('.rank').val();
      },

      send: function (e, data) {
        //using iframe fallback?
        if (data.dataType.indexOf('iframe') >= 0){iframe_fallback = true;}

        if (data.files[0].name.length > 0){//because Android will try to send nothing

          if (iframe_fallback){
            //we don't know when the download will finish
            //set timer to try loadPhoto in 10 sec
            setTimeout(function(){
              loadPhoto(photo_data);
            }, 10000); //10 seconds

          }else{
            //not using iframe, so we can show a progress bar
            $('#progress-bar-'+photo_data.rank).css('width', '0%');
            $('#progress-'+photo_data.rank).show();
          }

          //show loading and hide interaction elements
          spinner.spin(document.getElementById($(spinner_div).attr('id')));
          $(spinner_div).show();
          forms_div.hide();
        }
      },

      //'data' variable not available in iframe mode from here on
      //and the following callbacks don't even happen on Android 2.3

      progress: function (e, data) {
        //animate the progress bar during upload
        var progress = parseInt(data.loaded / data.total * 95, 10);
        $('#progress-bar-'+photo_data.rank).css('width', progress + '%');
      },

      done: function (e, data) {
        //the data cloudinary returns, but we don't need it.
        //response_data = data['response']();
        //response = response_data.result;

        if (!iframe_fallback){
          //confirm success on server, load thumbnail
          loadPhoto(photo_data);
        }
      },

      always: function (e, data) {
        //we're done here, hide the progress bar
        $('#progress-'+photo_data.rank).hide();
        spinner.stop();
        forms_div.show();
      }
    });//end fileupload
  }
}

function getFormData(form){ //just a generic ajax call that returns resulting response
  var form_data = {};
  $.ajax({
    async:    false, //function needs the result before it can continue
    cache:    false, //don't cache, time-sensitive variables
    type:     form.attr('method'),
    url:      form.attr('action'),
    data:     form.serialize(),
    dataType: 'json',

    success: function(data){
      form_data = data; //dictionary object of values cloudinary needs
    }
  });
  return form_data;
}

function loadPhoto(photo_data){
  //ask our server if the upload completed and get the thumb_url to load the photo

  $.ajax({
    async:    false,
    url:      $('#upload-check-url').val(),
    cache:    false,
    data:     photo_data,
    dataType: 'json'
  })

  .done(function(data, textStatus, jqXHR){
    switch(jqXHR.status){

      case 200: //photo exists, load it and hide loading animations
        $('#photo-'+photo_data.rank).find('img').attr('src', data.thumb_url);
        $('#progress-'+photo_data.rank).hide();
        $('#spinner-'+photo_data.rank).hide();
        $('#photo-forms-'+photo_data.rank).show();
        updateSummary();
        break;

      case 204: //photo does not exist yet, wait and try again
        setTimeout(function(){
          loadPhoto(photo_data);
        }, 2000); //wait 2 seconds and try again

      case 404: //internet cut out
        //todo: reload page?
        break;
    }
  })

  .fail(function(){ //well.. that sucks
  });

  return True
}
