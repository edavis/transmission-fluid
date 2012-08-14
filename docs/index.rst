Welcome to transmission-fluid's documentation!
==============================================

transmission-fluid is a Python wrapper around `Transmission's`_ `RPC interface`_.

License: MIT

.. image:: https://secure.travis-ci.org/edavis/transmission-fluid.png
   :target: http://travis-ci.org/#!/edavis/transmission-fluid

.. _RPC interface: https://trac.transmissionbt.com/browser/trunk/extras/rpc-spec.txt
.. _`Transmission's`: http://transmissionbt.com/

Getting started
###############

Installing
----------

transmission-fluid can be installed via `pip` or `easy_install`::

    $ pip install transmission-fluid

Creating a client
-----------------

Once installed, you create a client object via :class:`transmission.Transmission`::

    >>> from transmission import Transmission
    >>> client = Transmission()

SSL proxy support
~~~~~~~~~~~~~~~~~

Usage
#####

RPC syntax info here.

Dashes in keys
--------------

Timestamp handling
------------------

Examples
########

Getting torrent information
----------------------------

Adding torrents
---------------

Removing torrents
-----------------


.. .. toctree::
..   :maxdepth: 2



.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`

