Getting started
###############

transmission-fluid is available on PyPI_.

.. _PyPI: http://pypi.python.org/pypi/transmission-fluid

Installing
----------

Install via `pip` or `easy_install`::

   $ pip install transmission-fluid

Or download the source and run `python setup.py install`, if that's your thing.

transmission-fluid works with Python 2.6, 2.7, and 3.4.

It also depends on the `requests <http://python-requests.org/>`_
library, which will be automatically installed if
setuptools or distribute are available.

Creating a client
-----------------

Once installed, create a client object::

   >>> from transmission import Transmission
   >>> client = Transmission()

By default, the client connects to `localhost:9091` without authentication.

But that can be changed::

   >>> client = Transmission(host='192.168.1.102', port=9090,
   ...                       username='foo', password='bar')

.. versionadded:: 0.3
   Pass `ssl = True` when constructing the client to use `HTTPS for
   communication
   <https://github.com/edavis/transmission-fluid/pull/1>`_ between the
   client and the daemon. It's off by default.
