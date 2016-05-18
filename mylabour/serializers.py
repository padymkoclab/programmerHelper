
import datetime
import json

from django.contrib.sessions.serializers import JSONSerializer


class ComprehensiveJSONSerializer(JSONSerializer):
    """
    JSON encoder suppoerted Python types set() and frozenset().
    At that data set() and frozenset converted in JSON as list-array.
    """

    def dumps(self, objects):
        for key, value in objects.items():
            if isinstance(value, datetime.datetime):
                objects[key] = {
                    'year': value.year,
                    'month': value.month,
                    'day': value.day,
                    'hour': value.hour,
                    'minute': value.minute,
                    'second': value.second,
                    'microsecond': value.microsecond,
                    'tzinfo': value.tzinfo.zone,
                }
            if isinstance(value, (set, frozenset)):
                return list(value)
        return json.dumps(objects, separators=(',', ':')).encode('latin-1')

    def loads(self, data):
        raise Exception('Ooooops .....')
        return json.loads(data.decode('latin-1'))


class ComprehensiveJSONEncoder(json.JSONEncoder):
    """
    JSON encoder suppoerted Python types set() and frozenset().
    At that data set() and frozenset converted in JSON as list-array.
    """

    def default(self, obj):
        if isinstance(obj, (set, frozenset)):
            return list(obj)
        return json.JSONEncoder.default(self, obj)
