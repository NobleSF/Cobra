$(function(){//on page load

  $('.carousel').carousel({
    interval: false
  })

});

$('#unapprove').click(function(){
  button = $(this)
  $.get($(this).attr('data-approve-url'),
        {product_id:$(this).attr('data-product-id'), action:"hold"}
  ).done(function(){
    button.html('Unapproved.').addClass('disabled');
  });
})

$('.read-more').on('click', function(){
  $(this).prev('.short-description').hide();
  $(this).hide();
  $(this).next('.long-description').show();
});

//PRODUCT ANIMATION
$('.product').hover(
  function(){ //on mouseenter
    if(! navigator.userAgent.match(/(iPhone|iPod|iPad)/i)){
      $(this).find('.hover-show').each(function(){
        $(this).show();
      });
    }
  },
  function(){//on mouseleave
    if(! navigator.userAgent.match(/(iPhone|iPod|iPad)/i)){
      $(this).find('.hover-show').each(function(){
        $(this).fadeOut();
      });
    }
  }
);

$('#custom-order-button').click(function(){
  $('#custom-order').show();
  $.scrollTo($('#custom-order').first(), 600);
  $.scrollTo("-=50px", 100, {axis:'y'});
  //scrollTo #custom-order
});

$('#custom-order-submit-button').click(function(){
  if ($('#custom-order-message').val() == "") {
    $('#custom-order-message').addClass('error');
  }else if ($('#custom-order-email').val() == "") {
    $('#custom-order-email').addClass('error');
  }else{
    $('#custom-order-submit-button h2').html("Sending...");
    $('#custom-order-submit-button').attr('disabled', 'True')

    $.ajax({url: $('#custom-order-url').val(),
            data: { 'product_id': $('#custom-order-product-id').val(),
                    'email': $('#custom-order-email').val(),
                    'length': $('#custom-order-width').val(),
                    'width': $('#custom-order-length').val(),
                    'message': $('#custom-order-message').val()
                  },
            type: "POST"})
    .done(function(){
      $('#custom-order-form').hide();// hide form
      $('#custom-order-success').css('display', 'block');// show success
    })
    .fail(function(){
      $('#custom-order-fail').css('display', 'block');// show fail
      $('#custom-order-submit-button').hide(); //h ide submit button
    })
  }
});

//SCROLLTO from http://archive.plugins.jquery.com/project/ScrollTo
// Copyright (c) 2007-2012 Ariel Flesler - aflesler(at)gmail(dot)com | http://flesler.blogspot.com
// Dual licensed under MIT and GPL. @author Ariel Flesler @version 1.4.3.1
;(function($){var h=$.scrollTo=function(a,b,c){$(window).scrollTo(a,b,c)};h.defaults={axis:'xy',duration:parseFloat($.fn.jquery)>=1.3?0:1,limit:true};h.window=function(a){return $(window)._scrollable()};$.fn._scrollable=function(){return this.map(function(){var a=this,isWin=!a.nodeName||$.inArray(a.nodeName.toLowerCase(),['iframe','#document','html','body'])!=-1;if(!isWin)return a;var b=(a.contentWindow||a).document||a.ownerDocument||a;return/webkit/i.test(navigator.userAgent)||b.compatMode=='BackCompat'?b.body:b.documentElement})};$.fn.scrollTo=function(e,f,g){if(typeof f=='object'){g=f;f=0}if(typeof g=='function')g={onAfter:g};if(e=='max')e=9e9;g=$.extend({},h.defaults,g);f=f||g.duration;g.queue=g.queue&&g.axis.length>1;if(g.queue)f/=2;g.offset=both(g.offset);g.over=both(g.over);return this._scrollable().each(function(){if(e==null)return;var d=this,$elem=$(d),targ=e,toff,attr={},win=$elem.is('html,body');switch(typeof targ){case'number':case'string':if(/^([+-]=)?\d+(\.\d+)?(px|%)?$/.test(targ)){targ=both(targ);break}targ=$(targ,this);if(!targ.length)return;case'object':if(targ.is||targ.style)toff=(targ=$(targ)).offset()}$.each(g.axis.split(''),function(i,a){var b=a=='x'?'Left':'Top',pos=b.toLowerCase(),key='scroll'+b,old=d[key],max=h.max(d,a);if(toff){attr[key]=toff[pos]+(win?0:old-$elem.offset()[pos]);if(g.margin){attr[key]-=parseInt(targ.css('margin'+b))||0;attr[key]-=parseInt(targ.css('border'+b+'Width'))||0}attr[key]+=g.offset[pos]||0;if(g.over[pos])attr[key]+=targ[a=='x'?'width':'height']()*g.over[pos]}else{var c=targ[pos];attr[key]=c.slice&&c.slice(-1)=='%'?parseFloat(c)/100*max:c}if(g.limit&&/^\d+$/.test(attr[key]))attr[key]=attr[key]<=0?0:Math.min(attr[key],max);if(!i&&g.queue){if(old!=attr[key])animate(g.onAfterFirst);delete attr[key]}});animate(g.onAfter);function animate(a){$elem.animate(attr,f,g.easing,a&&function(){a.call(this,e,g)})}}).end()};h.max=function(a,b){var c=b=='x'?'Width':'Height',scroll='scroll'+c;if(!$(a).is('html,body'))return a[scroll]-$(a)[c.toLowerCase()]();var d='client'+c,html=a.ownerDocument.documentElement,body=a.ownerDocument.body;return Math.max(html[scroll],body[scroll])-Math.min(html[d],body[d])};function both(a){return typeof a=='object'?a:{top:a,left:a}}})(jQuery);
