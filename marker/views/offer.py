import logging
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

import deform
import colander

from ..models import (
    Company,
    Branch,
    Tender,
    Offer,
    )

from deform.schema import CSRFSchema
from ..paginator import get_paginator


log = logging.getLogger(__name__)


class OfferView(object):
    def __init__(self, request):
        self.request = request

    @property
    def offer_form(self):

        company_widget = deform.widget.AutocompleteInputWidget(
            values=self.request.route_url('company_select'),
            min_length=1,
            )
        branch_widget = deform.widget.AutocompleteInputWidget(
            values=self.request.route_url('branch_select'),
            min_length=1,
            )
        tender_widget = deform.widget.AutocompleteInputWidget(
            values=self.request.route_url('tender_select'),
            min_length=1,
            )

        def check_company(node, value):
            query = self.request.dbsession.query(Company)
            exists = query.filter_by(name=value).one_or_none()
            if not exists:
                raise colander.Invalid(node, 'Firma o tej nazwie nie występuje w bazie danych')

        def check_branch(node, value):
            query = self.request.dbsession.query(Branch)
            exists = query.filter_by(name=value).one_or_none()
            if not exists:
                raise colander.Invalid(node, 'Branża o tej nazwie nie występuje w bazie danych')

        def check_tender(node, value):
            query = self.request.dbsession.query(Tender)
            exists = query.filter_by(name=value).one_or_none()
            if not exists:
                raise colander.Invalid(node, 'Przetarg o tej nazwie nie występuje w bazie danych')

        class Schema(CSRFSchema):
            company = colander.SchemaNode(
                colander.String(),
                title='Firma',
                widget=company_widget,
                validator=check_company,
                )
            branch = colander.SchemaNode(
                colander.String(),
                title='Branża',
                widget=branch_widget,
                validator=check_branch,
                )
            tender = colander.SchemaNode(
                colander.String(),
                title='Przetarg',
                widget=tender_widget,
                validator=check_tender,
                )

        schema = Schema().bind(request=self.request)
        submit_btn = deform.form.Button(name='submit', title='Zapisz')
        return deform.Form(schema, buttons=(submit_btn,))

    def _get_company(self, name):
        return self.request.dbsession.query(Company).filter_by(name=name).one()

    def _get_branch(self, name):
        return self.request.dbsession.query(Branch).filter_by(name=name).one()

    def _get_tender(self, name):
        return self.request.dbsession.query(Tender).filter_by(name=name).one()

    @view_config(
        route_name='offers',
        renderer='offers.mako',
        permission='view'
    )
    def all(self):
        page = self.request.params.get('page', 1)
        offers = self.request.dbsession.query(Offer)
        paginator = get_paginator(self.request, offers, page=page)
        return {'paginator': paginator}

    @view_config(
        route_name='offer_view',
        renderer='offer.mako',
        permission='view'
    )
    def view(self):
        offer = self.request.context.offer
        return {'offer': offer}

    @view_config(
        route_name='offer_add',
        renderer='form.mako',
        permission='edit'
    )
    def add(self):
        form = self.offer_form
        appstruct = {}
        rendered_form = None
        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = form.validate(controls)
            except deform.exception.ValidationFailure as e:
                rendered_form = e.render()
            else:
                offer = Offer(
                    company=self._get_company(appstruct['company']),
                    branch=self._get_branch(appstruct['branch']),
                    tender=self._get_tender(appstruct['tender']),
                    )
                self.request.dbsession.add(offer)
                self.request.session.flash('success:Dodano do bazy danych')
                log.info(f'Użytkownik {self.request.user.username} dodał ofertę firmy {offer.company.name}')
                return HTTPFound(location=self.request.route_url('offers'))

        if rendered_form is None:
            rendered_form = form.render(appstruct=appstruct)
        reqts = form.get_widget_resources()

        return dict(
            heading='Dodaj ofertę',
            rendered_form=rendered_form,
            css_links=reqts['css'],
            js_links=reqts['js'],
            )

    @view_config(
        route_name='offer_edit',
        renderer='form.mako',
        permission='edit'
    )
    def edit(self):
        offer = self.request.context.offer
        form = self.offer_form
        rendered_form = None

        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = form.validate(controls)
            except deform.exception.ValidationFailure as e:
                rendered_form = e.render()
            else:
                offer.company = self._get_company(appstruct['company'])
                offer.branch = self._get_branch(appstruct['branch'])
                offer.tender = self._get_tender(appstruct['tender'])
                offer.edited_by = self.request.user
                self.request.session.flash('success:Dane oferty zostały zmienione')
                log.info(f'Użytkownik {self.request.user.username} zmienił ofertę firmy {offer.company.name}')
                return HTTPFound(location=self.request.route_url('offer_view',
                                                                 offer_id=offer.id))
        appstruct = {
            'company': offer.company.name if offer.company else '',
            'branch': offer.branch.name if offer.branch else '',
            'tender': offer.tender.name if offer.tender else '',
            }

        if rendered_form is None:
            rendered_form = form.render(appstruct=appstruct)
        reqts = form.get_widget_resources()

        return dict(
            heading='Edytuj dane oferty',
            rendered_form=rendered_form,
            css_links=reqts['css'],
            js_links=reqts['js'],
            )

    @view_config(
        route_name='offer_delete',
        request_method='POST',
        permission='edit'
    )
    def delete(self):
        offer = self.request.context.offer
        self.request.dbsession.delete(offer)
        self.request.session.flash('success:Usunięto z bazy danych')
        log.info(f'Użytkownik {self.request.user.username} usunął ofertę firmy {offer.company.name}')
        return HTTPFound(location=self.request.route_url('home'))
