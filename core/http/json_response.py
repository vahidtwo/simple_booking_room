from django.http import JsonResponse as BaseJsonResponse


class JsonResponse(BaseJsonResponse):
    def __init__(self, data=None, message='', extra=None, success=None, status=200, code=None,
                 **kwargs):
        message = 'something wrong try again' if status >= 500 and not message else message
        success = success if success is not None else status < 400
        content = {
            'code': code or status,
            'success': success,
            'message': message,
            'data': data or [],
            'extra': extra or {}
        }
        super().__init__(data=content, status=status, **kwargs)
