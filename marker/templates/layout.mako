<!DOCTYPE html>
<html lang="${request.locale_name}">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Katalog Generalnego Wykonawcy">
    <meta name="author" content="krysros">
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
          % if logged_in:
            <li class="dropdown">
              <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                <i class="fa fa-user" aria-hidden="true"></i> ${logged_in} <i class="fa fa-caret-down" aria-hidden="true"></i>
              </a>
              <ul class="dropdown-menu" role="menu">
                <li><a href="${request.route_url('account', username=logged_in)}">
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
          <form class="navbar-form navbar-right" action="${request.route_url('search')}">
            <input type="text" name="q" class="form-control" placeholder="Szukaj...">
            % if tab:
            <input type="hidden" name="tab" value="${tab}">
            % endif
          </form>
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
        <p><i class="fa fa-copyright"></i> Krystian Rosiński 2017</p>
      </div>
    </footer>
  </body>
</html>