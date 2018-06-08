$(function() {
  var submitForm = function(event) {
    var csrfToken = $('meta[name=csrf_token]').attr('content');
    var target = $(event.currentTarget);
    $.ajax({
      url: '/mark/company/' + target.val(),
      type: 'post',
      dataType: 'json',
      headers: {'X-CSRF-Token': csrfToken},
      success: function(data) {
        if (data.marker) {
          $('.marker').removeClass('fa-square-o').addClass('fa-check-square-o');
          target.prop('checked', true);
        } else {
          $('.marker').removeClass('fa-check-square-o').addClass('fa-square-o');
          target.prop('checked', false);
        }
      },
    });
  };
  $('.js-mark').on('click', function(event) {
    event.preventDefault();
    submitForm(event);
  });
});
