from api.v1.utils.api_helpers import APIHelpers


class APIException(Exception):
    def __init__(self, status=APIHelpers.GENERIC_FAILED_API_STATUS_CODE,
                 message=APIHelpers.GENERIC_FAILED_API_RESPONSE, *args, **kwargs):
        super(APIException, self).__init__(*args, **kwargs)
        self.status_code = status
        self.api_message = message


class FailedToCreateException(APIException):
    def __init__(self):
        super(FailedToCreateException, self). \
            __init__(status=APIHelpers.BAD_REQUEST, message="Failed to create")


class NotFoundException(APIException):
    def __init__(self, status=APIHelpers.NOT_FOUND, message="Entity not found"):
        super(NotFoundException, self).__init__(status=status, message=message)


class DeleteException(APIException):
    def __init__(self, status=APIHelpers.BAD_REQUEST, message="Failed to delete"):
        super(DeleteException, self).__init__(status=status, message=message)


class UpdateException(APIException):
    def __init__(self, status=APIHelpers.BAD_REQUEST, message="Failed to update"):
        super(UpdateException, self).__init__(status=status, message=message)
