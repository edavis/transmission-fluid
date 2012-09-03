transmission-fluid — get under the hood
========================================

<a href="http://travis-ci.org/#!/edavis/transmission-fluid"><img src="https://secure.travis-ci.org/edavis/transmission-fluid.png" alt="Travis-CI build status"/></a>

A Python wrapper around the [Transmission][transmission] BitTorrent client's [RPC interface][rpc].

```python
>>> from transmission import Transmission
>>> client = Transmission()
>>> response = client('torrent-get', ids=1, fields=['name']
>>> response['torrents']
[{u'name': u'torrent 1'}]
```

Complete documentation available on [ReadTheDocs][].

[transmission]: http://transmissionbt.com/
[rpc]: https://trac.transmissionbt.com/browser/trunk/extras/rpc-spec.txt
[ReadTheDocs]: http://transmission-fluid.readthedocs.org/
