from rest_framework.views import APIView
from accounts.models import User
from accounts.serializers import UserSerializer
from rest_framework.response import Response
from products.utils.permissions import MinimumAuthorization

class CurrentUser(APIView):
    permission_classes = [MinimumAuthorization]

    def get(self, request):
        user = User.objects.filter(id=request.user.id).first()

        serializer = UserSerializer(user)

        return Response({
            "user": serializer.data
        })

class AllUsers(APIView):
    permission_classes = [MinimumAuthorization]
    
    def get(self, request):
        users = User.objects.all()

        serializer = UserSerializer(users, many=True)

        return Response({
            "users": serializer.data
        })
