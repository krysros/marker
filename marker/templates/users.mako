<%inherit file="layout.mako"/>

<div class="row">
  <div class="col-md-12">
    <div class="table-responsive">
      <table id="users" class="table table-striped">
        <thead>
          <tr>
            <th class="col-sm-3">Nazwa użytkownika</th>
            <th class="col-sm-3">Imię i nazwisko</th>
            <th class="col-sm-3">Email</th>
            <th class="col-sm-3">Rola</th>
          </tr>
        </thead>
        <tbody>
        % for user in paginator.items:
          <tr>
            <td><a href="${request.route_url('user_view', username=user.username)}">${user.username}</a></td>
            <td>${user.fullname}</td>
            <td>${user.email}</td>
            <td>${user.role}</td>
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
