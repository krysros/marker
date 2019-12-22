<%inherit file="layout.mako"/>

<div class="panel panel-default">
  <div class="panel-body">
    % if query:
    <a href="${request.route_url('user_upvotes_export', username=user.username, _query={'sort': query})}" class="btn btn-primary" role="button">
    % else:
    <a href="${request.route_url('user_upvotes_export', username=user.username)}" class="btn btn-primary" role="button">
    % endif
    <i class="fa fa-download" aria-hidden="true"></i> Eksportuj
    </a>
    <div class="btn-group">
      <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-expanded="false">
        <i class="fa fa-sort-alpha-asc" aria-hidden="true"></i> Sortuj <i class="fa fa-caret-down" aria-hidden="true"></i>
      </button>
      <ul class="dropdown-menu" role="menu">
        <li><a href="${request.route_url('user_upvotes', username=user.username, _query={'sort': 'name'})}">wg nazwy</a></li>
        <li><a href="${request.route_url('user_upvotes', username=user.username, _query={'sort': 'city'})}">wg miasta</a></li>
        <li><a href="${request.route_url('user_upvotes', username=user.username, _query={'sort': 'voivodeship'})}">wg województwa</a></li>
        <li><a href="${request.route_url('user_upvotes', username=user.username, _query={'sort': 'upvotes'})}">wg liczby rekomendacji</a></li>
      </ul>
    </div>
    <div class="pull-right">
      <a data-toggle="modal" href="#clearModal" class="btn btn-danger" role="button"><i class="fa fa-thumbs-o-up" aria-hidden="true"></i> Wyczyść</a>
    </div>
  </div>
</div>

<div class="panel panel-default">
  <div class="panel-heading">
    <i class="fa fa-thumbs-up" aria-hidden="true"></i> Rekomendowane firmy
  </div>
  <div class="panel-body">
    <div class="row">
      <div class="col-md-12">
        <table id="companies" class="table table-striped">
          <thead>
            <tr>
              <th class="col-sm-1">#</th>
              <th class="col-sm-5">Nazwa firmy</th>
              <th class="col-sm-2">Miasto</th>
              <th class="col-sm-2">Województwo</th>
              <th class="col-sm-2">Rekomendacje</th>
            </tr>
          </thead>
          <tbody>
          % for company in paginator.items:
            <tr class="${company.category}">
              <td>
              % if company in user_marker:
                <input class="js-mark" type="checkbox" value="${company.id}" autocomplete="off" checked>
              % else:
                <input class="js-mark" type="checkbox" value="${company.id}" autocomplete="off">
              % endif
              </td>
              <td>
              % if company in user_upvotes:
                <i class="fa fa-thumbs-up" aria-hidden="true"></i>
              % endif
                <a href="${request.route_url('company_view', company_id=company.id, slug=company.slug)}">${company.name}</a>
              </td>
              <td>${company.city}</td>
              <td>${voivodeships.get(company.voivodeship)}</td>
              <td><a href="${request.route_url('company_upvotes', company_id=company.id, slug=company.slug)}">Pokaż</a> (${company.upvote_count})</td>
            </tr>
          % endfor
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>

<div class="modal fade" id="clearModal" tabindex="-1" role="dialog" aria-labelledby="clearModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title">Wyczyść</h4>
      </div>
      <div class="modal-body">
        Wyczyścić wszystkie rekomendacje?<br>Ta operacja nie usuwa firm z bazy danych. 
      </div>
      <div class="modal-footer">
        <form action="${request.route_url('user_upvotes_clear', username=user.username)}" method="post">
          <input type="hidden" name="csrf_token" value="${request.session.get_csrf_token()}">
          <button type="button" class="btn btn-default" data-dismiss="modal">Nie</button>
          <button type="submit" class="btn btn-primary" name="submit" value="clear">Tak</button>
        </form>
      </div>
    </div>
  </div>
</div>

<div class="text-center">
  <ul class="pagination">
    ${paginator.pager() | n}
  </ul>
</div>