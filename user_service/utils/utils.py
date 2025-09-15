# utils.py (buat file baru atau tambahkan di views.py)
from rest_framework.response import Response
from rest_framework import status

def create_response(success=True, message=None, data=None, status_code=status.HTTP_200_OK):
    """
    Create standardized API response
    """
    response_data = {
        'status': 'success' if success else 'error',
        'messages': message if isinstance(message, list) else [message] if message else [],
        'data': data if data is not None else {}
    }
    
    return Response(response_data, status=status_code)

def success_response(data=None, message="Operation successful", status_code=status.HTTP_200_OK):
    return create_response(True, message, data, status_code)

def error_response(message="Operation failed", data=None, status_code=status.HTTP_400_BAD_REQUEST):
    return create_response(False, message, data, status_code)

def delete_response(message="User deleted succesfully", data=None, status_code=status.HTTP_400_BAD_REQUEST):
    return create_response(False, message, data, status_code)




