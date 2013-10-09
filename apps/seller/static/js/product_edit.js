$().ready( function(){
  //run on page load
  //$(window).resize(function() {});

  //focus on inputs when icon clicked
  $('i').click(function(){
    $(this).closest('table').find('input').focus()
  });

  //show exit-button when focused on input (mobile)
  $('#id_price, #id_weight, #id_width, #id_height, #id_length')
  .on('focus', function(){
    $(this).closest('td').next('td').next('td').find('button')
    .css('opacity', '1');
  });
  $('#id_price, #id_weight, #id_width, #id_height, #id_length')
  .on('blur', function(){
    $(this).closest('td').next('td').next('td').find('button')
    .css('opacity', '0.01');
  });

  $('#id_weight').on('blur', function(){
    envelope = $('#shipping-option-chooser-section .asset[store-object_id=2]');
    if ($(this).val() > 450){
      //should use a box, so hide the envelope shipping option
      if ($(envelope).hasClass('selected')){
        $(envelope).click();
      }
      envelope.hide();
    }else{
      envelope.show();
    }
  });

  markAssignedAssetsAsSelected();

  //activate the "show more" link in the summary
  $('.total-cost').bind('click', function(){
    $('.extra').toggle();
  });

  //selection actions for choosing assets, etc
  $('.asset').each( function(){
    $(this).bind('click', function(){
      $(this).toggleClass('active');
      $(this).toggleClass('selected');
      toggleStoreAssetId($(this));
      toggleActiveState($(this));
    });
  });

  applyAutosaveDataToTextAttributes();
  applyAutosaveEvents();

  //validate form and show confirmation
  $('#submit').bind('click', function(){
    if (validateForm()){
      //todo: show progress spinner over button
      //and but bring back button if upload fails

      $.ajax({
        url: $('#product-ajax-url').attr('value'),
        data: { 'attribute':"active",
                'status': "yes",
                'product_id': $('#product-id').val()
              },
      }).success(function(){
        $('#product-edit-form').hide();
        $('#floating-photo').remove();
        $('#confirmation').show();
        $.scrollTo('#header');
      });

    }else{
      $.scrollTo($('.attention').first(), 1100);
    }
  });

});//end .ready

function markAssignedAssetsAsSelected(){
  //actual assets
  asset_ids = $('#id_assets').val().split(" ");
  $.each(asset_ids, function(index, value){
    if (value !== ""){
      var btn = $('[store-input_id="assets"][store-object_id="'+value+'"]');
      $(btn).addClass("active").addClass("selected");
    }
  });
  //colors
  color_ids = $('#id_colors').val().split(" ");
  $.each(color_ids, function(index, value){
    if (value !== ""){
      var btn = $('[store-input_id="colors"][store-object_id="'+value+'"]');
      $(btn).addClass("active").addClass("selected");
    }
  });
  //shipping options
  shipping_option_ids = $('#id_shipping_options').val().split(" ");
  $.each(shipping_option_ids, function(index, value){
    if (value !== ""){
      var btn = $('[store-input_id="shipping_options"][store-object_id="'+value+'"]');
      $(btn).addClass("active").addClass("selected");
    }
  });
}

function toggleStoreAssetId(asset_element){
  asset_id = asset_element.attr('store-object_id');
  input_element = $('#id_'+asset_element.attr('store-input_id'));
  input_element_value = input_element.attr('value');
  if (input_element_value === undefined){input_element_value=""}

  if (asset_element.hasClass('selected')){ //if selected
    if (!input_element_value.match(asset_id)){ //if does not already contain id
      input_element_value = input_element_value + ' ' + asset_id;
      input_element.attr('value', input_element_value);
    }
  }else{ //remove id
    input_element_value = input_element_value.replace(asset_id, '');
    input_element.attr('value', input_element_value);
  }
  input_element.trigger('change');//for any autosave function watching
}

function toggleActiveState(asset_element){
  asset_input = asset_element.find('input');
  if (asset_element.hasClass('selected')){ //if selected
    asset_input.attr('data-status', "active");
  }else{
    asset_input.attr('data-status', "");
  }
  asset_input.trigger('change');//for any autosave function watching
}

function applyAutosaveDataToTextAttributes(){
  $('.giveMeData').each(function(){
    $(this).attr('data-product_id', $('#id_product_id').val());
    attribute = $(this).attr('id').replace("id_","");
    $(this).attr('data-attribute', attribute);
  });
}

function applyAutosaveEvents(){
  $('.autosave').each(function(){
    $(this).autosave({
      url:$('#product-ajax-url').attr('value'),
      before:function(){$(this).addClass('updating');},
      success:function(data){
        $(this).removeClass('updating').addClass('saved');
        updateSummary(data);
      },
      error:function(){$(this).removeClass('updating').addClass('error');}
    });
  });
}

function updateSummary(data){
  //set photo
  first_photo_url = $('#photo1').closest('.photo-upload-div').find('img').attr('src');
  if(!first_photo_url){/*do nothing*/
  }else{
    $('#summary-section').find('.summary-image').find('img').attr('src', first_photo_url);
    $('#floating-photo').find('.image').find('img').attr('src', first_photo_url);
    $('#confirmation').find('.image').find('img').attr('src', first_photo_url);
  }
  //set price and Anou fee
  seller_price = data.summary_price;
  if (seller_price !== ""){
    $('#summary-price').html(seller_price);
  }
  //set shipping cost and totals
  shipping_cost = data.summary_shipping_cost
  if (parseInt(shipping_cost) !== 0){
    $('#summary-shipping').html(shipping_cost);
  }else{
    $('#summary-shipping').html("");
  }
  total = parseInt(seller_price) + parseInt(shipping_cost)
  $('#summary-total').html(total);
}

function validateForm(){
  //remove previously applied attention classes
  $('.attention').removeClass('attention');
  no_errors = true

  //product type selected
  if($('#product-chooser-section').find('.selected').length === 0){
    $('#product-chooser-section').addClass('attention');
    no_errors = false
  }
  //artisan selected
  if($('#artisan-chooser-section').find('.selected').length === 0){
    $('#artisan-chooser-section').addClass('attention');
    no_errors = false
  }
  //photo
  if($('#photos').find('.photo').first().find('img').length === 0){
    $('#photos-section').addClass('attention');
    no_errors = false
  }
  //price
  if(!($('#id_price').val() > 0)){
    $('#price-section').addClass('attention');
    no_errors = false
  }
  //weight provided
  if(!($('#id_weight').val() > 0)){
    $('#measurements-section').addClass('attention');
    no_errors = false
  }
  //shipping option selected
  if($('#id_shipping_options').val().trim().length === 0){
    $('#shipping-option-chooser-section').addClass('attention');
    no_errors = false
  }

  //run scripts to remove attention classes at interaction
  if (!no_errors){
    $('#photos').find('.photo-form').click(function(){
      $(this).closest('photos-section').removeClass('attention');
    });
    $('#product-chooser-section').click(function(){
      $(this).removeClass('attention');
    });
    $('#artisan-chooser-section').click(function(){
      $(this).removeClass('attention');
    });
    $('#id_price').click(function(){
      $(this).closest('#price-section').removeClass('attention');
    });
    $('#id_weight').click(function(){
      $(this).closest('#measurements-section').removeClass('attention');
    });
    $('#shipping-option-chooser-section').click(function(){
      $(this).removeClass('attention');
    });
  }

  return no_errors
}

//https://github.com/cfurrow/jquery.autosave.js
//example:
//  $("input").autosave({url:"/save",success:function(){},error:function(){}});
//
jQuery.fn.autosave=function(e){function n(e){var n=/^data\-(\w+)$/,r={};r.value=e.value;r.name=e.name;t.each(e.attributes,function(e,t){n.test(t.nodeName)&&(r[n.exec(t.nodeName)[1]]=t.value)});return r}var t=jQuery;t.each(this,function(){var r=t(this),i={data:{},event:"change",success:function(){},error:function(){},before:function(){}};e=t.extend(i,e);var s=n(this),o=s.event||e.event;r.on(o,function(){var r=t(this);s.value=r.val();s=t.extend(s,n(this));var i=s.url?s.url:e.url;e.before&&e.before.call(this,r);t.ajax({url:i,data:s,success:function(t){e.success(t,r)},error:function(t){e.error(t,r)}})})})};

// http://archive.plugins.jquery.com/project/ScrollTo
// Copyright (c) 2007-2012 Ariel Flesler - aflesler(at)gmail(dot)com | http://flesler.blogspot.com
// Dual licensed under MIT and GPL. @author Ariel Flesler @version 1.4.3.1
;(function($){var h=$.scrollTo=function(a,b,c){$(window).scrollTo(a,b,c)};h.defaults={axis:'xy',duration:parseFloat($.fn.jquery)>=1.3?0:1,limit:true};h.window=function(a){return $(window)._scrollable()};$.fn._scrollable=function(){return this.map(function(){var a=this,isWin=!a.nodeName||$.inArray(a.nodeName.toLowerCase(),['iframe','#document','html','body'])!=-1;if(!isWin)return a;var b=(a.contentWindow||a).document||a.ownerDocument||a;return/webkit/i.test(navigator.userAgent)||b.compatMode=='BackCompat'?b.body:b.documentElement})};$.fn.scrollTo=function(e,f,g){if(typeof f=='object'){g=f;f=0}if(typeof g=='function')g={onAfter:g};if(e=='max')e=9e9;g=$.extend({},h.defaults,g);f=f||g.duration;g.queue=g.queue&&g.axis.length>1;if(g.queue)f/=2;g.offset=both(g.offset);g.over=both(g.over);return this._scrollable().each(function(){if(e==null)return;var d=this,$elem=$(d),targ=e,toff,attr={},win=$elem.is('html,body');switch(typeof targ){case'number':case'string':if(/^([+-]=)?\d+(\.\d+)?(px|%)?$/.test(targ)){targ=both(targ);break}targ=$(targ,this);if(!targ.length)return;case'object':if(targ.is||targ.style)toff=(targ=$(targ)).offset()}$.each(g.axis.split(''),function(i,a){var b=a=='x'?'Left':'Top',pos=b.toLowerCase(),key='scroll'+b,old=d[key],max=h.max(d,a);if(toff){attr[key]=toff[pos]+(win?0:old-$elem.offset()[pos]);if(g.margin){attr[key]-=parseInt(targ.css('margin'+b))||0;attr[key]-=parseInt(targ.css('border'+b+'Width'))||0}attr[key]+=g.offset[pos]||0;if(g.over[pos])attr[key]+=targ[a=='x'?'width':'height']()*g.over[pos]}else{var c=targ[pos];attr[key]=c.slice&&c.slice(-1)=='%'?parseFloat(c)/100*max:c}if(g.limit&&/^\d+$/.test(attr[key]))attr[key]=attr[key]<=0?0:Math.min(attr[key],max);if(!i&&g.queue){if(old!=attr[key])animate(g.onAfterFirst);delete attr[key]}});animate(g.onAfter);function animate(a){$elem.animate(attr,f,g.easing,a&&function(){a.call(this,e,g)})}}).end()};h.max=function(a,b){var c=b=='x'?'Width':'Height',scroll='scroll'+c;if(!$(a).is('html,body'))return a[scroll]-$(a)[c.toLowerCase()]();var d='client'+c,html=a.ownerDocument.documentElement,body=a.ownerDocument.body;return Math.max(html[scroll],body[scroll])-Math.min(html[d],body[d])};function both(a){return typeof a=='object'?a:{top:a,left:a}}})(jQuery);
