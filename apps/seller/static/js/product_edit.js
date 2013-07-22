$().ready( function(){
  //run on page load
  var viewport_width = $(window).width();
  if (viewport_width < 500){
  }
  //$(window).resize(function() {});

  //only show the first 5 photo upload divs
  num_divs = 0;
  $('.photo-upload-div').each(function(){
    num_divs += 1;
    if (num_divs > 5){
      $(this).hide();
    }
  });

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

  //apply events for photo uploads
  $('.photo-upload-div').each(function(){
    file_input = $(this).find('.photo-input');
    display_div = $(this).find('.photo');
    uploader = new fileUploadAction();
    uploader.apply(file_input, display_div);
  });

  applyAutosaveDataToTextAttributes();
  applyAutosaveEvents();

  //set events for updating the summary
  //$('#photos').find('img').addClass('updates-summary');//just the first photo
  //$('#id_price').addClass('updates-summary');
  //$('#id_weight').addClass('updates-summary');
  //$('#id_shipping_options').addClass('updates-summary');
  //$('.updates-summary').each(function(){
  //  $(this).on('change', function(){updateSummary();});
  //});

  //validate form and show confirmation
  $('#submit').bind('click', function(){
    if (validateForm()){
      //show progress spinner over button

      $.ajax({
        url: $('#product-ajax-url').attr('value'),
        data: { 'attribute':"active",
                'status': "yes",
                'product_id': $('#product-id').val()
              },
      }).success(function(){
        $('#product-edit-form').hide();
        $('#confirmation').show();
      });

    }else{
      $('body').scrollTo($('.attention').first(), 1100);
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

function fileUploadAction(){
  this.apply = function(file_input, display_div){
    var this_file_input = file_input;
    var this_display_div = display_div;
    var photo_url = "http://res.cloudinary.com/anou/image/upload/_unique_id_.jpg";

    var progress_div = this_file_input.closest('.photo-upload-div').find('.progress');
    var button_div = this_file_input.closest('.photo-upload-div').find('.photo-form');
    progress_div.hide();
    button_div.show();
    var progress_bar = progress_div.find('.bar');
    var iframe_fallback = false;

    var spinner_id = progress_div.closest('.photo-upload-div').find('.spinner-div').attr('id');
    var spinner_target = document.getElementById(spinner_id);
    var spinner = new Spinner()

    this_file_input.fileupload({
      //forceIframeTransport: true,
      dataType: 'json',
      url: "http://api.cloudinary.com/v1_1/anou/image/upload",

      submit: function(e, data){
        var spinner_id = progress_div.closest('.photo-upload-div').find('.spinner-div').attr('id');
        var spinner_target = document.getElementById(spinner_id);
        spinner.spin(spinner_target);

        // call server to get signed form data
        var form = progress_bar.closest('.photo-upload-div').find('.data-form');
        data.formData = getFormData(form);

        //reset and save the url we should get back
        photo_url = "http://res.cloudinary.com/anou/image/upload/_unique_id_.jpg";
        photo_url = photo_url.replace("_unique_id_", data.formData['public_id']);
      },

      send: function (e, data) {
        if (data.dataType.indexOf('iframe') >= 0){
          //using iframe fallback, so use loadPhoto to bring it back later
          iframe_fallback = true;
          loadPhoto(progress_div, photo_url, spinner);
        }else{
          //not using iframe, so we can show a progress bar
          progress_bar.css('width', '0%');
          progress_div.show();
          button_div.hide();
        }
      },

      //'data' not available in iframe mode from here on
      //and the following callbacks don't even happen on Android 2.3

      progress: function (e, data) {
        var progress = parseInt(data.loaded / data.total * 100, 10);
        progress_bar.css('width', progress + '%');
      },

      done: function (e, data) {
        response_data = data['response']();
        response = response_data.result;
        if (!iframe_fallback){
          loadThumb(response['url'], this_display_div);
          storePhotoURL(response['url'], this_display_div);
          spinner.stop();
        }
      },

      always: function (e, data) {
        //we're done here, hide the progress bar
        progress_bar.css('width', '0%');
        progress_div.hide();
        button_div.show();
      }
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

function loadPhoto(progress_div, photo_url, spinner){
  $.ajax({
      url: photo_url,
      //cache: true, // i don't think this is possible, it should be a new image
      processData: false,

  }).success(function(){
    //photo exists, so load it up and and hide the loading animation
    display_div = progress_div.closest('.photo-upload-div').find('.photo');
    loadThumb(photo_url, display_div);
    storePhotoURL(photo_url, display_div);
    spinner.stop();

  }).error(function(){
    //photo doesn't exist yet, wiat 10 sec and try again.
    setTimeout(function(){
      loadPhoto(progress_div, photo_url, spinner);
    }, 10000); //wait 10 seconds
  });
}

function loadThumb(url, display_div){ //load thumb_url into display div
  thumb_url = url.replace("upload","upload/t_thumb");
  display_div.html('<img src="' + thumb_url + '">');
  //progress_div.closest('.photo-upload-div').find('.photo img').attr('src', photo_url);
}

function storePhotoURL(url, display_div){
  photo_save_input = display_div.closest('.photo-upload-div').find('.photo-id-save');
  photo_save_input.attr('value', url);
  photo_save_input.trigger('change');
}

function updateSummary(data){
  //set photo
  first_photo_url = $('#photo1').closest('.photo-upload-div').find('img').attr('src');
  if(!first_photo_url){/*do nothing*/
  }else{
    //summary_pinky_url = first_photo_url.replace('thumb','pinky');
    $('#summary-section').find('.summary-image').find('img').attr('src', first_photo_url);
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

//http://fgnass.github.io/spin.js/
//example:
//  var target = document.getElementById('foo');
//  var spinner = new Spinner(opts).spin(target);
;(function(t,e){if(typeof exports=="object")module.exports=e();else if(typeof define=="function"&&define.amd)define(e);else t.Spinner=e()})(this,function(){"use strict";var t=["webkit","Moz","ms","O"],e={},i;function o(t,e){var i=document.createElement(t||"div"),o;for(o in e)i[o]=e[o];return i}function n(t){for(var e=1,i=arguments.length;e<i;e++)t.appendChild(arguments[e]);return t}var r=function(){var t=o("style",{type:"text/css"});n(document.getElementsByTagName("head")[0],t);return t.sheet||t.styleSheet}();function s(t,o,n,s){var a=["opacity",o,~~(t*100),n,s].join("-"),f=.01+n/s*100,l=Math.max(1-(1-t)/o*(100-f),t),d=i.substring(0,i.indexOf("Animation")).toLowerCase(),u=d&&"-"+d+"-"||"";if(!e[a]){r.insertRule("@"+u+"keyframes "+a+"{"+"0%{opacity:"+l+"}"+f+"%{opacity:"+t+"}"+(f+.01)+"%{opacity:1}"+(f+o)%100+"%{opacity:"+t+"}"+"100%{opacity:"+l+"}"+"}",r.cssRules.length);e[a]=1}return a}function a(e,i){var o=e.style,n,r;if(o[i]!==undefined)return i;i=i.charAt(0).toUpperCase()+i.slice(1);for(r=0;r<t.length;r++){n=t[r]+i;if(o[n]!==undefined)return n}}function f(t,e){for(var i in e)t.style[a(t,i)||i]=e[i];return t}function l(t){for(var e=1;e<arguments.length;e++){var i=arguments[e];for(var o in i)if(t[o]===undefined)t[o]=i[o]}return t}function d(t){var e={x:t.offsetLeft,y:t.offsetTop};while(t=t.offsetParent)e.x+=t.offsetLeft,e.y+=t.offsetTop;return e}var u={lines:12,length:7,width:5,radius:10,rotate:0,corners:1,color:"#000",direction:1,speed:1,trail:100,opacity:1/4,fps:20,zIndex:2e9,className:"spinner",top:"auto",left:"auto",position:"relative"};function p(t){if(typeof this=="undefined")return new p(t);this.opts=l(t||{},p.defaults,u)}p.defaults={};l(p.prototype,{spin:function(t){this.stop();var e=this,n=e.opts,r=e.el=f(o(0,{className:n.className}),{position:n.position,width:0,zIndex:n.zIndex}),s=n.radius+n.length+n.width,a,l;if(t){t.insertBefore(r,t.firstChild||null);l=d(t);a=d(r);f(r,{left:(n.left=="auto"?l.x-a.x+(t.offsetWidth>>1):parseInt(n.left,10)+s)+"px",top:(n.top=="auto"?l.y-a.y+(t.offsetHeight>>1):parseInt(n.top,10)+s)+"px"})}r.setAttribute("role","progressbar");e.lines(r,e.opts);if(!i){var u=0,p=(n.lines-1)*(1-n.direction)/2,c,h=n.fps,m=h/n.speed,y=(1-n.opacity)/(m*n.trail/100),g=m/n.lines;(function v(){u++;for(var t=0;t<n.lines;t++){c=Math.max(1-(u+(n.lines-t)*g)%m*y,n.opacity);e.opacity(r,t*n.direction+p,c,n)}e.timeout=e.el&&setTimeout(v,~~(1e3/h))})()}return e},stop:function(){var t=this.el;if(t){clearTimeout(this.timeout);if(t.parentNode)t.parentNode.removeChild(t);this.el=undefined}return this},lines:function(t,e){var r=0,a=(e.lines-1)*(1-e.direction)/2,l;function d(t,i){return f(o(),{position:"absolute",width:e.length+e.width+"px",height:e.width+"px",background:t,boxShadow:i,transformOrigin:"left",transform:"rotate("+~~(360/e.lines*r+e.rotate)+"deg) translate("+e.radius+"px"+",0)",borderRadius:(e.corners*e.width>>1)+"px"})}for(;r<e.lines;r++){l=f(o(),{position:"absolute",top:1+~(e.width/2)+"px",transform:e.hwaccel?"translate3d(0,0,0)":"",opacity:e.opacity,animation:i&&s(e.opacity,e.trail,a+r*e.direction,e.lines)+" "+1/e.speed+"s linear infinite"});if(e.shadow)n(l,f(d("#000","0 0 4px "+"#000"),{top:2+"px"}));n(t,n(l,d(e.color,"0 0 1px rgba(0,0,0,.1)")))}return t},opacity:function(t,e,i){if(e<t.childNodes.length)t.childNodes[e].style.opacity=i}});function c(){function t(t,e){return o("<"+t+' xmlns="urn:schemas-microsoft.com:vml" class="spin-vml">',e)}r.addRule(".spin-vml","behavior:url(#default#VML)");p.prototype.lines=function(e,i){var o=i.length+i.width,r=2*o;function s(){return f(t("group",{coordsize:r+" "+r,coordorigin:-o+" "+-o}),{width:r,height:r})}var a=-(i.width+i.length)*2+"px",l=f(s(),{position:"absolute",top:a,left:a}),d;function u(e,r,a){n(l,n(f(s(),{rotation:360/i.lines*e+"deg",left:~~r}),n(f(t("roundrect",{arcsize:i.corners}),{width:o,height:i.width,left:i.radius,top:-i.width>>1,filter:a}),t("fill",{color:i.color,opacity:i.opacity}),t("stroke",{opacity:0}))))}if(i.shadow)for(d=1;d<=i.lines;d++)u(d,-2,"progid:DXImageTransform.Microsoft.Blur(pixelradius=2,makeshadow=1,shadowopacity=.3)");for(d=1;d<=i.lines;d++)u(d);return n(e,l)};p.prototype.opacity=function(t,e,i,o){var n=t.firstChild;o=o.shadow&&o.lines||0;if(n&&e+o<n.childNodes.length){n=n.childNodes[e+o];n=n&&n.firstChild;n=n&&n.firstChild;if(n)n.opacity=i}}}var h=f(o("group"),{behavior:"url(#default#VML)"});if(!a(h,"transform")&&h.adj)c();else i=a(h,"animation");return p});

// http://archive.plugins.jquery.com/project/ScrollTo
// Copyright (c) 2007-2012 Ariel Flesler - aflesler(at)gmail(dot)com | http://flesler.blogspot.com
// Dual licensed under MIT and GPL. @author Ariel Flesler @version 1.4.3.1
;(function($){var h=$.scrollTo=function(a,b,c){$(window).scrollTo(a,b,c)};h.defaults={axis:'xy',duration:parseFloat($.fn.jquery)>=1.3?0:1,limit:true};h.window=function(a){return $(window)._scrollable()};$.fn._scrollable=function(){return this.map(function(){var a=this,isWin=!a.nodeName||$.inArray(a.nodeName.toLowerCase(),['iframe','#document','html','body'])!=-1;if(!isWin)return a;var b=(a.contentWindow||a).document||a.ownerDocument||a;return/webkit/i.test(navigator.userAgent)||b.compatMode=='BackCompat'?b.body:b.documentElement})};$.fn.scrollTo=function(e,f,g){if(typeof f=='object'){g=f;f=0}if(typeof g=='function')g={onAfter:g};if(e=='max')e=9e9;g=$.extend({},h.defaults,g);f=f||g.duration;g.queue=g.queue&&g.axis.length>1;if(g.queue)f/=2;g.offset=both(g.offset);g.over=both(g.over);return this._scrollable().each(function(){if(e==null)return;var d=this,$elem=$(d),targ=e,toff,attr={},win=$elem.is('html,body');switch(typeof targ){case'number':case'string':if(/^([+-]=)?\d+(\.\d+)?(px|%)?$/.test(targ)){targ=both(targ);break}targ=$(targ,this);if(!targ.length)return;case'object':if(targ.is||targ.style)toff=(targ=$(targ)).offset()}$.each(g.axis.split(''),function(i,a){var b=a=='x'?'Left':'Top',pos=b.toLowerCase(),key='scroll'+b,old=d[key],max=h.max(d,a);if(toff){attr[key]=toff[pos]+(win?0:old-$elem.offset()[pos]);if(g.margin){attr[key]-=parseInt(targ.css('margin'+b))||0;attr[key]-=parseInt(targ.css('border'+b+'Width'))||0}attr[key]+=g.offset[pos]||0;if(g.over[pos])attr[key]+=targ[a=='x'?'width':'height']()*g.over[pos]}else{var c=targ[pos];attr[key]=c.slice&&c.slice(-1)=='%'?parseFloat(c)/100*max:c}if(g.limit&&/^\d+$/.test(attr[key]))attr[key]=attr[key]<=0?0:Math.min(attr[key],max);if(!i&&g.queue){if(old!=attr[key])animate(g.onAfterFirst);delete attr[key]}});animate(g.onAfter);function animate(a){$elem.animate(attr,f,g.easing,a&&function(){a.call(this,e,g)})}}).end()};h.max=function(a,b){var c=b=='x'?'Width':'Height',scroll='scroll'+c;if(!$(a).is('html,body'))return a[scroll]-$(a)[c.toLowerCase()]();var d='client'+c,html=a.ownerDocument.documentElement,body=a.ownerDocument.body;return Math.max(html[scroll],body[scroll])-Math.min(html[d],body[d])};function both(a){return typeof a=='object'?a:{top:a,left:a}}})(jQuery);
