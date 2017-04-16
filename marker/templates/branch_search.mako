<%inherit file="layout.mako"/>

<div class="page-header">
  <h1>Znajdź branżę</h1>
</div>

<form class="form-horizontal" action="${request.route_url('branch_search_results')}">
  <div class="form-group">
    <label class="control-label col-sm-2" for="name">Nazwa</label>
    <div class="col-sm-10">
      <input type="text" class="form-control" id="name" name="name" placeholder="Nazwa branży">
    </div>
  </div>
  <div class="form-group"> 
    <div class="col-sm-offset-2 col-sm-10">
      <button type="submit" class="btn btn-primary">Szukaj</button>
    </div>
  </div>
</form>