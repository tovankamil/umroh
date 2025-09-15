# serializers.py
import re
from rest_framework import serializers
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    # Gunakan UUIDField untuk sponsor_id agar validasi lebih akurat
    sponsor_id = serializers.UUIDField(required=True, write_only=True, allow_null=False)
    
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    ktp = serializers.CharField(
        required=True, 
        max_length=16, 
        min_length=16,
        error_messages={'min_length': 'Nomor KTP harus 16 digit.', 'max_length': 'Nomor KTP harus 16 digit.'}
    )

    class Meta:
        model = CustomUser
        fields = [
            'username', 'sponsor_id', 'name', 'email', 'password', 'first_name', 'last_name',
            'phone_number', 'ktp', 'address', 'province', 'city', 'district',
            'postal_code', 'level_status'
        ]
        extra_kwargs = {
            'username': {'validators': [], 'required': True}, # Kosongkan validator di sini
            'level_status': {'read_only': True} # Status level harusnya diatur otomatis
        }
    
    # Validasi custom untuk memastikan format UUID yang valid
    def validate_sponsor_id(self, value):
        if value:
            if not CustomUser.objects.filter(id=value).exists():
                raise serializers.ValidationError("ID sponsor tidak ditemukan.")
        return value

    def validate_username(self, value):
        # Memeriksa panjang karakter
        if len(value) < 3:
            raise serializers.ValidationError("Username minimal 3 karakter.")
        
        # Validasi karakter
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError(
                "Username hanya boleh mengandung huruf, angka, dan underscore (_)."
            )
            
        # Memeriksa duplikasi
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username sudah digunakan.")
        
        return value

    def create(self, validated_data):
        # Ambil sponsor_id jika ada
        sponsor_id = validated_data.pop('sponsor_id', None)
        
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        
        # Cari sponsor berdasarkan ID jika ada
        if sponsor_id:
            try:
                sponsor_user = CustomUser.objects.get(id=sponsor_id)
                user.sponsor_id = sponsor_user
            except CustomUser.DoesNotExist:
                # Sebaiknya ini sudah ditangani di validasi, tapi ini untuk safety
                pass
        
        user.save()
        return user