<%inherit file="layout.mako"/>

<div id="persons" class="table-responsive">
  <table id="persons" class="table table-striped">
    <thead>
      <tr>
        <th>Imię i nazwisko</th>
        <th>Firma</th>
        <th>Telefon</th>
        <th>Email</th>
      </tr>
    </thead>
    <tbody>
    % for person in paginator.items:
      <tr>
        <td>${person.fullname}</td>
        % if person.company:
        <td><a href="${request.route_url('company_view', company_id=person.company.id, slug=person.company.slug)}">${person.company.name}</a></td>
        % else:
        <td>---</td>
        % endif
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