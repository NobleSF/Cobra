$().ready( function(){
  //run on page load
  uploader = new fileUploadAction();
  uploader.apply($('#requirement-images').find('.image-input'));

  $.get("/admin/countries", function(data){
    var selected_country = $('#country').val();
    var html = "<select class='autosave' id='country' name='country'>";
    if(!selected_country){
      html += "<option value=''></option>";
    }
    $.each(data, function(i, item) {
      html += "<option value='" + item + "' ";
      if(item == selected_country){
        html += "selected='selected' ";
      }
      html += ">" + item + "</option>";
    });
    html += "</select>";
    $('#country').replaceWith(html);
    $('#country').autosave({
      url:    $('#autosave-url').val()
    });
  });

  $(".autosave").autosave({
      url:    $('#autosave-url').val(),
      method: "POST",
      event:  "change",
      done:   function(data){
        if ($(this).attr('data-cancel') == "cancel"){
          window.location.replace("/admin/commissions");
        }
      }
  });

  //activate requirement image uploading
  uploader = new fileUploadAction();
  uploader.apply($('#requirement-image-upload').find('.image-input'));
  uploader.apply($('#requirement-photo-upload').find('.photo-input'));

});

//Photo and Image Uploading
function fileUploadAction(){
  this.apply = function(file_input){
    var iframe_fallback = false;

    var this_file_input = file_input;
    var image_data = {}

    var forms_div = this_file_input.closest('.upload-div').find('.upload-forms');

    //hide progress
    //this_file_input.closest('.upload').find('.progress').hide();
    //show user actionable items
    //this_file_input.closest('.upload').find('.image-forms');

    //apply upload action callbacks
    this_file_input.fileupload({
      //forceIframeTransport: true,
      dataType: 'json',
      url: $('#requirement-image-upload-url').val(),

      submit: function(e, data){
        // call server to get signed form data
        var data_form = forms_div.find('.data-form');
        data.formData = getFormData(data_form);

        image_data = data.formData;
        image_data['commission_id'] = $(forms_div).find('.commission-id').val();
      },

      send: function (e, data) {
        //using iframe fallback?
        if (data.dataType.indexOf('iframe') >= 0){iframe_fallback = true;}

        if (data.files[0].name.length > 0){//because Android will try to send nothing

          if (iframe_fallback){
            //we don't know when the download will finish
            //set timer to try loadImage in 10 sec
            setTimeout(function(){
              loadImage(image_data);
            }, 10000); //wait 10 seconds

          }else{
            //not using iframe, so we can show a progress bar
            $('#progress-bar-'+image_data.commission_id).css('width', '0%');
            $('#progress-'+image_data.commission_id).show();
          }

          //show loading and hide interaction elements
          forms_div.hide();
        }
      },

      //'data' not available in iframe mode from here on
      //and the following callbacks don't even happen on Android 2.3

      progress: function (e, data) {
        //animate the progress bar during upload
        var progress = parseInt(data.loaded / data.total * 95, 10);
        $('#progress-bar-'+image_data.commission_id).css('width', progress + '%');
      },

      done: function (e, data) {
        //the data cloudinary returns, but we don't need it.
        //response_data = data['response']();
        //response = response_data.result;

        if (!iframe_fallback){

          //confirm success on server, load thumbnail
          loadImage(image_data);
        }
      },

      always: function (e, data) {
        //we're done here, hide the progress bar
        $('#progress-'+image_data.commission_id).hide();

        forms_div.show();
      }
    });//end fileupload
  }
}

function getFormData(form){//just a generic ajax call that returns resulting response
  var form_data = {};
  $.ajax({
    async: false, //function needs the result before it can continue
    cache: false, //don't cache, time-sensitive variables
    type: form.attr('method'),
    url: form.attr('action'),
    data: form.serialize(),
    dataType: 'json',

    success: function(data){
      form_data = data; //dictionary object of values cloudinary needs
    }
  });
  return form_data;
}

function loadImage(image_data){
  //ask our server if the upload completed and get the thumb_url to load the image

  $.ajax({
    async: false,
    url: $('#upload-check-url').val(),
    cache: false,
    data: image_data,
    dataType: 'json'
  })

  .done(function(data, textStatus, jqXHR){
    switch(jqXHR.status){

      case 200: //image exists, load it and hide loading animations
        $('#image-'+image_data.commission_id).find('img').attr('src', data.thumb_url);
        $('#progress-'+image_data.commission_id).hide();

        $('#image-forms-'+image_data.commission_id).show();
        break;

      case 204: //image does not exist yet, wait and try again
        setTimeout(function(){
          loadImage(image_data);
        }, 2000); //wait 2 seconds and try again

      case 404: //internet cut out
        //todo: reload page?
        break;
    }
  })
  .fail(function(){ //well.. that sucks
    //$('#asset-'+image_data.ilk+image_data.rank).addClass('error');
  });
}
