$('.title-row').click(function(){
  $(this).toggleClass('highlight');
  $(this).next('.actions-row').toggle();
});

$('.approve-seller').click(function(){
  var seller_id = $(this).attr('data-seller-id');
  approveSeller(seller_id, 'approve');
});

$('.unapprove-seller').click(function(){
  if (confirm("Deactivate This Seller's Account?")){
    var seller_id = $(this).attr('data-seller-id');
    approveSeller(seller_id, 'unapprove');
  }
});

function approveSeller(seller_id, action){
  var approve_url = $('#approve-url').val();
  button = $('#approve-button-'+seller_id)

  $.get(approve_url, {seller_id:seller_id,action:action})
  .done(function(){
    if (action === 'approve'){
      $(button).removeClass('approve-seller').removeClass('btn-success');
      $(button).removeClass('btn').html('Approved').unbind();
    }else if(action === 'unapprove'){
      $(button).removeClass('unapprove-seller').removeClass('btn-danger');
      $(button).removeClass('btn').html('Unapproved').unbind();
    }
  });
}
