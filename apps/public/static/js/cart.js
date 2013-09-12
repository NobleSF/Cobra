$(function(){//on page load

  //resize things for ipad
  if ((768 < $(window).width()) && ($(window).width() < 979) ||
      navigator.userAgent.match(/(iPhone|iPod|iPad)/i)){
    $('#main-content').removeClass('span8').addClass('span12');
    $('#information').removeClass('span4').addClass('span12');
  }

  $('.autosave').each(function(){
    $(this).autosave({
      url:$('#cart-ajax-url').attr('value'),
      before:function(){$(this).addClass('updating')},
      success:function(){$(this).removeClass('updating').addClass('saved')},
      error:function(){$(this).removeClass('updating').addClass('error')}
    });
  });

});

$('#checkout-button').on('click', function(){
  //hide cart, show checkout
  $('.part1').slideUp(400);
  $('.part2').delay(400).slideDown(400);
});
$('#pay-now-button').on('click', function(){
  //hide cart, show checkout
  if (validateForm()){
    $('#customer-info').slideUp(400);
    $('#payment').delay(400).slideDown(400);
  }
});
$('#cart-return-button').on('click', function(){
  //hide cart, show checkout
  $('.part3').slideUp(400);
  $('.part2').slideUp(400);
  $('.part1').delay(400).slideDown(400);
});

$('#checkout-form').find('#id_email').on('blur', function() {
  $(this).mailcheck({
    suggested: function(element, suggestion) {
      $('#suggested-email').html(suggestion.full);
      $('#email-suggestion').show();
    },
    empty: function(element) {
      $('#suggested-email').html('');
      $('#email-suggestion').hide();
    }
  });
});
$('#suggested-email').click(function(){
  $('#checkout-form').find('#id_email').val($('#suggested-email').html());
  $('#suggested-email').html('');
  $('#email-suggestion').hide();
  $('#checkout-form').find('#id_email').trigger('change');
})

$('input.required').on('change', function(){
  if ($(this).val() == ""){
    $(this).closest('.control-group').addClass('error');
  }else{
    if ($(this).closest('.control-group').hasClass('error')){
      validateForm();
    }
  }
});

function validateForm(){
  var complete = true;
  $('#checkout-form  input.required').each(function(){
    $(this).removeClass('error');
    if ($(this).val() == ""){
      complete = false;
      $(this).closest('.control-group').addClass('error');
      $(this).closest('.control-group').find('.help-inline').fadeOut().fadeIn();
    }else if ($(this).attr('id') == 'id_email'){
      if (!IsEmail($(this).val())){
        complete = false;
        $(this).closest('.control-group').addClass('error');
        $(this).closest('.control-group').find('.help-inline').fadeOut().fadeIn();
      }else{
        $(this).closest('.control-group').removeClass('error');
        $(this).closest('.control-group').find('.help-inline').fadeOut();
      }
    }
  });
  return complete
}

//http://stackoverflow.com/questions/2507030/email-validation-using-jquery
function IsEmail(email) {
  var regex = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
  return regex.test(email);
}

//MANUAL ADMIN ORDERING FUNCTIONS
$('#admin-checkout-button').click(function(){
  if (validateManualCheckout()){
    manualCheckout();
  }
});

function manualCheckout(){
  var checkout_url = $('#manual_checkout_url').val();

  $.get(checkout_url)
  .fail(function(){
    $('#admin-checkout-button').hide('300');
    $('.admin-checkout-error').show('300');
  })
  .done(function(){
    $('input').attr('disabled', 'disabled');
    $('#admin-checkout-button').hide('300');
    $('.admin-checkout-success').show('300');
  });
}

function validateManualCheckout(){
  return true;
}
// END MANUAL ADMIN ORDERING FUNCTIONS

//https://github.com/cfurrow/jquery.autosave.js
//example:
//  $("input").autosave({url:"/save",success:function(){},error:function(){}});
//
jQuery.fn.autosave=function(e){function n(e){var n=/^data\-(\w+)$/,r={};r.value=e.value;r.name=e.name;t.each(e.attributes,function(e,t){n.test(t.nodeName)&&(r[n.exec(t.nodeName)[1]]=t.value)});return r}var t=jQuery;t.each(this,function(){var r=t(this),i={data:{},event:"change",success:function(){},error:function(){},before:function(){}};e=t.extend(i,e);var s=n(this),o=s.event||e.event;r.on(o,function(){var r=t(this);s.value=r.val();s=t.extend(s,n(this));var i=s.url?s.url:e.url;e.before&&e.before.call(this,r);t.ajax({url:i,data:s,success:function(t){e.success(t,r)},error:function(t){e.error(t,r)}})})})};

//use mailcheck on email field
//https://github.com/kicksend/mailcheck
//
/*1.1*/var Kicksend={mailcheck:{threshold:3,defaultDomains:"yahoo.com google.com hotmail.com gmail.com me.com aol.com mac.com live.com comcast.net googlemail.com msn.com hotmail.co.uk yahoo.co.uk facebook.com verizon.net sbcglobal.net att.net gmx.com mail.com".split(" "),defaultTopLevelDomains:"co.uk com net org info edu gov mil".split(" "),run:function(a){a.domains=a.domains||Kicksend.mailcheck.defaultDomains;a.topLevelDomains=a.topLevelDomains||Kicksend.mailcheck.defaultTopLevelDomains;a.distanceFunction=
a.distanceFunction||Kicksend.sift3Distance;var b=Kicksend.mailcheck.suggest(encodeURI(a.email),a.domains,a.topLevelDomains,a.distanceFunction);b?a.suggested&&a.suggested(b):a.empty&&a.empty()},suggest:function(a,b,c,d){a=a.toLowerCase();a=this.splitEmail(a);if(b=this.findClosestDomain(a.domain,b,d)){if(b!=a.domain)return{address:a.address,domain:b,full:a.address+"@"+b}}else if(c=this.findClosestDomain(a.topLevelDomain,c),a.domain&&c&&c!=a.topLevelDomain)return b=a.domain,b=b.substring(0,b.lastIndexOf(a.topLevelDomain))+
c,{address:a.address,domain:b,full:a.address+"@"+b};return!1},findClosestDomain:function(a,b,c){var d,e=99,g=null;if(!a||!b)return!1;c||(c=this.sift3Distance);for(var f=0;f<b.length;f++){if(a===b[f])return a;d=c(a,b[f]);d<e&&(e=d,g=b[f])}return e<=this.threshold&&null!==g?g:!1},sift3Distance:function(a,b){if(null==a||0===a.length)return null==b||0===b.length?0:b.length;if(null==b||0===b.length)return a.length;for(var c=0,d=0,e=0,g=0;c+d<a.length&&c+e<b.length;){if(a.charAt(c+d)==b.charAt(c+e))g++;
else for(var f=e=d=0;5>f;f++){if(c+f<a.length&&a.charAt(c+f)==b.charAt(c)){d=f;break}if(c+f<b.length&&a.charAt(c)==b.charAt(c+f)){e=f;break}}c++}return(a.length+b.length)/2-g},splitEmail:function(a){a=a.split("@");if(2>a.length)return!1;for(var b=0;b<a.length;b++)if(""===a[b])return!1;var c=a.pop(),d=c.split("."),e="";if(0==d.length)return!1;if(1==d.length)e=d[0];else{for(b=1;b<d.length;b++)e+=d[b]+".";2<=d.length&&(e=e.substring(0,e.length-1))}return{topLevelDomain:e,domain:c,address:a.join("@")}}}};
window.jQuery&&function(a){a.fn.mailcheck=function(a){var c=this;if(a.suggested){var d=a.suggested;a.suggested=function(a){d(c,a)}}if(a.empty){var e=a.empty;a.empty=function(){e.call(null,c)}}a.email=this.val();Kicksend.mailcheck.run(a)}}(jQuery);
