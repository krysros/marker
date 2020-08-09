from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound

from sqlalchemy.sql.expression import desc
from sqlalchemy.sql import func

from ..models import (
    User,
    Branch,
    Company,
    Investor,
    Tender,
)

from ..models.company import companies_branches
from ..models.offer import offers_companies
from ..models.tender import investors_tenders
from ..models.user import upvotes

from ..paginator import get_paginator


@view_config(
    route_name='report',
    renderer='report.mako',
    permission='view'
)
def report_view(request):
    rel = request.params.get('rel', 'companies-voivodeships')
    page = request.params.get('page', 1)
    if rel == 'companies-voivodeships':
        data = request.dbsession.query(Company.voivodeship,
                                       func.count(Company.voivodeship).label('cv')).\
                                group_by(Company.voivodeship).\
                                order_by(desc('cv'))
    elif rel == 'companies-cities':
        data = request.dbsession.query(Company.city, func.count(Company.city).
                                       label('cc')).\
                                group_by(Company.city).\
                                order_by(desc('cc'))
    elif rel == 'companies-branches':
        data = request.dbsession.query(Branch.name,
                                       func.count(companies_branches.c.company_id).
                                       label('cb')).\
                                join(companies_branches).\
                                group_by(Branch).\
                                order_by(desc('cb'))
    elif rel == 'companies-upvotes':
        data = request.dbsession.query(Company.name,
                                       func.count(upvotes.c.company_id).label('cr')).\
                                join(upvotes).\
                                group_by(Company).\
                                order_by(desc('cr'))
    elif rel == 'companies-users':
        data = request.dbsession.query(User.username,
                                       func.count(Company.submitter_id).label('cu')).\
                                join(Company.added_by).\
                                group_by(User.username).\
                                order_by(desc('cu'))
    elif rel == 'offers-companies':
        data = request.dbsession.query(Company.name,
                                       func.count(offers_companies.c.offer_id).
                                       label('co')).\
                                join(offers_companies).\
                                group_by(Company).\
                                order_by(desc('co'))
    elif rel == 'investors-tenders':
        data = request.dbsession.query(Investor.name,
                                       func.count(investors_tenders.c.investor_id).
                                       label('ci')).\
                                join(investors_tenders).\
                                group_by(Investor).\
                                order_by(desc('ci'))
    elif rel == 'tenders-cities':
        data = request.dbsession.query(Tender.city, func.count(Tender.city).
                                       label('tc')).\
                                group_by(Tender.city).\
                                order_by(desc('tc'))
    else:
        raise HTTPNotFound

    paginator = get_paginator(request, data, page=page)
    return dict(
        rel=rel,
        paginator=paginator,
        )
