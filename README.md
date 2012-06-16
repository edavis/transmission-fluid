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

>>> # Defaults to http://localhost:9091/transmission/rpc
>>> client = Transmission()

>>> client('torrent-get', ids=1, fields=['name', 'hashString'])
{u'torrents': [{u'hashString': u'7c44acebe5828dc53f460c312454141aa3fd1317',
   u'name': u'Elvis spotted in Florida.mov'}]}

>>> client('torrent-get', ids=range(1,11), fields=['name'])
{u'torrents': [{u'name': u'Elvis spotted in Florida.mov'},
  {u'name': u'Bigfoot sings the hits'},
  # ...
  {u'name': u'a-song-of-ice-and-fire_final-chapter.txt'}]}
```

Requirements
------------

- [requests](http://python-requests.org/) (>= 0.11.2)
- [anyjson](http://pypi.python.org/pypi/anyjson) (>= 0.3.1)
