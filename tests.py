import nose
import mock
import unittest
from transmission import Transmission, BadRequest

class TestTransmission(unittest.TestCase):
    """
    Base class for Transmission testing.
    """
    def setUp(self):
        self.client = Transmission()

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
    @nose.tools.raises(BadRequest)
    def test_unsuccessful_request(self):
        """
        Any unsuccessful request raises BadRequest.
        """
        with mock.patch("anyjson.deserialize") as mocked:
            mocked.return_value = {"result": "failure"}
            self.client._deserialize_response(mock.MagicMock())

    @nose.tools.raises(BadRequest)
    def test_tag_mismatch(self):
        """
        Tag mismatches raises BadRequest.
        """
        with mock.patch("anyjson.deserialize") as mocked:
            mocked.return_value = {"tag": -1, "result": "success"}
            self.client._deserialize_response(mock.MagicMock())

    def test_tag_incremented_when_matches(self):
        """
        Tag param gets incremented when successful.
        """
        tag = self.client.tag
        with mock.patch("anyjson.deserialize") as mocked:
            mocked.return_value = {"result": "success", "tag": tag}
            self.client._deserialize_response(mock.MagicMock())
            self.assertEqual(tag + 1, self.client.tag)

    def test_return_arguments_if_exist(self):
        """
        Return the arguments key if it exists.
        """
        with mock.patch("anyjson.deserialize") as mocked:
            mocked.return_value = {"arguments": [1], "result": "success", "tag": 0}
            ret = self.client._deserialize_response(mock.MagicMock())
            self.assertEqual([1], ret)

    def test_return_none_when_no_arguments(self):
        """
        Return "None" if arguments doesn't exist or is False.
        """
        # "arguments" exists but is False
        with mock.patch("anyjson.deserialize") as mocked:
            mocked.return_value = {"arguments": [], "result": "success", "tag": self.client.tag}
            ret = self.client._deserialize_response(mock.MagicMock())
            self.assertEqual(None, ret)

        # "arguments" doesn't exist at all
        with mock.patch("anyjson.deserialize") as mocked:
            mocked.return_value = {"result": "success", "tag": self.client.tag}
            ret = self.client._deserialize_response(mock.MagicMock())
            self.assertEqual(None, ret)
