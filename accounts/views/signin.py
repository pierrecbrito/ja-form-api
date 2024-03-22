from rest_framework.views import APIView
from accounts.auth import Authentication
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.serializers import UserSerializer
from rest_framework.response import Response

class Signin(APIView):
    
    def post(self, request):
        """
            Função que cuidará da requisição de autenticação.

            :param request: requisição post.
        """
        email = request.data.get('email')
        password = request.data.get('password')

        user = Authentication.signin(self, email, password)
        
        token = RefreshToken.for_user(user)

        serializer = UserSerializer(user)

        return Response({
            "user": serializer.data,
            "refresh": str(token),
            "access": str(token.access_token)
        })
