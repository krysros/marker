<%inherit file="layout.mako"/>

<div class="panel panel-default">
  <div class="panel-body">
    <div class="btn-group">
      <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-expanded="false">
        Sortuj <i class="fa fa-caret-down" aria-hidden="true"></i>
      </button>
      <ul class="dropdown-menu" role="menu">
        <li><a href="${request.route_url('investors', _query={'sort': 'added'})}">wg daty dodania</a></li>
        <li><a href="${request.route_url('investors', _query={'sort': 'edited'})}">wg daty edycji</a></li>
        <li><a href="${request.route_url('investors', _query={'sort': 'alpha'})}">alfabetycznie</a></li>
      </ul>
    </div>
  </div>
</div>

<div class="row">
  <div class="col-md-12">
    <div class="table-responsive">
      <table id="investors" class="table table-striped">
        <thead>
          <tr>
            <th class="col-sm-8">Nazwa inwestora</th>
            <th class="col-sm-2">Miasto</th>
            % if query == 'edited':
            <th class="col-sm-2">Zmodyfikowano</th>
            % else:
            <th class="col-sm-2">Utworzono</th>
            % endif
          </tr>
        </thead>
        <tbody>
        % for investor in paginator.items:
          <tr>
            <td><a href="${request.route_url('investor_view', investor_id=investor.id, slug=investor.slug)}">${investor.name}</a></td>
            <td>${investor.city}</td>
            % if query == 'edited':
            <td>${investor.edited.strftime('%Y-%m-%d %H:%M:%S')}</td>
            % else:
            <td>${investor.added.strftime('%Y-%m-%d %H:%M:%S')}</td>
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