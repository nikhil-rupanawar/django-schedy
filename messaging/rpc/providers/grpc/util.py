

def parse_list(values, message):
    if isinstance(values[0], dict):
        for v in values:
            cmd = message.add()
            parse_dict(v,cmd)
    else:
        message.extend(values)


def parse_dict(values, message):
    for k, v in values.items():
        if isinstance(v, dict):
            parse_dict(v, getattr(message, k))
        elif isinstance(v, list):
            parse_list(v, getattr(message, k))
        else:
            setattr(message, k, v)


def dict_to_protobuf(value, message_cls):
    message = message_cls()
    parse_dict(value, message)
    return message

