<%inherit file="layout.mako"/>

<div class="page-header">
  <h1>Znajdź firmę</h1>
</div>

<form class="form-horizontal" action="${request.route_url('company_search_results')}">
  <div class="form-group">
    <label class="control-label col-sm-2" for="name">Nazwa</label>
    <div class="col-sm-10">
      <input type="text" class="form-control" id="name" name="name" placeholder="Nazwa firmy">
    </div>
  </div>
  <div class="form-group">
    <label class="control-label col-sm-2" for="city">Miasto</label>
    <div class="col-sm-10"> 
      <input type="text" class="form-control" id="city" name="city" placeholder="Siedziba firmy">
    </div>
  </div>
  <div class="form-group">
    <label class="control-label col-sm-2" for="voivodeship">Województwo</label>
    <div class="col-sm-10"> 
      <select class="form-control" id="voivodeship" name="voivodeship">
        % for k, v in voivodeships.items():
          <option value="${k}">${v}</option>
        % endfor
      </select>
    </div>
  </div>
  <div class="form-group">
    <label class="control-label col-sm-2" for="phone">Telefon</label>
    <div class="col-sm-10"> 
      <input type="text" class="form-control" id="phone" name="phone" placeholder="Telefon">
    </div>
  </div>
  <div class="form-group">
    <label class="control-label col-sm-2" for="email">Email</label>
    <div class="col-sm-10"> 
      <input type="text" class="form-control" id="email" name="email" placeholder="Adres email">
    </div>
  </div>
  <div class="form-group">
    <label class="control-label col-sm-2" for="www">WWW</label>
    <div class="col-sm-10"> 
      <input type="text" class="form-control" id="www" name="www" placeholder="Adres strony internetowej">
    </div>
  </div>
  <div class="form-group">
    <label class="control-label col-sm-2" for="nip">NIP</label>
    <div class="col-sm-10"> 
      <input type="text" class="form-control" id="nip" name="nip" placeholder="Numer NIP">
    </div>
  </div>
  <div class="form-group">
    <label class="control-label col-sm-2" for="regon">REGON</label>
    <div class="col-sm-10"> 
      <input type="text" class="form-control" id="regon" name="regon" placeholder="Numer REGON">
    </div>
  </div>
  <div class="form-group">
    <label class="control-label col-sm-2" for="krs">KRS</label>
    <div class="col-sm-10"> 
      <input type="text" class="form-control" id="krs" name="krs" placeholder="Numer KRS">
    </div>
  </div>
  <div class="form-group"> 
    <div class="col-sm-offset-2 col-sm-10">
      <button type="submit" class="btn btn-primary">Szukaj</button>
    </div>
  </div>
</form>