$().ready( function(){
  //run on page load
  image_ajax_url = $('#image_ajax_url').val();
  asset_ajax_url = $('#asset_ajax_url').val();

  //apply autosave function
  $('.asset').find('.autosave').autosave({
    url:asset_ajax_url,
    before:saveAssetBefore,
    success:saveAssetSuccess,
    error:saveAssetError
  });

});

function saveAssetBefore($this_element){
  //start 'updating' visual
  $this_element.closest('.asset').removeClass('error').removeClass('saved').addClass('updating');
  //set pending asset_id data for all elements
  if ($this_element.closest('.asset').find('#id_asset_id').val() == 'none'){
    $this_element.closest('.asset').find('#id_asset_id').attr('value',"pending");
    $this_element.closest('.asset').find('.autosave').attr('data-asset_id',"pending");
  }
  //provide new asset form if necessary
  addAssetForms();
}

function saveAssetSuccess(data,$this_element){
  //set asset_id data for all elements
  $this_element.closest('.asset').find('#id_asset_id').attr('value',data.asset_id);
  $this_element.closest('.asset').find('.autosave').attr('data-asset_id',data.asset_id);
  //finished visual
  $this_element.closest('.asset').removeClass('updating').addClass('saved');
  //remove if deleted
  if (data.asset_id == "deleted"){
    alert("asset has been deleted");
    $this_element.closest('.asset').fadeOut().remove();
  }
}

function saveAssetError(error,$this_element){
  //error visual
  $this_element.closest('.asset').removeClass('updating').addClass('error');
}

function applyFileUploadAction(file_input, image_destination){
  progress_bar = image_destination.siblings('.progress');
  progress_bar.hide();

  file_input.fileupload({
    dataType: 'json',
    url: image_ajax_url,

    //progressall: function (e, data) {
    //  var progress = parseInt(data.loaded / data.total * 100, 10);
    //  progress_bar.find('.bar').css('width', (progress*0.9) + '%');
    //},

    done: function (e, data) {
      response_data = data['response']();
      response = response_data.result;
      image_destination.html('<img src="' + response['thumb_url'] + '">');
      image_destination.closest('.asset').find('.image-id')
        .attr('value',response['image_id']).trigger('change');
    }
  });//end fileupload
}

//https://github.com/cfurrow/jquery.autosave.js
//example:
//  $("input").autosave({url:"/save",success:function(){},error:function(){}});
//
jQuery.fn.autosave=function(e){function n(e){var n=/^data\-(\w+)$/,r={};r.value=e.value;r.name=e.name;t.each(e.attributes,function(e,t){n.test(t.nodeName)&&(r[n.exec(t.nodeName)[1]]=t.value)});return r}var t=jQuery;t.each(this,function(){var r=t(this),i={data:{},event:"change",success:function(){},error:function(){},before:function(){}};e=t.extend(i,e);var s=n(this),o=s.event||e.event;r.on(o,function(){var r=t(this);s.value=r.val();s=t.extend(s,n(this));var i=s.url?s.url:e.url;e.before&&e.before.call(this,r);t.ajax({url:i,data:s,success:function(t){e.success(t,r)},error:function(t){e.error(t,r)}})})})};
