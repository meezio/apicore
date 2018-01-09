import jsonschema


def validate(data, schema):
    try:
        jsonschema.validate(data, schema)
    except jsonschema.exceptions.ValidationError:
        return False

    if schema["type"] == "object":
        allowed = list(schema["properties"].keys())
        for key in data.keys():
            if key not in allowed:
                return False

    return True
