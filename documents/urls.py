from django.urls import path
from documents.views.documents import Documents, CabecalhoToggleAprovado

urlpatterns = [
    path('', Documents.as_view()),
    path('cabecalho/<int:cabecalho_id>/', CabecalhoToggleAprovado.as_view())
]
