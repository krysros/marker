import transaction
from pyramid import testing


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

    def make_user(self, username, fullname, email, role):
        from ..models import User
        return User(username=username, fullname=fullname,
                    email=email, role=role)


class TestSetPassword(BaseTest):

    def test_password_hash_saved(self):
        user = self.make_user(username='foobar', fullname='Foo Bar',
                              email='foobar@example.com', role='basic')
        assert not user.password
        user.password = 'secret'
        assert user.password


class TestCheckPassword(BaseTest):

    def test_password_hash_not_set(self):
        user = self.make_user(username='foobar', fullname='Foo Bar',
                              email='foobar@example.com', role='basic')
        assert not user.password
        assert not user.check_password('secret')

    def test_correct_password(self):
        user = self.make_user(username='foobar', fullname='Foo Bar',
                              email='foobar@example.com', role='basic')
        user.password = 'secret'
        assert user.check_password('secret')

    def test_incorrect_password(self):
        user = self.make_user(username='foobar', fullname='Foo Bar',
                              email='foobar@example.com', role='basic')
        user.password = 'secret'
        assert not user.check_password('incorrect')
