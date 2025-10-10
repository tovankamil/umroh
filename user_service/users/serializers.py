import re
from rest_framework import serializers
from users.models import CustomUser 
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from users.models import CustomUser
from sponsorships.models import Sponsorship
from django.db import transaction
from sponsorships.serializers import SponsorshipSerializer

class UserRegistrasiSerializer(serializers.ModelSerializer):
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
    # ktp = serializers.CharField(
   
    #     max_length=16,
    #     error_messages={
    #         'max_length': 'Nomor KTP harus 16 digit.',
    #     }
    # )

    class Meta:
        model = CustomUser
        fields = [
            'username', 'name', 'email', 'password', 'first_name', 'last_name',
            'phone_number', 'ktp', 'address', 'province', 'city', 'district','ahliwaris',
            'postal_code', 'sponsor_username'
        ]
        extra_kwargs = {
            'username': {'validators': [], 'required': True},
            'level_status': {'read_only': True}
        }
    
    def validate_sponsor_username(self, value):
        if value:
            if not CustomUser.objects.filter(username=value).exists():
                raise serializers.ValidationError("Username sponsor tidak ditemukan.")
        return value

    # def validate_ktp(self, value):
    #     if not value.isdigit():
    #         raise serializers.ValidationError("Nomor KTP hanya boleh terdiri dari angka.")
    #     return value

    def validate_username(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Username minimal 3 karakter.")
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError("Username hanya boleh mengandung huruf, angka, dan underscore (_).")
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username sudah digunakan.")
        return value

    # def create(self, validated_data):
    #     password = validated_data.pop('password')
    #     sponsor_username = validated_data.pop('sponsor_username', None)

    #     with transaction.atomic():
    #         user = CustomUser.objects.create_user(**validated_data)
    #         user.set_password(password)
    #         user.save()

    #         if sponsor_username:
    #             sponsor = CustomUser.objects.get(username=sponsor_username)
    #             Sponsorship.objects.create(user=user, sponsor=sponsor)
    #     return user

class UserUpdateSerializer(serializers.ModelSerializer):
        password = serializers.CharField(write_only=True, required=False, allow_blank=True)
        class Meta:
            model = CustomUser
            fields = ('id', 'username', 'email', 'name', 'phone_number', 'ktp', 
                 'address', 'province', 'city', 'district', 'postal_code', 
                 'level_status', 'ahliwaris','password','bank_id','nasabah_name','account_number','branch')
            read_only_fields = ('id', 'level_status')
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
            
        }
        def validate(self, data):
        # Hapus password jika kosong
            if 'password' in data and data['password'] == '':
                data.pop('password')
        
        # Validasi username untuk update
            instance = self.instance
            
            if not CustomUser.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError({"username": "Username not found"})
        
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

class UserWithSponsorsSerializer(serializers.ModelSerializer):
    sponsorships = SponsorshipSerializer(many=True, read_only=True, source='my_sponsorships')
    sponsorships_given = SponsorshipSerializer(
        source='sponsored_by_me', 
        many=True, 
        read_only=True
    )
    class Meta:
        model = CustomUser
        fields = [
             'username', 'name', 'phone_number', 'ktp', 'address',
            'province', 'city', 'district', 'postal_code', 'level_status',
            'sponsorships','sponsorships_given'
        ]
    
    def get_total_sponsors(self, obj):
        return obj.my_sponsorships.count()

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
        
    