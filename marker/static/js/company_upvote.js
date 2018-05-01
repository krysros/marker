$(function() {
  var submitForm = function(event) {
    var csrfToken = $('meta[name=csrf_token]').attr('content');
    var target = $(event.currentTarget);
    $.ajax({
      url: '/upvote/company/' + target.val(),
      type: 'post',
      dataType: 'json',
      headers: {'X-CSRF-Token': csrfToken},
      success: function(data) {
        $('.upvote').removeClass('fa-thumbs-up fa-thumbs-o-up');
        if (data.upvote) {
          $('.upvote').addClass('fa-thumbs-up');
        } else {
          $('.upvote').addClass('fa-thumbs-o-up');
        }
      },
    });
  };
  $('.js-upvote').on('click', function(event) {
    event.preventDefault();
    submitForm(event);
  });
});