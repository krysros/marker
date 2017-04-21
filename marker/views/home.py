from pyramid.view import view_config


@view_config(route_name='home', renderer='home.mako')
def home_view(request):
    return {'project': 'marker'}
