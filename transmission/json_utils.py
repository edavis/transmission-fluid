"""
A JSON encoder and decoder to simplify working with the RPC's
datatypes.
"""

import json
import calendar
import datetime

class UTC(datetime.tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return datetime.timedelta(0)

    def tzname(self, dt):
        return 'UTC'

    def dst(self, dt):
        return datetime.timedelta(0)


# UNIX epochs to be turned into UTC datetimes
TIMESTAMP_KEYS = frozenset(
    ['activityDate',
     'addedDate',
     'dateCreated',
     'doneDate',
     'startDate',
     'lastAnnounceStartTime',
     'lastAnnounceTime',
     'lastScrapeStartTime',
     'lastScrapeTime',
     'nextAnnounceTime',
     'nextScrapeTime'])

def epoch_to_datetime(value):
    return datetime.datetime.fromtimestamp(value, UTC())

def datetime_to_epoch(value):
    if isinstance(value, datetime.datetime):
        return calendar.timegm(value.utctimetuple())
    elif isinstance(value, datetime.date):
        value = datetime.datetime(value.year, value.month, value.day)
        return calendar.timegm(value.utctimetuple())

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
    def default(self, value):
        # datetime is a subclass of date, so this'll catch both
        if isinstance(value, datetime.date):
            return datetime_to_epoch(value)
        else:
            return value
