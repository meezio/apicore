import json
from bson import objectid


def toJSON(data):
    return json.dumps(data, ensure_ascii=False, cls=genericJsonEncoder)


class genericJsonEncoder(json.JSONEncoder):
    def default(self, data):
        if isinstance(data, objectid.ObjectId):
            return str(data)
        else:
            return json.JSONEncoder.default(self, data)
