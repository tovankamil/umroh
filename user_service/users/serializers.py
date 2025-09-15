# # serializers.py
# import re
# from rest_framework import serializers
# from .models import CustomUser

# class UserRegistrationSerializer(serializers.ModelSerializer):
#     # Menggunakan field yang jelas untuk username sponsor
#     sponsor_username = serializers.CharField(
#         write_only=True, 
#         required=False, 
#         allow_blank=True,
#         max_length=255,
#         error_messages={'required': 'Username sponsor tidak boleh kosong.'}
#     )

#     password = serializers.CharField(
#         write_only=True, 
#         required=True, 
#         min_length=8,
#         error_messages={'min_length': 'Password minimal harus 8 karakter.'}
#     )

#     ktp = serializers.CharField(
#         required=True, 
#         max_length=16, 
#         min_length=16,
#         error_messages={'min_length': 'Nomor KTP harus 16 digit.', 'max_length': 'Nomor KTP harus 16 digit.'}
#     )

#     class Meta:
#         model = CustomUser
#         fields = [
#             'username', 'sponsor_username', 'name', 'email', 'password', 'first_name', 'last_name',
#             'phone_number', 'ktp', 'address', 'province', 'city', 'district',
#             'postal_code'
#         ]
#         # Hapus 'sponsor_id' dari Meta.fields karena akan di-handle secara terpisah
#         extra_kwargs = {
#             'username': {'required': True},
#             'level_status': {'read_only': True}
#         }
    
#     def validate_username(self, value):
#         if len(value) < 3:
#             raise serializers.ValidationError("Username minimal 3 karakter.")
        
#         if not re.match(r'^[a-zA-Z0-9_]+$', value):
#             raise serializers.ValidationError(
#                 "Username hanya boleh mengandung huruf, angka, dan underscore (_)."
#             )
            
#         if CustomUser.objects.filter(username=value).exists():
#             raise serializers.ValidationError("Username sudah digunakan.")
        
#         return value

#     def validate_sponsor_username(self, value):
#         if value:
#             if not CustomUser.objects.filter(username=value).exists():
#                 raise serializers.ValidationError("Username sponsor tidak ditemukan.")
#         return value

#     def create(self, validated_data):
#         # Pop field non-model dari validated_data
#         password = validated_data.pop('password')
#         sponsor_username = validated_data.pop('sponsor_username', None)
        
#         # Buat objek pengguna
#         user = CustomUser.objects.create_user(**validated_data)
#         user.set_password(password) # Mengatur password
        
#         # Cari dan kaitkan sponsor jika ada
#         if sponsor_username:
#             try:
#                 sponsor_user = CustomUser.objects.get(username=sponsor_username)
#                 user.sponsor_username = sponsor_user
#             except CustomUser.DoesNotExist:
#                 # Logika ini seharusnya tidak terjangkau karena sudah divalidasi
#                 pass
        
#         # Simpan perubahan pada objek user (termasuk sponsor_id)
#         user.save()
        
#         return user