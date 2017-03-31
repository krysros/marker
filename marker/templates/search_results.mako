<%inherit file="layout.mako"/>

<%
  tab_bar = [('branches', 'Branże'),
             ('companies', 'Firmy'),
             ('persons', 'Osoby'),
             ('investors', 'Inwestorzy'),
             ('tenders', 'Przetargi'),]
%>

<ul class="nav nav-tabs" role="tablist">
% for id, caption in tab_bar:
  <li${' class="active"' if id == tab else '' | n}>
  <a href="${request.route_url('search', _query={'q': q, 'tab': id})}">${caption}</a></li>
% endfor
</ul>

<div class="alert alert-info" role="alert">Wyszukiwana fraza: <strong>${q}</strong></div>

% if tab == 'branches':

<div id="branches" class="table-responsive">
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

% elif tab == 'companies':

<div id="companies" class="table-responsive">
  <table id="companies" class="table table-striped">
    <thead>
      <tr>
        <th class="col-sm-5">Nazwa firmy</th>
        <th class="col-sm-4">Miasto</th>
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
          <a href="${request.route_url('company_view', company_id=company.id, slug=company.slug)}">${company.name}</a></td>
        <td>${company.city}</td>
        <td>${voivodeships.get(company.voivodeship)}</td>
      </tr>
    % endfor
    </tbody>
  </table>
</div>

% elif tab == 'persons':

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

% elif tab == 'investors':

<div id="investors" class="table-responsive">
  <table id="investors" class="table table-striped">
    <thead>
      <tr>
        <th class="col-sm-12">Nazwa inwestora</th>
      </tr>
    </thead>
    <tbody>
    % for investor in paginator.items:
      <tr>
        <td><a href="${request.route_url('investor_view', investor_id=investor.id, slug=investor.slug)}">${investor.name}</a></td>
      </tr>
    % endfor
    </tbody>
  </table>
</div>

% elif tab == 'tenders':

<div id="tenders" class="table-responsive">
  <table id="tenders" class="table table-striped">
    <thead>
      <tr>
        <th class="col-sm-12">Nazwa przetargu</th>
      </tr>
    </thead>
    <tbody>
    % for tender in paginator.items:
      <tr>
        <td><a href="${request.route_url('tender_view', tender_id=tender.id, slug=tender.slug)}">${tender.name}</a></td>
      </tr>
    % endfor
    </tbody>
  </table>
</div>

% endif

<div class="text-center">
  <ul class="pagination">
    ${paginator.pager() | n}
  </ul>
</div>