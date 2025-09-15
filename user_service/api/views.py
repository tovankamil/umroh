from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from users.models import CustomUser
from .serializers import  UserRegistrasiSerializer,UserUpdateSerializer,LoginSerializer
from utils.utils import success_response,error_response
import logging

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
@permission_classes([IsAuthenticated])
def userlist(request):    
    
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
            status_code=201)
      
    # if request.method == 'POST':
    #     serializer = UserRegistrasiSerializer(data=request.data)
      
    #     if serializer.is_valid():
    #           # Mendapatkan username sponsor dari request data
    #         sponsor_username = request.data.get('sponsor_id')        
         
    #         if sponsor_username:
    #             try:
    #                 # Mencari pengguna sponsor berdasarkan username
    #                 sponsor_user = CustomUser.objects.get(id=sponsor_username)
    #                 savedata = serializer.save()  
    #                 return success_response(data={
    #                     'user_id': savedata.id,
    #                     'sponsor_id': sponsor_user.id
    #                 }, status_code=status.HTTP_201_CREATED,message="User succesfully created")
    #             except CustomUser.DoesNotExist:
    #                 return error_response(message= 'Sponsor not found', status=400)  
                
        
    #     return error_response(message= serializer.errors, status=400)
   
   
# Registrasi 

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Registrasi(request, username):
    serializer = UserRegistrasiSerializer(data=request.data)
      
    if serializer.is_valid():
        # Mendapatkan username sponsor dari request data
        sponsor_username = request.data.get('sponsor_id')           
         
        if sponsor_username:
                try:
                    # Mencari pengguna sponsor berdasarkan username
                    sponsor_user = CustomUser.objects.get(id=sponsor_username)
                    savedata = serializer.save()  
                    return success_response(data={
                        'user_id': savedata.id,
                        'sponsor_id': sponsor_user.id
                    }, status_code=status.HTTP_201_CREATED,message="User succesfully created")
                except CustomUser.DoesNotExist:
                    return error_response(message= 'Sponsor not found', status=status.HTTP_400_BAD_REQUEST)  
                
        
        return error_response(message= serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_details(request, username):    
    try:
        user = request.user 
          
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    
    if request.method == 'GET':
        serializer = UserRegistrasiSerializer(user)
        return Response(serializer.data)
             
    elif request.method == 'PUT':
        try:
            serializer = UserUpdateSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return success_response(message='Update user data successfully',data=serializer.data)
            return error_response(message= serializer.errors, status_code=400)
        except Exception as e:
            return error_response(
                message=f'Failed to update user: {str(e)}',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
     
    elif request.method == 'DELETE':
        try:
             user.delete()
             return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return error_response(
                message=f'Failed to update user: {str(e)}',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    try:
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            # Optional: Session login untuk browser
            # login(request, user)
            
            return success_response(
                data={
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'is_superuser': user.is_superuser
                },
                message="Login successful",
                status_code=status.HTTP_200_OK
            )
        
        return error_response(
            message="Login failed",
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