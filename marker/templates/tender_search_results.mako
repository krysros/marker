<%inherit file="layout.mako"/>

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