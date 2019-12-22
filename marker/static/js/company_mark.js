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
        if (data.marked) {
          target.prop('checked', true);
        } else {
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
