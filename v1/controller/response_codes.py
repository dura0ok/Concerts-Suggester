from enum import auto, IntEnum


# TODO: add more codes ?
class ResponseCodes(IntEnum):
    SUCCESS = auto()
    INTERNAL_ERROR = auto()
    INVALID_INPUT_DATA = auto()
