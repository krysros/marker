import datetime
import logging
from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )

import deform
import colander

from ..models import (
    Tender,
    Investor,
    )
from deform.schema import CSRFSchema
from ..paginator import get_paginator


log = logging.getLogger(__name__)


class TenderView(object):
    def __init__(self, request):
        self.request = request

    @property
    def tender_form(self):

        def check_name(node, value):
            query = self.request.dbsession.query(Tender)
            exists = query.filter_by(name=value).one_or_none()
            current_id = self.request.matchdict.get('tender_id', None)
            if current_id:
                current_id = int(current_id)
            if exists and current_id != exists.id:
                raise colander.Invalid(node, 'Ta nazwa przetargu jest już zajęta')

        def check_investor(node, value):
            query = self.request.dbsession.query(Investor)
            exists = query.filter_by(name=value).one_or_none()
            if not exists:
                raise colander.Invalid(
                    node, 'Inwestor o tej nazwie nie występuje w bazie danych',
                    )

        investor_widget = deform.widget.AutocompleteInputWidget(
            values=self.request.route_url('investor_select'),
            min_length=1,
            )

        class Schema(CSRFSchema):
            name = colander.SchemaNode(
                colander.String(),
                title='Nazwa przetargu',
                validator=colander.All(
                    colander.Length(min=3, max=100), check_name)
                )
            city = colander.SchemaNode(
                colander.String(),
                title='Miasto',
                validator=colander.Length(min=3, max=100),
                )
            investor = colander.SchemaNode(
                colander.String(),
                title='Inwestor',
                widget=investor_widget,
                validator=check_investor,
                )
            link = colander.SchemaNode(
                colander.String(),
                title='Link',
                missing='',
                validaror=colander.All(
                    colander.url, colander.Length(max=2000)),
                )
            deadline = colander.SchemaNode(
                colander.Date(),
                widget=deform.widget.DatePartsWidget(),
                title='Termin składania ofert',
                )

        schema = Schema().bind(request=self.request)
        submit_btn = deform.form.Button(name='submit', title='Zapisz')
        return deform.Form(schema, buttons=(submit_btn,))

    def _get_investor(self, name):
        return self.request.dbsession.query(Investor).filter_by(name=name).one()

    @view_config(
        route_name='tenders',
        renderer='tenders.mako',
        permission='view'
    )
    def all(self):
        page = self.request.params.get('page', 1)
        query = self.request.params.get('filter', 'all')
        now = datetime.datetime.now()
        if query == 'all':
            tenders = self.request.dbsession.query(Tender)
        elif query == 'inprogress':
            tenders = self.request.dbsession.query(Tender).\
                filter(Tender.deadline > now.date())
        elif query == 'completed':
            tenders = self.request.dbsession.query(Tender).\
                filter(Tender.deadline < now.date())
        else:
            return HTTPNotFound()
        paginator = get_paginator(self.request, tenders, page=page)
        return {'paginator': paginator}

    @view_config(
        route_name='tender_view',
        renderer='tender.mako',
        permission='view'
    )
    def view(self):
        tender = self.request.context.tender
        return {'tender': tender}

    @view_config(
        route_name='tender_add',
        renderer='form.mako',
        permission='edit'
    )
    def add(self):
        form = self.tender_form
        appstruct = {}
        rendered_form = None

        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = form.validate(controls)
            except deform.exception.ValidationFailure as e:
                rendered_form = e.render()
            else:
                tender = Tender(
                    name=appstruct['name'],
                    city=appstruct['city'],
                    investor=self._get_investor(appstruct['investor']),
                    link=appstruct['link'],
                    deadline=appstruct['deadline'],
                    )
                tender.added_by = self.request.user
                self.request.dbsession.add(tender)
                self.request.session.flash('success:Dodano do bazy danych')
                log.info(f'Użytkownik {self.request.user.username} dodał przetarg {tender.name}')
                return HTTPFound(location=self.request.route_url('tenders'))

        if rendered_form is None:
            rendered_form = form.render(appstruct=appstruct)
        reqts = form.get_widget_resources()

        return dict(
            heading='Dodaj przetarg',
            rendered_form=rendered_form,
            css_links=reqts['css'],
            js_links=reqts['js'],
            )

    @view_config(
        route_name='tender_edit',
        renderer='form.mako',
        permission='edit'
    )
    def edit(self):
        tender = self.request.context.tender
        form = self.tender_form
        rendered_form = None

        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = form.validate(controls)
            except deform.exception.ValidationFailure as e:
                rendered_form = e.render()
            else:
                tender.name = appstruct['name']
                tender.city = appstruct['city']
                tender.investor = self._get_investor(appstruct['investor'])
                tender.link = appstruct['link']
                tender.deadline = appstruct['deadline']
                tender.edited_by = self.request.user
                self.request.session.flash('success:Zmiany zostały zapisane')
                log.info(f'Użytkownik {self.request.user.username} zmienił dane przetargu {tender.name}')
                return HTTPFound(location=self.request.route_url('tender_edit',
                                                                 tender_id=tender.id,
                                                                 slug=tender.slug))
        appstruct = {
            'name': tender.name,
            'city': tender.city,
            'investor': tender.investor.name if tender.investor else '',
            'link': tender.link,
            'deadline': tender.deadline
            }

        if rendered_form is None:
            rendered_form = form.render(appstruct=appstruct)
        reqts = form.get_widget_resources()

        return dict(
            heading='Edytuj dane przetargu',
            rendered_form=rendered_form,
            css_links=reqts['css'],
            js_links=reqts['js'],
            )

    @view_config(
        route_name='tender_delete',
        request_method='POST',
        permission='edit'
    )
    def delete(self):
        tender = self.request.context.tender
        self.request.dbsession.delete(tender)
        self.request.session.flash('success:Usunięto z bazy danych')
        log.info(f'Użytkownik {self.request.user.username} usunął przetarg {tender.name}')
        return HTTPFound(location=self.request.route_url('home'))

    @view_config(
        route_name='tender_select',
        request_method='GET',
        renderer='json',
    )
    def select(self):
        term = self.request.params.get('term')
        query = self.request.dbsession.query(Tender)
        items = query.filter(Tender.name.ilike('%' + term + '%'))
        data = [i.name for i in items]
        return data

    @view_config(
        route_name='tender_search',
        renderer='tender_search.mako',
        permission='view'
    )
    def search(self):
        return {}

    @view_config(
        route_name='tender_search_results',
        renderer='tender_search_results.mako',
        permission='view'
    )
    def search_results(self):
        name = self.request.params.get('name')
        city = self.request.params.get('city')
        page = self.request.params.get('page', 1)
        results = self.request.dbsession.query(Tender).\
            filter(Tender.name.ilike('%' + name + '%')).\
            filter(Tender.city.ilike('%' + city + '%')).\
            order_by(Tender.name)
        paginator = get_paginator(self.request, results, page=page)
        return {'paginator': paginator}
