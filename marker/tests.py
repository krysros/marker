import transaction
from pyramid import testing


def dummy_request(dbsession):
    return testing.DummyRequest(dbsession=dbsession)


class BaseTest:
    def setup_method(self):
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:'
        })
        self.config.include('.models')
        settings = self.config.get_settings()

        from .models import (
            get_engine,
            get_session_factory,
            get_tm_session,
            )

        self.engine = get_engine(settings)
        session_factory = get_session_factory(self.engine)

        self.session = get_tm_session(session_factory, transaction.manager)

    def init_database(self):
        from .models.meta import Base
        Base.metadata.create_all(self.engine)

    def teardown_method(self):
        from .models.meta import Base

        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(self.engine)


class TestMyViewSuccessCondition(BaseTest):

    def setup_method(self):
        super().setup_method()
        self.init_database()

        from .models import User

        user = User(
            username='nowak',
            fullname='Jakub Nowak',
            password='supersecret',
            email='nowak@example.com',
            role='basic',
        )
        self.session.add(user)

    def test_passing_view(self):
        from .views.home import home_view
        self.config.testing_securitypolicy('nowak')
        info = home_view(dummy_request(self.session))
        assert info['project'] == 'marker'
