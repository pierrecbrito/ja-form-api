from accounts.views.signin import Signin
from accounts.views.signup import Signup
from accounts.views.current_user import CurrentUser, AllUsers
from django.urls import path

urlpatterns = [
    path('signin/', Signin.as_view()),
    path('signup/', Signup.as_view()),
    path('user/', CurrentUser.as_view()),
    path('users/', AllUsers.as_view())
]
