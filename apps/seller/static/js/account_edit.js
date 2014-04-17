$().ready( function(){

  //activate seller image uploading
  uploader = new fileUploadAction();
  uploader.apply($('#seller-account').find('.image-input'));

  $('#artisan-tab').trigger('click');//activate first tab

});//end .ready

$('.language-btn').click(function(){
  language = $(this).attr('data-lang');
  $('.lang').hide();
  $('.lang-'+language).show();
  $('.language-btn').removeClass('btn-success');
  $(this).addClass('btn-success');
});

$('.asset-tab').click(function(){//when an asset tab is clicked
  //make this tab active
  $('.asset-tab').removeClass('active');
  $(this).addClass('active');
  //hide all asset containers, then show the right one
  $('.asset-container').hide();
  $('#'+$(this).attr('ilk')+'-container').show();
});

function arrangeAssetForms(){
  $('#asset-forms .asset').each(function(){
    //move to proper asset container
    if ($(this).attr('ilk').length > 0){
      $(this).appendTo('#'+$(this).attr('ilk')+'-container');

      //activate image uploading
      uploader = new fileUploadAction();
      uploader.apply($(this).find('.image-input'));
    }
  });
}

function addAssetForms(){
  //copy blank asset forms to asset containers so there is always an extra new one.
  $('.asset-container').each(function(){ //for each asset container
    var this_container = $(this);
    var num_empty_forms = 0;

    //for each asset form inside the containter
    this_container.children('.asset').each(function(){
      this_asset = $(this);
      //count empty forms
      if (this_asset.hasClass('empty')){
        num_empty_forms++;
      }
    });

    //if there are no empty forms, add one
    if (num_empty_forms == 0){
      //grab an empty form from the hidden .asset-forms div
      var new_asset = $('#asset-forms .asset').first().clone(false);
      //assign the container's ilk to asset
      var ilk = this_container.attr('ilk');
      applyAssetIlkRank(new_asset, ilk);

      //place it in the container
      new_asset.appendTo(this_container);
      autosaveAssets($(new_asset).find('.autosave'));

      //activate image uploading
      uploader = new fileUploadAction();
      uploader.apply(new_asset.find('.image-input'));
    }//end if
  });//end for each asset-container
}

function applyAssetIlkRank(asset, ilk, rank){
  if (!rank){
    //calculate what the next rank should be
    var highest_rank = 0;
    $('.asset').each(function(){
      var this_rank = $(this).attr('rank');
      if (parseInt(this_rank) > highest_rank){
        highest_rank = parseInt(this_rank);
      }
    })
    rank = highest_rank + 1;
  }

  //set attrs on asset div and autosave fields
  $(asset).attr('id', $(asset).attr('id')+ilk+rank);
  $(asset).attr('ilk',ilk);
  $(asset).attr('rank', rank);
  $(asset).find('.autosave').each(function(){
    $(this).attr('id', ilk+rank+$(this).attr('id'));
    $(this).attr('data-ilk', ilk);
    $(this).attr('data-rank', rank);
  });

  //values in image form fields
  $(asset).find('.image-upload-div').find('.ilk').attr('id', "image-"+ilk+rank+"-ilk");
  $(asset).find('.image-upload-div').find('.ilk').attr('value', ilk);
  $(asset).find('.image-upload-div').find('.rank').attr('id', "image-"+ilk+rank+"-rank");
  $(asset).find('.image-upload-div').find('.rank').attr('value', rank);

  $(asset).find('*').each(function(){
    var id = $(this).attr('id');
    if (id && id.indexOf("ilkrank") !== -1){
      $(this).attr('id', id.replace("ilkrank", ilk+rank));
    }
  })

  //remove unecessary phone and category fields
  if(ilk == 'artisan'){
    $(asset).find('.asset-category').remove();
  }else if(ilk == 'product'){
    $(asset).find('.asset-phone').remove();
  }else{
    $(asset).find('.asset-phone').remove();
    $(asset).find('.asset-category').remove();
  }
}
