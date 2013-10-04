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

    var progress_div = this_file_input.closest('.asset, .seller-media').find('.progress');
    progress_div.hide();
    var progress_bar = progress_div.find('.bar');

    this_file_input.fileupload({
      dataType: 'json',
      url: $('#upload-url').val(),

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
        thumb_url = response['url'].replace("upload","upload/c_fill,g_center,h_225,q_85,w_300");
        this_display_div.html('<img src="' + thumb_url + '">');
        //save image_id in form field
        image_field = this_display_div.closest('.asset, #seller-account').find('.image-url');
        image_field.attr('value',response['url']).trigger('change');
        //hide progress bar
        progress_bar.css('width', '0%');
        progress_div.hide();
      }
    });//end fileupload
  }
}
