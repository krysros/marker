<%inherit file="layout.mako"/>

<%
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
               'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
               's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
%>

<div class="row">
  <div class="col-md-12">
    <ol class="breadcrumb">
      % for letter in letters:
        % if letter == selected_letter:
          <li class="active">${letter.upper()}</li>
        % else:
          <li><a href="${request.route_url('branch_index', letter=letter)}">${letter.upper()}</a></li>
        % endif
      % endfor
    </ol>
  </div>
</div>

<div class="row">
  <div class="col-md-12">
    <div class="table-responsive">
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
  </div>
</div>

<div class="text-center">
  <ul class="pagination">
    ${paginator.pager() | n}
  </ul>
</div>