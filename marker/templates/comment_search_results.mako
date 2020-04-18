<%inherit file="layout.mako"/>

% for comment in paginator.items:
<div class="panel panel-default">
    <div class="panel-heading">
    <i class="fa fa-comment" aria-hidden="true"></i> <a href="${request.route_url('company_view', company_id=comment.company.id, slug=comment.company.slug)}">${comment.company.name}</a> ${comment.added.strftime('%Y-%m-%d %H:%M:%S')}
    % if comment.added_by == request.user or request.user.username == 'admin':
    <a href="${request.route_url('comment_delete', comment_id=comment.id, _query={'from': 'user'})}">Usuń</a>
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