<%inherit file="layout.mako"/>

<div class="panel panel-default">
  <div class="panel-body">
    <div class="pull-right">
      <a href="${request.route_url('user_edit', username=user.username)}" class="btn btn-warning" role="button"><i class="fa fa-edit" aria-hidden="true"></i> Edytuj</a>
      <a data-toggle="modal" href="#deleteModal" class="btn btn-danger" role="button"><i class="fa fa-trash" aria-hidden="true"></i> Usuń</a>
    </div>
  </div>
</div>

<div class="panel panel-default">
  <div class="panel-body">
    <dl class="dl-horizontal">
      <dt>Nazwa użytkownika</dt>
      <dd>${user.username}</dd>
      <dt>Imię i nazwisko</dt>
      <dd>${user.fullname}</dd>
      <dt>Email</dt>
      <dd><a href="mailto:${user.email}">${user.email}</a></dd>
      <dt>Rola</dt>
      <dd>${user.role}</dd>
    </dl>
  </div>
</div>

<%
  tab_bar = [('comments', 'Komentarze'),
             ('branches', 'Branże'),
             ('companies', 'Firmy'),
             ('investors', 'Inwestorzy'),
             ('tenders', 'Przetargi'),
             ('offers', 'Oferty'),]
%>

<ul class="nav nav-tabs" role="tablist">
  % for id, caption in tab_bar:
    <li${' class="active"' if id == rel else '' | n}>
    <a href="${request.route_url('user_view', username=user.username, _query={'rel': id})}">${caption}</a></li>
  % endfor
</ul>

<div class="panel panel-info">
  <div class="panel-heading">Co to jest?</div>
  <div class="panel-body">
  % if rel == 'comments':
    <p>Komentarze dot. firm dodane przez użytkownika.</p>
  % elif rel == 'branches':
    <p>Branże dodane przez użytkownika.</p>
  % elif rel == 'companies':
    <p>Firmy dodane przez użytkownika.</p>
  % elif rel == 'investors':
    <p>Inwestorzy dodani przez użytkownika.</p>
  % elif rel == 'tenders':
    <p>Przetargi dodane przez użytkownika.</p>
  % elif rel == 'offers':
    <p>Oferty dodane przez użytkownika.</p>
  % endif
  </div>
</div>


% if rel == 'comments':
  % for comment in paginator.items:
    <div class="panel panel-default">
      <div class="panel-heading">
        % if comment.company:
        <i class="fa fa-comment" aria-hidden="true"></i> <a href="${request.route_url('company_view', company_id=comment.company.id, slug=comment.company.slug)}">${comment.company.name}</a> ${comment.added.strftime('%Y-%m-%d %H:%M:%S')}
        % else:
        FIRMA USUNIĘTA Z BAZY DANYCH
        % endif
        % if comment.added_by == request.user or request.user.username == 'admin':
        <a href="${request.route_url('comment_delete', comment_id=comment.id, _query={'from': 'user'})}">Usuń</a>
        % endif
      </div>
      <div class="panel-body">
        <p>  
          ${comment.comment}
        </p>    
      </div>
    </div>
  % endfor
% endif

% if rel == 'branches':
<div class="table-responsive">
  <table class="table table-striped">
    <thead>
      <tr>
        <th class="col-sm-8">Nazwa</th>
        <th class="col-sm-2">Utworzono</th>
        <th class="col-sm-2">Zmodyfikowano</th>
      </tr>
    </thead>
    <tbody>
    % for branch in paginator.items:
      <tr>
        <td><a href="${request.route_url('branch_companies', branch_id=branch.id, slug=branch.slug)}">${branch.name}</a></td>
        <td>${branch.added.strftime('%Y-%m-%d %H:%M:%S')}</td>
        <td>${branch.edited.strftime('%Y-%m-%d %H:%M:%S')}</td>
      </tr>
    % endfor
    </tbody>
  </table>
</div>
% endif

% if rel == 'companies':
<div class="table-responsive">
  <table class="table table-striped">
    <thead>
      <tr>
        <th class="col-sm-5">Nazwa</th>
        <th class="col-sm-3">Miasto</th>
        <th class="col-sm-2">Utworzono</th>
        <th class="col-sm-2">Zmodyfikowano</th>
      </tr>
    </thead>
    <tbody>
    % for company in paginator.items:
      <tr>
        <td><a href="${request.route_url('company_view', company_id=company.id, slug=company.slug)}">${company.name}</a></td>
        <td>${company.city}</td>
        <td>${company.added.strftime('%Y-%m-%d %H:%M:%S')}</td>
        <td>${company.edited.strftime('%Y-%m-%d %H:%M:%S')}</td>
      </tr>
    % endfor
    </tbody>
  </table>
</div>
% endif

% if rel == 'investors':
<div class="table-responsive">
  <table class="table table-striped">
    <thead>
      <tr>
        <th class="col-sm-5">Nazwa</th>
        <th class="col-sm-3">Miasto</th>
        <th class="col-sm-2">Utworzono</th>
        <th class="col-sm-2">Zmodyfikowano</th>
      </tr>
    </thead>
    <tbody>
    % for investor in paginator.items:
      <tr>
        <td><a href="${request.route_url('investor_view', investor_id=investor.id, slug=investor.slug)}">${investor.name}</a></td>
        <td>${investor.city}</td>
        <td>${investor.added.strftime('%Y-%m-%d %H:%M:%S')}</td>
        <td>${investor.edited.strftime('%Y-%m-%d %H:%M:%S')}</td>
      </tr>
    % endfor
    </tbody>
  </table>
</div>
% endif

% if rel == 'tenders':
<div class="table-responsive">
  <table class="table table-striped">
    <thead>
      <tr>
        <th class="col-sm-5">Nazwa</th>
        <th class="col-sm-3">Miasto</th>
        <th class="col-sm-2">Utworzono</th>
        <th class="col-sm-2">Zmodyfikowano</th>
      </tr>
    </thead>
    <tbody>
    % for tender in paginator.items:
      <tr>
        <td><a href="${request.route_url('tender_view', tender_id=tender.id, slug=tender.slug)}">${tender.name}</a></td>
        <td>${tender.city}</td>
        <td>${tender.added.strftime('%Y-%m-%d %H:%M:%S')}</td>
        <td>${tender.edited.strftime('%Y-%m-%d %H:%M:%S')}</td>
      </tr>
    % endfor
    </tbody>
  </table>
</div>
% endif

% if rel == 'offers':
<div class="row">
  <div class="col-md-12">
    <div class="table-responsive">
      <table id="offers" class="table table-striped">
        <thead>
          <tr>
            <th class="col-sm-4">Firma</th>
            <th class="col-sm-4">Przetarg</th>
            <th class="col-sm-3">Branża</th>
            <th class="col-sm-1">Szczegóły</th>
          </tr>
        </thead>
        <tbody>
        % for offer in paginator.items:
          <tr>
            <td>
              % if offer.company:
                <a href="${request.route_url('company_view', company_id=offer.company.id, slug=offer.company.slug)}">${offer.company.name}</a>
              % else:
                ---
              % endif
            </td>
            <td>
              % if offer.tender:
                <a href="${request.route_url('tender_view', tender_id=offer.tender.id, slug=offer.tender.slug)}">${offer.tender.name}
              % else:
                ---
              % endif
            </td>
            <td>
              % if offer.branch:
                <a href="${request.route_url('branch_offers', branch_id=offer.branch.id, slug=offer.branch.slug)}">${offer.branch.name}</a>
              % else:
                ---
              % endif
            </td>
            <td><a href="${request.route_url('offer_view', offer_id=offer.id)}">Pokaż</a></td>
          </tr>
        % endfor
        </tbody>
      </table>
    </div>
  </div>
</div>
% endif

<div class="text-center">
  <ul class="pagination">
    ${paginator.pager() | n}
  </ul>
</div>

<div class="modal fade" id="deleteModal" tabindex="-1" role="dialog" aria-labelledby="deleteModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title">Usuń</h4>
      </div>
      <div class="modal-body">
        Czy na pewno chcesz usunąć użytkownika z bazy danych?
      </div>
      <div class="modal-footer">
        <form action="${request.route_url('user_delete', username=user.username)}" method="post">
          <input type="hidden" name="csrf_token" value="${request.session.get_csrf_token()}">
          <button type="button" class="btn btn-default" data-dismiss="modal">Nie</button>
          <button type="submit" class="btn btn-primary" name="submit" value="delete">Tak</button>
        </form>
      </div>
    </div>
  </div>
</div>
