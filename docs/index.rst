Welcome to transmission-fluid's documentation!
==============================================

transmission-fluid is a Python wrapper around the `Transmission`_ BitTorrent client's `RPC interface`_.

.. _RPC interface: https://trac.transmissionbt.com/browser/trunk/extras/rpc-spec.txt
.. _Transmission: http://transmissionbt.com/

::

   >>> from transmission import Transmission
   >>> client = Transmission()
   >>> response = client('torrent-get', ids=1, fields=['name']
   >>> response['torrents']
   [{u'name': u'torrent 1'}]

.. toctree::
   :maxdepth: 2

   getting-started
   usage
   examples
   developers
