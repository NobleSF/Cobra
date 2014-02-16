$(function(){//on page load

  //LAZY PRODUCT LOADING
  $('.lazy-load').lazyload(800);

  //SEARCH AND SORTING
  parent_category = window.location.hash.split("#")[1]
  child_category = window.location.hash.split("#")[2] || parent_category
  if (parent_category && parent_category !== "everything"){
    //MARK SELECTED CATEGORIES IN SEARCH BAR
    selectCategories(parent_category, child_category);
    //SORT PRODUCTS ACCORDING TO CHOSEN CATEOGORIES
    sortProductsBy(parent_category, child_category)
  }

  //HOVER ANIMATION
  addHoverAnimation($('.product'));

});

$('.button.shop').click(function(){
  $.scrollTo($('#store').first(), 600);
  $.scrollTo("-=50px", 400, {axis:'y'});
});

//PRODUCT ANIMATION
function addHoverAnimation(selection){
  $(selection).hover(
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
}

//SEARCH AND SORTING FUNCTIONS
$('#search-toolbar .category').on('click', function(){
  parent_category = $(this).attr('data-parent-category');
  child_category = $(this).attr('data-child-category');

  //MARK SELECTED CATEGORIES IN SEARCH BAR
  selectCategories(parent_category, child_category);
  //SORT PRODUCTS ACCORDING TO CHOSEN CATEOGORIES
  sortProductsBy(parent_category, child_category)

  state = {parent_category: parent_category, child_category: child_category}
  if (parent_category === child_category){
    url_hash = "#" + parent_category
  }else{
    url_hash = "#" + parent_category + "#" + child_category
  }
  history.replaceState(state, "filter", url_hash)
});

function selectCategories(parent_category, child_category){
  //REMOVE ALL SELECTED
  $('#search-toolbar .category').removeClass('selected');

  //SELECT THE PARENT
  $('#search-toolbar .category.parent[data-child-category='+parent_category+']')
    .addClass('selected');

  //HIDE ALL CHILD CATEGORIES
  $('#search-toolbar .category.child').hide();

  //SHOW RELEVENT CHILD CATEGORIES
  $('#search-toolbar .category.child[data-parent-category='+parent_category+']').show()

  //SELECT CLICKED CHILD CATEGORY
  if (parent_category !== child_category){
    $('#search-toolbar .category.child[data-child-category='+child_category+']')
      .addClass('selected');
  }
}

function sortProductsBy(parent_category, child_category){
  // EVERYTHING, EVERYTHING SHOWS ALL
  // PARENT, PARENT SHOWS ALL IN PARENT CATEGORY
  // PARENT, CHILD SHOWS ALL IN CHILD CATEGORY
  // PARENT, OTHER SHOWS ALL WHERE CHILD == PARENT

  //HIDE ALL PRODUCTS
  $('.product-area').hide();

  //MOVE THE CATEGORY PRODUCTS FIRST
  if (parent_category == "everything"){
    //nothing to do here

  }else if (parent_category == child_category){//all in parent
    $('#product-container .product-area').each(function(){
      if ($(this).attr('data-parent-category') == parent_category){
        $(this).appendTo($('#product-sorting-container'))
      }
    });

  }else if(child_category == "other"){//all child == parent
    $('#product-container .product-area').each(function(){
      if ($(this).attr('data-parent-category') == parent_category &&
          $(this).attr('data-child-category') == parent_category){
        $(this).appendTo($('#product-sorting-container'))
      }
    });

  }else if(parent_category != child_category){//child only
    $('#product-container .product-area').each(function(){
      if ($(this).attr('data-parent-category') == parent_category &&
          $(this).attr('data-child-category') == child_category){
        $(this).appendTo($('#product-sorting-container'))
      }
    });
  }

  //THEN MOVE ALL THE REST TO FOLLOW BEHIND
  $('#product-container .product-area').each(function(){
    $(this).appendTo($('#product-sorting-container'))
  });
  //ALL PRODUCTS SHOULD BE IN THE SORTING CONTAINER NOW

  //MOVE ALL PRODUCTS BACK INTO ROWS
  if (child_category == 'everything'){
    $('#product-sorting-container .product-area').each(function(){
      //FIND THE ROW IT ORIGINALLY BELONGED TO AND PUT IT THERE
      row_number = Math.floor($(this).attr('data-order')/3)
      $(this).appendTo($('#product-container .product-row')[row_number])
    });
  }else{
    var next_position = 0;
    //NOW PUT THEM ALL BACK INTO ROWS - THEY ARE ALREADY IN ORDER
    $('#product-sorting-container .product-area').each(function(){
      row_number = Math.floor(next_position/3);
      $(this).appendTo($('#product-container .product-row')[row_number])
      next_position++;
    });
  }
  $('.lazy-load:lt(5)').trigger('loadnow');

  //this_category = $(this).attr('data-category');
  //this_position = $(this).attr('data-order');

  if (parent_category == 'everything'){//everything
    $('.product-area').show();

  }else if (parent_category == child_category){//all in parent
    $('.product-area[data-parent-category='+parent_category+']').show();

  }else if(child_category == "other"){//all child == parent
    $('.product-area[data-child-category='+parent_category+']').show();

  }else if(parent_category != child_category){//child only
    $('.product-area[data-parent-category='+parent_category+'][data-child-category='+child_category+']').show();
  }
}

// LAZY LOAD PRODUCTS BASED ON JQUERY UNVEIL AT http://luis-almeida.github.com/unveil
;(function($) {
  $.fn.lazyload = function(given_threshold) {

    var $w = $(window),
        threshold = given_threshold || 0, //default visibility threshold of 0 pixels
        containers = this,
        url = $('#load-products-url').val(),
        loaded, inview, product_areas, product_ids;

    this.on("loadnow", function() {
      //get unloaded products
      product_areas = $(this).children('.unloaded').removeClass('unloaded');

      if (product_areas.length){ //if any products, load them
        product_ids = product_areas.map(function(){ //get id list
          return $(this).attr('data-product-id');
        }).get();

        $.ajax({type:"GET", url:url, data:{product_ids:product_ids.join()}})
        .done(function(response){
          for (var key in response){ //for each (id, html) in response
            if (response.hasOwnProperty(key)){
              var product_area = $(".product-area[data-product-id='"+key+"']")
              $(product_area).html(response[key]);
              $(product_area).addClass('loaded'); //mark loaded
              addHoverAnimation($(product_area).find('.product'));
            }
          }
        })
        .fail(function(){
          product_areas.addClass('unloaded');
        });
      }
    }); //end loading function

    function lazyload(){ //find objects within range that need loading
      inview = containers.filter(function() {
        var $e = $(this),
            wt = $w.scrollTop(),
            wb = wt + $w.height(),
            et = $e.offset().top,
            eb = et + $e.height();
        return eb >= wt - threshold && et <= wb + threshold;
      });
      inview.trigger("loadnow"); //always keep triggering, products can hop in and out
    }

    $w.scroll(lazyload); //run on window scroll
    $w.resize(lazyload); //run on window resize
    lazyload(); //run right now
    return this;
  };
})(window.jQuery);

//SCROLLTO from http://archive.plugins.jquery.com/project/ScrollTo
// Copyright (c) 2007-2012 Ariel Flesler - aflesler(at)gmail(dot)com | http://flesler.blogspot.com
// Dual licensed under MIT and GPL. @author Ariel Flesler @version 1.4.3.1
;(function($){var h=$.scrollTo=function(a,b,c){$(window).scrollTo(a,b,c)};h.defaults={axis:'xy',duration:parseFloat($.fn.jquery)>=1.3?0:1,limit:true};h.window=function(a){return $(window)._scrollable()};$.fn._scrollable=function(){return this.map(function(){var a=this,isWin=!a.nodeName||$.inArray(a.nodeName.toLowerCase(),['iframe','#document','html','body'])!=-1;if(!isWin)return a;var b=(a.contentWindow||a).document||a.ownerDocument||a;return/webkit/i.test(navigator.userAgent)||b.compatMode=='BackCompat'?b.body:b.documentElement})};$.fn.scrollTo=function(e,f,g){if(typeof f=='object'){g=f;f=0}if(typeof g=='function')g={onAfter:g};if(e=='max')e=9e9;g=$.extend({},h.defaults,g);f=f||g.duration;g.queue=g.queue&&g.axis.length>1;if(g.queue)f/=2;g.offset=both(g.offset);g.over=both(g.over);return this._scrollable().each(function(){if(e==null)return;var d=this,$elem=$(d),targ=e,toff,attr={},win=$elem.is('html,body');switch(typeof targ){case'number':case'string':if(/^([+-]=)?\d+(\.\d+)?(px|%)?$/.test(targ)){targ=both(targ);break}targ=$(targ,this);if(!targ.length)return;case'object':if(targ.is||targ.style)toff=(targ=$(targ)).offset()}$.each(g.axis.split(''),function(i,a){var b=a=='x'?'Left':'Top',pos=b.toLowerCase(),key='scroll'+b,old=d[key],max=h.max(d,a);if(toff){attr[key]=toff[pos]+(win?0:old-$elem.offset()[pos]);if(g.margin){attr[key]-=parseInt(targ.css('margin'+b))||0;attr[key]-=parseInt(targ.css('border'+b+'Width'))||0}attr[key]+=g.offset[pos]||0;if(g.over[pos])attr[key]+=targ[a=='x'?'width':'height']()*g.over[pos]}else{var c=targ[pos];attr[key]=c.slice&&c.slice(-1)=='%'?parseFloat(c)/100*max:c}if(g.limit&&/^\d+$/.test(attr[key]))attr[key]=attr[key]<=0?0:Math.min(attr[key],max);if(!i&&g.queue){if(old!=attr[key])animate(g.onAfterFirst);delete attr[key]}});animate(g.onAfter);function animate(a){$elem.animate(attr,f,g.easing,a&&function(){a.call(this,e,g)})}}).end()};h.max=function(a,b){var c=b=='x'?'Width':'Height',scroll='scroll'+c;if(!$(a).is('html,body'))return a[scroll]-$(a)[c.toLowerCase()]();var d='client'+c,html=a.ownerDocument.documentElement,body=a.ownerDocument.body;return Math.max(html[scroll],body[scroll])-Math.min(html[d],body[d])};function both(a){return typeof a=='object'?a:{top:a,left:a}}})(jQuery);
