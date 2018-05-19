import logging
from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )

from sqlalchemy import func

import deform
import colander

from ..models import (
    User,
    marker,
    upvotes,
    Company,
    )
from deform.schema import CSRFSchema
from ..paginator import get_paginator
from ..helpers import export_to_xlsx


log = logging.getLogger(__name__)


class UserView(object):
    def __init__(self, request):
        self.request = request

    @property
    def user_form(self):

        def check_name(node, value):
            query = self.request.dbsession.query(User)
            exists = query.filter_by(username=value).one_or_none()
            username = self.request.matchdict.get('username', None)
            if exists and username != exists.username:
                raise colander.Invalid(node,
                                       'Ta nazwa użytkownika jest już zajęta')

        choices = (
            ('basic', 'Wyświetlanie'),
            ('editor', 'Edytowanie'),
            ('admin', 'Administrator'),
        )

        class Schema(CSRFSchema):
            username = colander.SchemaNode(
                colander.String(),
                title='Nazwa użytkownika',
                validator=colander.All(
                    colander.Length(min=3, max=30), check_name)
                )
            fullname = colander.SchemaNode(
                colander.String(),
                title='Imię i nazwisko',
                validator=colander.Length(min=5, max=50),
                )
            email = colander.SchemaNode(
                colander.String(),
                title='Adres email',
                validator=colander.Email(),
                )
            role = colander.SchemaNode(
                colander.String(),
                title="Rola",
                widget=deform.widget.SelectWidget(values=choices)
                )
            password = colander.SchemaNode(
                colander.String(),
                title="Hasło",
                validator=colander.Length(min=5, max=100),
                widget=deform.widget.PasswordWidget()
                )

        schema = Schema().bind(request=self.request)
        submit_btn = deform.form.Button(name='submit', title='Zapisz')
        return deform.Form(schema, buttons=(submit_btn,))

    @view_config(
        route_name='users',
        renderer='users.mako',
        permission='view'
    )
    def all(self):
        page = self.request.params.get('page', 1)
        users = self.request.dbsession.query(User)
        paginator = get_paginator(self.request, users, page=page)

        return {'paginator': paginator}

    @view_config(
        route_name='user_view',
        renderer='user.mako',
        permission='view'
    )
    def view(self):
        user = self.request.context.user
        return {'user': user}

    @view_config(
        route_name='user_add',
        renderer='form.mako',
        permission='admin'
    )
    def add(self):
        form = self.user_form
        appstruct = {}
        rendered_form = None

        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = form.validate(controls)
            except deform.exception.ValidationFailure as e:
                rendered_form = e.render()
            else:
                user = User(
                    username=appstruct['username'],
                    fullname=appstruct['fullname'],
                    email=appstruct['email'],
                    role=appstruct['role'],
                    password=appstruct['password'],
                    )
                self.request.dbsession.add(user)
                self.request.session.flash('success:Dodano do bazy danych')
                log.warn(f'Użytkownik {self.request.user.username} dodał użytkownika {user.username}')
                return HTTPFound(location=self.request.route_url('users'))

        if rendered_form is None:
            rendered_form = form.render(appstruct=appstruct)
        reqts = form.get_widget_resources()

        return dict(
            heading='Dodaj użytkownika',
            rendered_form=rendered_form,
            css_links=reqts['css'],
            js_links=reqts['js'],
            )

    @view_config(
        route_name='user_edit',
        renderer='form.mako',
        permission='admin'
    )
    def edit(self):
        user = self.request.context.user
        form = self.user_form
        rendered_form = None

        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = form.validate(controls)
            except deform.exception.ValidationFailure as e:
                rendered_form = e.render()
            else:
                user.username = appstruct['username']
                user.fullname = appstruct['fullname']
                user.email = appstruct['email']
                user.role = appstruct['role']
                user.password = appstruct['password']

                self.request.session.flash('success:Zmiany zostały zapisane')
                log.warn(f'Użytkownik {self.request.user.username} zmienił dane użytkownika {user.username}')
                return HTTPFound(location=self.request.route_url('users'))

        appstruct = {
            'username': user.username,
            'fullname': user.fullname,
            'email': user.email,
            'role': user.role,
            'password': user.password,
        }
        if rendered_form is None:
            rendered_form = form.render(appstruct=appstruct)
        reqts = form.get_widget_resources()

        return dict(
            heading='Edytuj dane użytkownika',
            rendered_form=rendered_form,
            css_links=reqts['css'],
            js_links=reqts['js'],
            )

    @view_config(
        route_name='user_delete',
        request_method='POST',
        permission='admin'
    )
    def delete(self):
        user = self.request.context.user
        self.request.dbsession.delete(user)
        self.request.session.flash('success:Usunięto z bazy danych')
        log.warn(f'Użytkownik {self.request.user.username} usunął użytkownika {user.username}')
        return HTTPFound(location=self.request.route_url('users'))

    @view_config(
        route_name='user_search',
        renderer='user_search.mako',
        permission='view'
    )
    def search(self):
        return {}

    @view_config(
        route_name='user_search_results',
        renderer='user_search_results.mako',
        permission='view'
    )
    def search_results(self):
        username = self.request.params.get('username')
        page = self.request.params.get('page', 1)
        results = self.request.dbsession.query(User).\
            filter(User.username.ilike('%' + username + '%')).\
            order_by(User.username)
        paginator = get_paginator(self.request, results, page=page)
        return {'paginator': paginator}

    @view_config(
        route_name='user_marked',
        renderer='user_marked.mako',
        permission='view'
    )
    def marked(self):
        from .voivodeships import VOIVODESHIPS
        user = self.request.context.user
        page = self.request.params.get('page', 1)
        query = self.request.params.get('sort', 'name')

        if query not in ['name', 'city', 'voivodeship', 'upvotes']:
            return HTTPNotFound()

        if query == 'upvotes':
            companies = self.request.dbsession.query(Company).\
                join(marker).filter(user.id == marker.c.user_id).\
                join(upvotes).group_by(Company).order_by(
                    func.count(upvotes.c.company_id).desc(),
                    Company.id
                )
        else:
            companies = self.request.dbsession.query(Company).\
                join(marker).filter(user.id == marker.c.user_id).\
                order_by(query, Company.id)

        voivodeships = dict(VOIVODESHIPS)
        paginator = get_paginator(self.request, companies, page=page)

        try:
            user_upvotes = self.request.user.upvotes
        except AttributeError:
            user_upvotes = []

        try:
            user_marker = self.request.user.marker
        except AttributeError:
            user_marker = []

        return dict(
            user=user,
            query=query,
            paginator=paginator,
            user_upvotes=user_upvotes,
            user_marker=user_marker,
            voivodeships=voivodeships,
            )

    @view_config(
        route_name='user_marked_export',
        permission='view'
    )
    def export_marked(self):
        user = self.request.context.user
        query = self.request.params.get('sort', 'name')

        if query not in ['name', 'city', 'voivodeship', 'upvotes']:
            return HTTPNotFound()

        if query == 'upvotes':
            companies = self.request.dbsession.query(Company).\
                join(marker).filter(user.id == marker.c.user_id).\
                join(upvotes).group_by(Company).order_by(
                    func.count(upvotes.c.company_id).desc(),
                    Company.id
                )
        else:
            companies = self.request.dbsession.query(Company).\
                join(marker).filter(user.id == marker.c.user_id).\
                order_by(query, Company.id)

        response = export_to_xlsx(companies)
        log.warn(f'Użytkownik {self.request.user.username} eksportował dane zaznaczonych firm')
        return response

    @view_config(
        route_name='user_marked_clear',
        request_method='POST',
        permission='view'
    )
    def clear_marked(self):
        user = self.request.context.user
        user.marker = []
        return HTTPFound(location=self.request.route_url('user_marked', username=user.username))

    @view_config(
        route_name='user_upvotes',
        renderer='user_upvotes.mako',
        permission='view'
    )
    def upvotes(self):
        from .voivodeships import VOIVODESHIPS
        user = self.request.context.user
        page = self.request.params.get('page', 1)
        query = self.request.params.get('sort', 'name')

        if query not in ['name', 'city', 'voivodeship', 'upvotes']:
            return HTTPNotFound()

        if query == 'upvotes':
            companies = self.request.dbsession.query(Company).\
                join(upvotes).filter(user.id == upvotes.c.user_id).\
                group_by(Company).order_by(
                    func.count(upvotes.c.company_id).desc(),
                    Company.id
                )
        else:
            companies = self.request.dbsession.query(Company).\
                join(upvotes).filter(user.id == upvotes.c.user_id).\
                order_by(query, Company.id)            

        voivodeships = dict(VOIVODESHIPS)
        paginator = get_paginator(self.request, companies, page=page)

        try:
            user_upvotes = self.request.user.upvotes
        except AttributeError:
            user_upvotes = []

        try:
            user_marker = self.request.user.marker
        except AttributeError:
            user_marker = []

        return dict(
            user=user,
            query=query,
            paginator=paginator,
            user_upvotes=user_upvotes,
            user_marker=user_marker,
            voivodeships=voivodeships,
            )

    @view_config(
        route_name='user_upvotes_export',
        permission='view'
    )
    def export_upvotes(self):
        user = self.request.context.user
        query = self.request.params.get('sort', 'name')

        if query not in ['name', 'city', 'voivodeship', 'upvotes']:
            return HTTPNotFound()

        if query == 'upvotes':
            companies = self.request.dbsession.query(Company).\
                join(upvotes).filter(user.id == upvotes.c.user_id).\
                group_by(Company).order_by(
                    func.count(upvotes.c.company_id).desc(),
                    Company.id
                )
        else:
            companies = self.request.dbsession.query(Company).\
                join(upvotes).filter(user.id == upvotes.c.user_id).\
                order_by(query, Company.id) 

        response = export_to_xlsx(companies)
        log.warn(f'Użytkownik {self.request.user.username} eksportował dane rekomendowanych firm')
        return response

    @view_config(
        route_name='user_upvotes_clear',
        request_method='POST',
        permission='view'
    )
    def clear_upvotes(self):
        user = self.request.context.user
        user.upvotes = []
        log.warn(f'Użytkownik {self.request.user.username} wyczyścił wszystkie rekomendacje')
        return HTTPFound(location=self.request.route_url('user_upvotes', username=user.username))
