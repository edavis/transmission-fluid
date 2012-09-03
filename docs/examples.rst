Examples
########

Getting torrent information
---------------------------

Say you want the name and infohash for the first torrent in
Transmission::

   >>> response = client('torrent-get', ids=1, fields=['name', 'hashString']
   >>> response['torrents']
   [{u'hashString': u'7c44acebe5828dc53f460c312454141aa3fd1317',
     u'name': 'torrent 1'}]

You can also specify a list of IDs::

   >>> response = client('torrent-get', ids=range(1,11), fields=['name', 'hashString']
   >>> response['torrents']
   [{u'hashString': u'7c44acebe5828dc53f460c312454141aa3fd1317',
     u'name': 'torrent 1'},
    {u'hashString': u'833e29014ed46e5ea05becc89aaaffb81d0ea9d0',
     u'name': 'torrent 2'}, ... ]

`ids` can also accept infohashes, if you're already working with them::

   >>> infohash = '833e29014ed46e5ea05becc89aaaffb81d0ea9d0'
   >>> response = client('torrent-get', ids=infohash, fields=['name']
   >>> response['torrents']
   [{u'name': 'torrent 2'}]

Adding torrents
---------------

Add a torrent to Transmission by filename::

   >>> client('torrent-add', filename='/path/to/file.torrent')

Removing torrents
-----------------

Say you wanted to remove all torrents that were added more than 30
days ago::

   >>> import datetime
   >>> def is_old(torrent):
   ...   now = datetime.datetime.utcnow()
   ...   elapsed = now - torrent['addedDate']
   ...   return elapsed.days > 30

   >>> # When no ids are given, grabs from all torrents
   >>> torrents = client('torrent-get', fields=['id', 'addedDate'])['torrents']

   >>> torrent_ids = [torrent['id'] for torrent in torrents if is_old(torrent)]
   >>> client('torrent-remove', ids=torrent_ids)

Operate on torrents in batches
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Always try to structure your program to operate on a list of torrent
IDs rather than looping through a list of torrents and making an RPC
call for each torrent ID.

It's the difference between making one HTTP request with all the
torrents you want to operate on and *N* HTTP requests with one ID at a
time.  The overhead can get noticable quick.

.. note:: The IDs don't have to be numeric, either. If you're using
   infohashes already, you can use them as-is in any `ids`
   request argument.
