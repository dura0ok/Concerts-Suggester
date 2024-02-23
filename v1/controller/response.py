from dataclasses import dataclass
from typing import Optional

from .response_codes import ResponseCodes


@dataclass(frozen=True)
class Response:
    result: Optional[object]
    is_success: bool = True
    message: str = 'Success'
    code: ResponseCodes = ResponseCodes.SUCCESS


def create_error_response(message: str, code: Optional[ResponseCodes] = None) -> Response:
    return Response(result=None, is_success=False, message=message, code=code)
