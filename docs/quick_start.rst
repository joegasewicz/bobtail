Quick Start
===========

A Minimal Bobtail app
---------------------

.. code-block:: python

    from typing import Tuple, Optional, Dict
    from bobtail import BobTail, AbstractRoute, Request, Response

    class Images:

        def get(self, req, res):
            res.set_body({id: 1})

    routes = [
        (Images(), "/images")
    ]

    app = BobTail(routes=routes)

Running Bobtail with Gunicorn
-----------------------------
Bobtail requires a WSGI compatible server such as Gunicorn.

.. code-block:: text

    $ pipenv run gunicorn api:app