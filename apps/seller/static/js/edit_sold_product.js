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

  //activate the "show more" link in the summary
  $('.total-cost').on('click', function(){
    $('.extra').toggle();
  });

  $('input').not('#price').attr('disabled','disabled')

  //autosave for inputs
  $('input.autosave#price').autosave({
    url:      $('#edit-product-url').val(),
    event:    'blur',
    type:     'json',
    data:     {'product_id':$('#product-id').val()},

    before:   function(){
      $(this).removeClass('saved').removeClass('error').addClass('updating');
    },
    done:     function(response){
      $(this).removeClass('updating').addClass('saved');
      //if element not in focus, update value
      if( !$(this).is(":focus") && $(this).attr('name') == response.name ){
        $(this).val(response.value);
      }
      updateSummary(response);
    },
    fail:     function(jqXHR){
      $(this).removeClass('updating').addClass('error');
      //todo: if 404 error, trigger this event again
      //if( jqXHR.status.code == 404 ){
      //  $(this).val("");
      //}
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
    done:     function(response){
      if( response.activated ){
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
    done:     function(response){
      if( response.activated ){
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
  no_errors = true;
  //price
  if(!($('#price').val() > 0)){
    $('#price-section').addClass('attention');
    no_errors = false;
  }
  return no_errors
}
// remove .attention when editing section
$('.section').on('click', function(){
  $(this).removeClass('attention');
});

//AUTOSAVE from https://github.com/tomcounsell/jquery-autosave
//example: $("input").autosave({options});
;(function(a,b,c,d){function g(b,c){this.element=b,this.options=a.extend({},f,c),this._defaults=f,this._name=e,this.init()}var e="autosave",f={url:"",method:"POST",event:"change",data:{},type:"html",debug:!1,before:function(){},done:function(){},fail:function(){},always:function(){}};g.prototype.init=function(){function e(b){var c=/^data\-(\w+)$/,d={};return d.value=b.val()||"",d.name=b.attr("name")||"",a(b[0].attributes).each(function(){c.test(this.nodeName)&&(attribute_name=c.exec(this.nodeName)[1],d[attribute_name]=this.nodeValue)}),d}var b=a(this.element),c=e(b),d=this.options,c=e(b);d.event=c.event||d.event,b.on(d.event,function(c){d.before&&d.before.call(b);var f=e(b);options=a.extend({},d,f);var g=a.extend({},options.data,f);options.debug=="false"&&(options.debug=!1),delete g.url,delete g.method,delete g.type,delete g.debug,g.event=options.event,options.debug?console.log(g):a.ajax({url:options.url,type:options.method,cache:!1,data:g,dataType:options.type}).done(function(a,c,d){b.data("autosave-data",a),b.data("autosave-textStatus",c),b.data("autosave-jqXHR",d),b.trigger("autosave-done")}).fail(function(a,c,d){b.data("autosave-jqXHR",a),b.data("autosave-textStatus",c),b.data("autosave-errorThrown",d),b.trigger("autosave-fail")}).always(function(){b.trigger("autosave-always")})}),d.done&&b.on("autosave-done",function(){var a=b.data("autosave-data"),c=b.data("autosave-textStatus"),d=b.data("autosave-jqXHR");options.done.call(b,a,c,d)}),d.fail&&b.on("autosave-fail",function(){var a=b.data("autosave-jqXHR"),c=b.data("autosave-textStatus"),d=b.data("autosave-errorThrown");options.fail.call(b,a,c,d)}),d.always&&b.on("autosave-always",function(){options.always.call(b)})},a.fn.autosave=function(a){return this.each(function(){new g(this,a)})}})(jQuery,window,document)
