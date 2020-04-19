<%inherit file="layout.mako"/>

<div class="panel panel-default">
  <div class="panel-body">
    <div class="pull-right">
      <a href="${request.route_url('offer_edit', offer_id=offer.id)}" class="btn btn-warning" role="button"><i class="fa fa-edit" aria-hidden="true"></i> Edytuj</a>
      <a data-toggle="modal" href="#deleteModal" class="btn btn-danger" role="button"><i class="fa fa-trash" aria-hidden="true"></i> Usuń</a>
    </div>
  </div>
</div>

<div class="panel panel-default">
  <div class="panel-heading"><i class="fa fa-puzzle-piece" aria-hidden="true"></i> Oferta</div>
  <div class="panel-body">
    <dl class="dl-horizontal">
      <dt>Firma</dt>
      <dd>
      % if offer.company:
        <a href="${request.route_url('company_view', company_id=offer.company.id, slug=offer.company.slug)}">${offer.company.name}</a>
      % else:
        ---
      % endif
      </dd>
      <dt>Branża</dt>
      <dd>
      % if offer.branch:
        <a href="${request.route_url('branch_companies', branch_id=offer.branch.id, slug=offer.branch.slug)}">${offer.branch.name}</a>
      % else:
        ---
      % endif
      </dd>
      <dt>Przetarg</dt>
      <dd>
      % if offer.tender:
        <a href="${request.route_url('tender_view', tender_id=offer.tender.id, slug=offer.tender.slug)}">${offer.tender.name}</a>
      % else:
        ---
      % endif
      </dd>
      <dt>Kategoria</dt>
      <dd>${offer.category}</dd>
      <dt>Jednostka</dt>
      <dd>${offer.unit}</dd>
      <dt>Cena</dt>
      <dd>${offer.cost}</dd>
      <dt>Waluta</dt>
      <dd>${offer.currency}</dd>
    </dl>
  </div>
</div>

% if offer.description:
<div class="panel panel-default">
  <div class="panel-heading"><i class="fa fa-sticky-note-o" aria-hidden="true"></i> Opis</div>
  <div class="panel-body">
    <textarea readonly class="form-control" rows="10">${offer.description}</textarea>
  </div>
</div>
% endif

<div class="panel panel-default">
  <div class="panel-heading"><i class="fa fa-clock-o" aria-hidden="true"></i> Data modyfikacji</div>
  <div class="panel-body">
    <p>
      Utworzono: ${offer.added.strftime('%Y-%m-%d %H:%M:%S')}
      % if offer.added_by:
        przez <a href="${request.route_url('user_view', username=offer.added_by.username, what='info')}">${offer.added_by.username}</a>
      % endif
      <br>
      % if offer.edited:
        Zmodyfikowano: ${offer.edited.strftime('%Y-%m-%d %H:%M:%S')}
        % if offer.edited_by:
          przez <a href="${request.route_url('user_view', username=offer.edited_by.username, what='info')}">${offer.edited_by.username}</a>
        % endif
      % endif
    </p>
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
        Czy na pewno chcesz usunąć ofertę z bazy danych?
      </div>
      <div class="modal-footer">
        <form action="${request.route_url('offer_delete', offer_id=offer.id)}" method="post">
          <input type="hidden" name="csrf_token" value="${request.session.get_csrf_token()}">
          <button type="button" class="btn btn-default" data-dismiss="modal">Nie</button>
          <button type="submit" class="btn btn-primary" name="submit" value="delete">Tak</button>
        </form>
      </div>
    </div>
  </div>
</div>