<!DOCTYPE html>
<html lang="${request.locale_name}">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Katalog Generalnego Wykonawcy">
    <meta name="author" content="krysros">
    <meta name="csrf_token" content="${request.session.get_csrf_token()}">
    <link rel="shortcut icon" href="${request.static_url('marker:static/img/favicon.png')}">
    <title>Marker</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="${request.static_url('deform:static/css/bootstrap.min.css')}">
    <link rel="stylesheet" href="${request.static_url('deform:static/css/form.css')}">
    % if css_links:
      % for reqt in css_links:
      <link rel="stylesheet" href="${request.static_url(reqt)}">
      % endfor
    % endif
    <!-- Custom styles for this template -->
    <link rel="stylesheet" href="${request.static_url('marker:static/css/marker.css')}">
    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="//oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="//oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>
    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="${request.static_url('deform:static/scripts/jquery-2.0.3.min.js')}" type="text/javascript"></script>
    <script src="${request.static_url('deform:static/scripts/bootstrap.min.js')}" type="text/javascript"></script>
    % if js_links:
      % for reqt in js_links:
      <script src="${request.static_url(reqt)}" type="text/javascript"></script>
      % endfor
    % endif
    <script src="${request.static_url('marker:static/js/company_mark.js')}" type="text/javascript"></script>
    <script src="${request.static_url('marker:static/js/company_upvote.js')}" type="text/javascript"></script>
    <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
      <div class="container-fluid">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="${request.route_url('home')}">MARKER</a>
        </div>
        <div class="navbar-collapse collapse">
          <ul class="nav navbar-nav navbar-right">
          % if request.user is not None:
            <li class="dropdown">
              <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                <i class="fa fa-user" aria-hidden="true"></i> ${request.user.username} <i class="fa fa-caret-down" aria-hidden="true"></i>
              </a>
              <ul class="dropdown-menu" role="menu">
                <li><a href="${request.route_url('account', username=request.user.username)}">
                  <i class="fa fa-edit" aria-hidden="true"></i> Konto</a>
                </li>
                <li class="divider"></li>
                <li><a href="${request.application_url}/logout">
                  <i class="fa fa-sign-out" aria-hidden="true"></i> Wyloguj</a>
                </li>
              </ul>
            </li>
          % else:
            <li><a href="${request.application_url}/login">Zaloguj</a></li>
          % endif
          </ul>
          <ul class="nav navbar-nav navbar-right">
            <li class="dropdown">
              <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                <i class="fa fa-search" aria-hidden="true"></i> Szukaj <i class="fa fa-caret-down" aria-hidden="true"></i>
              </a>
              <ul class="dropdown-menu" role="menu">
                <li><a href="${request.route_url('branch_search')}"><i class="fa fa-cube" aria-hidden="true"></i> branżę</a></li>
                <li><a href="${request.route_url('company_search')}"><i class="fa fa-industry" aria-hidden="true"></i> firmę</a></li>
                <li><a href="${request.route_url('investor_search')}"><i class="fa fa-euro" aria-hidden="true"></i> inwestora</a></li>
                <li><a href="${request.route_url('tender_search')}"><i class="fa fa-briefcase" aria-hidden="true"></i> przetarg</a></li>
                <li><a href="${request.route_url('person_search')}"><i class="fa fa-user-o" aria-hidden="true"></i> osobę</a></li>
                <li><a href="${request.route_url('user_search')}"><i class="fa fa-user" aria-hidden="true"></i> użytkownika</a></li>
              </ul>
            </li>
          </ul>
          <ul class="nav navbar-nav navbar-right">
            <li class="dropdown">
              <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                <i class="fa fa-plus" aria-hidden="true"></i> Dodaj <i class="fa fa-caret-down" aria-hidden="true"></i>
              </a>
              <ul class="dropdown-menu" role="menu">
                <li><a href="${request.route_url('branch_add')}"><i class="fa fa-cube" aria-hidden="true"></i> branżę</a></li>
                <li><a href="${request.route_url('company_add')}"><i class="fa fa-industry" aria-hidden="true"></i> firmę</a></li>
                <li><a href="${request.route_url('investor_add')}"><i class="fa fa-euro" aria-hidden="true"></i> inwestora</a></li>
                <li><a href="${request.route_url('tender_add')}"><i class="fa fa-briefcase" aria-hidden="true"></i> przetarg</a></li>
                <li><a href="${request.route_url('offer_add')}"><i class="fa fa-puzzle-piece" aria-hidden="true"></i> ofertę</a></li>
                <li><a href="${request.route_url('user_add')}"><i class="fa fa-user" aria-hidden="true"></i> użytkownika</a></li>
              </ul>
            </li>
          </ul>
          <ul class="nav navbar-nav navbar-right">
            <li class="dropdown">
              <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                <i class="fa fa-database" aria-hidden="true"></i> Baza danych <i class="fa fa-caret-down" aria-hidden="true"></i>
              </a>
              <ul class="dropdown-menu" role="menu">
                <li><a href="${request.route_url('branches')}"><i class="fa fa-cube" aria-hidden="true"></i> Branże</a></li>
                <li><a href="${request.route_url('companies')}"><i class="fa fa-industry" aria-hidden="true"></i> Firmy</a></li>
                <li><a href="${request.route_url('investors')}"><i class="fa fa-euro" aria-hidden="true"></i> Inwestorzy</a></li>
                <li><a href="${request.route_url('tenders')}"><i class="fa fa-briefcase" aria-hidden="true"></i> Przetargi</a></li>
                <li><a href="${request.route_url('offers')}"><i class="fa fa-puzzle-piece" aria-hidden="true"></i> Oferty</a></li>
                <li><a href="${request.route_url('users')}"><i class="fa fa-user" aria-hidden="true"></i> Użytkownicy</a></li>
              </ul>
            </li>
          </ul>
          % if request.user is not None:
          <ul class="nav navbar-nav navbar-right">
              <li><a href="${request.route_url('user_marked', username=request.user.username)}"><i class="fa fa-check-square-o" aria-hidden="true"></i> Zaznaczone</a></li>
              <li><a href="${request.route_url('user_upvotes', username=request.user.username)}"><i class="fa fa-thumbs-up" aria-hidden="true"></i> Rekomendowane</a></li>
          </ul>
          % endif
        </div>
      </div>
    </div>
    <div class="container">
      <div class="row">
        <div class="col-md-12 main">
          % if request.session.peek_flash():
            % for message in request.session.pop_flash():
              <div class="alert alert-${message.split(':')[0]} alert-dismissable">
                ${message.split(':')[1] | n}
              </div>
            % endfor
          % endif
          ${self.body()}
        </div>
      </div>
    </div>
    <footer class="footer">
      <div class="container">
        <hr>
        <p class="pull-right"><a href="#top"><i class="fa fa-arrow-up"></i> Do góry</a></p>
        <p><i class="fa fa-copyright"></i> Krystian Rosiński 2020</p>
      </div>
    </footer>
  </body>
</html>