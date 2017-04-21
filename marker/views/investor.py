from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

import deform
import colander

from ..models import Investor
from deform.schema import CSRFSchema
from ..paginator import get_paginator


class InvestorView(object):
    def __init__(self, request):
        self.request = request

    @property
    def investor_form(self):

        def check_name(node, value):
            query = self.request.dbsession.query(Investor)
            exists = query.filter_by(name=value).one_or_none()
            if exists:
                raise colander.Invalid(node, 'Ta nazwa inwestora jest już zajęta')

        class Schema(CSRFSchema):
            name = colander.SchemaNode(
                colander.String(),
                title='Nazwa inwestora',
                validator=colander.All(
                    colander.Length(min=3, max=100), check_name)
                )

        schema = Schema().bind(request=self.request)
        submit_btn = deform.form.Button(name='submit', title='Zapisz')
        return deform.Form(schema, buttons=(submit_btn,))

    @view_config(
        route_name='investors',
        renderer='investors.mako',
        permission='view'
    )
    def all(self):
        page = self.request.params.get('page', 1)
        query = self.request.dbsession.query(Investor)
        investors = query.order_by(Investor.name)
        paginator = get_paginator(self.request, investors, page=page)
        return {'paginator': paginator}

    @view_config(
        route_name='investor_view',
        renderer='investor.mako',
        permission='view'
    )
    def view(self):
        investor_id = self.request.matchdict['investor_id']
        query = self.request.dbsession.query(Investor)
        investor = query.filter_by(id=investor_id).one()
        return {'investor': investor}

    @view_config(
        route_name='investor_add',
        renderer='form.mako',
        permission='edit'
    )
    def add(self):
        form = self.investor_form
        appstruct = {}
        rendered_form = None
        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = form.validate(controls)
            except deform.exception.ValidationFailure as e:
                rendered_form = e.render()
            else:
                investor = Investor(appstruct['name'])
                self.request.dbsession.add(investor)
                self.request.session.flash('success:Dodano do bazy danych')
                return HTTPFound(location=self.request.route_url('investors'))

        if rendered_form is None:
            rendered_form = form.render(appstruct=appstruct)

        return dict(
            heading='Dodaj inwestora',
            rendered_form=rendered_form,
            )

    @view_config(
        route_name='investor_edit',
        renderer='form.mako',
        permission='edit'
    )
    def edit(self):
        investor_id = self.request.matchdict['investor_id']
        query = self.request.dbsession.query(Investor)
        investor = query.filter_by(id=investor_id).one()
        form = self.investor_form
        rendered_form = None

        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = form.validate(controls)
            except deform.exception.ValidationFailure as e:
                rendered_form = e.render()
            else:
                investor.name = appstruct['name']
                self.request.session.flash('success:Nazwa inwestora została zmieniona')
                return HTTPFound(location=self.request.route_url('investor_edit',
                                                                 investor_id=investor.id,
                                                                 slug=investor.slug))
        appstruct = {'name': investor.name}
        if rendered_form is None:
            rendered_form = form.render(appstruct=appstruct)

        return dict(
            heading='Edytuj dane inwestora',
            rendered_form=rendered_form,
            )

    @view_config(
        route_name='investor_delete',
        request_method='POST',
        permission='edit'
    )
    def delete(self):
        investor_id = self.request.matchdict['investor_id']
        query = self.request.dbsession.query(Investor)
        investor = query.filter_by(id=investor_id).one()
        self.request.dbsession.delete(investor)
        self.request.session.flash('success:Usunięto z bazy danych')
        return HTTPFound(location=self.request.route_url('home'))

    @view_config(
        route_name='investor_select',
        request_method='GET',
        renderer='json',
    )
    def select(self):
        term = self.request.params.get('term')
        query = self.request.dbsession.query(Investor.name)
        items = query.filter(Investor.name.ilike('%' + term + '%'))
        data = [i.name for i in items]
        return data

    @view_config(
        route_name='investor_search',
        renderer='investor_search.mako',
        permission='view'
    )
    def search(self):
        return {}

    @view_config(
        route_name='investor_search_results',
        renderer='investor_search_results.mako',
        permission='view'
    )
    def search_results(self):
        name = self.request.params.get('name')
        page = self.request.params.get('page', 1)
        results = self.request.dbsession.query(Investor).\
            filter(Investor.name.ilike('%' + name + '%')).\
            order_by(Investor.name)
        paginator = get_paginator(self.request, results, page=page)
        return {'paginator': paginator}
