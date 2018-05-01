<%inherit file="layout.mako"/>

<div class="panel panel-default">
  <div class="panel-heading">
    <i class="fa fa-thumbs-up" aria-hidden="true"></i> Rekomendowane firmy
  </div>
  <div class="panel-body">
    <div class="row">
      <div class="col-md-12">
        <table id="companies" class="table table-striped">
          <thead>
            <tr>
              <th class="col-sm-1">#</th>
              <th class="col-sm-5">Nazwa firmy</th>
              <th class="col-sm-2">Miasto</th>
              <th class="col-sm-2">Województwo</th>
              <th class="col-sm-2">Rekomendacje</th>
            </tr>
          </thead>
          <tbody>
          % for company in paginator.items:
            <tr>
              <td>
              % if company in user_marker:
                <input class="js-mark" type="checkbox" id="marker" name="marker" value="${company.id}" checked>
              % else:
                <input class="js-mark" type="checkbox" id="marker" name="marker" value="${company.id}">
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
              <td><a href="${request.route_url('company_upvotes', company_id=company.id, slug=company.slug)}">Pokaż</a> (${company.upvote_count})</td>
            </tr>
          % endfor
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>

<div class="text-center">
  <ul class="pagination">
    ${paginator.pager() | n}
  </ul>
</div>