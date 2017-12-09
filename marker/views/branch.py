import io
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )

from sqlalchemy import func

import deform
import colander
import xlsxwriter

from ..models import (
    Branch,
    Company,
    upvotes,
    )
from deform.schema import CSRFSchema
from ..paginator import get_paginator


class BranchView(object):
    def __init__(self, request):
        self.request = request

    @property
    def branch_form(self):

        def check_name(node, value):
            query = self.request.dbsession.query(Branch)
            exists = query.filter_by(name=value).one_or_none()
            current_id = self.request.matchdict.get('branch_id', None)
            if current_id:
                current_id = int(current_id)
            if exists and current_id != exists.id:
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
            )

    @view_config(
        route_name='branch_companies',
        renderer='branch_companies.mako',
        permission='view'
    )
    def view_companies(self):
        from .voivodeships import VOIVODESHIPS
        branch = self.request.context.branch
        page = self.request.params.get('page', 1)
        query = self.request.params.get('sort', 'name')

        if query not in ['name', 'city', 'voivodeship', 'upvotes']:
            return HTTPNotFound()

        if query == 'upvotes':
            companies = self.request.dbsession.query(Company).\
                filter(Company.branches.any(name=branch.name)).\
                join(upvotes).group_by(Company).order_by(
                    func.count(upvotes.c.company_id).desc(),
                    Company.id
                )
        else:
            companies = self.request.dbsession.query(Company).\
                filter(Company.branches.any(name=branch.name)).\
                order_by(query, Company.id)

        voivodeships = dict(VOIVODESHIPS)
        paginator = get_paginator(self.request, companies, page=page)

        try:
            user_upvotes = self.request.user.upvotes
        except AttributeError:
            user_upvotes = []

        return dict(
            branch=branch,
            query=query,
            paginator=paginator,
            user_upvotes=user_upvotes,
            voivodeships=voivodeships,
            )

    @view_config(
        route_name='branch_offers',
        renderer='branch_offers.mako',
        permission='view'
    )
    def view_offers(self):
        branch = self.request.context.branch
        page = self.request.params.get('page', 1)
        paginator = get_paginator(self.request, branch.offers, page=page)

        return dict(
            branch=branch,
            paginator=paginator,
            )

    @view_config(
        route_name='branch_export',
        permission='view'
    )
    def export(self):
        branch = self.request.context.branch
        query = self.request.params.get('sort', 'name')

        if query not in ['name', 'city', 'voivodeship', 'upvotes']:
            return HTTPNotFound()

        if query == 'upvotes':
            companies = self.request.dbsession.query(Company).\
                filter(Company.branches.any(name=branch.name)).\
                join(upvotes).group_by(Company).order_by(
                    func.count(upvotes.c.company_id).desc(),
                    Company.id
                )
        else:
            companies = self.request.dbsession.query(Company).\
                filter(Company.branches.any(name=branch.name)).\
                order_by(query, Company.id)

        # Create an in-memory output file for the new workbook.
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'constant_memory': True})
        worksheet = workbook.add_worksheet()

        # Write rows.
        header = ['Firma', 'Miasto', 'Województwo', 'Rekomendacje',
                  'Imię i nazwisko', 'Stanowisko', 'Telefon', 'Email']

        for j, col in enumerate(header):
            worksheet.write(0, j, col)

        i = 1
        for company in companies:
            cols = [company.name, company.city, company.voivodeship,
                    company.upvote_count, '', 'BIURO',
                    company.phone, company.email]
            for j, col in enumerate(cols):
                worksheet.write(i, j, col)
            i += 1
            for person in company.people:
                cols = [company.name, company.city,
                        company.voivodeship, company.upvote_count,
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
            )

    @view_config(
        route_name='branch_edit',
        renderer='form.mako',
        permission='edit'
    )
    def edit(self):
        branch = self.request.context.branch
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
            )

    @view_config(
        route_name='branch_delete',
        request_method='POST',
        permission='edit'
    )
    def delete(self):
        branch = self.request.context.branch
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
        return {}

    @view_config(
        route_name='branch_search_results',
        renderer='branch_search_results.mako',
        permission='view'
    )
    def search_results(self):
        name = self.request.params.get('name')
        page = self.request.params.get('page', 1)
        results = self.request.dbsession.query(Branch).\
            filter(Branch.name.ilike('%' + name + '%')).\
            order_by(Branch.name)
        paginator = get_paginator(self.request, results, page=page)
        return {'paginator': paginator}
