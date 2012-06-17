import anyjson
import requests

CSRF_ERROR_CODE = 409
CSRF_HEADER = 'X-Transmission-Session-Id'

class BadRequest(Exception): pass

class Transmission(object):
    def __init__(self, host='localhost', port=9091, path='/transmission/rpc'):
        self.url = "http://%s:%d%s" % (host, port, path)
        self.headers = {}
        self.tag = 0

    def __call__(self, method, **kwargs):
        body = anyjson.serialize(self._format_request_body(method, **kwargs))
        response = requests.post(self.url, data=body, headers=self.headers)
        if response.status_code == CSRF_ERROR_CODE:
            self.headers[CSRF_HEADER] = response.headers[CSRF_HEADER]
            return self(method, **kwargs)
        return self._deserialize_response(response)

    def _format_request_body(self, method, **kwargs):
        """
        Create a request object to be serialized and sent to Transmission.
        """
        fixed = {}
        # As Python can't accept dashes in kwargs keys, replace any
        # underscores with them here.
        for k, v in kwargs.iteritems():
            fixed[k.replace('_', '-')] = v
        return {"method": method, "tag": self.tag, "arguments": fixed}

    def _deserialize_response(self, response):
        doc = anyjson.deserialize(response.content)

        if doc['result'] != 'success':
            raise BadRequest("Request failed: '%s'" % doc['result'])

        if doc['tag'] != self.tag:
            raise BadRequest("Tag mismatch: (got %d, expected %d)" % (doc['tag'], self.tag))
        else:
            del doc['tag']
            self.tag += 1

        # Return doc['arguments'] if exists, else whole doc
        # If either of them are false, return None
        return doc.get('arguments', doc) or None
