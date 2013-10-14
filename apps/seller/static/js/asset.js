$().ready( function(){
  //run on page load

  //show exit-button when focused on input (mobile)
  $('input,textarea').on('focus', function(){
    $(this).closest('.asset-fields').find('.go').show();
    $(this).closest('.asset-fields').find('.delete-asset').hide();
  });
  $('.go').on('click', function(){
    $(this).closest('.asset-fields').find('.go').hide();
  });

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
  this.apply = function(file_input){
    var iframe_fallback = false;

    var this_file_input = file_input;
    var image_data = {}
    var spinner = new Spinner()
    var spinner_div = this_file_input.closest('.image-upload-div').find('.spinner-div');
    var forms_div = this_file_input.closest('.image-upload-div').find('.image-forms');

    //hide progress
    this_file_input.closest('.asset-media').find('.progress').hide();
    //show user actionable items
    this_file_input.closest('.image-upload-div').find('.image-forms');

    //apply upload action callbacks
    this_file_input.fileupload({
      //forceIframeTransport: true,
      dataType: 'json',
      url: $('#upload-url').val(),

      submit: function(e, data){
        // call server to get signed form data
        var data_form = forms_div.find('.data-form');
        data.formData = getFormData(data_form);

        image_data = data.formData;
        image_data['ilk'] = $(forms_div).find('.ilk').val();
        image_data['rank'] = $(forms_div).find('.rank').val();
        image_data['ilkrank'] = image_data.ilk + image_data.rank
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
            $('#progress-bar-'+image_data.ilkrank).css('width', '0%');
            $('#progress-'+image_data.ilkrank).show();
          }

          //show loading and hide interaction elements
          spinner.spin(document.getElementById($(spinner_div).attr('id')));
          $(spinner_div).show();
          forms_div.hide();
        }
      },

      //'data' not available in iframe mode from here on
      //and the following callbacks don't even happen on Android 2.3

      progress: function (e, data) {
        //animate the progress bar during upload
        var progress = parseInt(data.loaded / data.total * 95, 10);
        $('#progress-bar-'+image_data.ilkrank).css('width', progress + '%');
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
        $('#progress-'+image_data.ilkrank).hide();
        spinner.stop();
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
      form_data = data //dictionary object of values cloudinary needs
    },
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
    dataType: 'json',
  })

  .done(function(data, textStatus, jqXHR){
    switch(jqXHR.status){

      case 200: //image exists, load it and hide loading animations
        $('#image-'+image_data.ilkrank).find('img').attr('src', data.thumb_url);
        $('#progress-'+image_data.ilkrank).hide();
        $('#spinner-'+image_data.ilkrank).hide();
        $('#image-forms-'+image_data.ilkrank).show();

        //update the asset
        $('#asset-'+image_data.ilk+image_data.rank)
        .removeClass('empty')
        .removeClass('error')
        .addClass('saved');

        addAssetForms();
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
    $('#asset-'+image_data.ilk+image_data.rank).addClass('error');
  });
}
