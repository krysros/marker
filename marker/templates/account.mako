<%inherit file="layout.mako"/>  

<ul class="nav nav-tabs" role="tablist">
  <li${' class="active"' if heading == 'Dane użytkownika' else '' | n}>
    <a href="${request.route_url('account', username=user.username)}">Konto</a>
  </li>
  <li${' class="active"' if heading == 'Zmiana hasła' else '' | n}>
    <a href="${request.route_url('password', username=user.username)}">Hasło</a>
  </li>
</ul>

<div class="panel panel-default">
  <div class="panel-heading">${heading}</div>
  <div class="panel-body">
    ${rendered_form | n}
  </div>
</div>