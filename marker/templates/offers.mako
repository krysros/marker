<%inherit file="layout.mako"/>

<div class="row">
  <div class="col-md-12">
    <div class="table-responsive">
      <table id="offers" class="table table-striped">
        <thead>
          <tr>
            <th>Firma</th>
            <th>Przetarg</th>
            <th>Branża</th>
            <th>Szczegóły</th>
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

<div class="text-center">
  <ul class="pagination">
    ${paginator.pager() | n}
  </ul>
</div>