import pytest


class TestInitializeDB:

    def test_usage(self):
        from ..scripts.initializedb import main
        with pytest.raises(SystemExit):
            main(argv=['foo'])
