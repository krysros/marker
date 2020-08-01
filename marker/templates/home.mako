<%inherit file="layout.mako"/>

<div class="jumbotron">
  <h1>Marker <small>Katalog Generalnego Wykonawcy</small></h1>
  <p>
    Informacje o firmach, przetargach, inwestorach i ofertach.
    Znajdź firmy o określonym profilu działalności oraz te
    najczęściej rekomendowane. Sprawdź, które regiony kraju
    są najbardziej przedsiębiorcze i w jakich branżach jest
    największa konkurencja.
  </p>
</div>

<div class="row">
  <div class="col-xs-6 col-lg-4">
    <h2><i class="fa fa-cubes" aria-hidden="true"></i> Branże</h2>
    <p>
      Wyświetl firmy o określonym profilu działalności.
      Pokaż listę ofert na wybrany zakres prac. 
    </p>
    <p><a class="btn btn-default"
          href="${request.route_url('branches')}"
          role="button">Pokaż &raquo;</a></p>
  </div>
  <div class="col-xs-6 col-lg-4">
    <h2><i class="fa fa-industry" aria-hidden="true"></i> Firmy</h2>
    <p>
      Wyświetl listę firm ostatnio dodanych do bazy danych.
      Pokaż firmy, których dane zostały ostatnio zmienione.
    </p>
    <p><a class="btn btn-default"
          href="${request.route_url('companies')}"
          role="button">Pokaż &raquo;</a></p>
  </div>
  <div class="col-xs-6 col-lg-4">
    <h2><i class="fa fa-euro" aria-hidden="true"></i> Inwestorzy</h2>
    <p>
      Pokaż listę inwestorów. Sprawdź, jakie przetargi
      zostały przez nich ogłoszone.
    </p>
    <p><a class="btn btn-default"
          href="${request.route_url('investors')}"
          role="button">Pokaż &raquo;</a></p>
  </div>
  <div class="col-xs-6 col-lg-4">
    <h2><i class="fa fa-briefcase" aria-hidden="true"></i> Przetargi</h2>
    <p>
      Pokaż listę przetargów. Filtruj przetargi, aby wyświetlić te,
      które są w trakcie lub zostały zakończone.
    </p>
    <p><a class="btn btn-default"
          href="${request.route_url('tenders')}"
          role="button">Pokaż &raquo;</a></p>
  </div>
  <div class="col-xs-6 col-lg-4">
    <h2><i class="fa fa-puzzle-piece" aria-hidden="true"></i> Oferty</h2>
    <p>
      Wyświetl listę ofert ostatnio dodanych do bazy danych.
      Sprawdź, które firmy je złożyły i w jakich przetargach.
    </p>
    <p><a class="btn btn-default"
          href="${request.route_url('offers')}"
          role="button">Pokaż &raquo;</a></p>
  </div>
  <div class="col-xs-6 col-lg-4">
    <h2><i class="fa fa-line-chart" aria-hidden="true"></i> Raporty</h2>
    <p>
      Wyświetl podsumowanie zawartości bazy danych.
      Analizuj dane o firmach, inwestorach i przetargach.
    </p>
    <p><a class="btn btn-default"
          href="${request.route_url('report')}"
          role="button">Pokaż &raquo;</a></p>
  </div>
  <div class="col-xs-6 col-lg-4">
    <h2><i class="fa fa-search" aria-hidden="true"></i> Wyszukiwarka</h2>
    <p>
      Wyszukaj dane kontaktowe, informacje o firmach, inwestorach,
      przetargach i relacjach pomiędzy nimi.
    </p>
  </div>
  <div class="col-xs-6 col-lg-4">
    <h2><i class="fa fa-file-excel-o" aria-hidden="true"></i> Eksport</h2>
    <p>
      Wyeksportuj wybrane dane kontaktowe do Excela.
      Skorzystaj z korespondencji seryjnej.
    </p>
  </div>
  <div class="col-xs-6 col-lg-4">
    <h2><i class="fa fa-users" aria-hidden="true"></i> Użytkownicy</h2>
    <p>
      Wyświetl listę użytkowników bazy danych.
    </p>
    <p><a class="btn btn-default"
          href="${request.route_url('users')}"
          role="button">Pokaż &raquo;</a></p>
  </div>
</div>
