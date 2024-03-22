from rest_framework.views import APIView
from config.models import GeneralConfig
from config.serializer import ConfigSerializer
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from products.utils.permissions import MinimumAuthorization, ConfigPermission

class Config(APIView):
    permission_classes = [MinimumAuthorization]

    def get(self, request):
        configs = GeneralConfig.objects.all()

        serializer = ConfigSerializer(configs, many=True)
        
        return Response({
            "configs": serializer.data
        })
    
class ConfigDetail(APIView):
    permission_classes = [MinimumAuthorization]

    def get(self, request, config_id):
        config = GeneralConfig.objects.filter(id=config_id)

        if not config.exists():
            raise APIException('Configuração não encontrada.')

        serializer = ConfigSerializer(config.first())
        
        return Response({
            "configs": serializer.data
        })
    
    def put(self, request, config_id):
        config = GeneralConfig.objects.filter(id=config_id)

        if not config.exists():
            raise APIException('Configuração não encontrada.')
        
        config = config.first()
        config.value = request.data.get('value') or config.value

        config.save()

        serializer = ConfigSerializer(config)
        
        return Response({
            "configs": serializer.data
        })
