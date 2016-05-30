
import re
import uuid
import datetime
from decimal import Decimal
import json

from dateutil.parser import parse

from django.contrib.sessions.serializers import JSONSerializer


class ComprehensiveSessionJSONEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that knows how to encode datetime/date, decimal types and UUIDs, set/frozenset
    """
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return 'datetime.datetime({0})'.format(obj.isoformat())
        elif isinstance(obj, datetime.date):
            return repr(obj)
        elif isinstance(obj, Decimal):
            return repr(obj)
        elif isinstance(obj, uuid.UUID):
            return repr(obj)
        # elif isinstance(obj, (set, frozenset)):
        #     if isinstance(obj, set):
        #         obj = frozenset(obj)
        #     return repr(obj)
        else:
            return super(ComprehensiveSessionJSONEncoder, self).default(obj)


class ComprehensiveSessionJSONDecoder(json.JSONDecoder):
    """
    JSONDecoder subclass that knows how to decode datetime/date, decimal types and UUIDs
    """

    def decode(self, json_data):
        json_result = json.loads(json_data)
        for key, value in json_result.items():
            if isinstance(value, (list, tuple)):
                for i, el in enumerate(value):
                    if re.match(r'\Adatetime.date\(\d{1,4}, \d{1,2}, \d{1,2}\)\Z', el):
                        date = el[14:-1]
                        el = parse(date).date()
                        del value[i]
                        value.insert(i, el)
            if isinstance(value, str):
                if re.match(r'\Adatetime.datetime\(\d{1,4}', value):
                    datetime = value[18:-1]
                    value = parse(datetime)
                    json_result[key] = value
                elif re.match(r'\Adatetime.date\(\d{1,4}, \d{1,2}, \d{1,2}\)\Z', value):
                    date = value[14:-1]
                    value = parse(date).date()
                    json_result[key] = value
                elif re.match(r'\ADecimal\(\'[.\w]+\'\)\Z', value):
                    number_as_str = value[9:-2]
                    value = Decimal(number_as_str)
                    json_result[key] = value
                elif re.match(r'\AUUID\(\'[-\w]+\'\)\Z', value):
                    uu_id = value[6:-2]
                    value = uuid.UUID(uu_id)
                    json_result[key] = value
                # elif re.match(r'\Afrozenset\({?[/\\\'\", \w]*}?\)\Z', value):
                #     elements = value[11:-2]
                #     value = set(elements.split(','))
                #     json_result[key] = value
        return json_result


class ComprehensiveSessionJSONSerializer(JSONSerializer):
    """
    JSON encoder supported Python types unsopperted in standart JSON.
    It is well work with Decimal, datetime, date.
    """

    def dumps(self, objects):
        return json.dumps(objects, separators=(',', ': '), cls=ComprehensiveSessionJSONEncoder).encode('utf8')

    def loads(self, data):
        return json.loads(data.decode('utf-8'), cls=ComprehensiveSessionJSONDecoder)

"""
import json
import uuid
from mylabour.serializers import ComprehensiveSessionJSONDecoder, ComprehensiveSessionJSONEncoder
from decimal import Decimal
import datetime
data = json.dumps([timezone.now(), datetime.datetime.now(), Decimal(3213.2132123), datetime.date.today(), uuid.uuid4()], cls=ComprehensiveSessionJSONEncoder)
json.loads(data, cls=ComprehensiveSessionJSONDecoder)
"""
