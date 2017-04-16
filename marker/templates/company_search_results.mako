<%inherit file="layout.mako"/>

<div class="row">
  <div class="col-md-12">
    <div class="table-responsive">
      <table id="companies" class="table table-striped">
        <thead>
          <tr>
            <th class="col-sm-6">Nazwa firmy</th>
            <th class="col-sm-3">Miasto</th>
            <th class="col-sm-3">Województwo</th>
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
            <td>${voivodeships.get(company.voivodeship)}</td>
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