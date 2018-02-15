threedi-connector
=================

Python client library for interacting with the 3Di API.

Install
-------

::

    pip install git+https://github.com/nens/threedi-connector.git

Usage
-----

Start a simulation::

    >>> import threedi
    >>> simulation_parameters = {
            'model_slug': 'v2_bergermeer-v2_bergermeer_bres_maalstop-55-784c561ecebf9433cd7beb8b6a22a14f2841cda4',
            'organisation_uuid': '61f5a464c35044c19bc7d4b42d7f58cb',
            'scenario_name': 'test-lib (this result can be deleted)',
            'start': '2016-10-18T00:00',
            'end': '2016-10-18T00:30',
        }
    >>> sim = threedi.start_simulation(**simulation_parameters)
    >>> sim.info  # metadata
    {u'organisation_id': u'61f5a464c35044c19bc7d4b42d7f58cb',
     u'result_id': u'300f9ed8d1d54ff8b4def220a81060c8',
     u'status': u'received',
     u'subgrid_id': u'headless:1e0a2077d55044399a857c766e328645'}
