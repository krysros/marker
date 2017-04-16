<%inherit file="layout.mako"/>

<div class="row">
  <div class="col-md-12">
    <div class="table-responsive">
      <table id="branches" class="table table-striped">
        <thead>
          <tr>
            <th class="col-sm-12">Nazwa branży</th>
          </tr>
        </thead>
        <tbody>
        % for branch in paginator.items:
          <tr>
            <td><a href="${request.route_url('branch_companies', branch_id=branch.id, slug=branch.slug)}">${branch.name}</a></td>
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