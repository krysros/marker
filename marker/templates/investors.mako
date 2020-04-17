<%inherit file="layout.mako"/>

<div class="row">
  <div class="col-md-12">
    <div class="table-responsive">
      <table id="investors" class="table table-striped">
        <thead>
          <tr>
            <th class="col-sm-9">Nazwa inwestora</th>
            <th class="col-sm-3">Miasto</th>
          </tr>
        </thead>
        <tbody>
        % for investor in paginator.items:
          <tr>
            <td><a href="${request.route_url('investor_view', investor_id=investor.id, slug=investor.slug)}">${investor.name}</a></td>
            <td>${investor.city}</td>
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