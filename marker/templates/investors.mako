<%inherit file="layout.mako"/>

<div class="row">
  <div class="col-md-12">
    <div class="table-responsive">
      <table id="investors" class="table table-striped">
        <thead>
          <tr>
            <th class="col-sm-12">Nazwa inwestora</th>
          </tr>
        </thead>
        <tbody>
        % for investor in paginator.items:
          <tr>
            <td><a href="${request.route_url('investor_view', investor_id=investor.id, slug=investor.slug)}">${investor.name}</a></td>
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