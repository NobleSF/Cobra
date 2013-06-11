$(function(){//on page load

  $('.autosave').each(function(){
    $(this).autosave({
      url:$('#cart-ajax-url').attr('value'),
      before:function(){$(this).addClass('updating')},
      success:function(){$(this).removeClass('updating').addClass('saved')},
      error:function(){$(this).removeClass('updating').addClass('error')}
    });
  });

});

$('#checkout').on('click', function(){
  //hide cart, show checkout
  $('#cart #items').slideUp();
  $('#cart #summary').slideUp();
  $('#cart-sentance').slideUp();
  $('#cart-paragraph').removeClass('hidden');
  $('#cart-return').removeClass('hidden');
  $('#cart-form').removeClass('hidden');

  //hack wepay widget
  $('.wepay-widget-input').val($('#order-total').html()).attr('disabled','disabled');
});

$('#cart-return').on('click', function(){
  //hide cart, show checkout
  $('#cart-paragraph').addClass('hidden');
  $('#cart-return').addClass('hidden');
  $('#cart-form').addClass('hidden');
  $('#cart #items').slideDown();
  $('#cart #summary').slideDown();
  $('#cart-sentance').slideDown();
});


$('#pay-now').on('click', function(){

});

//use mailcheck on email field
//https://github.com/kicksend/mailcheck


//https://github.com/cfurrow/jquery.autosave.js
//example:
//  $("input").autosave({url:"/save",success:function(){},error:function(){}});
//
jQuery.fn.autosave=function(e){function n(e){var n=/^data\-(\w+)$/,r={};r.value=e.value;r.name=e.name;t.each(e.attributes,function(e,t){n.test(t.nodeName)&&(r[n.exec(t.nodeName)[1]]=t.value)});return r}var t=jQuery;t.each(this,function(){var r=t(this),i={data:{},event:"change",success:function(){},error:function(){},before:function(){}};e=t.extend(i,e);var s=n(this),o=s.event||e.event;r.on(o,function(){var r=t(this);s.value=r.val();s=t.extend(s,n(this));var i=s.url?s.url:e.url;e.before&&e.before.call(this,r);t.ajax({url:i,data:s,success:function(t){e.success(t,r)},error:function(t){e.error(t,r)}})})})};
