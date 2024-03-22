from accounts.views.signin import Signin
from accounts.views.signup import Signup
from accounts.views.current_user import CurrentUser
from django.urls import path

urlpatterns = [
    path('signin/', Signin.as_view()),
    path('signup/', Signup.as_view()),
    path('user/', CurrentUser.as_view())
]
