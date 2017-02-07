def convert_to_int(in_value):
    try:
        return int(float(str(in_value)))
    except ValueError:
        return ''


def convert_to_date(in_value):
    return str(in_value).strip().split(' ')[0]


def convert_to_bool_int(in_value):
    val = str(in_value).strip().casefold()

    if val == 'y':
        return 1
    elif val == 'n':
        return 0
    else:
        return ''


def merge_boolean_fields(fields):
    return int(any(True if str(v) == 'True'
                   else False
                   for v in fields))


def bool_to_int(val):
    if str(val) == 'True':
        return 1
    else:
        return 0
