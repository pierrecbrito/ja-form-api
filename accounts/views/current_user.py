from rest_framework.views import APIView
from accounts.models import User
from accounts.serializers import UserSerializer
from rest_framework.response import Response

class CurrentUser(APIView):

    def get(self, request):
        user = User.objects.filter(id=request.user.id).first()

        serializer = UserSerializer(user)

        return Response({
            "user": serializer.data
        })
