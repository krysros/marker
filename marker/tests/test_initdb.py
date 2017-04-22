# import os
import pytest


class TestInitializeDB:

    def test_usage(self):
        from ..scripts.initializedb import main
        with pytest.raises(SystemExit):
            main(argv=['foo'])

    # def test_run(self):
    #     from ..scripts.initializedb import main
    #     main(argv=['foo', 'development.ini'])
    #     assert os.path.exists('tutorial.sqlite')) == True
    #     os.remove('tutorial.sqlite')
