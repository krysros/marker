<%inherit file="layout.mako"/>

<div class="panel panel-default">
  <div class="panel-body">
    <div class="pull-right">
      % if tender.link:
        <a href="${tender.link}" class="btn btn-info" role="button" target="_blank"><i class="fa fa-external-link" aria-hidden="true"></i> Ogłoszenie</a>
      % endif
      <a href="${request.route_url('tender_edit', tender_id=tender.id, slug=tender.slug)}" class="btn btn-warning" role="button"><i class="fa fa-edit" aria-hidden="true"></i> Edytuj</a>
      <a data-toggle="modal" href="#deleteModal" class="btn btn-danger" role="button"><i class="fa fa-trash" aria-hidden="true"></i> Usuń</a>
    </div>
  </div>
</div>

<div class="panel panel-default">
  <div class="panel-heading"><i class="fa fa-briefcase" aria-hidden="true"></i> Przetarg</div>
  <div class="panel-body">
    <dl class="dl-horizontal">
      <dt>Nazwa przetargu</dt>
      <dd>${tender.name}</dd>
      <dt>Miasto</dt>
      <dd><a href="https://maps.google.pl/maps?q=${tender.city}">${tender.city}</a></dd>
      <dt>Inwestor</dt>
      % if tender.investor:
        <dd><a href="${request.route_url('investor_view', investor_id=tender.investor.id, slug=tender.investor.slug)}">${tender.investor.name}</a></dd>
      % else:
        <dd>---</dd>
      % endif
      <dt>Termin składania ofert</dt>
      <dd>${tender.deadline}</dd>
    </dl>
  </div>
</div>

<div class="panel panel-default">
  <div class="panel-heading"><i class="fa fa-puzzle-piece" aria-hidden="true"></i> Oferty</div>
  <div class="panel-body">
    <div class="table-responsive">
      <table id="offers" class="table table-striped">
        <thead>
          <tr>
            <th>Firma</th>
            <th>Branża</th>
            <th>Utworzono</th>
            <th>Szczegóły</th>
          </tr>
        </thead>
        <tbody>
        % for offer in tender.offers:
          <tr>
            <td>
              % if offer.company:
                <a href="${request.route_url('company_view', company_id=offer.company.id, slug=offer.company.slug)}">${offer.company.name}</a>
              % else:
                ---
              % endif
            </td>
            <td>
              % if offer.branch:
                <a href="${request.route_url('branch_companies', branch_id=offer.branch.id, slug=offer.branch.slug)}">${offer.branch.name}</a>
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

<div class="panel panel-default">
  <div class="panel-heading"><i class="fa fa-clock-o" aria-hidden="true"></i> Data modyfikacji</div>
  <div class="panel-body">
    <p>
      Utworzono: ${tender.added.strftime('%Y-%m-%d %H:%M:%S')}
      % if tender.added_by:
        przez <a href="${request.route_url('user_view', username=tender.added_by.username, what='info')}">${tender.added_by.username}</a>
      % endif
      <br>
      % if tender.edited:
        Zmodyfikowano: ${tender.edited.strftime('%Y-%m-%d %H:%M:%S')}
        % if tender.edited_by:
          przez <a href="${request.route_url('user_view', username=tender.edited_by.username, what='info')}">${tender.edited_by.username}</a>
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
        Czy na pewno chcesz usunąć przetarg z bazy danych?
      </div>
      <div class="modal-footer">
        <form action="${request.route_url('tender_delete', tender_id=tender.id, slug=tender.slug)}" method="post">
          <input type="hidden" name="csrf_token" value="${request.session.get_csrf_token()}">
          <button type="button" class="btn btn-default" data-dismiss="modal">Nie</button>
          <button type="submit" class="btn btn-primary" name="submit" value="delete">Tak</button>
        </form>
      </div>
    </div>
  </div>
</div>