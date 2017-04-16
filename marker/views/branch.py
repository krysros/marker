from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )

import io
import deform
import colander
import xlsxwriter

from ..models import (
    Branch,
    Company,
    User,
    )
from ..csrf import CSRFSchema
from ..paginator import get_paginator


class BranchView(object):
    def __init__(self, request):
        self.request = request

    @property
    def branch_form(self):

        def check_name(node, value):
            query = self.request.dbsession.query(Branch)
            exists = query.filter_by(name=value).one_or_none()
            if exists:
                raise colander.Invalid(node, 'Ta nazwa branży jest już zajęta')

        class Schema(CSRFSchema):
            name = colander.SchemaNode(
                colander.String(),
                title='Nazwa branży',
                validator=colander.All(
                    colander.Length(min=3, max=50), check_name)
                )

        schema = Schema().bind(request=self.request)
        submit_btn = deform.form.Button(name='submit', title='Zapisz')
        return deform.Form(schema, buttons=(submit_btn,))

    @view_config(
        route_name='branches',
        renderer='branches.mako',
        permission='view'
    )
    @view_config(
        route_name='branch_index',
        renderer='branches.mako',
        permission='view'
    )
    def all(self):
        letter = self.request.matchdict.get('letter', 'a')
        page = self.request.params.get('page', 1)
        query = self.request.dbsession.query(Branch)
        branches = query.filter(Branch.name.ilike(letter.lower() + '%')).\
            order_by(Branch.name)
        paginator = get_paginator(self.request, branches, page=page)

        return dict(
            selected_letter=letter,
            paginator=paginator,
            logged_in=self.request.authenticated_userid,
            )

    @view_config(
        route_name='branch_companies',
        renderer='branch_companies.mako',
        permission='view'
    )
    def view_companies(self):
        from .voivodeships import VOIVODESHIPS
        branch_id = self.request.matchdict['branch_id']
        page = self.request.params.get('page', 1)
        branch = self.request.dbsession.query(Branch).\
            filter_by(id=branch_id).one()
        query = self.request.params.get('sort', 'name')
        if query in ['name', 'city', 'voivodeship']:
            companies = self.request.dbsession.query(Company).\
                filter(Company.branches.any(name=branch.name)).\
                order_by(query, Company.id)
        else:
            return HTTPNotFound()

        voivodeships = dict(VOIVODESHIPS)
        paginator = get_paginator(self.request, companies, page=page)

        username = self.request.authenticated_userid
        user = self.request.dbsession.query(User).\
            filter_by(username=username).one()
        try:
            upvotes = user.upvotes
        except AttributeError:
            upvotes = []

        return dict(
            branch=branch,
            query=query,
            paginator=paginator,
            upvotes=upvotes,
            voivodeships=voivodeships,
            logged_in=self.request.authenticated_userid,
            )

    @view_config(
        route_name='branch_offers',
        renderer='branch_offers.mako',
        permission='view'
    )
    def view_offers(self):
        branch_id = self.request.matchdict['branch_id']
        page = self.request.params.get('page', 1)
        branch = self.request.dbsession.query(Branch).\
            filter_by(id=branch_id).one()
        paginator = get_paginator(self.request, branch.offers, page=page)

        return dict(
            branch=branch,
            paginator=paginator,
            logged_in=self.request.authenticated_userid,
            )

    @view_config(
        route_name='branch_export',
        permission='view'
    )
    def export(self):
        branch_id = self.request.matchdict['branch_id']
        branch = self.request.dbsession.query(Branch).\
            filter_by(id=branch_id).one()
        query = self.request.params.get('sort', 'name')
        if query in ['name', 'city', 'voivodeship']:
            companies = self.request.dbsession.query(Company).\
                filter(Company.branches.any(name=branch.name)).\
                order_by(query, Company.id)
        else:
            return HTTPNotFound()

        # Create an in-memory output file for the new workbook.
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'constant_memory': True})
        worksheet = workbook.add_worksheet()

        # Write rows.
        header = ['Firma', 'Miasto', 'Województwo',
                  'Imię i nazwisko', 'Stanowisko', 'Telefon', 'Email']

        for j, col in enumerate(header):
            worksheet.write(0, j, col)

        i = 1
        for company in companies:
            cols = [company.name, company.city, company.voivodeship,
                    '', 'BIURO', company.phone, company.email]
            for j, col in enumerate(cols):
                worksheet.write(i, j, col)
            i += 1
            for person in company.people:
                cols = [company.name, company.city, company.voivodeship,
                        person.fullname, person.position,
                        person.phone, person.email]
                for j, col in enumerate(cols):
                    worksheet.write(i, j, col)
                i += 1

        # Close the workbook before streaming the data.
        workbook.close()
        # Rewind the buffer.
        output.seek(0)
        # Construct a server response.
        response = Response()
        response.body_file = output
        response.content_type = 'application/vnd.openxmlformats-' \
                                'officedocument.spreadsheetml.sheet'
        response.content_disposition = 'attachment; filename="export.xlsx"'
        return response

    @view_config(
        route_name='branch_add',
        renderer='form.mako',
        permission='edit'
    )
    def add(self):
        form = self.branch_form
        appstruct = {}
        rendered_form = None

        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = form.validate(controls)
            except deform.exception.ValidationFailure as e:
                rendered_form = e.render()
            else:
                branch = Branch(appstruct['name'])
                self.request.dbsession.add(branch)
                self.request.session.flash('success:Dodano do bazy danych')
                return HTTPFound(location=self.request.route_url('branches'))

        if rendered_form is None:
            rendered_form = form.render(appstruct=appstruct)

        return dict(
            heading='Dodaj branżę',
            rendered_form=rendered_form,
            logged_in=self.request.authenticated_userid
            )

    @view_config(
        route_name='branch_edit',
        renderer='form.mako',
        permission='edit'
    )
    def edit(self):
        branch_id = self.request.matchdict['branch_id']
        query = self.request.dbsession.query(Branch)
        branch = query.filter_by(id=branch_id).one()
        form = self.branch_form
        rendered_form = None

        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = form.validate(controls)
            except deform.exception.ValidationFailure as e:
                rendered_form = e.render()
            else:
                branch.name = appstruct['name']
                self.request.session.flash('success:Nazwa branży została zmieniona')
                return HTTPFound(location=self.request.route_url('branch_edit',
                                                                 branch_id=branch.id,
                                                                 slug=branch.slug))
        appstruct = {'name': branch.name}
        if rendered_form is None:
            rendered_form = form.render(appstruct=appstruct)

        return dict(
            heading='Edytuj dane branży',
            rendered_form=rendered_form,
            logged_in=self.request.authenticated_userid
            )

    @view_config(
        route_name='branch_delete',
        request_method='POST',
        permission='edit'
    )
    def delete(self):
        branch_id = self.request.matchdict['branch_id']
        query = self.request.dbsession.query(Branch)
        branch = query.filter_by(id=branch_id).one()
        self.request.dbsession.delete(branch)
        self.request.session.flash('success:Usunięto z bazy danych')
        return HTTPFound(location=self.request.route_url('home'))

    @view_config(
        route_name='branch_select',
        request_method='GET',
        renderer='json',
    )
    def select(self):
        term = self.request.params.get('term')
        query = self.request.dbsession.query(Branch)
        items = query.filter(Branch.name.ilike('%' + term + '%'))
        data = [i.name for i in items]
        return data

    @view_config(
        route_name='branch_search',
        renderer='branch_search.mako',
        permission='view'
    )
    def search(self):
        return {'logged_in': self.request.authenticated_userid}

    @view_config(
        route_name='branch_search_results',
        renderer='branch_search_results.mako',
        permission='view'
    )
    def search_results(self):
        name = self.request.params.get('name')
        page = self.request.params.get('page', 1)
        results = self.request.dbsession.query(Branch).\
            filter(Branch.name.ilike('%' + name + '%'))
        paginator = get_paginator(self.request, results, page=page)
        return dict(
            paginator=paginator,
            logged_in=self.request.authenticated_userid,
        )
