<%inherit file="layout.mako"/>

<div class="panel panel-default">
  <div class="panel-body">
    <div class="pull-right">
      <a href="${request.route_url('user_edit', username=user.username)}" class="btn btn-warning" role="button"><i class="fa fa-edit" aria-hidden="true"></i> Edytuj</a>
      <a data-toggle="modal" href="#deleteModal" class="btn btn-danger" role="button"><i class="fa fa-trash" aria-hidden="true"></i> Usuń</a>
    </div>
  </div>
</div>

<div class="panel panel-default">
  <div class="panel-body">
    <dl class="dl-horizontal">
      <dt>Nazwa użytkownika</dt>
      <dd>${user.username}</dd>
      <dt>Imię i nazwisko</dt>
      <dd>${user.fullname}</dd>
      <dt>Email</dt>
      <dd><a href="mailto:${user.email}">${user.email}</a></dd>
      <dt>Rola</dt>
      <dd>${user.role}</dd>
    </dl>
  </div>
</div>

% for comment in paginator.items:
<div class="panel panel-info">
  <div class="panel-heading">
    <i class="fa fa-comment" aria-hidden="true"></i> <a href="${request.route_url('company_view', company_id=comment.companies[0].id, slug=comment.companies[0].slug)}">${comment.companies[0].name}</a> ${comment.added.strftime('%Y-%m-%d %H:%M:%S')}
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

<div class="modal fade" id="deleteModal" tabindex="-1" role="dialog" aria-labelledby="deleteModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title">Usuń</h4>
      </div>
      <div class="modal-body">
        Czy na pewno chcesz usunąć użytkownika z bazy danych?
      </div>
      <div class="modal-footer">
        <form action="${request.route_url('user_delete', username=user.username)}" method="post">
          <input type="hidden" name="csrf_token" value="${request.session.get_csrf_token()}">
          <button type="button" class="btn btn-default" data-dismiss="modal">Nie</button>
          <button type="submit" class="btn btn-primary" name="submit" value="delete">Tak</button>
        </form>
      </div>
    </div>
  </div>
</div>
