from rest_framework import serializers
from users.models import CustomUser 
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

class UserRegistrasiSerializer(serializers.ModelSerializer):
    sponsor_id = serializers.UUIDField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = CustomUser
        fields = [
            'username', 'sponsor_id', 'password', 'name', 'email',
            'phone_number', 'ktp', 'address', 'province', 'city', 
            'district', 'postal_code', 'level_status'
        ]
        read_only_fields = ['id']
        extra_kwargs = {
            'email': {'required': False, 'allow_blank': True},
            'phone_number': {'required': False, 'allow_blank': True},
            'ktp': {'required': False, 'allow_blank': True},
            'name': {'required': False, 'allow_blank': True},
        }
    
    
    
    def validate_username(self, value):
        """Validasi username unique"""
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username sudah digunakan")
        return value
    

    
    
    def create(self, validated_data):
        # Handle sponsor_id
        sponsor_id = validated_data.pop('sponsor_id', None)
        password = validated_data.pop('password')
        
        # Get sponsor object if sponsor_id provided
        sponsor = None
        if sponsor_id:
            try:
                sponsor = CustomUser.objects.get(id=sponsor_id)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError({"sponsor_id": "Sponsor tidak ditemukan"})
        
        # Create user
        user = CustomUser.objects.create(
            sponsor_id=sponsor,
            **validated_data
        )
        
        # Set password properly
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