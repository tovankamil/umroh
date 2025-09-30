from rest_framework import serializers
from .models import  Sponsorship
class SponsorshipSerializer(serializers.ModelSerializer):
    member_sponsorhip = serializers.CharField(source='user.username', read_only=True)
    
    
    class Meta:
        model = Sponsorship
        fields = ['id', 'sponsor', 'member_sponsorhip',  'created_at', 'updated_at']