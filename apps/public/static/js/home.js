$(function(){//on page load

  $(this).find('.extra').find('div').find('*').each(function(){
    $(this).hide();
  });

});

//BOOTSTRAP CAROUSEL
$('#video-image').on('click', function(){
  $('#video-image').hide();
  $('#video').show();
});

//PRODUCT ANIMATION
$('.product').hover(
  function(){ //on mouseenter
    $(this).find('.hover-show').each(function(){
      $(this).show();
    });
  },
  function(){//on mouseleave
    $(this).find('.hover-show').each(function(){
      $(this).fadeOut();
    });
  }
);

// SUBSCRIBING FUNCTIONS
//show submit button if using form
$('#subscribe-name,#subscribe-email').on('focus', function(){
  $('#subscribe-buttons button:nth-child(3)').hide('500');//success
  $('#subscribe-buttons button:nth-child(4)').hide('500');//error
  $('#subscribe-buttons button:nth-child(1)').show();
});

$('#subscribe-submit').on('click',function(){
  if (validateForm()){
    processSubscribe();
  }
});

function processSubscribe(){
  $.ajax({
    url:$('#subscribe-form').attr('data-url'),
    beforeSend: function(){
      subscribeProgress();
      $('#subscribe-name,#subscribe-email').attr('disabled', 'disabled');
    },
    data:{
      'email':$('#subscribe-email').val(),
      'name':$('#subscribe-name').val()
    }
  })
  .done(function(data){
    if (data.success){
      subscribeSuccess();
    }else{
      subscribeFail();
    }
  })
  .fail(function(data){
    subscribeFail();
  })
  .always(function(data){
    $('#subscribe-name,#subscribe-email').removeAttr('disabled');
  });
}

function subscribeProgress(){
  $('#subscribe-buttons button').hide('500');//all buttons
  $('#subscribe-buttons button:nth-child(2)').show('500');//in progress
}
function subscribeSuccess(){
  $('#subscribe-buttons button').hide('500');//all buttons
  $('#subscribe-buttons button:nth-child(3)').show('500');//success
}
function subscribeFail(){//fail animation
  $('#subscribe-buttons button').hide('500');//all butons
  $('#subscribe-buttons button:nth-child(4)').show('500');//error
}

//validate email address when user leaves email field
$('#subscribe-email').on('blur', function() {
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
  $('#subscribe-email').val($('#suggested-email').html());
  $('#suggested-email').html('');
  $('#email-suggestion').hide();
  $('#subscribe-email').trigger('change');
})

function validateForm(){
  var complete = true;
  $('input.required').each(function(){
    $(this).removeClass('error');
    if ($(this).val() == ""){
      complete = false;
      $(this).closest('.control-group').addClass('error');
      $(this).closest('.control-group').find('.help-inline').fadeOut().fadeIn();
    }else if ($(this).attr('id') == 'subscribe-email'){
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

//use mailcheck on email field
//https://github.com/kicksend/mailcheck
//
/*1.1*/var Kicksend={mailcheck:{threshold:3,defaultDomains:"yahoo.com google.com hotmail.com gmail.com me.com aol.com mac.com live.com comcast.net googlemail.com msn.com hotmail.co.uk yahoo.co.uk facebook.com verizon.net sbcglobal.net att.net gmx.com mail.com".split(" "),defaultTopLevelDomains:"co.uk com net org info edu gov mil".split(" "),run:function(a){a.domains=a.domains||Kicksend.mailcheck.defaultDomains;a.topLevelDomains=a.topLevelDomains||Kicksend.mailcheck.defaultTopLevelDomains;a.distanceFunction=
a.distanceFunction||Kicksend.sift3Distance;var b=Kicksend.mailcheck.suggest(encodeURI(a.email),a.domains,a.topLevelDomains,a.distanceFunction);b?a.suggested&&a.suggested(b):a.empty&&a.empty()},suggest:function(a,b,c,d){a=a.toLowerCase();a=this.splitEmail(a);if(b=this.findClosestDomain(a.domain,b,d)){if(b!=a.domain)return{address:a.address,domain:b,full:a.address+"@"+b}}else if(c=this.findClosestDomain(a.topLevelDomain,c),a.domain&&c&&c!=a.topLevelDomain)return b=a.domain,b=b.substring(0,b.lastIndexOf(a.topLevelDomain))+
c,{address:a.address,domain:b,full:a.address+"@"+b};return!1},findClosestDomain:function(a,b,c){var d,e=99,g=null;if(!a||!b)return!1;c||(c=this.sift3Distance);for(var f=0;f<b.length;f++){if(a===b[f])return a;d=c(a,b[f]);d<e&&(e=d,g=b[f])}return e<=this.threshold&&null!==g?g:!1},sift3Distance:function(a,b){if(null==a||0===a.length)return null==b||0===b.length?0:b.length;if(null==b||0===b.length)return a.length;for(var c=0,d=0,e=0,g=0;c+d<a.length&&c+e<b.length;){if(a.charAt(c+d)==b.charAt(c+e))g++;
else for(var f=e=d=0;5>f;f++){if(c+f<a.length&&a.charAt(c+f)==b.charAt(c)){d=f;break}if(c+f<b.length&&a.charAt(c)==b.charAt(c+f)){e=f;break}}c++}return(a.length+b.length)/2-g},splitEmail:function(a){a=a.split("@");if(2>a.length)return!1;for(var b=0;b<a.length;b++)if(""===a[b])return!1;var c=a.pop(),d=c.split("."),e="";if(0==d.length)return!1;if(1==d.length)e=d[0];else{for(b=1;b<d.length;b++)e+=d[b]+".";2<=d.length&&(e=e.substring(0,e.length-1))}return{topLevelDomain:e,domain:c,address:a.join("@")}}}};
window.jQuery&&function(a){a.fn.mailcheck=function(a){var c=this;if(a.suggested){var d=a.suggested;a.suggested=function(a){d(c,a)}}if(a.empty){var e=a.empty;a.empty=function(){e.call(null,c)}}a.email=this.val();Kicksend.mailcheck.run(a)}}(jQuery);
