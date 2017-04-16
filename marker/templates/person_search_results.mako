<%inherit file="layout.mako"/>

<div id="persons" class="table-responsive">
  <table id="persons" class="table table-striped">
    <thead>
      <tr>
        <th class="col-sm-3">Imię i nazwisko</th>
        <th class="col-sm-3">Firma</th>
        <th class="col-sm-3">Telefon</th>
        <th class="col-sm-3">Email</th>
      </tr>
    </thead>
    <tbody>
    % for person in paginator.items:
      <tr>
        <td>${person.fullname}</td>
        <td><a href="${request.route_url('company_view', company_id=person.companies.id, slug=person.companies.slug)}">${person.companies.name}</a></td>
        <td>${person.phone}</td>
        <td><a href="mailto:${person.email}">${person.email}</a></td>
      </tr>
    % endfor
    </tbody>
  </table>
</div>

<div class="text-center">
  <ul class="pagination">
    ${paginator.pager() | n}
  </ul>
</div>