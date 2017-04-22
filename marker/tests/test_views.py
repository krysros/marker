import transaction
from pyramid import testing


def dummy_request(dbsession):
    return testing.DummyRequest(dbsession=dbsession)


class BaseTest:
    def setup_method(self):
        from ..models import get_tm_session
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:'
        })
        self.config.include('..models')
        self.config.include('..routes')

        session_factory = self.config.registry['dbsession_factory']
        self.session = get_tm_session(session_factory, transaction.manager)

        self.init_database()

    def init_database(self):
        from ..models.meta import Base
        session_factory = self.config.registry['dbsession_factory']
        engine = session_factory.kw['bind']
        Base.metadata.create_all(engine)

    def teardown_method(self):
        testing.tearDown()
        transaction.abort()


class ViewHomeTest:
    def setup_method(self):
        self.config = testing.setUp()
        self.config.include('..routes')

    def teardown_method(self):
        testing.tearDown()

    def _callFUT(self, request):
        from marker.views.home import home_view
        return home_view(request)

    def test_it(self):
        request = testing.DummyRequest()
        response = self._callFUT(request)
        assert response['project'] == 'marker'
