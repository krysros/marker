import transaction
from pyramid import testing


def dummy_request(dbsession):
    return testing.DummyRequest(dbsession=dbsession)


class DummyPostData(dict):
    def getlist(self, key):
        v = self[key]
        if not isinstance(v, (list, tuple)):
            v = [v]
        return v

    def mixed(self):
        """Required by paginator."""


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

    def get_csrf_request(self, post):
        csrf = 'abc'
        if 'csrf_token' not in post:
            post['csrf_token'] = csrf
        return testing.DummyRequest(post, method='POST',
                                    dbsession=self.session)

    def make_branch(self, name):
        from ..models import Branch
        return Branch(name)

    def make_company(self, name, city, voivodeship,
                     phone, email, www, nip, regon, krs,
                     branches, people):
        from ..models import Company
        return Company(name, city, voivodeship,
                       phone, email, www, nip, regon, krs,
                       branches, people)


class TestViewHome:
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


class TestBranch(BaseTest):
    def _callFUT(self, request):
        from marker.views.branch import BranchView
        return BranchView(request)

    def test_it_all(self):
        foo = self.make_branch('foo')
        bar = self.make_branch('bar')
        baz = self.make_branch('baz')
        self.session.add_all([foo, bar, baz])

        request = testing.DummyRequest(DummyPostData(), dbsession=self.session)
        request.matchdict = {'letter': 'b'}
        request.params = {'page': 1}
        res = self._callFUT(request).all()
        assert res['selected_letter'] == 'b'
        assert res['paginator'].items == [bar, baz]

    def test_it_view_companies_sorted_by_default(self):
        from ..models import Branch
        from ..routes import BranchResource
        from marker.views.voivodeships import VOIVODESHIPS
        foo = self.make_branch('foo')
        bar = self.make_company(
            name='Bar',
            city='Poznań',
            voivodeship='WP',
            phone='123 123 123',
            email='bar@example.com',
            www='',
            nip='',
            regon='',
            krs='',
            branches=[foo],
            people=[],
            )
        baz = self.make_company(
            name='Baz',
            city='Bydgoszcz',
            voivodeship='KP',
            phone='321 321 321',
            email='baz@example.com',
            www='',
            nip='',
            regon='',
            krs='',
            branches=[foo],
            people=[],
            )
        self.session.add_all([bar, baz])
        request = testing.DummyRequest(DummyPostData(), dbsession=self.session)
        request.context = BranchResource(foo)
        voivodeships = dict(VOIVODESHIPS)
        res = self._callFUT(request).view_companies()
        branch = self.session.query(Branch).filter_by(name='foo').one()
        assert res['branch'] == branch
        assert res['query'] == 'name'
        assert res['paginator'].items == [bar, baz]
        assert res['user_upvotes'] == []
        assert res['user_marker'] == []
        assert res['voivodeships'] == voivodeships

    def test_it_view_companies_sorted_by_name(self):
        from ..models import Branch
        from ..routes import BranchResource
        from marker.views.voivodeships import VOIVODESHIPS
        foo = self.make_branch('foo')
        bar = self.make_company(
            name='Bar',
            city='Poznań',
            voivodeship='WP',
            phone='123 123 123',
            email='bar@example.com',
            www='',
            nip='',
            regon='',
            krs='',
            branches=[foo],
            people=[],
            )
        baz = self.make_company(
            name='Baz',
            city='Bydgoszcz',
            voivodeship='KP',
            phone='321 321 321',
            email='baz@example.com',
            www='',
            nip='',
            regon='',
            krs='',
            branches=[foo],
            people=[],
            )
        self.session.add_all([bar, baz])
        request = testing.DummyRequest(DummyPostData(), dbsession=self.session)
        request.context = BranchResource(foo)
        request.params = {'sort': 'name', 'page': 1}
        voivodeships = dict(VOIVODESHIPS)
        res = self._callFUT(request).view_companies()
        branch = self.session.query(Branch).filter_by(name='foo').one()
        assert res['branch'] == branch
        assert res['query'] == 'name'
        assert res['paginator'].items == [bar, baz]
        assert res['user_upvotes'] == []
        assert res['user_marker'] == []
        assert res['voivodeships'] == voivodeships

    def test_it_view_companies_sorted_by_city(self):
        from ..models import Branch
        from ..routes import BranchResource
        from marker.views.voivodeships import VOIVODESHIPS
        foo = self.make_branch('foo')
        bar = self.make_company(
            name='Bar',
            city='Poznań',
            voivodeship='WP',
            phone='123 123 123',
            email='bar@example.com',
            www='',
            nip='',
            regon='',
            krs='',
            branches=[foo],
            people=[],
            )
        baz = self.make_company(
            name='Baz',
            city='Bydgoszcz',
            voivodeship='KP',
            phone='321 321 321',
            email='baz@example.com',
            www='',
            nip='',
            regon='',
            krs='',
            branches=[foo],
            people=[],
            )
        self.session.add_all([bar, baz])
        request = testing.DummyRequest(DummyPostData(), dbsession=self.session)
        request.context = BranchResource(foo)
        request.params = {'sort': 'city', 'page': 1}
        voivodeships = dict(VOIVODESHIPS)
        res = self._callFUT(request).view_companies()
        branch = self.session.query(Branch).filter_by(name='foo').one()
        assert res['branch'] == branch
        assert res['query'] == 'city'
        assert res['paginator'].items == [baz, bar]
        assert res['user_upvotes'] == []
        assert res['user_marker'] == []
        assert res['voivodeships'] == voivodeships

    def test_it_view_companies_sorted_by_voivodeship(self):
        from ..models import Branch
        from ..routes import BranchResource
        from marker.views.voivodeships import VOIVODESHIPS
        foo = self.make_branch('foo')
        bar = self.make_company(
            name='Bar',
            city='Poznań',
            voivodeship='WP',
            phone='123 123 123',
            email='bar@example.com',
            www='',
            nip='',
            regon='',
            krs='',
            branches=[foo],
            people=[],
            )
        baz = self.make_company(
            name='Baz',
            city='Bydgoszcz',
            voivodeship='KP',
            phone='321 321 321',
            email='baz@example.com',
            www='',
            nip='',
            regon='',
            krs='',
            branches=[foo],
            people=[],
            )
        self.session.add_all([bar, baz])
        request = testing.DummyRequest(DummyPostData(), dbsession=self.session)
        request.context = BranchResource(foo)
        request.params = {'sort': 'voivodeship', 'page': 1}
        voivodeships = dict(VOIVODESHIPS)
        res = self._callFUT(request).view_companies()
        branch = self.session.query(Branch).filter_by(name='foo').one()
        assert res['branch'] == branch
        assert res['query'] == 'voivodeship'
        assert res['paginator'].items == [baz, bar]
        assert res['user_upvotes'] == []
        assert res['user_marker'] == []
        assert res['voivodeships'] == voivodeships

    def test_it_view_companies_sorted_by_upvotes(self):
        pass
