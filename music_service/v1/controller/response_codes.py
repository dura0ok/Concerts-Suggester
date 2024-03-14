from enum import IntEnum, auto


class ResponseCodes(IntEnum):
    SUCCESS = auto()
    INTERNAL_ERROR = auto()
    NOT_FOUND_ERROR = auto()
