import base64
import anyjson
import datetime
import operator
from constants import TORRENT_GET_FIELDS

CSRF_ERROR_CODE = 409
CSRF_HEADER = 'X-Transmission-Session-Id'

RPC_HOST, RPC_PORT, RPC_PATH = ('localhost', 9091, '/transmission/rpc')

class BadRequest(Exception): pass

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
        return self._deserialize_response(response, method)

    def _format_request_body(self, method, **kwargs):
        """
        Create a request object to be serialized and sent to Transmission.
        """
        ids = kwargs.get('ids')
        if ids is not None:
            kwargs['ids'] = ids if isinstance(ids, (list, tuple)) else [ids]
        return {"method": method, "arguments": kwargs}

    def _deserialize_response(self, response, method):
        doc = anyjson.deserialize(response.content)

        if doc['result'] != 'success':
            raise BadRequest("Request failed: '%s'" % doc['result'])

        convert_map = {
            "activityDate": datetime.datetime.fromtimestamp,
            "addedDate": datetime.datetime.fromtimestamp,
            "dateCreated": datetime.datetime.fromtimestamp,
            "doneDate": datetime.datetime.fromtimestamp,
            "startDate": datetime.datetime.fromtimestamp,
            "pieces": lambda p: bytearray(base64.b64decode(p)),
        }

        if method == "torrent-get":
            for info in doc["arguments"]["torrents"]:
                for (key, value) in info.items():
                    convert_func = convert_map.get(key)
                    if convert_func is not None:
                        info[key] = convert_func(value)
        return doc

class Torrent(object):
    def __init__(self, info):
        self.info = info

    def __getattr__(self, key):
        return self.info[key]

    def __repr__(self):
        return r'<Torrent "%s">' % self.name.encode('utf-8')

class Transmission(object):
    def __init__(self, host=RPC_HOST, port=RPC_PORT, path=RPC_PATH):
        self.client = Client(host, port, path)

    def get(self, *ids):
        response = self.client.request("torrent-get", ids=ids, fields=TORRENT_GET_FIELDS)
        torrents = []
        for info in response["arguments"]["torrents"]:
            torrents.append(Torrent(info))
        return torrents
