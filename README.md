transmission-fluid -- get under the hood
========================================

A python wrapper around [Transmission's][transmission] [RPC
interface][rpc].

[transmission]: http://transmissionbt.com/
[rpc]: https://trac.transmissionbt.com/browser/trunk/extras/rpc-spec.txt

Usage
-----

```python
>>> from transmission import Transmission
>>> client = Transmission()
```

Getting started is pretty simple. By default, it connects to
http://localhost:9091/transmission/rpc if no `host`, `port` or `path`
arguments are given.

After creating a client object, use the following syntax to make RPC calls:

```python
>>> client(<required method>, [optional key-value arguments])
```

And transmission-fluid will return the appropriate response (if there
is one) after making sure the request succeeded.

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

Requirements
------------

- [requests](http://python-requests.org/)
- [anyjson](http://pypi.python.org/pypi/anyjson)

License
-------

MIT
