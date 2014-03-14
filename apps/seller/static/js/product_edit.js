$().ready( function(){ //run on page load
  //$(window).resize(function() {});

  var fail_count = 0;
  function countFail(autosave_status){
    autosave_status = autosave_status || {}
    if( autosave_status.code == "404" ){
      fail_count++;
    }
    if( fail_count > 1 ){
      // todo: do something
    }
  }

  //focus on inputs when icon clicked
  $('i').click(function(){
    $(this).closest('table').find('input').focus()
  });

  //show/hide exit-button for elements that have one: .has-exit-button
  $(document).on({
    'focus': function(){
      $(this).closest('td').next('td').next('td').find('button')
      .css('opacity', '1');
    },
    'blur': function(){
      $(this).closest('td').next('td').next('td').find('button')
      .css('opacity', '0.01');
    }
  }, '.has-exit-button');

  //special logic for heavy items, they require a box.
  //todo: take this logic server side
  $('#weight').on('blur', function(){
    envelope = $('#shipping-option-chooser-section .asset[store-object_id=2]');
    if ($(this).val() > 450){
      //heavy items require a box, so hide the envelope shipping option
      if ($(envelope).hasClass('selected')){
        $(envelope).trigger('click'); //a click should de-select and save
      }
      envelope.hide();
    }else{
      envelope.show();
    }
  });

  //activate the "show more" link in the summary
  $('.total-cost').on('click', function(){
    $('.extra').toggle();
  });

  //autosave for inputs
  $('input.autosave').autosave({
    url:      $('#edit-product-url').val(),
    event:    'blur',
    type:     'json',
    data:     {'product_id':$('#product-id').val()},

    before:   function(){
      $(this).removeClass('saved').removeClass('error').addClass('updating');
    },
    done:     function(){
      $(this).removeClass('updating').addClass('saved');
      response_data = $(this).data('autosave-response');
      //if element not in focus, update value
      if( !$(this).is(":focus") && $(this).attr('name') == response_data.name ){
        $(this).val(response_data.value);
      }
      updateSummary($(this).data('autosave-response'));
    },
    fail:     function(){
      $(this).removeClass('updating').addClass('error');
      //todo: if 404 error, trigger this event again
      $(this).val("");
    }
  });

  //autosave for asset buttons
  $('.asset.autosave').autosave({
    url:      $('#edit-product-url').val(),
    event:    'click',
    type:     'json',
    data:     {'product_id':$('#product-id').val()},
    before:   function(){
      $(this).toggleClass('selected');
      if ($(this).hasClass('selected')){
        $(this).attr('data-selected', 'yes');
      }else{
        $(this).attr('data-selected', '');
      }
    },
    done:      function(){
      updateSummary($(this).data('autosave-response'));
    },
    fail:      function(){
      countFail($(this).data('autosave')['status']);
      $(this).toggleClass('selected'); //should toggle back to what it was
    }
  });

  $('#activate').autosave({
    url:      $('#edit-product-url').val(),
    event:    'click',
    type:     'json',
    data:     {'product_id':$('#product-id').val()},
    before:   function(){
      if( !validateForm() ){ //validate form
        $.scrollTo($('.attention').first(), 1100);
      }
      //todo: disable button, show spinner
    },
    done:     function(){
      if( $(this).data('autosave-response')['activated'] ){
        // show confirmation
        $('#product-edit-form').hide();
        $('#floating-photo').remove();
        $('#confirmation').show();
        $.scrollTo('#header');
      }else{
        // if the form looks valid here, but it's not server-side
        // refresh the page and re-run validation
        // or get error location from server
      }
    }
  })

});//end .ready

function updateSummary(data){
  data = typeof data !== 'undefined' ? data : null; //parameter default values

  //set photo
  first_photo_url = $('#photo-1').find('img').attr('src');
  $('#summary-section').find('.summary-image').find('img').attr('src', first_photo_url);
  $('#floating-photo').find('.image').find('img').attr('src', first_photo_url);
  $('#confirmation').find('.image').find('img').attr('src', first_photo_url);

  if (data){
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
}

function validateForm(){
  //remove previously applied attention classes
  $('.attention').removeClass('attention');
  no_errors = true
  //product type selected
  if($('#product-chooser-section .selected').length === 0){
    $('#product-chooser-section').addClass('attention');
    no_errors = false
  }
  //artisan selected
  if($('#artisan-chooser-section .selected').length === 0){
    $('#artisan-chooser-section').addClass('attention');
    no_errors = false
  }
  //photo
  if($('#photos .photo').first().find('img').length === 0){
    $('#photos-section').addClass('attention');
    no_errors = false
  }
  //price
  if(!($('#price').val() > 0)){
    $('#price-section').addClass('attention');
    no_errors = false
  }
  //weight provided
  if(!($('#weight').val() > 0)){
    $('#measurements-section').addClass('attention');
    no_errors = false
  }
  //shipping option selected
  if($('#shipping-option-chooser-section .selected').length === 0){
    $('#shipping-option-chooser-section').addClass('attention');
    no_errors = false
  }
  return no_errors
}
// remove .attention when editing section
$('.section').on('click', function(){
  $(this).removeClass('attention');
});

//AUTOSAVE from https://github.com/tomcounsell/jquery-autosave
//example: $("input").autosave({options});
;(function(a,b,c,d){function g(b,c){this.element=b,this.options=a.extend({},f,c),this._defaults=f,this._name=e,this.init()}var e="autosave",f={url:"",method:"POST",event:"change",data:{},type:"html",debug:!1,before:function(){},done:function(){},fail:function(){},always:function(){}};g.prototype.init=function(){function e(b){var c=/^data\-(\w+)$/,d={};return d.value=b.val()||"",d.name=b.attr("name")||"",a(b[0].attributes).each(function(){c.test(this.nodeName)&&(attribute_name=c.exec(this.nodeName)[1],d[attribute_name]=this.nodeValue)}),d}var b=a(this.element),c=e(b),d=this.options,c=e(b);d.event=c.event||d.event,b.on(d.event,function(c){d.before&&d.before.call(b);var f=e(b);options=a.extend({},d,f);var g=a.extend({},options.data,f);options.debug=="false"&&(options.debug=!1),delete g.url,delete g.method,delete g.type,delete g.debug,g.event=options.event,options.debug?console.log(g):a.ajax({url:options.url,type:options.method,cache:!1,data:g,dataType:options.type}).done(function(a,c,d){b.data("autosave-response",a),b.data("autosave-status",{text:d.statusText,code:d.status}),b.trigger("autosave-done")}).fail(function(a,c,d){b.data("autosave-status",{text:a.statusText,code:a.status}),b.data("autosave-error",d),b.trigger("autosave-fail")}).always(function(){b.trigger("autosave-always")})}),d.done&&b.on("autosave-done",function(){var a=b.data("autosave-response"),c=b.data("autosave-status");options.done.call(b,a,c)}),d.fail&&b.on("autosave-fail",function(){error=b.data("autosave-error"),status=b.data("autosave-status"),options.fail.call(b,error,status)}),d.always&&b.on("autosave-always",function(){status=b.data("autosave-status"),options.always.call(b,status)})},a.fn.autosave=function(a){return this.each(function(){new g(this,a)})}})(jQuery,window,document)

//SCROLLTO from http://archive.plugins.jquery.com/project/ScrollTo
// Copyright (c) 2007-2012 Ariel Flesler - aflesler(at)gmail(dot)com | http://flesler.blogspot.com
// Dual licensed under MIT and GPL. @author Ariel Flesler @version 1.4.3.1
;(function($){var h=$.scrollTo=function(a,b,c){$(window).scrollTo(a,b,c)};h.defaults={axis:'xy',duration:parseFloat($.fn.jquery)>=1.3?0:1,limit:true};h.window=function(a){return $(window)._scrollable()};$.fn._scrollable=function(){return this.map(function(){var a=this,isWin=!a.nodeName||$.inArray(a.nodeName.toLowerCase(),['iframe','#document','html','body'])!=-1;if(!isWin)return a;var b=(a.contentWindow||a).document||a.ownerDocument||a;return/webkit/i.test(navigator.userAgent)||b.compatMode=='BackCompat'?b.body:b.documentElement})};$.fn.scrollTo=function(e,f,g){if(typeof f=='object'){g=f;f=0}if(typeof g=='function')g={onAfter:g};if(e=='max')e=9e9;g=$.extend({},h.defaults,g);f=f||g.duration;g.queue=g.queue&&g.axis.length>1;if(g.queue)f/=2;g.offset=both(g.offset);g.over=both(g.over);return this._scrollable().each(function(){if(e==null)return;var d=this,$elem=$(d),targ=e,toff,attr={},win=$elem.is('html,body');switch(typeof targ){case'number':case'string':if(/^([+-]=)?\d+(\.\d+)?(px|%)?$/.test(targ)){targ=both(targ);break}targ=$(targ,this);if(!targ.length)return;case'object':if(targ.is||targ.style)toff=(targ=$(targ)).offset()}$.each(g.axis.split(''),function(i,a){var b=a=='x'?'Left':'Top',pos=b.toLowerCase(),key='scroll'+b,old=d[key],max=h.max(d,a);if(toff){attr[key]=toff[pos]+(win?0:old-$elem.offset()[pos]);if(g.margin){attr[key]-=parseInt(targ.css('margin'+b))||0;attr[key]-=parseInt(targ.css('border'+b+'Width'))||0}attr[key]+=g.offset[pos]||0;if(g.over[pos])attr[key]+=targ[a=='x'?'width':'height']()*g.over[pos]}else{var c=targ[pos];attr[key]=c.slice&&c.slice(-1)=='%'?parseFloat(c)/100*max:c}if(g.limit&&/^\d+$/.test(attr[key]))attr[key]=attr[key]<=0?0:Math.min(attr[key],max);if(!i&&g.queue){if(old!=attr[key])animate(g.onAfterFirst);delete attr[key]}});animate(g.onAfter);function animate(a){$elem.animate(attr,f,g.easing,a&&function(){a.call(this,e,g)})}}).end()};h.max=function(a,b){var c=b=='x'?'Width':'Height',scroll='scroll'+c;if(!$(a).is('html,body'))return a[scroll]-$(a)[c.toLowerCase()]();var d='client'+c,html=a.ownerDocument.documentElement,body=a.ownerDocument.body;return Math.max(html[scroll],body[scroll])-Math.min(html[d],body[d])};function both(a){return typeof a=='object'?a:{top:a,left:a}}})(jQuery);

//SPINNER from http://fgnass.github.io/spin.js/
//example:
//  var target = document.getElementById('foo');
//  var spinner = new Spinner(opts).spin(target);
;(function(t,e){if(typeof exports=="object")module.exports=e();else if(typeof define=="function"&&define.amd)define(e);else t.Spinner=e()})(this,function(){"use strict";var t=["webkit","Moz","ms","O"],e={},i;function o(t,e){var i=document.createElement(t||"div"),o;for(o in e)i[o]=e[o];return i}function n(t){for(var e=1,i=arguments.length;e<i;e++)t.appendChild(arguments[e]);return t}var r=function(){var t=o("style",{type:"text/css"});n(document.getElementsByTagName("head")[0],t);return t.sheet||t.styleSheet}();function s(t,o,n,s){var a=["opacity",o,~~(t*100),n,s].join("-"),f=.01+n/s*100,l=Math.max(1-(1-t)/o*(100-f),t),d=i.substring(0,i.indexOf("Animation")).toLowerCase(),u=d&&"-"+d+"-"||"";if(!e[a]){r.insertRule("@"+u+"keyframes "+a+"{"+"0%{opacity:"+l+"}"+f+"%{opacity:"+t+"}"+(f+.01)+"%{opacity:1}"+(f+o)%100+"%{opacity:"+t+"}"+"100%{opacity:"+l+"}"+"}",r.cssRules.length);e[a]=1}return a}function a(e,i){var o=e.style,n,r;if(o[i]!==undefined)return i;i=i.charAt(0).toUpperCase()+i.slice(1);for(r=0;r<t.length;r++){n=t[r]+i;if(o[n]!==undefined)return n}}function f(t,e){for(var i in e)t.style[a(t,i)||i]=e[i];return t}function l(t){for(var e=1;e<arguments.length;e++){var i=arguments[e];for(var o in i)if(t[o]===undefined)t[o]=i[o]}return t}function d(t){var e={x:t.offsetLeft,y:t.offsetTop};while(t=t.offsetParent)e.x+=t.offsetLeft,e.y+=t.offsetTop;return e}var u={lines:12,length:7,width:5,radius:10,rotate:0,corners:1,color:"#000",direction:1,speed:1,trail:100,opacity:1/4,fps:20,zIndex:2e9,className:"spinner",top:"auto",left:"auto",position:"relative"};function p(t){if(typeof this=="undefined")return new p(t);this.opts=l(t||{},p.defaults,u)}p.defaults={};l(p.prototype,{spin:function(t){this.stop();var e=this,n=e.opts,r=e.el=f(o(0,{className:n.className}),{position:n.position,width:0,zIndex:n.zIndex}),s=n.radius+n.length+n.width,a,l;if(t){t.insertBefore(r,t.firstChild||null);l=d(t);a=d(r);f(r,{left:(n.left=="auto"?l.x-a.x+(t.offsetWidth>>1):parseInt(n.left,10)+s)+"px",top:(n.top=="auto"?l.y-a.y+(t.offsetHeight>>1):parseInt(n.top,10)+s)+"px"})}r.setAttribute("role","progressbar");e.lines(r,e.opts);if(!i){var u=0,p=(n.lines-1)*(1-n.direction)/2,c,h=n.fps,m=h/n.speed,y=(1-n.opacity)/(m*n.trail/100),g=m/n.lines;(function v(){u++;for(var t=0;t<n.lines;t++){c=Math.max(1-(u+(n.lines-t)*g)%m*y,n.opacity);e.opacity(r,t*n.direction+p,c,n)}e.timeout=e.el&&setTimeout(v,~~(1e3/h))})()}return e},stop:function(){var t=this.el;if(t){clearTimeout(this.timeout);if(t.parentNode)t.parentNode.removeChild(t);this.el=undefined}return this},lines:function(t,e){var r=0,a=(e.lines-1)*(1-e.direction)/2,l;function d(t,i){return f(o(),{position:"absolute",width:e.length+e.width+"px",height:e.width+"px",background:t,boxShadow:i,transformOrigin:"left",transform:"rotate("+~~(360/e.lines*r+e.rotate)+"deg) translate("+e.radius+"px"+",0)",borderRadius:(e.corners*e.width>>1)+"px"})}for(;r<e.lines;r++){l=f(o(),{position:"absolute",top:1+~(e.width/2)+"px",transform:e.hwaccel?"translate3d(0,0,0)":"",opacity:e.opacity,animation:i&&s(e.opacity,e.trail,a+r*e.direction,e.lines)+" "+1/e.speed+"s linear infinite"});if(e.shadow)n(l,f(d("#000","0 0 4px "+"#000"),{top:2+"px"}));n(t,n(l,d(e.color,"0 0 1px rgba(0,0,0,.1)")))}return t},opacity:function(t,e,i){if(e<t.childNodes.length)t.childNodes[e].style.opacity=i}});function c(){function t(t,e){return o("<"+t+' xmlns="urn:schemas-microsoft.com:vml" class="spin-vml">',e)}r.addRule(".spin-vml","behavior:url(#default#VML)");p.prototype.lines=function(e,i){var o=i.length+i.width,r=2*o;function s(){return f(t("group",{coordsize:r+" "+r,coordorigin:-o+" "+-o}),{width:r,height:r})}var a=-(i.width+i.length)*2+"px",l=f(s(),{position:"absolute",top:a,left:a}),d;function u(e,r,a){n(l,n(f(s(),{rotation:360/i.lines*e+"deg",left:~~r}),n(f(t("roundrect",{arcsize:i.corners}),{width:o,height:i.width,left:i.radius,top:-i.width>>1,filter:a}),t("fill",{color:i.color,opacity:i.opacity}),t("stroke",{opacity:0}))))}if(i.shadow)for(d=1;d<=i.lines;d++)u(d,-2,"progid:DXImageTransform.Microsoft.Blur(pixelradius=2,makeshadow=1,shadowopacity=.3)");for(d=1;d<=i.lines;d++)u(d);return n(e,l)};p.prototype.opacity=function(t,e,i,o){var n=t.firstChild;o=o.shadow&&o.lines||0;if(n&&e+o<n.childNodes.length){n=n.childNodes[e+o];n=n&&n.firstChild;n=n&&n.firstChild;if(n)n.opacity=i}}}var h=f(o("group"),{behavior:"url(#default#VML)"});if(!a(h,"transform")&&h.adj)c();else i=a(h,"animation");return p});
