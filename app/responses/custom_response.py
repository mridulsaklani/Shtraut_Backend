
from fastapi.responses import JSONResponse
from fastapi import status


def success_response(data: dict = None, message: str = "Success", code: int = status.HTTP_200_OK):
    return JSONResponse(
        status_code=code,
        content={
            'status': True,
            'message': message,
            'data': data
        }
    )


def error_response(message: str = "Something went wrong", code :int = status.HTTP_500_INTERNAL_SERVER_ERROR, data :dict = None):
    return JSONResponse(
        status_code=code,
        content={
            'status': False,
            "message": message,
            'error': data
        }
    )
 