<%inherit file="layout.mako"/>

<div class="panel panel-default">
  <div class="panel-body">
    <div class="btn-group">
      <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-expanded="false">
        Widok <i class="fa fa-caret-down" aria-hidden="true"></i>
      </button>
      <ul class="dropdown-menu" role="menu">
        <li><a role="menuitem" tabindex="-1" data-toggle="modal" href="${request.route_url('branch_companies', branch_id=branch.id, slug=branch.slug)}">firmy</a></li>
        <li><a role="menuitem" tabindex="-1" data-toggle="modal" href="${request.route_url('branch_offers', branch_id=branch.id, slug=branch.slug)}">oferty</a></li>
      </ul>
    </div>
    <div class="pull-right">
      <a href="${request.route_url('branch_edit', branch_id=branch.id, slug=branch.slug)}" class="btn btn-warning" role="button"><i class="fa fa-edit" aria-hidden="true"></i> Edytuj</a>
      <a data-toggle="modal" href="#deleteModal" class="btn btn-danger" role="button"><i class="fa fa-trash" aria-hidden="true"></i> Usuń</a>
    </div>
  </div>
</div>

<div class="panel panel-default">
  <div class="panel-heading"><i class="fa fa-cube" aria-hidden="true"></i> Oferty branży ${branch.name}</div>
  <div class="panel-body">
    <div class="row">
      <div class="col-md-12">
        <table id="companies" class="table table-striped">
          <thead>
            <tr>
              <th class="col-sm-6">Nazwa firmy</th>
              <th class="col-sm-6">Nazwa przetargu</th>
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
                <a href="${request.route_url('tender_view', tender_id=offer.tender.id, slug=offer.tender.slug)}">${offer.tender.name}</a>
                % else:
                ---
                % endif
              </td>
            </tr>
          % endfor
          </tbody>
        </table>
      </div>
    </div>
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
        Czy na pewno chcesz usunąć branżę z bazy danych?
      </div>
      <div class="modal-footer">
        <form action="${request.route_url('branch_delete', branch_id=branch.id, slug=branch.slug)}" method="post">
          <input type="hidden" name="csrf_token" value="${request.session.get_csrf_token()}">
          <button type="button" class="btn btn-default" data-dismiss="modal">Nie</button>
          <button type="submit" class="btn btn-primary" name="submit" value="delete">Tak</button>
        </form>
      </div>
    </div>
  </div>
</div>

<div class="text-center">
  <ul class="pagination">
    ${paginator.pager() | n}
  </ul>
</div>