<%inherit file="layout.mako"/>

<div class="panel panel-default">
  <div class="panel-body">
    <label class="btn btn-default">
    % if marker:
      <input class="js-mark" type="checkbox" value="${company.id}" autocomplete="off" checked>
    % else:
      <input class="js-mark" type="checkbox" value="${company.id}" autocomplete="off">
    % endif
    </label>
    <button class="btn btn-default js-upvote" value="${company.id}">
    % if upvote:
      <span class="upvote fa fa-thumbs-up fa-lg"></span>
    % else:
      <span class="upvote fa fa-thumbs-o-up fa-lg"></span>
    % endif
    </button>
    <a href="${request.route_url('company_upvotes', company_id=company.id, slug=company.slug)}" class="btn btn-default" role="button">Kto poleca?</a>
    <div class="pull-right">
      <a href="${request.route_url('comment_add', company_id=company.id)}" class="btn btn-info" role="button"><i class="fa fa-plus" aria-hidden="true"></i> Komentarz</a>
      <a href="${request.route_url('company_edit', company_id=company.id, slug=company.slug)}" class="btn btn-warning" role="button"><i class="fa fa-edit" aria-hidden="true"></i> Edytuj</a>
      <a data-toggle="modal" href="#deleteModal" class="btn btn-danger" role="button"><i class="fa fa-trash" aria-hidden="true"></i> Usuń</a>
    </div>
  </div>
</div>

<div class="panel panel-${company.category}">
  <div class="panel-heading"><i class="fa fa-industry" aria-hidden="true"></i> Firma</div>
  <div class="panel-body">
    <h1>${company.name}</h1>
    <div class="row">
      <div class="col-md-4">
        <address>
          <h3><i class="fa fa-map-marker" aria-hidden="true"></i> Adres</h3>
          ${company.city}<br>
          ${voivodeships.get(company.voivodeship)}<br>
          <a href="https://maps.google.pl/maps?q=${company.city}">Pokaż na mapie</a>
        </address>
      </div>
      <div class="col-md-4">
        <address>
          <h3><i class="fa fa-phone" aria-hidden="true"></i> Kontakt</h3>
          <abbr title="Telefon">T:</abbr> ${company.phone}<br>
          <abbr title="Email">E:</abbr> <a href="mailto:${company.email}">${company.email}</a><br>
          <abbr title="WWW">W:</abbr>
          % if company.www.startswith('http'):
            <a href="${company.www}">
          % else:
            <a href="${'http://' + company.www}">
          % endif
          ${company.www}</a>
        </address>
      </div>
      <div class="col-md-4">
        <h3><i class="fa fa-certificate" aria-hidden="true"></i> Dane rejestrowe</h3>
        NIP: ${company.nip or "brak"}<br>
        REGON: ${company.regon or "brak"}<br>
        KRS: ${company.krs or "brak"}
      </div>
    </div>
  </div>
</div>

<div class="panel panel-default">
  <div class="panel-heading"><i class="fa fa-cubes" aria-hidden="true"></i> Branże</div>
  <div class="panel-body">
    <div class="table-responsive">
      <table id="branches" class="table table-striped">
        <thead>
          <tr>
            <th class="col-sm-12">Nazwa branży</th>
          </tr>
        </thead>
        <tbody>
        % for branch in company.branches:
          <tr>
            <td><a href="${request.route_url('branch_companies', branch_id=branch.id, slug=branch.slug)}">${branch.name}</a></td>
          </tr>
        % endfor
        </tbody>
      </table>
    </div>
  </div>
</div>

<div class="panel panel-default">
  <div class="panel-heading"><i class="fa fa-group" aria-hidden="true"></i> Osoby do kontaktu</div>
  <div class="panel-body">
    <div class="table-responsive">
      <table id="people" class="table table-striped">
        <thead>
          <tr>
            <th class="col-sm-3">Imię i nazwisko</th>
            <th class="col-sm-3">Stanowisko</th>
            <th class="col-sm-2">Telefon</th>
            <th class="col-sm-3">Email</th>
          </tr>
        </thead>
        <tbody>
        % for person in company.people:
          <tr>
            <td>${person.fullname}</a></td>
            <td>${person.position}</td>
            <td>${person.phone}</td>
            <td><a href="mailto:${person.email}">${person.email}</a></td>
          </tr>
        % endfor
        </tbody>
      </table>
    </div>
  </div>
</div>

<div class="panel panel-default">
  <div class="panel-heading"><i class="fa fa-puzzle-piece" aria-hidden="true"></i> Oferty</div>
  <div class="panel-body">
    <div class="table-responsive">
      <table id="offers" class="table table-striped">
        <thead>
          <tr>
            <th class="col-sm-6">Przetarg</th>
            <th class="col-sm-4">Data</th>
            <th class="col-sm-2">Szczegóły</th>
          </tr>
        </thead>
        <tbody>
        % for offer in company.offers:
          <tr>
            <td>
              % if offer.tender:
                <a href="${request.route_url('tender_view', tender_id=offer.tender.id, slug=offer.tender.slug)}">${offer.tender.name}</a>
              % else:
                ---
              % endif
            </td>
            <td>${offer.added.strftime('%Y-%m-%d %H:%M:%S')}</td>
            <td><a href="${request.route_url('offer_view', offer_id=offer.id)}">Pokaż</a></td>
          </tr>
        % endfor
        </tbody>
      </table>
    </div>
  </div>
</div>

% for comment in company.comments:
<div class="panel panel-default">
  <div class="panel-heading">
    <i class="fa fa-comment" aria-hidden="true"></i> <a href="${request.route_url('user_view', username=comment.added_by.username, what='info')}" title="${comment.added_by.fullname}">${comment.added_by.username}</a> ${comment.added.strftime('%Y-%m-%d %H:%M:%S')}
    % if comment.added_by == request.user or request.user.username == 'admin':
    <a href="${request.route_url('comment_delete', company_id=company.id, comment_id=comment.id)}">Usuń</a>
    % endif
  </div>
  <div class="panel-body">
    <p>  
      ${comment.comment}
    </p>    
  </div>
</div>
% endfor

<div class="panel panel-default">
  <div class="panel-heading"><i class="fa fa-clock-o" aria-hidden="true"></i> Data modyfikacji</div>
  <div class="panel-body">
    <p>
      Utworzono: ${company.added.strftime('%Y-%m-%d %H:%M:%S')}
      % if company.added_by:
        przez <a href="${request.route_url('user_view', username=company.added_by.username, what='info')}">${company.added_by.username}</a>
      % endif
      <br>
      % if company.edited:
        Zmodyfikowano: ${company.edited.strftime('%Y-%m-%d %H:%M:%S')}
        % if company.edited_by:
          przez <a href="${request.route_url('user_view', username=company.edited_by.username, what='info')}">${company.edited_by.username}</a>
        % endif
      % endif
    </p>
  </div>
</div>

<div class="panel panel-default">
  <div class="panel-heading">Podobne</div>
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
          % for similar_company in paginator.items:
          <tr class="${similar_company.category}">
            <td>
            % if similar_company in user_marker:
              <input class="js-mark" type="checkbox" value="${similar_company.id}" autocomplete="off" checked>
            % else:
              <input class="js-mark" type="checkbox" value="${similar_company.id}" autocomplete="off">
            % endif
            </td>
            <td>
            % if similar_company in user_upvotes:
              <i class="fa fa-thumbs-up" aria-hidden="true"></i>
            % endif
              <a href="${request.route_url('company_view', company_id=similar_company.id, slug=similar_company.slug)}">${similar_company.name}</a>
            </td>
            <td>${similar_company.city}</td>
            <td>${voivodeships.get(similar_company.voivodeship)}</td>
            <td><a href="${request.route_url('company_upvotes', company_id=similar_company.id, slug=similar_company.slug)}">Pokaż</a> (${similar_company.upvote_count})</td>
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
</div>

<div class="modal fade" id="deleteModal" tabindex="-1" role="dialog" aria-labelledby="deleteModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title">Usuń</h4>
      </div>
      <div class="modal-body">
        Czy na pewno chcesz usunąć firmę z bazy danych?
      </div>
      <div class="modal-footer">
        <form action="${request.route_url('company_delete', company_id=company.id, slug=company.slug)}" method="post">
          <input type="hidden" name="csrf_token" value="${request.session.get_csrf_token()}">
          <button type="button" class="btn btn-default" data-dismiss="modal">Nie</button>
          <button type="submit" class="btn btn-primary" name="submit" value="delete">Tak</button>
        </form>
      </div>
    </div>
  </div>
</div>