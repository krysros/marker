<%inherit file="layout.mako"/>

<div class="page-header">
  <h1>Znajdź osobę</h1>
</div>

<form class="form-horizontal" action="${request.route_url('person_search_results')}">
  <div class="form-group">
    <label class="control-label col-sm-2" for="fullname">Imię i nazwisko</label>
    <div class="col-sm-10">
      <input type="text" class="form-control" id="fullname" name="fullname" placeholder="Imię i nazwisko">
    </div>
  </div>
  <div class="form-group">
    <label class="control-label col-sm-2" for="position">Stanowisko</label>
    <div class="col-sm-10">
      <input type="text" class="form-control" id="position" name="position" placeholder="Stanowisko">
    </div>
  </div>
  <div class="form-group">
    <label class="control-label col-sm-2" for="phone">Telefon</label>
    <div class="col-sm-10">
      <input type="text" class="form-control" id="phone" name="phone" placeholder="Numer telefonu">
    </div>
  </div>
  <div class="form-group">
    <label class="control-label col-sm-2" for="email">Email</label>
    <div class="col-sm-10">
      <input type="text" class="form-control" id="email" name="email" placeholder="Adres email">
    </div>
  </div>
  <div class="form-group"> 
    <div class="col-sm-offset-2 col-sm-10">
      <button type="submit" class="btn btn-primary">Szukaj</button>
    </div>
  </div>
</form>