from django.urls import path
from documents.views.documents import Documents

urlpatterns = [
    path('', Documents.as_view()),
]
