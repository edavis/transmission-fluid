transmission-fluid -- get under the hood
========================================

A python wrapper around [Transmission's][transmission] [RPC
interface][rpc].

[transmission]: http://transmissionbt.com/
[rpc]: https://trac.transmissionbt.com/browser/trunk/extras/rpc-spec.txt

Usage
-----

### Getting started

```python
>>> from transmission import Transmission
>>> client = Transmission()
```

Getting started is pretty simple. By default, it connects to
http://localhost:9091/transmission/rpc if no `host`, `port` or `path`
arguments are given.

### RPC syntax

After creating a client object, use the following syntax to make RPC calls:

```python
>>> client(<required method>, [optional key-value arguments])
```

And transmission-fluid will return the appropriate response (if there
is one) after making sure the request succeeds.

transmission-fluid purposefully exposes the RPC spec instead of trying
to abstract it away.  This is done for two reasons:

1. *Easy for developers.* Developers already have enough on their
plate when writing a program. Making them learn how a new library
works is one more source of friction.

2. *Stays current.* As the Transmission developers add more methods
and arguments, you'll be able to use them right away instead of
waiting for this wrapper to be updated to take advantage of them.

### Getting torrent info

Say, for example, you want the name and infohash hexdigest for the
first torrent in Transmission:

```python
>>> client('torrent-get', ids=1, fields=['name', 'hashString'])
{u'torrents': [
  {u'hashString': u'7c44acebe5828dc53f460c312454141aa3fd1317',
   u'name': u'Elvis spotted in Florida.mov'}
]}
```

Note how the method, request arguments and response correspond
directly with the `torrent-get` [API docs](https://trac.transmissionbt.com/browser/trunk/extras/rpc-spec.txt#L131).

And because `torrent-get` can accept a list of IDs, you can do this:

```python
>>> client('torrent-get', ids=range(1,11), fields=['name'])
{u'torrents': [
  {u'name': u'Elvis spotted in Florida.mov'},
  {u'name': u'Bigfoot sings the hits'},
  # ...
  {u'name': u'a-song-of-ice-and-fire_final-chapter.txt'}
]}
```

### Dashes in keys

Some methods require arguments with dashes in them. Python doesn't
accept dashes dashes in keyword arguments, so replace any dashes with
underscores and transmission-fluid will do the right thing:

```python
>>> client('torrent-set', ids=1, peer_limit=30)
```

Requirements
------------

- [requests](http://python-requests.org/)
- [anyjson](http://pypi.python.org/pypi/anyjson)

License
-------

MIT
