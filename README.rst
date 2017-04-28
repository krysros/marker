marker
======

Getting Started
---------------

- Change directory into your newly created project.

.. code-block:: bash

    cd marker

- Create a Python virtual environment.

.. code-block:: bash

    python3 -m venv env

- Upgrade packaging tools.

.. code-block:: bash

    env/bin/pip install --upgrade pip setuptools

- Install the project in editable mode with its testing requirements.

.. code-block:: bash

    env/bin/pip install -e ".[testing]"

- Configure the database.

.. code-block:: bash

    env/bin/initialize_marker_db development.ini

- Run your project's tests.

.. code-block:: bash

    env/bin/pytest

- Run your project.

.. code-block:: bash

    env/bin/pserve development.ini