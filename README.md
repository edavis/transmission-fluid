transmission-fluid — get under the hood
========================================

A Python wrapper around [Transmission's][transmission] [RPC
interface][rpc].

![Build Status][travis-status]

[transmission]: http://transmissionbt.com/
[rpc]: https://trac.transmissionbt.com/browser/trunk/extras/rpc-spec.txt
[travis-status]: https://secure.travis-ci.org/edavis/transmission-fluid.png "Travis CI build status"

Usage
-----

### Getting started

```python
>>> from transmission import Transmission
>>> client = Transmission()
```

By default, it connects to http://localhost:9091/transmission/rpc
without authentication.

If that doesn't work for you, you can change it:

```python
>>> client = Transmission(host='192.168.1.102', port=9090, username='foo', password='baz')
```

#### SSL proxying

Pass `ssl=True` when constructing a client to use HTTPS for
communication. You can find an example nginx config for setting up SSL
proxying [here](https://github.com/edavis/transmission-fluid/pull/1).

*(New in version 0.3)*

### RPC syntax

After creating a client object, use the following syntax to make RPC calls:

```python
>>> client(<required method>, [optional key-value arguments])
```

And transmission-fluid will return the appropriate response, if there
is one.

transmission-fluid purposefully exposes almost all of the RPC
specification instead of trying to abstract it away.  This is done for
two reasons:

1. **Easy for developers.** Developers already have enough on their
plate when writing a program. Making them learn how a new library
works is one more source of friction.

2. **Stays current.** As the Transmission developers add more methods
and arguments, you'll be able to use them right away instead of
waiting for this wrapper to be updated to take advantage of them.

The only exception to this rule is how timestamps are handled. The
Transmission RPC returns UNIX epoch timestamps for all fields
containing date and time information while transmission-fluid
transparently converts these values into UTC `datetime.datetime`
objects.

#### Dashes in keys

Some methods require arguments with dashes in them. Python doesn't
accept dashes dashes in keyword arguments, so replace any dashes with
underscores and transmission-fluid will do the right thing:

```python
>>> client('torrent-set', ids=1, peer_limit=30)
```

Examples
--------

### Getting torrent information

Say you want the name and infohash hexdigest for the first torrent in
Transmission:

```python
>>> client('torrent-get', ids=1, fields=['name', 'hashString'])
{u'torrents': [
  {u'hashString': u'7c44acebe5828dc53f460c312454141aa3fd1317',
   u'name': u'Elvis spotted in Florida.mov'}
]}
```

To get torrent information from a bunch of torrents at once, use a
list of IDs:

```python
>>> client('torrent-get', ids=range(1,11), fields=['name'])
{u'torrents': [
  {u'name': u'Elvis spotted in Florida.mov'},
  {u'name': u'Bigfoot sings the hits'},
  # ...
  {u'name': u'a-song-of-ice-and-fire_final-chapter.txt'}
]}
```

### Removing old torrents

Say you want to remove all torrents added more than 30 days ago:

```python
>>> import datetime
>>> def is_old(torrent):
...   now = datetime.datetime.utcnow()
...   delta = now - torrent['addedDate']
...   return delta.days > 30
...
>>> # If you omit the ids argument, it'll grab all torrents
>>> torrents = client('torrent-get', fields=['id', 'addedDate'])['torrents']
>>> torrent_ids = [torrent['id'] for torrent in filter(is_old, torrents)]
>>> client('torrent-remove', ids=torrent_ids)
```

#### Operating on torrents in batches

Always try to structure your program to operate on a list of torrent
IDs rather than looping through a list of torrents and making an RPC
call for each torrent ID.

It's the difference between making one HTTP request with all the
torrents you want to operate on and *N* HTTP requests with one ID at a
time.  The overhead can get noticable quick.

*Note:* The IDs don't have to be numeric, either. If you're using
 infohash hexdigests already, you can use them as-is in any `ids`
 request argument.

Installation
------------

```
$ pip install transmission-fluid
```

Requirements
------------

- [requests](http://python-requests.org/)
- Python 2.6 or 2.7

License
-------

MIT

ChangeLog
---------

- [v0.2.1][] — June 24, 2012
    - Bugfix: Fix `anyjson` ImportError when loading setup.py
    - Add project to [Travis CI][travis-ci]

[travis-ci]: http://travis-ci.org/#!/edavis/transmission-fluid

- [v0.2][] — June 23, 2012
    - Use setuptools, if available
    - Add extensive test suite
    - Test against Python 2.6 and 2.7
    - Misc. documentation updates

- [v0.1][] — June 16, 2012
    - Initial release

[v0.1]: transmission-fluid/tree/v0.1
[v0.2]: transmission-fluid/tree/v0.2
[v0.2.1]: transmission-fluid/tree/v0.2.1
