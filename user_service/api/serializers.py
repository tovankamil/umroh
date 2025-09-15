import re
from rest_framework import serializers
from users.models import CustomUser 
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

class UserRegistrasiSerializer(serializers.ModelSerializer):
    # Menggunakan field yang jelas untuk username sponsor
    sponsor_username = serializers.CharField(
        write_only=True, 
        required=False, 
        allow_blank=True,
        max_length=255
    )

    password = serializers.CharField(
        write_only=True, 
        required=True, 
        min_length=8,
        error_messages={'min_length': 'Password minimal harus 8 karakter.'}
    )

    ktp = serializers.CharField(
        required=True, 
        max_length=16, 
        
        error_messages={'min_length': 'Nomor KTP harus 16 digit.', 'max_length': 'Nomor KTP harus 16 digit.'}
    )

    class Meta:
        model = CustomUser
        fields = [
            'username', 'sponsor_username', 'name', 'email', 'password', 'first_name', 'last_name',
            'phone_number', 'ktp', 'address', 'province', 'city', 'district',
            'postal_code'
        ]
        extra_kwargs = {
            'username': {
                'validators': [],  # Hapus validator default jika Anda punya
                'required': True
            },
            'level_status': {'read_only': True}
        }
    
    # Validator untuk sponsor_username
    def validate_sponsor_username(self, value):
        if value:
            if not CustomUser.objects.filter(username=value).exists():
                raise serializers.ValidationError("Username sponsor tidak ditemukan.")
        return value

    # Validator untuk username (user baru)
    def validate_username(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Username minimal 3 karakter.")
        
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError("Username hanya boleh mengandung huruf, angka, dan underscore (_).")
            
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username sudah digunakan.")
        
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        return user
    def update(self, instance,validated_data):
        # Hapus sponsor_input dari validated_data agar tidak bisa diupdate
        validated_data.pop('username', None)
        validated_data.pop('sponsor', None)
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.ktp = validated_data.get('ktp', instance.ktp)
        instance.address = validated_data.get('address', instance.address)
        instance.province = validated_data.get('province', instance.province)
        instance.city = validated_data.get('city', instance.city)
        instance.district = validated_data.get('district', instance.district)
        instance.postal_code = validated_data.get('postal_code', instance.postal_code)
        instance.level_status = validated_data.get('level_status', instance.level_status)
        password = validated_data.get('password', None)
        if password:  # Hanya update password jika ada nilai baru
            instance.set_password(password)
        
        instance.save()
        return instance
    
    
class UserUpdateSerializer(serializers.ModelSerializer):
        password = serializers.CharField(write_only=True, required=False, allow_blank=True)
        class Meta:
            model = CustomUser
            fields = ('id', 'username', 'email', 'name', 'phone_number', 'ktp', 
                 'address', 'province', 'city', 'district', 'postal_code', 
                 'level_status', 'password')
        extra_kwargs = {
            'username': {'validators': []},  # Nonaktifkan validators uniqueness
            'email': {'required': False},
            'name': {'required': False},
            'phone_number': {'required': False},
            'ktp': {'required': False},
            'address': {'required': False},
            'province': {'required': False},
            'city': {'required': False},
            'district': {'required': False},
            'postal_code': {'required': False},
            'level_status': {'required': False},
        }
        def validate(self, data):
        # Hapus password jika kosong
            if 'password' in data and data['password'] == '':
                data.pop('password')
        
        # Validasi username untuk update
            instance = self.instance
            if instance and 'username' in data and data['username'] != instance.username:
                if CustomUser.objects.filter(username=data['username']).exists():
                    raise serializers.ValidationError({"username": "Username sudah digunakan"})
        
            return data
        def update(self, instance, validated_data):
            validated_data.pop('username', None)
        
            # Handle password update
            password = validated_data.pop('password', None)
            if password:  # Hanya update password jika ada nilai dan tidak kosong
                instance.set_password(password)
        
        # Update field lainnya
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            
            instance.save()
            return instance

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = authenticate(username = username, password = password)
            
            if user:
                if user.is_active:
                    data['user']= user
                    return data
                else:
                    raise serializers.ValidationError("User account is disabled.")
            else:
                raise serializers.ValidationError("Invalid username or password.")
        else:
            raise serializers.ValidationError("Must include username and password.")