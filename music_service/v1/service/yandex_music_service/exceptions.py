class ServiceException(Exception):
    pass


class NotFoundException(ServiceException):
    pass


class InternalServiceErrorException(ServiceException):
    pass
