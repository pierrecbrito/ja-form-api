from rest_framework.views import APIView
from accounts.auth import Authentication
from accounts.serializers import UserSerializer
from rest_framework.response import Response

class Signup(APIView):

    def post(self, request):
        """
            Função que cuidará da requisição de registro de usuário.

            :param request: requisição post.
        """
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')

        user = Authentication.signup(self, name=name, email=email, password=password)
        
        serializer = UserSerializer(user)

        return Response({
            "user": serializer.data
        })