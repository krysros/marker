<%inherit file="layout.mako"/>

<div class="panel panel-default">
  <div class="panel-body">
    <div class="btn-group">
      <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-expanded="false">
        <i class="fa fa-sort-numeric-desc" aria-hidden="true"></i> Sortuj <i class="fa fa-caret-down" aria-hidden="true"></i>
      </button>
      <ul class="dropdown-menu" role="menu">
        <li><a href="${request.route_url('companies', _query={'sort': 'added'})}">wg daty dodania</a></li>
        <li><a href="${request.route_url('companies', _query={'sort': 'edited'})}">wg daty edycji</a></li>
        <li><a href="${request.route_url('companies', _query={'sort': 'alpha'})}">alfabetycznie</a></li>
      </ul>
    </div>
  </div>
</div>

<div class="row">
  <div class="col-md-12">
    <div class="table-responsive">
      <table id="companies" class="table table-striped">
        <thead>
          <tr>
            <th class="col-sm-1">#</th>
            <th class="col-sm-5">Nazwa firmy</th>
            <th class="col-sm-2">Miasto</th>
            <th class="col-sm-2">Data</th>
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
            % if query == 'edited':
              <td>${company.edited.strftime('%Y-%m-%d %H:%M:%S')}</td>
            % else:
              <td>${company.added.strftime('%Y-%m-%d %H:%M:%S')}</td>
            % endif
            <td><a href="${request.route_url('company_upvotes', company_id=company.id, slug=company.slug)}">Pokaż</a> (${company.upvote_count})</td>
          </tr>
          % endfor
        </tbody>
      </table>
    </div>
  </div>
</div>

<div class="text-center">
  <ul class="pagination">
    ${paginator.pager() | n}
  </ul>
</div>