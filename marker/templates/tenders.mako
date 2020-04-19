<%inherit file="layout.mako"/>

<div class="panel panel-default">
  <div class="panel-body">
    <div class="btn-group">
      <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-expanded="false">
        <i class="fa fa-filter" aria-hidden="true"></i> Filtruj <i class="fa fa-caret-down" aria-hidden="true"></i>
      </button>
      <ul class="dropdown-menu" role="menu">
        <li><a href="${request.route_url('tenders', _query={'filter': 'inprogress'})}">w trakcie</a></li>
        <li><a href="${request.route_url('tenders', _query={'filter': 'completed'})}">zakończone</a></li>
        <li><a href="${request.route_url('tenders', _query={'filter': 'all'})}">wszystkie</a></li>
      </ul>
    </div>
  </div>
</div>

<div class="row">
  <div class="col-md-12">
    <div class="table-responsive">
      <table id="tenders" class="table table-striped">
        <thead>
          <tr>
            <th>Przetarg</th>
            <th>Miasto</th>
            <th>Termin składania ofert</th>
          </tr>
        </thead>
        <tbody>
        % for tender in paginator.items:
          <tr>
            <td><a href="${request.route_url('tender_view', tender_id=tender.id, slug=tender.slug)}">${tender.name}</a></td>
            <td>${tender.city}</td>
            <td>${tender.deadline}</td>
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