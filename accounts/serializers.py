from rest_framework import serializers
from accounts.models import User
from rest_framework.serializers import ModelSerializer

class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'email',
            'role'
        )
    
    def get_role(self, obj):
        name = obj.role.name
        return name 