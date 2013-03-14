$(function(){//on page load
  $('#navigation').addClass('nav').addClass('nav-pills').addClass('pull-right')
  $('#navigation li').addClass('btn-large');

  //Footer
  $('#footer .container div').addClass('row');
  $('#footer .container div div').addClass('span'+(12/($('#footer .container div div').length)));

});
