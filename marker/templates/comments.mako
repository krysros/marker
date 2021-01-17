<%inherit file="layout.mako"/>

<div class="page-header">
  <h4>Komentarze</h4>
</div>

% for comment in paginator.items:
<div class="panel panel-default">
  <div class="panel-heading">
    <i class="fa fa-comment" aria-hidden="true"></i>
    <a href="${request.route_url('user_view', username=comment.added_by.username, what='info')}" title="${comment.added_by.fullname}">${comment.added_by.username}</a> ${comment.added.strftime('%Y-%m-%d %H:%M:%S')}
    % if comment.added_by == request.user or request.user.username == 'admin':
    <a href="${request.route_url('comment_delete', comment_id=comment.id, _query={'from': 'company'})}">Usuń</a>
    % endif
  </div>
  <div class="panel-body">
    <p>  
      ${comment.comment}
    </p>
  </div>
</div>
% endfor

<div class="text-center">
  <ul class="pagination">
    ${paginator.pager() | n}
  </ul>
</div>