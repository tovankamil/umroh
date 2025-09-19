from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from rest_framework import status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import NotFound
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
import logging
from .tasks import create_user_task
from users.serializers import UserRegistrasiSerializer, UserUpdateSerializer, LoginSerializer, UserWithSponsorsSerializer
from utils.utils import success_response, error_response
from users.models import CustomUser
from sponsorships.models import Sponsorship 
from sponsorships.serializers import SponsorshipSerializer

logger = logging.getLogger(__name__)

class CustomPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 2
    
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })

@api_view(['GET'])
@permission_classes([AllowAny])
def userlist(request):    
    try:
        users = CustomUser.objects.filter(is_superuser=False)
        
        # Filtering berdasarkan query parameters
        username = request.GET.get('username')
        if username:
            users = users.filter(username__icontains=username)
        
        email = request.GET.get('email')
        if email:
            users = users.filter(email__icontains=email)
        
        # Ordering
        order_by = request.GET.get('order_by', 'id')
        users = users.order_by(order_by)
        
        # Pagination
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        start = (page - 1) * page_size
        end = start + page_size
        
        total_users = users.count()
        total_pages = (total_users + page_size - 1) // page_size
        
        users_page = users[start:end]
        serializer = UserRegistrasiSerializer(users_page, many=True)
        
        return success_response(
            data={
                'count': total_users,
                'total_pages': total_pages,
                'current_page': page,
                'page_size': page_size,
                'next_page': page + 1 if end < total_users else None,
                'previous_page': page - 1 if start > 0 else None,
                'results': serializer.data
            },
            message="Success get all user",
            status_code=200
        )
    except Exception as e:
        logger.error(f"Error in userlist: {str(e)}")
        return error_response(
            message="Failed to get users",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# Registrasi 
@api_view(['POST'])
@permission_classes([AllowAny])
def Registrasi(request):
    try:
        serializer = UserRegistrasiSerializer(data=request.data)
        if serializer.is_valid():
            # Convert OrderedDict to a standard dictionary
            task_data = dict(serializer.validated_data) 
           
            # Pass the standard dictionary to the task
            task = create_user_task.delay(task_data)

            return success_response(
                data={
                    'message': 'Registrasi sedang diproses secara asynchronous',
                    'task_id': task.id
                },
                status_code=status.HTTP_201_CREATED,
                message="User successfully created"
            )
        else:
            error_messages = []
            for field, errors in serializer.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            
            return Response({
                "message": "Validasi gagal.",
                "errors": error_messages
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return error_response(
            message='Registration failed',
            data=str(e),
            status_code=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])  
def user_details(request, username):    
    try:
        # Cek apakah user yang diminta ada
        user = get_object_or_404(CustomUser, username=username)
        
        # Cek authorization (user hanya bisa mengakses data sendiri, kecuali admin)
        if not request.user.is_superuser and request.user.username != username:
            return error_response(
                message="You don't have permission to access this user's data",
                status_code=status.HTTP_403_FORBIDDEN
            )
    
    except CustomUser.DoesNotExist:
        return error_response(
            message='User not found',
            status_code=status.HTTP_404_NOT_FOUND
        )    
    
    if request.method == 'GET':
        try:
            # Mendapatkan semua sponsorship yang diterima user (dimana user disponsori)
            sponsorships_received = Sponsorship.objects.filter(sponsor=user.id)
      
            # Mendapatkan semua sponsorship yang diberikan user (dimana user menjadi sponsor)
            sponsorships_given = Sponsorship.objects.filter(sponsor=user)
            
            serializer = UserWithSponsorsSerializer(user)
            # print(serializer)
            response_data = {
                'user': serializer.data,
                'sponsorships_received_count': sponsorships_received.count(),
                'sponsorships_given_count': sponsorships_given.count(),
                'sponsorships_received': SponsorshipSerializer(sponsorships_received, many=True).data,
                'sponsorships_given': SponsorshipSerializer(sponsorships_given, many=True).data
            }
            
            return success_response(
                data=response_data,
                message="User data retrieved successfully",
                status_code=status.HTTP_200_OK
            )
            
        except Exception as e:
            logger.error(f"Error getting user details: {str(e)}")
            return error_response(
                message="Failed to get user details",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
              
    elif request.method == 'PUT':
        try:
            serializer = UserUpdateSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return success_response(
                    message='User data updated successfully',
                    data=serializer.data,
                    status_code=status.HTTP_200_OK
                )
            return error_response(
                message=serializer.errors, 
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error updating user: {str(e)}")
            return error_response(
                message=f'Failed to update user: {str(e)}',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
     
    elif request.method == 'DELETE':
        try:
            # Hanya superuser yang bisa delete user
            if not request.user.is_superuser:
                return error_response(
                    message="Only admin users can delete accounts",
                    status_code=status.HTTP_403_FORBIDDEN
                )
                
            user.delete()
            return success_response(
                message='User deleted successfully',
                status_code=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            logger.error(f"Error deleting user: {str(e)}")
            return error_response(
                message=f'Failed to delete user: {str(e)}',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    try:
        serializer = LoginSerializer(data=request.data)        
        if serializer.is_valid():
            user = serializer.validated_data['user']    
            print(user)        
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)            
                      
            return success_response(
                data={
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'level_status': user.level_status,
                    'name': user.name
                },
                message="Login successful",
                status_code=status.HTTP_200_OK
            )
        
        return error_response(
            message="Invalid credentials",
            data=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return error_response(
            message="Internal server error during login",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        # Logout session
        logout(request)        
        # Untuk JWT, client side harus menghapus token
        return success_response(
            message="Logout successful",
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return error_response(
            message=f"Logout failed: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token_view(request):
    try:
        refresh_token = request.data.get('refresh_token')
        
        if not refresh_token:
            return error_response(
                message="Refresh token is required",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)
        
        return success_response(
            data={
                'access_token': access_token
            },
            message="Token refreshed successfully",
            status_code=status.HTTP_200_OK
        )
        
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        return error_response(
            message=f"Token refresh failed: {str(e)}",
            status_code=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def not_found(request):
    return error_response(
        message="Endpoint not found",
        status_code=status.HTTP_404_NOT_FOUND
    )