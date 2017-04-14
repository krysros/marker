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
            <th class="col-sm-6">Nazwa firmy</th>
            <th class="col-sm-3">Miasto</th>
            <th class="col-sm-3">Data</th>
          </tr>
        </thead>
        <tbody>
        % for company in paginator.items:
          <tr>
            <td>
            % if company in upvotes:
              <i class="fa fa-thumbs-up" aria-hidden="true"></i>
            % endif
              <a href="${request.route_url('company_view', company_id=company.id, slug=company.slug)}">${company.name}</a>
            </td>
            <td>${company.city}</td>
            % if query == 'added' or query == 'alpha':
              <td>${company.added.strftime('%Y-%m-%d %H:%M:%S')}</td>
            % elif query == 'edited':
              <td>${company.edited.strftime('%Y-%m-%d %H:%M:%S')}</td>
            % endif
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