$().ready( function(){
  //run on page load
  uploader = new fileUploadAction();
  uploader.apply($('#seller-paid').find('.image-input'));
});

// CLICKABLE ICONS RED -> GREEN
$('.changeable').click(function(){
  var confirm_message
  var url = $('#update-order-url').val();
  var icon = $(this);

  if ($(this).hasClass("seller_paid")){
    if ($('#seller-paid .image img').attr('src')){
      confirm_message = "This seller was paid?";
      data = {'order_id': icon.attr('data-order-id'),
              'action':"seller paid"
              };
    }else{
      alert('upload photo of receipt.')
    }
  }

  if (confirm_message && confirm(confirm_message)){
    $.ajax({url: url, data: data})
    .done(function(data){
      icon.removeClass('changeable').removeClass('red').addClass('green')
    })
    .fail(function(){
      alert("update failed.")
    });
  }
});

//ADD NOTES
$('#add-note').click(function(){
  var notes_before = $("#notes").html();
  var notes_after = ""
  var url = $('#update-order-url').val();
  var data = {'action':'add note',
              'note':$('#new-note').val(),
              'order_id': $('#order-id').val()}

  $.ajax({url: url, data: data})
  .done(function(data){
    //append note to notes area
    notes_after = notes_before + "<br>" + $('#new-note').val();
    $("#notes").html(notes_after);
    //clear add-note form
    $('#new-note').html("");
  })
  .fail(function(){
    //sad face
    $('#add-note').html("<i class='symbol-sad'></i>");
    $('#add-note').removeClass('btn-info').addClass('btn-danger');
  });
})

function fileUploadAction(){
  this.apply = function(file_input){
    var iframe_fallback = false;

    var this_file_input = file_input;
    var image_data = {}
    var spinner = new Spinner()
    var spinner_div = this_file_input.closest('.image-upload-div').find('.spinner-div');
    var forms_div = this_file_input.closest('.image-upload-div').find('.image-forms');

    //hide progress
    this_file_input.closest('.image-upload-div').find('.progress').hide();
    //show user actionable items
    this_file_input.closest('.image-upload-div').find('.image-forms');

    //apply upload action callbacks
    this_file_input.fileupload({
      //forceIframeTransport: true,
      dataType: 'json',
      url: $('#upload-url').val(),

      submit: function(e, data){
        // call server to get signed form data
        var data_form = forms_div.find('.data-form');
        data.formData = getFormData(data_form);

        image_data = data.formData;
        image_data['order_id'] = $(forms_div).find('.order-id').val();
      },

      send: function (e, data) {
        //using iframe fallback?
        if (data.dataType.indexOf('iframe') >= 0){iframe_fallback = true;}

        if (data.files[0].name.length > 0){//because Android will try to send nothing

          if (iframe_fallback){
            //we don't know when the download will finish
            //set timer to try loadImage in 10 sec
            setTimeout(function(){
              loadImage(image_data);
            }, 10000); //wait 10 seconds

          }else{
            //not using iframe, so we can show a progress bar
            $('#progress-bar-'+image_data.order_id).css('width', '0%');
            $('#progress-'+image_data.order_id).show();
          }

          //show loading and hide interaction elements
          spinner.spin(document.getElementById($(spinner_div).attr('id')));
          $(spinner_div).show();
          forms_div.hide();
        }
      },

      //'data' not available in iframe mode from here on
      //and the following callbacks don't even happen on Android 2.3

      progress: function (e, data) {
        //animate the progress bar during upload
        var progress = parseInt(data.loaded / data.total * 95, 10);
        $('#progress-bar-'+image_data.order_id).css('width', progress + '%');
      },

      done: function (e, data) {
        //the data cloudinary returns, but we don't need it.
        //response_data = data['response']();
        //response = response_data.result;

        if (!iframe_fallback){

          //confirm success on server, load thumbnail
          loadImage(image_data);
        }
      },

      always: function (e, data) {
        //we're done here, hide the progress bar
        $('#progress-'+image_data.order_id).hide();
        spinner.stop();
        forms_div.show();
      }
    });//end fileupload
  }
}

function getFormData(form){//just a generic ajax call that returns resulting response
  var form_data = {};
  $.ajax({
    async: false, //function needs the result before it can continue
    cache: false, //don't cache, time-sensitive variables
    type: form.attr('method'),
    url: form.attr('action'),
    data: form.serialize(),
    dataType: 'json',

    success: function(data){
      form_data = data //dictionary object of values cloudinary needs
    },
  });
  return form_data;
}

function loadImage(image_data){
  //ask our server if the upload completed and get the thumb_url to load the image

  $.ajax({
    async: false,
    url: $('#upload-check-url').val(),
    cache: false,
    data: image_data,
    dataType: 'json',
  })

  .done(function(data, textStatus, jqXHR){
    switch(jqXHR.status){

      case 200: //image exists, load it and hide loading animations
        $('#image-'+image_data.order_id).find('img').attr('src', data.thumb_url);
        $('#progress-'+image_data.order_id).hide();
        $('#spinner-'+image_data.order_id).hide();
        $('#image-forms-'+image_data.order_id).show();
        break;

      case 204: //image does not exist yet, wait and try again
        setTimeout(function(){
          loadImage(image_data);
        }, 2000); //wait 2 seconds and try again

      case 404: //internet cut out
        //todo: reload page?
        break;
    }
  })
  .fail(function(){ //well.. that sucks
    //$('#asset-'+image_data.ilk+image_data.rank).addClass('error');
  });
}

//SPINNER from http://fgnass.github.io/spin.js/
//example:
//  var target = document.getElementById('foo');
//  var spinner = new Spinner(opts).spin(target);
;(function(t,e){if(typeof exports=="object")module.exports=e();else if(typeof define=="function"&&define.amd)define(e);else t.Spinner=e()})(this,function(){"use strict";var t=["webkit","Moz","ms","O"],e={},i;function o(t,e){var i=document.createElement(t||"div"),o;for(o in e)i[o]=e[o];return i}function n(t){for(var e=1,i=arguments.length;e<i;e++)t.appendChild(arguments[e]);return t}var r=function(){var t=o("style",{type:"text/css"});n(document.getElementsByTagName("head")[0],t);return t.sheet||t.styleSheet}();function s(t,o,n,s){var a=["opacity",o,~~(t*100),n,s].join("-"),f=.01+n/s*100,l=Math.max(1-(1-t)/o*(100-f),t),d=i.substring(0,i.indexOf("Animation")).toLowerCase(),u=d&&"-"+d+"-"||"";if(!e[a]){r.insertRule("@"+u+"keyframes "+a+"{"+"0%{opacity:"+l+"}"+f+"%{opacity:"+t+"}"+(f+.01)+"%{opacity:1}"+(f+o)%100+"%{opacity:"+t+"}"+"100%{opacity:"+l+"}"+"}",r.cssRules.length);e[a]=1}return a}function a(e,i){var o=e.style,n,r;if(o[i]!==undefined)return i;i=i.charAt(0).toUpperCase()+i.slice(1);for(r=0;r<t.length;r++){n=t[r]+i;if(o[n]!==undefined)return n}}function f(t,e){for(var i in e)t.style[a(t,i)||i]=e[i];return t}function l(t){for(var e=1;e<arguments.length;e++){var i=arguments[e];for(var o in i)if(t[o]===undefined)t[o]=i[o]}return t}function d(t){var e={x:t.offsetLeft,y:t.offsetTop};while(t=t.offsetParent)e.x+=t.offsetLeft,e.y+=t.offsetTop;return e}var u={lines:12,length:7,width:5,radius:10,rotate:0,corners:1,color:"#000",direction:1,speed:1,trail:100,opacity:1/4,fps:20,zIndex:2e9,className:"spinner",top:"auto",left:"auto",position:"relative"};function p(t){if(typeof this=="undefined")return new p(t);this.opts=l(t||{},p.defaults,u)}p.defaults={};l(p.prototype,{spin:function(t){this.stop();var e=this,n=e.opts,r=e.el=f(o(0,{className:n.className}),{position:n.position,width:0,zIndex:n.zIndex}),s=n.radius+n.length+n.width,a,l;if(t){t.insertBefore(r,t.firstChild||null);l=d(t);a=d(r);f(r,{left:(n.left=="auto"?l.x-a.x+(t.offsetWidth>>1):parseInt(n.left,10)+s)+"px",top:(n.top=="auto"?l.y-a.y+(t.offsetHeight>>1):parseInt(n.top,10)+s)+"px"})}r.setAttribute("role","progressbar");e.lines(r,e.opts);if(!i){var u=0,p=(n.lines-1)*(1-n.direction)/2,c,h=n.fps,m=h/n.speed,y=(1-n.opacity)/(m*n.trail/100),g=m/n.lines;(function v(){u++;for(var t=0;t<n.lines;t++){c=Math.max(1-(u+(n.lines-t)*g)%m*y,n.opacity);e.opacity(r,t*n.direction+p,c,n)}e.timeout=e.el&&setTimeout(v,~~(1e3/h))})()}return e},stop:function(){var t=this.el;if(t){clearTimeout(this.timeout);if(t.parentNode)t.parentNode.removeChild(t);this.el=undefined}return this},lines:function(t,e){var r=0,a=(e.lines-1)*(1-e.direction)/2,l;function d(t,i){return f(o(),{position:"absolute",width:e.length+e.width+"px",height:e.width+"px",background:t,boxShadow:i,transformOrigin:"left",transform:"rotate("+~~(360/e.lines*r+e.rotate)+"deg) translate("+e.radius+"px"+",0)",borderRadius:(e.corners*e.width>>1)+"px"})}for(;r<e.lines;r++){l=f(o(),{position:"absolute",top:1+~(e.width/2)+"px",transform:e.hwaccel?"translate3d(0,0,0)":"",opacity:e.opacity,animation:i&&s(e.opacity,e.trail,a+r*e.direction,e.lines)+" "+1/e.speed+"s linear infinite"});if(e.shadow)n(l,f(d("#000","0 0 4px "+"#000"),{top:2+"px"}));n(t,n(l,d(e.color,"0 0 1px rgba(0,0,0,.1)")))}return t},opacity:function(t,e,i){if(e<t.childNodes.length)t.childNodes[e].style.opacity=i}});function c(){function t(t,e){return o("<"+t+' xmlns="urn:schemas-microsoft.com:vml" class="spin-vml">',e)}r.addRule(".spin-vml","behavior:url(#default#VML)");p.prototype.lines=function(e,i){var o=i.length+i.width,r=2*o;function s(){return f(t("group",{coordsize:r+" "+r,coordorigin:-o+" "+-o}),{width:r,height:r})}var a=-(i.width+i.length)*2+"px",l=f(s(),{position:"absolute",top:a,left:a}),d;function u(e,r,a){n(l,n(f(s(),{rotation:360/i.lines*e+"deg",left:~~r}),n(f(t("roundrect",{arcsize:i.corners}),{width:o,height:i.width,left:i.radius,top:-i.width>>1,filter:a}),t("fill",{color:i.color,opacity:i.opacity}),t("stroke",{opacity:0}))))}if(i.shadow)for(d=1;d<=i.lines;d++)u(d,-2,"progid:DXImageTransform.Microsoft.Blur(pixelradius=2,makeshadow=1,shadowopacity=.3)");for(d=1;d<=i.lines;d++)u(d);return n(e,l)};p.prototype.opacity=function(t,e,i,o){var n=t.firstChild;o=o.shadow&&o.lines||0;if(n&&e+o<n.childNodes.length){n=n.childNodes[e+o];n=n&&n.firstChild;n=n&&n.firstChild;if(n)n.opacity=i}}}var h=f(o("group"),{behavior:"url(#default#VML)"});if(!a(h,"transform")&&h.adj)c();else i=a(h,"animation");return p});
