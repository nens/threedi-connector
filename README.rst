threedi-connector
=================

Python client library for interacting with the 3Di API.

Install
-------

.. code-block:: bash

    $ pip install git+https://github.com/nens/threedi-connector.git

Use
---

Import the threedi_connector module:

.. code-block:: python

    >>> import threedi_connector

Start a simulation:

.. code-block:: python

    >>> simulation = threedi_connector.start_simulation(
    ...    model_slug='v2_bergermeer-v2_bergermeer_bres_maalstop-55-784c561ecebf9433cd7beb8b6a22a14f2841cda4',
    ...    organisation_uuid='61f5a464c35044c19bc7d4b42d7f58cb',
    ...    scenario_name='test-lib (this result can be deleted)',
    ...    start='2016-10-18T00:00',
    ...    end='2016-10-18T00:30')
    Username: <your username>
    Password: <your pw>
    Simulation started.

Get simulation task metadata using the returned ``Simulation`` object:

.. code-block:: python

    >>> simulation.info
    {u'organisation_id': u'61f5a464c35044c19bc7d4b42d7f58cb',
     u'result_id': u'300f9ed8d1d54ff8b4def220a81060c8',
     u'status': u'received',
     u'subgrid_id': u'headless:1e0a2077d55044399a857c766e328645'}

Information from 3Di API can be requested using the ``SimulationManager``.
For example, getting the saved states and queued simulation:

.. code-block:: python

    >>> sim_manager = threedi_connector.SimulationManager()
    >>> sim_manager.authenticate()  # authenticate once for this session
    Username: <your username>
    Password: <your pw>
    >>> sim_manager.saved_states
    [{'some': 'data...', ...}]
    >>> sm.queued_tasks
    [{'more': 'data...', ...}]

Interactive mode
^^^^^^^^^^^^^^^^

Interactive mode is on by default. You can disable interactive prompts by
authenticating using the ``.authenticate(username, password)`` method on
``SimulationManager`` or ``Simulation`` objects. Note: if you call
``.authenticate()`` without arguments, it will prompt for credentials.

To disable interactivity completely it is safer to just instantiate with
``interactive=False``:

.. code-block:: python

    >>> sim_manager = threedi_connector.SimulationManager(interactive=False)
    >>> simulation = threedi_connector.Simulation(interactive=False)


Running tests
-------------

Tests are run with ``pytest``:

.. code-block:: bash

    $ python setup.py test

Design philosophy
-----------------

Be good at doing **one** (or maybe two or three) thing(s).

A **very simple** API, with clear public and private classes/methods/functions. A simple API means also less need for thorough documentation.

As **few** dependencies as possible for maximum portability (ideally: **0**; the current situation).

Designed for both Jupyter notebook use (therefore i.e. interactive authentication), and use as a library.
