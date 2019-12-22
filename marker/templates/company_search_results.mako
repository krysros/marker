<%inherit file="layout.mako"/>

<div class="row">
  <div class="col-md-12">
    <div class="table-responsive">
      <table id="companies" class="table table-striped">
        <thead>
          <tr>
            <th class="col-sm-1">#</th>
            <th class="col-sm-5">Nazwa firmy</th>
            <th class="col-sm-3">Miasto</th>
            <th class="col-sm-3">Województwo</th>
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