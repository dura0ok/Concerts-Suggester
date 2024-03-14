from typing import Optional
from dataclasses import dataclass

from .response_codes import ResponseCodes


@dataclass
class Response:
    result: Optional[object]
    is_success: bool = True
    message: str = 'Success'
    code: ResponseCodes = ResponseCodes.SUCCESS


def create_error_response(message: str, code: ResponseCodes) -> Response:
    return Response(result=None, is_success=False, message=message, code=code)
