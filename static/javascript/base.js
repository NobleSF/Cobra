$(function(){//on page load
  $('#navigation').addClass('nav').addClass('nav-pills').addClass('pull-right')
  $('#navigation li').addClass('btn-large');

  //Footer
  $('#footer .container div').addClass('row');
  $('#footer .container div div').addClass('span'+(12/($('#footer .container div div').length)));

  //Thumbnails
  $('.thumbnails').addClass('fluid-row');
  $('.thumbnail img').addClass('img-polaroid');

  $('.thumbnail .actions').addClass('inline');
  $('.thumbnail .actions .price').addClass('btn').addClass('btn-small');
  $('.thumbnail .actions .info').addClass('btn').addClass('btn-info').addClass('btn-small');
  $('.thumbnail .actions .save').addClass('btn').addClass('btn-warning').addClass('btn-small');
  $('.thumbnail .actions .buy').addClass('btn').addClass('btn-success').addClass('btn-small');

  $('.thumbnail').each( function() {
    var num_thumbnails = $(this).parent('li').siblings('li').length + 1;
    if (num_thumbnails == 5){ num_thumbnails = 6;}
    $(this).closest('li').addClass('span'+12/num_thumbnails);
    if (num_thumbnails > 4){
      $(this).find('.actions .btn').removeClass('btn-small').addClass('btn-mini');
      $(this).find('.actions .buy').hide();
    }
  });

  $('.thumbnail .actions .info').html('<i class="icon-info-sign"></i> Info');
  $('.thumbnail .actions .save').html('<i class="icon-star-empty"></i> Save');
  $('.thumbnail .actions .buy').html('<i class="icon-ok"></i> Buy');

  sizeElements();

});

$(window).resize(function() { //Todo: not working
  //sizeElements();
});

function sizeElements(){
  $('.thumbnail .title').each( function() {
    $(this).width($(this).prevAll('img:first').width()-10);
    var offset = $(this).prev('img').offset();
    offset.top -= $(this).height() + 20;
    $(this).offset({ top: offset.top, left: offset.left});
  });

  $('.thumbnail .actions').each( function() {
    var offset = $(this).prev().offset();
    offset.top += $(this).prev('p').height() + 40;
    $(this).offset({ top: offset.top, left: offset.left});
  });

  $('.thumbnail .caption').each( function() {
    $(this).width($(this).prevAll('img:first').width()-10);
    var offset = $(this).prev().offset();
    offset.top += $(this).prev('p').height() + 30;
    $(this).offset({ top: offset.top, left: offset.left});
  });
}
