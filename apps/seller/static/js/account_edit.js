$().ready( function(){

  //assign bootstrap classes
  $('#asset-tabs').children('li').first().addClass('active');//first tab active
  $('#artisan_tab').trigger('click');//activate first tab

  //run on page load for seller form
  //autosave requires data- attributes
  //set ilk, rank to dummy values 'seller', '0'
  applyDataAttrs($('#seller-account'), 'seller', '0');
  applyEvents($('#seller-account'), to_assets="no");//just for seller image now

  //run on page load for assets
  arrangeAssetForms();//move assets to their respective tab
  addAssetForms();//create blank assets as needed

});//end .ready

$('.language-btn').click(function(){
  language = $(this).attr('data-lang');
  $('.lang').hide();
  $('.lang-'+language).show();
  $('.language-btn').removeClass('btn-success');
  $(this).addClass('btn-success');
});

$('.asset-tab').click(function(){//when an asset tab is clicked
  //make this tab active
  $('.asset-tab').removeClass('active');
  $(this).addClass('active');
  //hide all asset containers, then show the right one
  $('.asset-container').hide();
  asset_ilk = $(this).attr('id').replace('_tab','');
  $('#'+asset_ilk+'_container').show();
});

function arrangeAssetForms(){
  $('#asset-forms .asset').each(function(){
    //autosave requires data- attributes
    applyDataAttrs($(this));
    //apply autosave and any other js event handlers
    applyEvents($(this));

    var ilk = $(this).find('#id_ilk').val();
    if (ilk != ''){
      //move to proper asset container
      $(this).appendTo('#'+ilk+'_container');
    }
  });
}

function addAssetForms(){
  //copy blank asset forms to asset containers so there is always an extra new one.

  //for each asset container
  $('.asset-container').each(function(){
    var this_container = $(this);
    var num_empty_forms = 0;

    //for each asset form inside the containter
    this_container.children('.asset').each(function(){
      this_asset = $(this);

      //count empty forms
      if (this_asset.hasClass('empty')){
        num_empty_forms++;
      }
    });

    //if there are no empty forms, add one
    if (num_empty_forms == 0){

      //grab an empty form from the hidden .asset-forms div
      var new_asset = $('#asset-forms .asset').first().clone(false);
      var ilk = this_container.attr('id').replace('_container','');

      //calculate what the next rank should be
      var highest_rank = 0;
      $('.asset').each(function(){
        var this_rank = $(this).find('input#id_rank').val();
        if (parseInt(this_rank) > highest_rank){
          highest_rank = parseInt(this_rank);
        }
      })
      var next_rank = highest_rank + 1;
      new_asset.find('input.rank').attr('value', next_rank);
      new_asset.find('input.ilk').attr('value', ilk);
      new_asset.attr('id', ('asset-'+ilk+next_rank));

      //place it in the container
      new_asset.appendTo(this_container);
      applyDataAttrs(new_asset, ilk, next_rank);
      applyEvents(new_asset);

    }//end if
  });//end for each asset-container
}

function applyDataAttrs(asset_div, ilk, rank){
  //make unique id's and add data- attributes to autosave inputs

  seller_id = asset_div.find('input.seller-id').val();
  ilk = ilk || asset_div.find('input.ilk').val();
  rank = rank || asset_div.find('input.rank').val();

  //give all elements unique ids
  asset_div.find('[id*="-ilkrank"]').each(function(){
    var id = $(this).attr('id');
    var new_id = id.replace('ilkrank', (ilk+rank));
    $(this).attr('id', new_id);
  });

  //give all autosave elements seller_id and new ilk, rank values
  asset_div.find('.autosave').each(function(){
    $(this).attr('data-seller_id', seller_id)
    $(this).attr('data-ilk', ilk)
    $(this).attr('data-rank', rank)
  });

  //if not product container, hide category element
  if ( ilk !== 'product'){
    asset_div.find('.asset-category').hide();
  }else{
    asset_div.find('.asset-category').show();
  }

  if (ilk !=='artisan'){
    asset_div.find('.asset-phone').hide();
  }else{
    asset_div.find('.asset-phone').show();
  }
}

function applyEvents(asset_div, to_assets){
  uploader = new fileUploadAction();
  uploader.apply(asset_div.find('.image-input'));

  //for input fields
  to_assets = to_assets || "yes";//parameter defaults to true if not provided
  if (to_assets === "yes"){
    applyAssetAutosave(asset_div);
    applyAssetDeleteAction(asset_div);
  }
}

//AUTOSAVE from https://github.com/cfurrow/jquery.autosave.js
//example:
//  $("input").autosave({url:"/save",success:function(){},error:function(){}});
//
jQuery.fn.autosave=function(e){function n(e){var n=/^data\-(\w+)$/,r={};r.value=e.value;r.name=e.name;t.each(e.attributes,function(e,t){n.test(t.nodeName)&&(r[n.exec(t.nodeName)[1]]=t.value)});return r}var t=jQuery;t.each(this,function(){var r=t(this),i={data:{},event:"change",success:function(){},error:function(){},before:function(){}};e=t.extend(i,e);var s=n(this),o=s.event||e.event;r.on(o,function(){var r=t(this);s.value=r.val();s=t.extend(s,n(this));var i=s.url?s.url:e.url;e.before&&e.before.call(this,r);t.ajax({url:i,data:s,success:function(t){e.success(t,r)},error:function(t){e.error(t,r)}})})})};

//SPINNER from http://fgnass.github.io/spin.js/
//example:
//  var target = document.getElementById('foo');
//  var spinner = new Spinner(opts).spin(target);
;(function(t,e){if(typeof exports=="object")module.exports=e();else if(typeof define=="function"&&define.amd)define(e);else t.Spinner=e()})(this,function(){"use strict";var t=["webkit","Moz","ms","O"],e={},i;function o(t,e){var i=document.createElement(t||"div"),o;for(o in e)i[o]=e[o];return i}function n(t){for(var e=1,i=arguments.length;e<i;e++)t.appendChild(arguments[e]);return t}var r=function(){var t=o("style",{type:"text/css"});n(document.getElementsByTagName("head")[0],t);return t.sheet||t.styleSheet}();function s(t,o,n,s){var a=["opacity",o,~~(t*100),n,s].join("-"),f=.01+n/s*100,l=Math.max(1-(1-t)/o*(100-f),t),d=i.substring(0,i.indexOf("Animation")).toLowerCase(),u=d&&"-"+d+"-"||"";if(!e[a]){r.insertRule("@"+u+"keyframes "+a+"{"+"0%{opacity:"+l+"}"+f+"%{opacity:"+t+"}"+(f+.01)+"%{opacity:1}"+(f+o)%100+"%{opacity:"+t+"}"+"100%{opacity:"+l+"}"+"}",r.cssRules.length);e[a]=1}return a}function a(e,i){var o=e.style,n,r;if(o[i]!==undefined)return i;i=i.charAt(0).toUpperCase()+i.slice(1);for(r=0;r<t.length;r++){n=t[r]+i;if(o[n]!==undefined)return n}}function f(t,e){for(var i in e)t.style[a(t,i)||i]=e[i];return t}function l(t){for(var e=1;e<arguments.length;e++){var i=arguments[e];for(var o in i)if(t[o]===undefined)t[o]=i[o]}return t}function d(t){var e={x:t.offsetLeft,y:t.offsetTop};while(t=t.offsetParent)e.x+=t.offsetLeft,e.y+=t.offsetTop;return e}var u={lines:12,length:7,width:5,radius:10,rotate:0,corners:1,color:"#000",direction:1,speed:1,trail:100,opacity:1/4,fps:20,zIndex:2e9,className:"spinner",top:"auto",left:"auto",position:"relative"};function p(t){if(typeof this=="undefined")return new p(t);this.opts=l(t||{},p.defaults,u)}p.defaults={};l(p.prototype,{spin:function(t){this.stop();var e=this,n=e.opts,r=e.el=f(o(0,{className:n.className}),{position:n.position,width:0,zIndex:n.zIndex}),s=n.radius+n.length+n.width,a,l;if(t){t.insertBefore(r,t.firstChild||null);l=d(t);a=d(r);f(r,{left:(n.left=="auto"?l.x-a.x+(t.offsetWidth>>1):parseInt(n.left,10)+s)+"px",top:(n.top=="auto"?l.y-a.y+(t.offsetHeight>>1):parseInt(n.top,10)+s)+"px"})}r.setAttribute("role","progressbar");e.lines(r,e.opts);if(!i){var u=0,p=(n.lines-1)*(1-n.direction)/2,c,h=n.fps,m=h/n.speed,y=(1-n.opacity)/(m*n.trail/100),g=m/n.lines;(function v(){u++;for(var t=0;t<n.lines;t++){c=Math.max(1-(u+(n.lines-t)*g)%m*y,n.opacity);e.opacity(r,t*n.direction+p,c,n)}e.timeout=e.el&&setTimeout(v,~~(1e3/h))})()}return e},stop:function(){var t=this.el;if(t){clearTimeout(this.timeout);if(t.parentNode)t.parentNode.removeChild(t);this.el=undefined}return this},lines:function(t,e){var r=0,a=(e.lines-1)*(1-e.direction)/2,l;function d(t,i){return f(o(),{position:"absolute",width:e.length+e.width+"px",height:e.width+"px",background:t,boxShadow:i,transformOrigin:"left",transform:"rotate("+~~(360/e.lines*r+e.rotate)+"deg) translate("+e.radius+"px"+",0)",borderRadius:(e.corners*e.width>>1)+"px"})}for(;r<e.lines;r++){l=f(o(),{position:"absolute",top:1+~(e.width/2)+"px",transform:e.hwaccel?"translate3d(0,0,0)":"",opacity:e.opacity,animation:i&&s(e.opacity,e.trail,a+r*e.direction,e.lines)+" "+1/e.speed+"s linear infinite"});if(e.shadow)n(l,f(d("#000","0 0 4px "+"#000"),{top:2+"px"}));n(t,n(l,d(e.color,"0 0 1px rgba(0,0,0,.1)")))}return t},opacity:function(t,e,i){if(e<t.childNodes.length)t.childNodes[e].style.opacity=i}});function c(){function t(t,e){return o("<"+t+' xmlns="urn:schemas-microsoft.com:vml" class="spin-vml">',e)}r.addRule(".spin-vml","behavior:url(#default#VML)");p.prototype.lines=function(e,i){var o=i.length+i.width,r=2*o;function s(){return f(t("group",{coordsize:r+" "+r,coordorigin:-o+" "+-o}),{width:r,height:r})}var a=-(i.width+i.length)*2+"px",l=f(s(),{position:"absolute",top:a,left:a}),d;function u(e,r,a){n(l,n(f(s(),{rotation:360/i.lines*e+"deg",left:~~r}),n(f(t("roundrect",{arcsize:i.corners}),{width:o,height:i.width,left:i.radius,top:-i.width>>1,filter:a}),t("fill",{color:i.color,opacity:i.opacity}),t("stroke",{opacity:0}))))}if(i.shadow)for(d=1;d<=i.lines;d++)u(d,-2,"progid:DXImageTransform.Microsoft.Blur(pixelradius=2,makeshadow=1,shadowopacity=.3)");for(d=1;d<=i.lines;d++)u(d);return n(e,l)};p.prototype.opacity=function(t,e,i,o){var n=t.firstChild;o=o.shadow&&o.lines||0;if(n&&e+o<n.childNodes.length){n=n.childNodes[e+o];n=n&&n.firstChild;n=n&&n.firstChild;if(n)n.opacity=i}}}var h=f(o("group"),{behavior:"url(#default#VML)"});if(!a(h,"transform")&&h.adj)c();else i=a(h,"animation");return p});
