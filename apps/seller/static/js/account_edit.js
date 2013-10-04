$().ready( function(){

  //assign bootstrap classes
  $('#asset-tabs').children('li').first().addClass('active');//first tab active
  $('#artisan_tab').trigger('click');//activate first tab

  //run on page load for seller form
  //autosave requires data- attributes
  //set ilk and rank to dummy value ('seller')
  applyDataAttrs($('#seller-account'), 'seller', 'seller');
  applyEvents($('#seller-account'), to_assets=false);//just for seller image now
  applySellerAutosave();//autosave seller form elements

  //run on page load for assets
  arrangeAssetForms();//move assets to their respective tab
  addAssetForms();//create blank assets as needed

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
  asset_ilk = $(this).attr('id').replace('_tab','');
  $('#'+asset_ilk+'_container').show();
});

function applySellerAutosave() {
  $('#seller-account').find('.autosave').autosave({
    url:$('#save-seller-url').val(),
    before:saveSellerBefore,
    success:saveSellerSuccess,
    error:saveSellerError
  });
}

function saveSellerBefore($this_element){
  //start 'updating' visual
  $this_element.closest('#seller-account').removeClass('error').removeClass('saved').addClass('updating');
}
function saveSellerSuccess(data,$this_element){
  //finished visual
  $this_element.closest('.asset').removeClass('updating').addClass('saved');
}
function saveSellerError(error,$this_element){
  //error visual
  $this_element.closest('.asset').removeClass('updating').addClass('error');
}

function arrangeAssetForms(){
  $('#asset-forms .asset').each(function(){
    //autosave requires data- attributes
    applyDataAttrs($(this));
    //apply autosave and any other js event handlers
    applyEvents($(this));

    var ilk = $(this).find('#id_ilk').val();
    if (ilk != ''){
      //move to proper asset container
      $(this).appendTo('#'+ilk+'_container');
    }
  });
}

function addAssetForms(){
  //copy blank asset forms to asset containers so there is always an extra new one.

  //for each asset container
  $('.asset-container').each(function(){
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
      var ilk = this_container.attr('id').replace('_container','');

      //calculate what the next rank should be
      var highest_rank = 0;
      $('.asset').each(function(){
        var this_rank = $(this).find('input#id_rank').val();
        if (parseInt(this_rank) > highest_rank){
          highest_rank = parseInt(this_rank);
        }
      })
      var next_rank = highest_rank + 1;
      new_asset.find('input#id_rank').attr('value', next_rank);
      new_asset.find('input#id_ilk').attr('value', ilk);

      new_asset.attr('id', ('asset-'+ilk+next_rank));

      //place it in the container
      new_asset.appendTo(this_container);
      applyDataAttrs(new_asset);
      applyEvents(new_asset);

    }//end if
  });//end for each asset-container
}

function applyDataAttrs(asset_div, ilk, rank){
  //organize input fields and add data- attributes for autosave ajax

  ilk = ilk || asset_div.find('#id_ilk').val();
  rank = rank || asset_div.find('#id_rank').val();

  //if not product container, hide category element
  if ( ilk !== 'product'){
    asset_div.find('.asset-category').hide();
  }else{
    asset_div.find('.asset-category').show();
  }

  if (ilk !=='artisan'){
    asset_div.find('.asset-phone').hide();
  }else{
    asset_div.find('.asset-phone').show();
  }

  //give the image div a new unique id
  asset_div.find('.image').attr('id', (ilk+rank+'-image-div'));

  //give the image input a new unique id
  asset_div.find('.image-input').attr('id', (ilk+rank+'-image-input'));

  //tell form and autosave elements the ilk and rank
  asset_div.find('.autosave').attr('data-ilk', ilk);
  asset_div.find('.autosave').attr('data-rank', rank);
}

function applyEvents(asset_div, to_assets){
  //for images uploader
  image_input = asset_div.find('.image-input');
  image_div = asset_div.find('.image');
  uploader = new fileUploadAction();
  uploader.apply(image_input, image_div);

  //for input fields
  to_assets = to_assets || true;//parameter defaults to true if not provided
  if (to_assets){
    applyAssetAutosave(asset_div);
    applyAssetDeleteAction(asset_div);
  }
}

//https://github.com/cfurrow/jquery.autosave.js
//example:
//  $("input").autosave({url:"/save",success:function(){},error:function(){}});
//
jQuery.fn.autosave=function(e){function n(e){var n=/^data\-(\w+)$/,r={};r.value=e.value;r.name=e.name;t.each(e.attributes,function(e,t){n.test(t.nodeName)&&(r[n.exec(t.nodeName)[1]]=t.value)});return r}var t=jQuery;t.each(this,function(){var r=t(this),i={data:{},event:"change",success:function(){},error:function(){},before:function(){}};e=t.extend(i,e);var s=n(this),o=s.event||e.event;r.on(o,function(){var r=t(this);s.value=r.val();s=t.extend(s,n(this));var i=s.url?s.url:e.url;e.before&&e.before.call(this,r);t.ajax({url:i,data:s,success:function(t){e.success(t,r)},error:function(t){e.error(t,r)}})})})};
