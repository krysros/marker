from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound

from ..models import (
    Company,
    Person,
    Branch,
    Investor,
    Tender,
    User,
    )
from ..paginator import get_paginator
from .voivodeships import VOIVODESHIPS


@view_config(
    route_name='search',
    renderer='search_results.mako',
    permission='view'
)
def search_results_view(request):
    q = request.params.get('q')
    tab = request.params.get('tab', 'branches')
    page = request.params.get('page', 1)
    if tab == 'branches':
        results = request.dbsession.query(Branch).\
            filter(Branch.name.ilike('%' + q + '%'))
    elif tab == 'companies':
        results = request.dbsession.query(Company).\
            filter(Company.name.ilike('%' + q + '%'))
    elif tab == 'persons':
        results = request.dbsession.query(Person).\
            filter(Person.fullname.ilike('%' + q + '%'))
    elif tab == 'investors':
        results = request.dbsession.query(Investor).\
            filter(Investor.name.ilike('%' + q + '%'))
    elif tab == 'tenders':
        results = request.dbsession.query(Tender).\
            filter(Tender.name.ilike('%' + q + '%'))
    else:
        raise HTTPNotFound

    paginator = get_paginator(request, results, page=page)
    voivodeships = dict(VOIVODESHIPS)

    username = request.authenticated_userid
    user = request.dbsession.query(User).\
        filter_by(username=username).one()
    try:
        upvotes = user.upvotes
    except AttributeError:
        upvotes = []

    return dict(
        q=q,
        tab=tab,
        paginator=paginator,
        voivodeships=voivodeships,
        upvotes=upvotes,
        logged_in=request.authenticated_userid,
        )
