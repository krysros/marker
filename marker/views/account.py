import logging
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

import colander
import deform

from deform.schema import CSRFSchema


log = logging.getLogger(__name__)


class Account(CSRFSchema):
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


class Password(CSRFSchema):
    password = colander.SchemaNode(
        colander.String(),
        title='Hasło',
        validator=colander.Length(min=5),
        widget=deform.widget.CheckedPasswordWidget()
        )


class AccountView(object):
    def __init__(self, request):
        self.request = request

    @property
    def account_form(self):
        schema = Account().bind(request=self.request)
        submit_btn = deform.form.Button(name='submit', title='Zapisz')
        return deform.Form(schema, buttons=(submit_btn,))

    @view_config(
        route_name='account',
        renderer='account.mako',
        permission='edit'
    )
    def account_edit(self):
        user = self.request.user
        form = self.account_form

        if self.request.method == 'POST':
            if 'submit' in self.request.POST:
                controls = self.request.POST.items()
                try:
                    appstruct = form.validate(controls)
                except deform.exception.ValidationFailure as e:
                    rendered_form = e.render()
                else:
                    user.fullname = appstruct['fullname']
                    user.email = appstruct['email']
                    self.request.session.flash('success:Zmiany zostały zapisane')
                    log.warn(f'Użytkownik {user.username} zmienił swoje dane')
                    return HTTPFound(location=self.request.route_url('account'))
        else:
            appstruct = {'fullname': user.fullname, 'email': user.email}
            rendered_form = form.render(appstruct=appstruct)

        return dict(
            heading='Dane użytkownika',
            rendered_form=rendered_form,
            )

    @property
    def password_form(self):
        schema = Password().bind(request=self.request)
        submit_btn = deform.form.Button(name='submit', title='Zapisz')
        return deform.Form(schema, buttons=(submit_btn,))

    @view_config(
        route_name='password',
        renderer='account.mako',
        permission='edit'
    )
    def password_edit(self):
        user = self.request.user
        form = self.password_form

        if self.request.method == 'POST':
            if 'submit' in self.request.POST:
                controls = self.request.POST.items()
                try:
                    appstruct = form.validate(controls)
                except deform.exception.ValidationFailure as e:
                    rendered_form = e.render()
                else:
                    user.password = appstruct['password']
                    self.request.session.flash('success:Zmiany zostały zapisane')
                    log.warn(f'Użytkownik {user.username} zmienił hasło')
                    return HTTPFound(location=self.request.route_url('password'))
        else:
            rendered_form = form.render()

        return dict(
            heading='Zmiana hasła',
            rendered_form=rendered_form,
            )
