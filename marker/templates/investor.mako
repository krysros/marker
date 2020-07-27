<%inherit file="layout.mako"/>

<div class="panel panel-default">
  <div class="panel-body">
    <div class="pull-right">
      % if investor.link:
        <a href="${investor.link}" class="btn btn-info" role="button" target="_blank"><i class="fa fa-external-link" aria-hidden="true"></i> Link</a>
      % endif
      <a href="${request.route_url('investor_edit', investor_id=investor.id, slug=investor.slug)}" class="btn btn-warning" role="button"><i class="fa fa-edit" aria-hidden="true"></i> Edytuj</a>
      <a data-toggle="modal" href="#deleteModal" class="btn btn-danger" role="button"><i class="fa fa-trash" aria-hidden="true"></i> Usuń</a>
    </div>
  </div>
</div>

<div class="panel panel-default">
  <div class="panel-heading"><i class="fa fa-euro" aria-hidden="true"></i> Inwestor</div>
  <div class="panel-body">
    <h1>${investor.name}</h1>
    <div class="row">
      <div class="col-md-12">
        <address>
          <h3><i class="fa fa-map-marker" aria-hidden="true"></i> Adres</h3>
          ${investor.city}<br>
          % if investor.city:
            <a href="https://maps.google.pl/maps?q=${investor.city}">Pokaż na mapie</a>
          % endif
        </address>
      </div>
    </div>
  </div>
</div>

<div class="panel panel-default">
  <div class="panel-heading"><i class="fa fa-briefcase" aria-hidden="true"></i> Przetargi</div>
  <div class="panel-body">
    <div class="table-responsive">
      <table id="tenders" class="table table-striped">
        <thead>
          <tr>
            <th>Przetarg</th>
            <th>Miasto</th>
          </tr>
        </thead>
        <tbody>
        % for tender in investor.tenders:
          <tr>
            <td><a href="${request.route_url('tender_view', tender_id=tender.id, slug=tender.slug)}">${tender.name}</a></td>
            <td>${tender.city}</td>
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
      Utworzono: ${investor.added.strftime('%Y-%m-%d %H:%M:%S')}
      % if investor.added_by:
        przez <a href="${request.route_url('user_view', username=investor.added_by.username, what='info')}">${investor.added_by.username}</a>
      % endif
      <br>
      % if investor.edited:
        Zmodyfikowano: ${investor.edited.strftime('%Y-%m-%d %H:%M:%S')}
        % if investor.edited_by:
          przez <a href="${request.route_url('user_view', username=investor.edited_by.username, what='info')}">${investor.edited_by.username}</a>
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
        Czy na pewno chcesz usunąć inwestora z bazy danych?
      </div>
      <div class="modal-footer">
        <form action="${request.route_url('investor_delete', investor_id=investor.id, slug=investor.slug)}" method="post">
          <input type="hidden" name="csrf_token" value="${request.session.get_csrf_token()}">
          <button type="button" class="btn btn-default" data-dismiss="modal">Nie</button>
          <button type="submit" class="btn btn-primary" name="submit" value="delete">Tak</button>
        </form>
      </div>
    </div>
  </div>
</div>