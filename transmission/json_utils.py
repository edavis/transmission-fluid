"""
A JSON encoder and decoder to simplify working with the RPC's
datatypes.
"""

import json
import calendar
import datetime

# UNIX epochs to be turned into UTC datetimes
TIMESTAMP_KEYS = frozenset(
    ['activityDate',
     'addedDate',
     'dateCreated',
     'doneDate',
     'startDate'])

def epoch_to_datetime(value):
    return datetime.datetime.utcfromtimestamp(value)

class TransmissionJSONDecoder(json.JSONDecoder):
    def __init__(self, **kwargs):
        return super(TransmissionJSONDecoder, self).__init__(
            object_hook=self.object_hook, **kwargs)

    def object_hook(self, obj):
        for key, value in obj.items():
            if key in TIMESTAMP_KEYS:
                value = epoch_to_datetime(value)
            obj[key] = value
        return obj

class TransmissionJSONEncoder(json.JSONEncoder):
    def default(self, o):
        # datetime.datetime must be first otherwise it'll get picked
        # up by datetime.date
        if isinstance(o, datetime.datetime):
            return calendar.timegm(o.utctimetuple())
        elif isinstance(o, datetime.date):
            value = datetime.datetime(o.year, o.month, o.day)
            return calendar.timegm(value.utctimetuple())
        else:
            return o
