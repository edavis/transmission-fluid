First steps
###########

After creating a client object, communicating with Transmission is a
breeze::

   >>> response = client('torrent-get', ids=[1,2,3], fields=['name'])
   >>> response['torrents']
   [{u'name': u'torrent 1'}, {u'name': u'torrent 2'}, {u'name': u'torrent 3'}]

This calls the `torrent-get method`_ along with the `ids` and `fields`
request arguments.

.. _torrent-get method: https://trac.transmissionbt.com/browser/trunk/extras/rpc-spec.txt?rev=13328#L129

No matter what RPC method you're calling, the syntax will always be the same:

.. function:: client(method_name[, **request_arguments])
   :noindex:

   :param string method_name: A method name as described in `RPC
      specification`_ sections 3.1 to 4.6 (*e.g.,* torrent-start,
      torrent-add, session-get, etc.)

   :param request_arguments: Keyword arguments as explained in the
      specification

   :rtype: A dictionary of the "arguments" object returned from
      Transmission

Dashes in request arguments
---------------------------

Some request arguments contain dashes in their name. As this is
invalid in Python, replace any dashes with underscores::

   >>> client('torrent-set', ids=1, peer_limit=30) # instead of 'peer-limit'

Timestamp handling
------------------

The only area where transmission-fluid deviates from the RPC
specification is when dealing with timestamps.

The RPC specification returns all date and time information as `Unix
timestamps <http://en.wikipedia.org/wiki/Unix_time>`_. To make life
easier for developers, transmission-fluid transparently converts these
timestamps to UTC :class:`~datetime.datetime` objects::

   >>> response = client('torrent-get', ids=1, fields=['addedDate'])
   >>> response['torrents']
   [{u'addedDate': datetime.datetime(2011, 10, 31, 20, 1, 23)}]

Similarly, you can pass :class:`~datetime.datetime` objects as request
arguments and they'll be converted to Unix timestamps before being
transmitted to Transmission.

.. versionadded:: 0.3

.. _RPC specification: https://trac.transmissionbt.com/browser/trunk/extras/rpc-spec.txt
