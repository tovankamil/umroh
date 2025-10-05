from django.urls import path
from users.views import userlist, user_details,login_view,logout_view,refresh_token_view,not_found,Registrasi
from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    
    # Authentication endpoints
    path('v1/login/', login_view, name='login'),
    path('v1/logout/', logout_view, name='logout'),     
    path('v1/refresh-token/', refresh_token_view, name='refresh_token'),
    path('v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # User endpoints
    path('v1/users/', userlist, name='user-list-list'),
    path('v1/users/<str:username>/', user_details, name='user-detail'),  
    
    # Reegistration endpoints
    path('v1/registrasi/', Registrasi, name='registration-new-user'),
    
    # Not found endpoin
    path('v1/api/<path:undefined>/', not_found, name='not_found'),
]