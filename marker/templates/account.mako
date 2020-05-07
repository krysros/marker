<%inherit file="layout.mako"/>  

<ul class="nav nav-tabs" role="tablist">
  % if heading == 'Dane użytkownika':
  <li class="active">
  % else:
  <li>
  % endif
    <a href="${request.route_url('account', username=request.user.username)}">Konto</a>
  </li>
  % if heading == 'Zmiana hasła':
  <li class="active">
  % else:
  <li>
  % endif
    <a href="${request.route_url('password', username=request.user.username)}">Hasło</a>
  </li>
</ul>

<div class="panel panel-default">
  <div class="panel-heading">${heading}</div>
  <div class="panel-body">
    ${rendered_form | n}
  </div>
</div>