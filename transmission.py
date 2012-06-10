import base64
import anyjson
import requests
import datetime
import operator

CSRF_ERROR_CODE = 409
CSRF_HEADER = 'X-Transmission-Session-Id'

RPC_HOST, RPC_PORT, RPC_PATH = ('localhost', 9091, '/transmission/rpc')

class BadRequest(Exception): pass
class BadOperator(Exception): pass

class Client(object):
    def __init__(self, host=RPC_HOST, port=RPC_PORT, path=RPC_PATH):
        self.url = "http://%s:%d%s" % (host, port, path)
        self.headers = {}

    def request(self, method, **kwargs):
        body = anyjson.serialize(self._format_request_body(method, **kwargs))
        response = requests.post(self.url, data=body, headers=self.headers)
        if response.status_code == CSRF_ERROR_CODE:
            self.headers[CSRF_HEADER] = response.headers[CSRF_HEADER]
            return self.request(method, **kwargs)
        return self._deserialize_response(response)

    def _format_request_body(self, method, **kwargs):
        """
        Create a request object to be serialized and sent to Transmission.
        """
        body = {"method": method}
        if 'tag' in kwargs:
            body['tag'] = kwargs.pop('tag')
        body.update({"arguments": kwargs})
        return body

    def _deserialize_response(self, response):
        doc = anyjson.deserialize(response.content)
        if doc['result'] != 'success':
            raise BadRequest("Request failed: '%s'" % doc['result'])
        return doc

class TorrentIterator(object):
    def __init__(self, client):
        self.client = client
        self.torrents = []

    def filter(self, ids, predicates):
        # Always include the 'name' and 'id' fields
        fields = [p[0] for p in predicates] + ['name', 'id']

        request_params = {'fields': fields}
        if ids:
            request_params['ids'] = ids

        response = self.client.request('torrent-get', **request_params)

        for torrent in response['arguments']['torrents']:
            predicate_results = []
            for (key, op, value) in predicates:

                # Do case-insensitive filtering on string values
                try:
                    torrent_value = torrent[key].lower()
                    test_value = value.lower()
                except AttributeError:
                    torrent_value = torrent[key]
                    test_value = value

                ret = op(torrent_value, test_value)

                predicate_results.append(ret)
                if not ret: break

            if all(predicate_results):
                self.torrents.append(torrent)

        return self

    def all(self):
        fields = ['id', 'name']
        response = self.client.request('torrent-get', fields=fields)
        self.torrents = response['arguments']['torrents']
        return self

    def __len__(self):
        return len(self.torrents)

    def __iter__(self):
        for torrent in self.torrents:
            yield torrent

class Transmission(object):
    def __init__(self, host=RPC_HOST, port=RPC_PORT, path=RPC_PATH):
        self.client = Client(host, port, path)

    def all(self):
        return TorrentIterator(self.client).all()

    def __iter__(self):
        return iter(self.all())

    def __len__(self):
        return len(self.all())

    def active(self):
        return self.filter(ids='recently-active')

    def get(self, **kwargs):
        torrents = iter(self.filter(**kwargs))
        try:
            item = next(torrents)
        except StopIteration:
            item = None
        return item

    def filter(self, **kwargs):
        predicates = []
        ids = kwargs.pop('ids', None)

        for key, value in kwargs.iteritems():
            if '__' in key:
                (field, key_op) = key.split('__')
            else:
                (field, key_op) = (key, 'eq')

            try:
                op = getattr(operator, key_op)
            except AttributeError:
                raise BadOperator("'%s' not a valid operator" % key_op)

            predicates.append((field, op, value))

        return TorrentIterator(self.client).filter(ids, predicates)

if __name__ == "__main__":
    client = Transmission()
    for torrent in client:
        print torrent['name'].encode('utf-8')
