from django.urls import path
from .views import index, users_detail

urlpatterns = [
    path('users/', index, name='user-index'),
    path('users/<uuid:user_id>/', users_detail, name='user-detail'),
]