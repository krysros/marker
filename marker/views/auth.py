import logging
from pyramid.httpexceptions import HTTPFound
from pyramid.security import (
    remember,
    forget,
    )
from pyramid.view import (
    view_config,
    forbidden_view_config,
    )

import deform
import colander

from ..models import User
from deform.schema import CSRFSchema


log = logging.getLogger(__name__)


class Schema(CSRFSchema):
    login = colander.SchemaNode(
        colander.String(),
        title="Login"
        )
    password = colander.SchemaNode(
        colander.String(),
        title="Hasło",
        validator=colander.Length(min=5, max=100),
        widget=deform.widget.PasswordWidget()
        )


@view_config(
    route_name='login',
    renderer='form.mako'
)
def login(request):
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/'  # never use the login form itself as next_url
    next_url = request.params.get('next', referrer)
    schema = Schema().bind(request=request)
    submit_btn = deform.form.Button(name='submit', title="Zaloguj się")
    form = deform.Form(schema, buttons=(submit_btn,))
    rendered_form = None

    if request.method == 'POST':
        if 'submit' in request.POST:
            controls = request.POST.items()
            try:
                appstruct = form.validate(controls)
            except deform.exception.ValidationFailure as e:
                rendered_form = e.render()
            else:
                login = appstruct['login']
                password = appstruct['password']
                query = request.dbsession.query(User)
                user = query.filter_by(username=login).one_or_none()
                if user is not None and user.check_password(password):
                    headers = remember(request, user.id)
                    request.session.flash('success:Witaj w aplikacji Marker!')
                    log.info(f'Użytkownik {user.username} zalogował się')
                    return HTTPFound(location=next_url, headers=headers)
                else:
                    request.session.flash('danger:Logowanie nie powiodło się')

    if rendered_form is None:
        rendered_form = form.render()

    return dict(
        url=request.route_url('login'),
        next_url=next_url,
        heading='Zaloguj się do aplikacji Marker',
        rendered_form=rendered_form,
        )


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    next_url = request.route_url('home')
    request.session.flash('success:Wylogowano z aplikacji Marker')
    log.info(f'Użytkownik {request.user.username} wylogował się')
    return HTTPFound(location=next_url, headers=headers)


@forbidden_view_config()
def forbidden_view(request):
    next_url = request.route_url('login', _query={'next': request.url})
    request.session.flash('warning:Brak wymaganych uprawnień')
    return HTTPFound(location=next_url)
