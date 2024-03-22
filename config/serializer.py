from rest_framework.serializers import ModelSerializer
from config.models import GeneralConfig

class ConfigSerializer(ModelSerializer):

    class Meta:
        model = GeneralConfig
        fields = (
            'id',
            'name',
            'value'
        )