$().ready( function(){
  //assign bootstrap classes
  $('button').addClass('btn');
  $('.file-button').addClass('btn').html('<i class="icon-camera"></i>');

  //run on page load
  num_divs = 0
  $('.photo-upload-div').each(function(){
    num_divs += 1;
    if (num_divs > 5){
      $(this).hide();
    }
  });

  $('#summary-show-more').bind('click', function(){
    $('.summary-detail').show();
    $('#summary-show-more').hide();
  });

  $('.asset').each( function(){
    $(this).bind('click', function(){
      $(this).toggleClass('selected');
      toggleSaveAssetId($(this));
    });
  });

  $('.photo-upload-div').each(function(){
    file_input = $(this).find('.image-input');
    display_div = $(this).find('.photo');
    uploader = new fileUploadAction();
    uploader.apply(file_input, display_div);
  });

});//end .ready

function toggleSaveAssetId(asset_element){
  asset_id = asset_element.attr('data-object-id');
  input_element = $('#'+asset_element.attr('data-input-id'));
  input_element_value = input_element.attr('value');

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

function fileUploadAction(){
  this.apply = function(file_input, display_div){
    var this_file_input = file_input;
    var this_display_div = display_div;

    var progress_div = this_file_input.closest('.photo-upload-div').find('.progress');
    progress_div.hide();
    var progress_bar = progress_div.find('.bar');

    this_file_input.fileupload({
      dataType: 'json',
      url: $('#photo-ajax-url').val(),

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
        this_display_div.html('<img src="' + response['thumb_url'] + '">');
        //save image_id in form field
        image_ids_input = this_display_div.closest('#product-edit-form')
                                          .find('input#images');
        image_ids_input.attr('value',response['image_id']);
        image_ids_input.trigger('change');//for any autosave function watching
        //hide progress bar
        progress_div.hide()
      }
    });//end fileupload
  }
}

//https://github.com/cfurrow/jquery.autosave.js
//example:
//  $("input").autosave({url:"/save",success:function(){},error:function(){}});
//
jQuery.fn.autosave=function(e){function n(e){var n=/^data\-(\w+)$/,r={};r.value=e.value;r.name=e.name;t.each(e.attributes,function(e,t){n.test(t.nodeName)&&(r[n.exec(t.nodeName)[1]]=t.value)});return r}var t=jQuery;t.each(this,function(){var r=t(this),i={data:{},event:"change",success:function(){},error:function(){},before:function(){}};e=t.extend(i,e);var s=n(this),o=s.event||e.event;r.on(o,function(){var r=t(this);s.value=r.val();s=t.extend(s,n(this));var i=s.url?s.url:e.url;e.before&&e.before.call(this,r);t.ajax({url:i,data:s,success:function(t){e.success(t,r)},error:function(t){e.error(t,r)}})})})};
