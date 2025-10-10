from rest_framework import serializers
from .models import Bank

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class BankListSerializer(serializers.ModelSerializer):
    """Serializer untuk list bank (field terbatas)"""
    class Meta:
        model = Bank
        fields = ('id','name', 'bank_code')

class BankCreateSerializer(serializers.ModelSerializer):
    """Serializer khusus untuk create bank"""
    class Meta:
        model = Bank
        fields = ('name', 'bank_code', 'fee', 'queue', 'status')
        
    def validate_bank_code(self, value):
        """Validasi unique bank_code"""
        if Bank.objects.filter(bank_code=value).exists():
            raise serializers.ValidationError("Bank code already exists")
        return value