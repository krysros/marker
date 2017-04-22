from pyramid.testing import DummyRequest


class TestMyAuthenticationPolicy:

    def test_no_user(self):
        request = DummyRequest()
        request.user = None

        from ..security import MyAuthenticationPolicy
        policy = MyAuthenticationPolicy(None)
        assert policy.authenticated_userid(request) is None

    def test_authenticated_user(self):
        from ..models import User
        request = DummyRequest()
        request.user = User()
        request.user.id = 'foo'

        from ..security import MyAuthenticationPolicy
        policy = MyAuthenticationPolicy(None)
        assert policy.authenticated_userid(request) == 'foo'
