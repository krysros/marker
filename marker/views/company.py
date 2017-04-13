import re
from operator import mul
from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )

import deform
import colander

from ..models import (
    Company,
    Person,
    Branch,
    User,
    )
from ..csrf import CSRFSchema
from ..paginator import get_paginator
from .voivodeships import VOIVODESHIPS


# removes whitespace, newlines, and tabs from the beginning/end of a string
strip_whitespace = lambda v: v.strip(' \t\n\r') if v is not colander.null else v
# removes dashes
remove_dashes = lambda v: v.replace('-', '').replace(' ', '') if v is not colander.null else v
# replaces multiple spaces with a single space
remove_multiple_spaces = lambda v: re.sub(' +', ' ', v) if v is not colander.null else v


class CompanyView(object):
    def __init__(self, request):
        self.request = request

    @property
    def company_form(self):

        def check_name(node, value):
            query = self.request.dbsession.query(Company)
            exists = query.filter_by(name=value).one_or_none()
            current_id = self.request.matchdict.get('company_id', None)
            if current_id:
                current_id = int(current_id)
            if exists and current_id != exists.id:
                raise colander.Invalid(node, 'Ta nazwa firmy jest już zajęta')

        def validate_nip(node, value):
            if len(value) != 10 or not value.isdigit():
                raise colander.Invalid(node, 'Numer NIP powinien się składać z 10 cyfr')

            digits = list(map(int, value))
            weights = (6, 5, 7, 2, 3, 4, 5, 6, 7)
            check_sum = sum(map(mul, digits[0:9], weights)) % 11
            if check_sum != digits[9]:
                raise colander.Invalid(node, 'Nieprawidłowy numer NIP')

        def _check_sum_9(digits):
            weights9 = (8, 9, 2, 3, 4, 5, 6, 7)
            check_sum = sum(map(mul, digits[0:8], weights9)) % 11
            if check_sum == 10:
                check_sum = 0
            if check_sum == digits[8]:
                return True
            else:
                return False

        def _check_sum_14(digits):
            weights14 = (2, 4, 8, 5, 0, 9, 7, 3, 6, 1, 2, 4, 8)
            check_sum = sum(map(mul, digits[0:13], weights14)) % 11
            if check_sum == 10:
                check_sum = 0
            if check_sum == digits[13]:
                return True
            else:
                return False

        def validate_regon(node, value):
            if (len(value) != 9 and len(value) != 14 or
                    not value.isdigit()):
                raise colander.Invalid(node, 'Numer REGON powinien '
                                       'się składać z 9 lub 14 cyfr')
            digits = list(map(int, value))

            if len(value) == 9:
                valid = _check_sum_9(digits)
            else:
                valid = _check_sum_9(digits) and _check_sum_14(digits)

            if not valid:
                raise colander.Invalid(node, 'Nieprawidłowy numer REGON')

        def validate_krs(node, value):
            if len(value) != 10 or not value.isdigit():
                raise colander.Invalid(node, 'Numer KRS powinien '
                                       'się składać z 10 cyfr')

        widget = deform.widget.AutocompleteInputWidget(
            values=self.request.route_url('branch_select'),
            )

        class Branches(colander.SequenceSchema):
            name = colander.SchemaNode(
                colander.String(),
                title='Branża',
                widget=widget,
                validator=colander.Length(min=3, max=50),
                )

        class Person(colander.Schema):
            fullname = colander.SchemaNode(
                colander.String(),
                title='Imię i nazwisko',
                validator=colander.Length(max=50),
                )
            position = colander.SchemaNode(
                colander.String(),
                title='Stanowisko',
                validator=colander.Length(max=50),
                )
            phone = colander.SchemaNode(
                colander.String(),
                title='Telefon',
                validator=colander.Length(max=50),
                )
            email = colander.SchemaNode(
                colander.String(),
                title='Email',
                validator=colander.Email(),
                )

        class People(colander.SequenceSchema):
            person = Person(title="Nowy kontakt")

        class Schema(CSRFSchema):
            name = colander.SchemaNode(
                colander.String(),
                title='Nazwa firmy',
                validator=colander.All(
                    colander.Length(min=3, max=100), check_name),
                )
            city = colander.SchemaNode(
                colander.String(),
                title='Miasto',
                validator=colander.Length(max=100),
                )
            voivodeship = colander.SchemaNode(
                colander.String(),
                title='Województwo',
                widget=deform.widget.SelectWidget(values=VOIVODESHIPS),
                )
            phone = colander.SchemaNode(
                colander.String(),
                title='Telefon',
                validator=colander.Length(max=50),
                )
            email = colander.SchemaNode(
                colander.String(),
                title='Email',
                validator=colander.Email(),
                )
            www = colander.SchemaNode(
                colander.String(),
                title='WWW',
                missing='',
                validator=colander.Length(max=50),
                )
            nip = colander.SchemaNode(
                colander.String(),
                title='NIP',
                missing='',
                preparer=[strip_whitespace, remove_dashes, remove_multiple_spaces],
                validator=validate_nip,
                )
            regon = colander.SchemaNode(
                colander.String(),
                title='REGON',
                missing='',
                preparer=[strip_whitespace, remove_dashes, remove_multiple_spaces],
                validator=validate_regon,
                )
            krs = colander.SchemaNode(
                colander.String(),
                title='KRS',
                missing='',
                preparer=[strip_whitespace, remove_dashes, remove_multiple_spaces],
                validator=validate_krs,
                )
            branches = Branches(title="Branże")
            people = People(title="Osoby do kontaktu")

        schema = Schema().bind(request=self.request)
        submit_btn = deform.form.Button(name='submit', title='Zapisz')
        form = deform.Form(schema, buttons=(submit_btn,))
        form['branches'].widget = deform.widget.SequenceWidget(min_len=1)
        return form

    @view_config(
        route_name='companies',
        renderer='companies.mako',
        permission='view'
    )
    def all(self):
        page = self.request.params.get('page', 1)
        query = self.request.params.get('sort', 'added')
        if query == 'added':
            companies = self.request.dbsession.query(Company).\
                order_by(Company.id.desc())
        elif query == 'edited':
            companies = self.request.dbsession.query(Company).\
                order_by(Company.edited.desc(), Company.id)
        else:
            return HTTPNotFound()

        paginator = get_paginator(self.request, companies, page=page)

        username = self.request.authenticated_userid
        user = self.request.dbsession.query(User).\
            filter_by(username=username).one()
        try:
            upvotes = user.upvotes
        except AttributeError:
            upvotes = []

        return dict(
            query=query,
            paginator=paginator,
            upvotes=upvotes,
            logged_in=self.request.authenticated_userid,
            )

    @view_config(
        route_name='company_view',
        renderer='company.mako',
        permission='view'
    )
    def view(self):
        company_id = self.request.matchdict['company_id']
        query = self.request.dbsession.query(Company)
        company = query.filter_by(id=company_id).one()
        voivodeships = dict(VOIVODESHIPS)
        username = self.request.authenticated_userid
        query = self.request.dbsession.query(User)
        user = query.filter_by(username=username).one()
        upvote = company in user.upvotes
        return dict(
            company=company,
            upvote=upvote,
            voivodeships=voivodeships,
            logged_in=self.request.authenticated_userid,
            )

    def _get_branches(self, appstruct):
        branches = []
        for b in appstruct['branches']:
            query = self.request.dbsession.query(Branch)
            branch = query.filter_by(name=b).one_or_none()
            if not branch:
                branch = Branch(name=b)
            if branch not in branches:
                branches.append(branch)
        return branches

    def _get_people(self, appstruct):
        people = []
        for p in appstruct['people']:
            person = Person(
                fullname=p['fullname'],
                position=p['position'],
                phone=p['phone'],
                email=p['email'],
            )
            people.append(person)
        return people

    @view_config(
        route_name='company_add',
        renderer='form.mako',
        permission='edit'
    )
    def add(self):
        form = self.company_form
        appstruct = {}
        rendered_form = None

        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = form.validate(controls)
            except deform.exception.ValidationFailure as e:
                rendered_form = e.render()
            else:
                company = Company(
                    name=appstruct['name'],
                    city=appstruct['city'],
                    voivodeship=appstruct['voivodeship'],
                    phone=appstruct['phone'],
                    email=appstruct['email'],
                    www=appstruct['www'],
                    nip=appstruct['nip'],
                    regon=appstruct['regon'],
                    krs=appstruct['krs'],
                    branches=self._get_branches(appstruct),
                    people=self._get_people(appstruct),
                    )
                username = self.request.authenticated_userid
                company.added_by = self.request.dbsession.query(User).\
                    filter_by(username=username).first()
                self.request.dbsession.add(company)
                self.request.session.flash('success:Dodano do bazy danych')
                return HTTPFound(location=self.request.route_url('companies'))

        if rendered_form is None:
            rendered_form = form.render(appstruct=appstruct)
        reqts = form.get_widget_resources()

        return dict(
            heading='Dodaj firmę',
            rendered_form=rendered_form,
            logged_in=self.request.authenticated_userid,
            css_links=reqts['css'],
            js_links=reqts['js'],
            )

    @view_config(
        route_name='company_edit',
        renderer='form.mako',
        permission='edit'
    )
    def edit(self):
        company_id = self.request.matchdict['company_id']
        query = self.request.dbsession.query(Company)
        company = query.filter_by(id=company_id).one()
        form = self.company_form
        rendered_form = None

        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = form.validate(controls)
            except deform.exception.ValidationFailure as e:
                rendered_form = e.render()
            else:
                company.name = appstruct['name']
                company.city = appstruct['city']
                company.voivodeship = appstruct['voivodeship']
                company.phone = appstruct['phone']
                company.email = appstruct['email']
                company.www = appstruct['www']
                company.nip = appstruct['nip']
                company.regon = appstruct['regon']
                company.krs = appstruct['krs']
                company.branches = self._get_branches(appstruct)
                company.people = self._get_people(appstruct)
                username = self.request.authenticated_userid
                company.edited_by = self.request.dbsession.query(User).\
                    filter_by(username=username).first()
                self.request.session.flash('success:Zmiany zostały zapisane')
                return HTTPFound(location=self.request.route_url('company_view',
                                                                 company_id=company.id,
                                                                 slug=company.slug))
        branches = []
        for b in company.branches:
            branches.append(b.name)

        people = []
        for p in company.people:
            people.append(
                {
                    'fullname': p.fullname,
                    'position': p.position,
                    'phone': p.phone,
                    'email': p.email,
                }
            )

        appstruct = dict(
            name=company.name,
            city=company.city,
            voivodeship=company.voivodeship,
            phone=company.phone,
            email=company.email,
            www=company.www,
            nip=company.nip,
            regon=company.regon,
            krs=company.krs,
            branches=branches,
            people=people,
        )

        if rendered_form is None:
            rendered_form = form.render(appstruct=appstruct)
        reqts = form.get_widget_resources()

        return dict(
            heading='Edytuj dane firmy',
            rendered_form=rendered_form,
            logged_in=self.request.authenticated_userid,
            css_links=reqts['css'],
            js_links=reqts['js'],
            )

    @view_config(
        route_name='company_delete',
        request_method='POST',
        permission='edit'
    )
    def delete(self):
        company_id = self.request.matchdict['company_id']
        query = self.request.dbsession.query(Company)
        company = query.filter_by(id=company_id).one()
        self.request.dbsession.delete(company)
        self.request.session.flash('success:Usunięto z bazy danych')
        return HTTPFound(location=self.request.route_url('home'))

    @view_config(
        route_name='company_upvote',
        request_method='POST',
        renderer='json',
        permission='view'
    )
    def upvote(self):
        company_id = self.request.matchdict['company_id']
        query = self.request.dbsession.query(Company)
        company = query.filter_by(id=company_id).one()
        username = self.request.authenticated_userid
        query = self.request.dbsession.query(User)
        user = query.filter_by(username=username).one()

        if company in user.upvotes:
            user.upvotes.remove(company)
            return {'upvote': False}
        else:
            user.upvotes.append(company)
            return {'upvote': True}

    @view_config(
        route_name='company_select',
        request_method='GET',
        renderer='json',
    )
    def select(self):
        term = self.request.params.get('term')
        query = self.request.dbsession.query(Company)
        items = query.filter(Company.name.ilike('%' + term + '%'))
        data = [i.name for i in items]
        return data
