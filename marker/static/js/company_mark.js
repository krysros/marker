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
          target.prop('checked', true);
        } else {
          target.prop('checked', false);
        }
      },
    });
  };

  var submitFormButton = function(event) {
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
        } else {
          $('.marker').removeClass('fa-check-square-o').addClass('fa-square-o');
        }
      },
    });
  };

  $('.js-mark').on('click', function(event) {
    event.preventDefault();
    submitForm(event);
  });

  $('.js-mark-button').on('click', function(event) {
    event.preventDefault();
    submitFormButton(event);
  });

});
