from tournament.utils.enums import ResponseStatus


def json_data(data=None, status=ResponseStatus.SUCCESS, message=''):
    return {
        'results': data,
        'status': status,
        'message': message
    }
