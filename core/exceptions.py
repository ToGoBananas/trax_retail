from starlette import status


class BadRequestException(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST


class NotFoundException(BaseException):
    status_code = status.HTTP_404_NOT_FOUND