from rest_framework.exceptions import AuthenticationFailed, APIException
from django.contrib.auth.hashers import check_password, make_password
from accounts.models import User

class Authentication():
    """
        Regras de negócio para login e registro
    """
    def signin(self, email=None, password=None):
        """
            Retorna um usuário cadastrado em caso de credenciais corretas. E caso de credenciais incorretas,
            lança uma AuthenticationFailed exception.

            :param email: E-mail recebido.
            :param password: Senha recebida.
            :return: Usuário cadastrado.
        """
        user = User.objects.filter(email=email)#Busca algum usuário com o e-mail
        if not user.exists():
            raise AuthenticationFailed('E-mail/senha incorretos.')
        
        user = user.first() 
        if not check_password(password=password, encoded=user.password): #Verifica se a senha está correta
            raise AuthenticationFailed('E-mail/Senha incorretos.')
        
        return user
    
    def signup(self, name, email, password, role=3):
        """
            Retorna um usuário cadastrado em caso de dados enviados corretamente. Em caso de dados vazios ou únicos-já-existentes,
            lança uma APIException.

            :param name: nome recebido.
            :param email: E-mail recebido.
            :param password: Senha recebida.
            :param role: id da função do usuário (1 - Mastes, 2- Controle, 3- Colaborador [Padrão]).
            :return: Usuário recém cadastrado.
        """

        if not name or name == '' or not email or email == '' or not password or password == '':
            raise APIException('Envie os dados (name, email, password) corretamente.')
        
        #Verifica se o e-mail já está sendo utilizado:
        user = User.objects.filter(email=email)
        if user.exists():
            raise  APIException("Esse e-mail já está sendo utilizado nesse sistema.")
        
        password_hashed = make_password(password)
        created_user = User.objects.create(
            name=name,
            email=email,
            password=password_hashed,
            role_id=role
        )

        return created_user



    