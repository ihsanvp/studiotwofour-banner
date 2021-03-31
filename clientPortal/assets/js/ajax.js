$('#form-submit').on('click', function () {

  var message = $('#message');

  if (message.val() != '') {
    $(this).addClass('disabled');
    $('#spinner').removeClass('d-none');
    $('#form-submit').val('Sending');
    
  }

})

$('#contact').submit(function(e) {
  e.preventDefault();
  var post_url = $(this).attr('action');
  var message = $('#message');

  $.ajax({
    url:post_url,
    type: 'post',
    data: {
      message: message.val(),
      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
    },
    success: function() {
      $('#myModal').modal('show');
      $('#message').val('');
      $('#spinner').addClass('d-none');
      $('#form-submit').removeClass('disabled');
      $('#form-submit').val('Send Message')
      
    }
  })
})
