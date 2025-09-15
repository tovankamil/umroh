# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from .models import CustomUser
# from .serializers import UserRegistrationSerializer, UserSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         # Tambahkan klaim kustom
#         token['username'] = user.username
#         return token

# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer

# class UserRegistrationView(generics.CreateAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserRegistrationSerializer
#     permission_classes = [AllowAny]
    
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         # Kirim sinyal ke Celery untuk membuat wallet
#         from .tasks import create_wallet_task
#         create_wallet_task.delay(user.id)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# class UserProfileView(generics.RetrieveUpdateAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         return self.request.user

from django.http import JsonResponse
from .models import CustomUser

def index(request):
    users = CustomUser.objects.all()
    return   JsonResponse({'users': list(users.values())})
    
def users_detail(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        return JsonResponse({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone_number': user.phone_number,
            'address': user.address,
            'province': user.province,
            'city': user.city,
            'district': user.district,
            'postal_code': user.postal_code,
            'level_status': user.level_status,
            'ktp': user.ktp,
        })
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)