import nose
import mock
import json
import datetime
import unittest
import transmission
from copy import deepcopy

class CopyingMock(mock.MagicMock):
    """
    By default, MagicMock stores args/kwargs by reference rather
    than by value.

    By using deepcopy, we allow ourselves to assert how mocked objects
    were called -- even if a value changes in the mean time.

    http://www.voidspace.org.uk/python/mock/examples.html#coping-with-mutable-arguments
    """
    def __call__(self, *args, **kwargs):
        args = deepcopy(args)
        kwargs = deepcopy(kwargs)
        return super(CopyingMock, self).__call__(*args, **kwargs)

class TestTransmission(unittest.TestCase):
    """
    Base class for Transmission testing.
    """
    def setUp(self):
        self.client = transmission.Transmission()

class TestTransmissionBodyFormatting(TestTransmission):
    """
    Test that requests are formatted properly before being sent to
    Transmission.
    """
    def test_format_body(self):
        """
        Sanity check to make sure requests conform to Transmission API.
        """
        body = self.client._format_request_body(
            "torrent-get", ids=1, fields=["name"])
        expected = {"method": "torrent-get", "tag": 0,
                    "arguments": {"ids": 1, "fields": ["name"]}}
        self.assertEqual(expected, body)

    def test_format_body_replace_underscore(self):
        """
        Underscores get replaced as dashes.
        """
        body = self.client._format_request_body(
            "torrent-set", ids=1, peer_limit=10)
        expected = {"method": "torrent-set", "tag": 0,
                    "arguments": {"ids": 1, "peer-limit": 10}}
        self.assertEqual(expected, body)

class TestTransmissionResponseDeserializing(TestTransmission):
    """
    Test how responses are deserialized and handled.
    """
    @nose.tools.raises(transmission.BadRequest)
    def test_unsuccessful_request(self):
        """
        Any unsuccessful request raises BadRequest.
        """
        with mock.patch("json.loads") as mocked:
            mocked.return_value = {"result": "failure"}
            self.client._deserialize_response(mock.MagicMock())

    @nose.tools.raises(transmission.BadRequest)
    def test_tag_mismatch(self):
        """
        Tag mismatches raises BadRequest.
        """
        with mock.patch("json.loads") as mocked:
            mocked.return_value = {"tag": -1, "result": "success"}
            self.client._deserialize_response(mock.MagicMock())

    def test_tag_incremented_when_matches(self):
        """
        Tag param gets incremented when successful.
        """
        tag = self.client.tag
        with mock.patch("json.loads") as mocked:
            mocked.return_value = {"result": "success", "tag": tag}
            self.client._deserialize_response(mock.MagicMock())
            self.assertEqual(tag + 1, self.client.tag)

    def test_return_arguments_if_exist(self):
        """
        Return the arguments key if it exists.
        """
        with mock.patch("json.loads") as mocked:
            mocked.return_value = {"arguments": [1], "result": "success", "tag": 0}
            ret = self.client._deserialize_response(mock.MagicMock())
            self.assertEqual([1], ret)

    def test_return_none_when_no_arguments(self):
        """
        Return "None" if arguments doesn't exist or is False.
        """
        # "arguments" exists but is False
        with mock.patch("json.loads") as mocked:
            mocked.return_value = {"arguments": [], "result": "success", "tag": self.client.tag}
            ret = self.client._deserialize_response(mock.MagicMock())
            self.assertEqual(None, ret)

        # "arguments" doesn't exist at all
        with mock.patch("json.loads") as mocked:
            mocked.return_value = {"result": "success", "tag": self.client.tag}
            ret = self.client._deserialize_response(mock.MagicMock())
            self.assertEqual(None, ret)

    def test_json_deserialization(self):
        obj = {
            'result': 'success',
            'tag': 0,
            'arguments': {
                'foo': 1,
                'bar': 2,
            },
        }
        response = mock.MagicMock(text=json.dumps(obj))
        self.assertEqual({'foo': 1, 'bar': 2}, self.client._deserialize_response(response))

class TestTransmissionJSON(TestTransmission):
    """
    Test the custom JSON encoder and decoder.
    """
    def test_epochs_to_datetimes(self):
        """
        Convert UNIX timestamps into UTC datetimes.
        """
        returned = json.loads(json.dumps({"addedDate": 1320091283}),
                              cls=transmission.TransmissionJSONDecoder)
        expected = {"addedDate": datetime.datetime(2011, 10, 31, 20, 1, 23,
                                                   tzinfo=transmission.UTC())}
        self.assertEqual(expected, returned)

    def test_datetimes_to_epochs(self):
        """
        Convert UTC datetimes into UNIX epochs.
        """
        returned = json.dumps({"addedDate": datetime.datetime(2011, 10, 31, 20, 1, 23)},
                              cls=transmission.TransmissionJSONEncoder)
        expected = '{"addedDate": 1320091283}'
        self.assertEqual(expected, returned)

    def test_dates_to_epochs(self):
        """
        Convert UTC dates to UNIX epochs.
        """
        returned = json.dumps({"addedDate": datetime.date(2011, 10, 31)},
                              cls=transmission.TransmissionJSONEncoder)
        expected = '{"addedDate": 1320019200}'
        self.assertEqual(expected, returned)

class TestTransmissionRequests(TestTransmission):
    def test_csrf_handling(self):
        """
        Make sure the CSRF dance goes smoothly.
        """
        headers = {transmission.CSRF_HEADER: '123'}
        with mock.patch("requests.post", new_callable=CopyingMock) as mocked:
            mocked.side_effect = [mock.MagicMock(name='csrf', status_code=transmission.CSRF_ERROR_CODE, headers=headers),
                                  mock.MagicMock(name='okay')]

            self.client._make_request("torrent-get", ids=1, fields=['name'])
            (csrf, okay) = mocked.mock_calls

            kwargs = csrf[-1]
            self.assertEqual({}, kwargs['headers'])

            kwargs = okay[-1]
            self.assertEqual(headers, kwargs['headers'])
