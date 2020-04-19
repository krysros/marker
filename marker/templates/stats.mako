<%inherit file="layout.mako"/>

<%!
  from marker.views.voivodeships import VOIVODESHIPS
  voivodeships = dict(VOIVODESHIPS)
%>

<%
  tab_bar = [('companies-voivodeships', 'Województwa'),
             ('companies-cities', 'Miasta'),
             ('companies-branches', 'Branże'),
             ('companies-upvotes', 'Rekomendacje'),
             ('companies-users', 'Użytkownicy'),
             ('offers-companies', 'Oferty'),
             ('investors-tenders', 'Inwestorzy'),
             ('tenders-cities', 'Przetargi')]
%>

<ul class="nav nav-tabs" role="tablist">
% for id, caption in tab_bar:
  <li${' class="active"' if id == rel else '' | n}>
  <a href="${request.route_url('stats', _query={'rel': id})}">${caption}</a></li>
% endfor
</ul>

<div class="panel panel-info">
  <div class="panel-heading">Co to jest?</div>
  <div class="panel-body">
  % if rel == 'companies-voivodeships':
    <p>Liczba firm w poszczególnych województwach.</p>
  % elif rel == 'companies-cities':
    <p>Zestawienie miast o największej liczbie firm.</p>
  % elif rel == 'companies-branches':
    <p>Zestawienie branż o nawiększej liczbie firm.</p>
  % elif rel == 'companies-upvotes':
    <p>Zestawienie firm, które otrzymały największą liczbę rekomendacji.</p>
  % elif rel == 'companies-users':
    <p>Zestawienie użytkowników, którzy dodali najwięcej firm do bazy danych.</p>
  % elif rel == 'offers-companies':
    <p>Zestawienie firm, które złożyły najwięcej ofert.</p>
  % elif rel == 'investors-tenders':
    <p>Zestawienie inwestorów, którzy zorganizowali najwięcej przetargów.</p>
  % elif rel == 'tenders-cities':
    <p>Zestawienie miast o największej liczbie przetargów.</p>
  % endif
  </div>
</div>

<!-- Table -->
<div class="table-responsive">
  <table id="companies" class="table table-striped">
    <thead>
      <tr>
        <th>Opis</th>
        <th>Liczba</th>
      </tr>
    </thead>
    <tbody>
    % for k, v in paginator.items:
      <tr>
        % if rel == 'companies-voivodeships':
          <td>${voivodeships[k]}</td>
        % else:
          <td>${k}</td>
        % endif
        <td>${v}</td>
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
