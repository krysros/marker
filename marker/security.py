from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from .models import User


def rolefinder(userid, request):
    query = request.dbsession.query(User)
    user = query.filter(User.username == userid).first()
    if user:
        return ['role:%s' % user.role]


def includeme(config):
    settings = config.get_settings()
    authn_policy = AuthTktAuthenticationPolicy(
        settings.get('auth.secret'),
        callback=rolefinder,
        hashalg='sha512'
        )
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
