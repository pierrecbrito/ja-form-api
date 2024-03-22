from config.views.config import Config, ConfigDetail
from django.urls import path

urlpatterns = [
    path('', Config.as_view()),
    path('<int:config_id>/', ConfigDetail.as_view()),
]
