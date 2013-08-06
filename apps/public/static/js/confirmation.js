// SUBSCRIBING FUNCTIONS

$('#subscribe-submit').on('click',function(){
  processSubscribe();
});

function processSubscribe(){
  $.ajax({
    url:$('#subscribe').attr('data-url'),
    beforeSend: function(){
      subscribeProgress();
    },
    data:{
      'email':$('#subscribe-email').html(),
      'name':$('#subscribe-name').html()
    }
  })
  .always(function(data){
    subscribeSuccess();
    $('#subscribe .before').hide();
    $('#subscribe .after').show();
  })
}

function subscribeProgress(){
  $('#subscribe button').hide('500');//all buttons
  $('#subscribe button:nth-child(2)').show('500');//in progress
}
function subscribeSuccess(){
  $('#subscribe button').hide('500');//all buttons
  $('#subscribe button:nth-child(3)').show('500');//success
}
