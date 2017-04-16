from pyramid.security import (
    Allow,
    Authenticated,
    ALL_PERMISSIONS,
    )

from pyramid.httpexceptions import HTTPNotFound
from .models import (
    User,
    Branch,
    Company,
    Investor,
    Tender,
    Offer,
    )


def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('static_deform', 'deform:static')
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    config.add_route('account', '/user/{username}/account',
                     factory=account_factory)
    config.add_route('password', '/user/{username}/password',
                     factory=account_factory)

    config.add_route('search', '/search', factory=default_factory)
    config.add_route('stats', '/stats', factory=default_factory)

    config.add_route('branches', '/branches', factory=default_factory)
    config.add_route('branch_index', '/branches/{letter:[a-z]}',
                     factory=default_factory)
    config.add_route('branch_companies',
                     '/branch/{branch_id:\d+}/{slug}/companies',
                     factory=branch_factory)
    config.add_route('branch_offers',
                     '/branch/{branch_id:\d+}/{slug}/offers',
                     factory=branch_factory)
    config.add_route('branch_export', '/branch/{branch_id:\d+}/{slug}/export',
                     factory=branch_factory)
    config.add_route('branch_add', '/branch/add', factory=default_factory)
    config.add_route('branch_search', '/branch/search',
                     factory=default_factory)
    config.add_route('branch_search_results', '/branch/search/results',
                     factory=default_factory)
    config.add_route('branch_select', '/branch/select',
                     factory=default_factory)
    config.add_route('branch_edit', '/branch/{branch_id:\d+}/{slug}/edit',
                     factory=branch_factory)
    config.add_route('branch_delete', '/branch/{branch_id:\d+}/{slug}/delete',
                     factory=branch_factory)

    config.add_route('companies', '/companies', factory=default_factory)
    config.add_route('company_add', '/company/add',
                     factory=default_factory)
    config.add_route('company_search', '/company/search',
                     factory=default_factory)
    config.add_route('company_search_results', '/company/search/results',
                     factory=default_factory)
    config.add_route('company_select', '/company/select',
                     factory=default_factory)
    config.add_route('company_view', '/company/{company_id:\d+}/{slug}',
                     factory=company_factory)
    config.add_route('company_edit', '/company/{company_id:\d+}/{slug}/edit',
                     factory=company_factory)
    config.add_route('company_delete',
                     '/company/{company_id:\d+}/{slug}/delete',
                     factory=company_factory)
    config.add_route('company_upvote',
                     '/company/{company_id:\d+}/{slug}/upvote',
                     factory=company_factory)

    config.add_route('person_search', '/person/search',
                     factory=default_factory)
    config.add_route('person_search_results', '/person/search/results',
                     factory=default_factory)

    config.add_route('investors', '/investors', factory=default_factory)
    config.add_route('investor_add', '/investor/add', factory=default_factory)
    config.add_route('investor_search', '/investor/search',
                     factory=default_factory)
    config.add_route('investor_search_results', '/investor/search/results',
                     factory=default_factory)
    config.add_route('investor_select', '/investor/select',
                     factory=default_factory)
    config.add_route('investor_view', '/investor/{investor_id:\d+}/{slug}',
                     factory=investor_factory)
    config.add_route('investor_edit',
                     '/investor/{investor_id:\d+}/{slug}/edit',
                     factory=investor_factory)
    config.add_route('investor_delete',
                     '/investor/{investor_id:\d+}/{slug}/delete',
                     factory=investor_factory)

    config.add_route('tenders', '/tenders', factory=default_factory)
    config.add_route('tender_add', '/tender/add', factory=default_factory)
    config.add_route('tender_search', '/tender/search',
                     factory=default_factory)
    config.add_route('tender_search_results', '/tender/search/results',
                     factory=default_factory)
    config.add_route('tender_select', '/tender/select',
                     factory=default_factory)
    config.add_route('tender_view', '/tender/{tender_id:\d+}/{slug}',
                     factory=tender_factory)
    config.add_route('tender_edit', '/tender/{tender_id:\d+}/{slug}/edit',
                     factory=tender_factory)
    config.add_route('tender_delete', '/tender/{tender_id:\d+}/{slug}/delete',
                     factory=tender_factory)

    config.add_route('offers', '/offers', factory=default_factory)
    config.add_route('offer_add', '/offer/add', factory=default_factory)
    config.add_route('offer_view', '/offer/{offer_id:\d+}',
                     factory=offer_factory)
    config.add_route('offer_edit', '/offer/{offer_id:\d+}/edit',
                     factory=offer_factory)
    config.add_route('offer_delete', '/offer/{offer_id:\d+}/delete',
                     factory=offer_factory)

    config.add_route('users', '/users', factory=default_factory)
    config.add_route('user_add', '/user/add', factory=default_factory)
    config.add_route('user_search', '/user/search',
                     factory=default_factory)
    config.add_route('user_search_results', '/user/search/results',
                     factory=default_factory)
    config.add_route('user_view', '/user/{username}',
                     factory=user_factory)
    config.add_route('user_edit', '/user/{username}/edit',
                     factory=user_factory)
    config.add_route('user_delete', '/user/{username}/delete',
                     factory=user_factory)


class DefaultResource(object):
    def __acl__(self):
        return [
            (Allow, Authenticated, 'view'),
            (Allow, 'role:editor', ('add', 'edit')),
            (Allow, 'role:admin', ALL_PERMISSIONS),
        ]


class UserResource(object):
    def __init__(self, username):
        self.username = username

    def __acl__(self):
        return [
            (Allow, self.username, 'view'),
            (Allow, self.username, 'edit'),
            (Allow, 'role:admin', ALL_PERMISSIONS),
        ]


def default_factory(request):
    return DefaultResource()


def account_factory(request):
    username = request.matchdict['username']
    query = request.dbsession.query(User)
    user = query.filter_by(username=username).one_or_none()
    if not user:
        raise HTTPNotFound
    return UserResource(username)


def branch_factory(request):
    branch_id = request.matchdict['branch_id']
    query = request.dbsession.query(Branch)
    branch = query.filter_by(id=branch_id).one_or_none()
    if not branch:
        raise HTTPNotFound
    return DefaultResource()


def company_factory(request):
    company_id = request.matchdict['company_id']
    query = request.dbsession.query(Company)
    company = query.filter_by(id=company_id).one_or_none()
    if not company:
        raise HTTPNotFound
    return DefaultResource()


def investor_factory(request):
    investor_id = request.matchdict['investor_id']
    query = request.dbsession.query(Investor)
    investor = query.filter_by(id=investor_id).one_or_none()
    if not investor:
        raise HTTPNotFound
    return DefaultResource()


def tender_factory(request):
    tender_id = request.matchdict['tender_id']
    query = request.dbsession.query(Tender)
    tender = query.filter_by(id=tender_id).one_or_none()
    if not tender:
        raise HTTPNotFound
    return DefaultResource()


def offer_factory(request):
    offer_id = request.matchdict['offer_id']
    query = request.dbsession.query(Offer)
    offer = query.filter_by(id=offer_id).one_or_none()
    if not offer:
        raise HTTPNotFound
    return DefaultResource()


def user_factory(request):
    username = request.matchdict['username']
    query = request.dbsession.query(User)
    user = query.filter_by(username=username).one_or_none()
    if not user:
        raise HTTPNotFound
    return DefaultResource()
