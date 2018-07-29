import traceback
from functools import wraps

from django.http import JsonResponse

from web.settings import DEBUG


class APIHelpers:
    OK = 200,
    CREATED = 201,
    NO_CONTENT = 204,
    SUCCESSFULLY_DELETED = 204,
    NOT_MODIFIED = 304,
    BAD_REQUEST = 400,
    UNAUTHORIZED = 401,
    FORBIDDEN = 403,
    NOT_FOUND = 404,
    CONFLICT = 409,
    INTERNAL_SERVER_ERROR = 500

    HTTP_STATUSES = {
        "OK": 200,
        "CREATED": 201,
        "NO_CONTENT": 204,
        "SUCCESSFULLY_DELETED": 204,
        "NOT_MODIFIED": 304,
        "BAD_REQUEST": 400,
        "UNAUTHORIZED": 401,
        "FORBIDDEN": 403,
        "NOT_FOUND": 404,
        "CONFLICT": 409,
        "INTERNAL_SERVER_ERROR": 500
    }

    GENERIC_FAILED_API_RESPONSE = 'Sorry, API failed is not responsive' \
                                  ' at the moment. Please try again after sometime.'
    GENERIC_FAILED_API_STATUS_CODE = 500

    @staticmethod
    def handle_api_exceptions(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            from api.v1.utils.exceptions import APIException
            status = kwargs.get("status", APIHelpers.INTERNAL_SERVER_ERROR)
            response = dict()
            response['success'] = False
            try:
                return fn(*args, **kwargs)
            except APIException as e:
                status = e.status_code
                response['message'] = traceback.format_exc() if DEBUG else e.api_message
            except Exception as e:
                response['message'] = traceback.format_exc() if DEBUG else e.args
                pass
            return JsonResponse(response, status=status)

        return wrapper

    @staticmethod
    def check_if_entity_exists(fn):
        @wraps(fn)
        def wrapper(model, model_id, *args, **kwargs):
            result = model.find({"id": model_id})
            if result.count() != 1:
                from api.v1.utils.exceptions import NotFoundException
                raise NotFoundException()
            return fn(model, model_id, *args, **kwargs)

        return wrapper


for key, value in APIHelpers.HTTP_STATUSES.items():
    setattr(APIHelpers, key, value)
