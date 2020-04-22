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
    Branch,
    Company,
    upvotes,
    Offer,
    Tender,
    )
from deform.schema import CSRFSchema
from ..paginator import get_paginator
from ..helpers import (
    export_companies_to_xlsx,
    export_offers_to_xlsx,
    )


log = logging.getLogger(__name__)


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

        try:
            user_marker = self.request.user.marker
        except AttributeError:
            user_marker = []

        return dict(
            branch=branch,
            query=query,
            paginator=paginator,
            user_upvotes=user_upvotes,
            user_marker=user_marker,
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
        query = self.request.params.get('sort', 'added')

        if query not in ['company', 'tender', 'category',
                         'unit', 'cost', 'currency', 'added']:
            return HTTPNotFound()

        if query == 'company':
            offers = branch.offers.filter(Offer.company).order_by(func.lower(Company.name))
        elif query == 'tender':
            offers = branch.offers.filter(Offer.tender).order_by(func.lower(Tender.name))
        elif query == 'category':
            offers = branch.offers.order_by(Offer.category)
        elif query == 'unit':
            offers = branch.offers.order_by(Offer.unit)
        elif query == 'cost':
            offers = branch.offers.order_by(Offer.cost)
        elif query == 'currency':
            offers = branch.offers.order_by(Offer.currency)
        else:
            offers = branch.offers.order_by(Offer.id.desc())

        paginator = get_paginator(self.request, offers, page=page)

        return dict(
            branch=branch,
            query=query,
            paginator=paginator,
            )

    @view_config(
        route_name='branch_export_companies',
        permission='view'
    )
    def export_companies(self):
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

        response = export_companies_to_xlsx(companies)
        log.info(f'Użytkownik {self.request.user.username} eksportował dane firm z branży {branch.name}')
        return response

    @view_config(
        route_name='branch_export_offers',
        permission='view'
    )
    def export_offers(self):
        branch = self.request.context.branch
        query = self.request.params.get('sort', 'added')

        if query not in ['company', 'tender', 'category',
                         'unit', 'cost', 'currency', 'added']:
            return HTTPNotFound()

        if query == 'company':
            offers = branch.offers.filter(Offer.company).order_by(func.lower(Company.name))
        elif query == 'tender':
            offers = branch.offers.filter(Offer.tender).order_by(func.lower(Tender.name))
        elif query == 'category':
            offers = branch.offers.order_by(Offer.category)
        elif query == 'unit':
            offers = branch.offers.order_by(Offer.unit)
        elif query == 'cost':
            offers = branch.offers.order_by(Offer.cost)
        elif query == 'currency':
            offers = branch.offers.order_by(Offer.currency)
        else:
            offers = branch.offers.order_by(Offer.id.desc())

        response = export_offers_to_xlsx(offers)
        log.info(f'Użytkownik {self.request.user.username} eksportował oferty z branży {branch.name}')
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
                branch.added_by = self.request.user
                self.request.dbsession.add(branch)
                self.request.session.flash('success:Dodano do bazy danych')
                log.info(f'Użytkownik {self.request.user.username} dodał branżę {branch.name}')
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
                branch.edited_by = self.request.user
                self.request.session.flash('success:Zmiany zostały zapisane')
                log.info(f'Użytkownik {self.request.user.username} zmienił nazwę branży {branch.name}')
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
        branch_id = branch.id
        branch_name = branch.name
        self.request.dbsession.delete(branch)
        self.request.session.flash('success:Usunięto z bazy danych')
        log.info(f'Użytkownik {self.request.user.username} usunął branżę {branch_name} (id {branch_id})')
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
