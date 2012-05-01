transmission-fluid
==================

A python library for interacting with the
[Transmission BitTorrent client][transmission] via its
[RPC interface][rpc].

[transmission]: http://transmissionbt.com/
[rpc]: https://trac.transmissionbt.com/browser/trunk/extras/rpc-spec.txt

Usage
-----

```python
>>> from transmission import Transmission
>>> client = Transmission() # defaults to http://localhost:9091/transmission/rpc

# Grab torrents by IDs
>>> client.get(10)
[<Torrent "foo">]
>>> client.get(10, 'f207b1d826a0786a44150d3bd6ae35946d701f83')
[<Torrent "foo">, <Torrent "foo2">]

# The objects returned contain all torrent stats/metainfo
>>> (torrent,) = client.get(10)
>>> torrent.name
"foo"
>>> torrent.hashString
"8202f5d04056356a07f9170b85ff8f801b636f8f"
>>> torrent.uploadRatio
0.773
```

Requirements
------------

- [requests](http://python-requests.org/) (>= 0.11.2)
- [anyjson](http://pypi.python.org/pypi/anyjson) (>= 0.3.1)

TODO
-----------

- Authentication
- Right now only the `torrent-get` method is implemented -- write the rest
