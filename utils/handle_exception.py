from rest_framework.views import exception_handler as _exception_handler


def exception_handler(exc, context):

    response = _exception_handler(exc, context)
    response.data['code'] = 0
    pass