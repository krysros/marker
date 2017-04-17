from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

import deform
import colander

from ..models import User
from deform.schema import CSRFSchema
from ..paginator import get_paginator


class UserView(object):
    def __init__(self, request):
        self.request = request

    @property
    def user_form(self):

        def check_name(node, value):
            query = self.request.dbsession.query(User)
            exists = query.filter_by(username=value).one_or_none()
            if exists:
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

        return dict(
            paginator=paginator,
            logged_in=self.request.authenticated_userid,
            )

    @view_config(
        route_name='user_view',
        renderer='user.mako',
        permission='view'
    )
    def view(self):
        username = self.request.matchdict['username']
        query = self.request.dbsession.query(User)
        user = query.filter_by(username=username).one()
        return dict(
            user=user,
            logged_in=self.request.authenticated_userid,
            )

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
                return HTTPFound(location=self.request.route_url('users'))

        if rendered_form is None:
            rendered_form = form.render(appstruct=appstruct)
        reqts = form.get_widget_resources()

        return dict(
            heading='Dodaj użytkownika',
            rendered_form=rendered_form,
            logged_in=self.request.authenticated_userid,
            css_links=reqts['css'],
            js_links=reqts['js'],
            )

    @view_config(
        route_name='user_edit',
        renderer='form.mako',
        permission='admin'
    )
    def edit(self):
        username = self.request.matchdict['username']
        query = self.request.dbsession.query(User)
        user = query.filter_by(username=username).one()
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
            logged_in=self.request.authenticated_userid,
            css_links=reqts['css'],
            js_links=reqts['js'],
            )

    @view_config(
        route_name='user_delete',
        request_method='POST',
        permission='admin'
    )
    def delete(self):
        username = self.request.matchdict['username']
        query = self.request.dbsession.query(User)
        user = query.filter_by(username=username).one()
        self.request.dbsession.delete(user)
        self.request.session.flash('success:Usunięto z bazy danych')
        return HTTPFound(location=self.request.route_url('users'))

    @view_config(
        route_name='user_search',
        renderer='user_search.mako',
        permission='view'
    )
    def search(self):
        return {'logged_in': self.request.authenticated_userid}

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
        return dict(
            paginator=paginator,
            logged_in=self.request.authenticated_userid,
        )
