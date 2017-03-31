marker README
==================

Getting Started
---------------

- cd <directory containing this file>

- $VENV/bin/pip install -e .

- $VENV/bin/initialize_marker_db development.ini

- $VENV/bin/pserve development.ini

Running tests
-------------

- $VENV/bin/pip install -e ".[testing]"

- $VENV/bin/py.test
