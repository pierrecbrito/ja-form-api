from rest_framework.views import APIView
from documents.models import Documento_Instalacao, Documento_Pos_Venda
from documents.serializer import DocumentoInstalacaoSerializer, DocumentoPosVendasSerializer
from rest_framework.response import Response

class Documents(APIView):

    def get(self, request):
        documents_setup = Documento_Instalacao.objects.all()
        documents_after_sales = Documento_Pos_Venda.objects.all()

        serializer1 = DocumentoInstalacaoSerializer(documents_setup, many=True)
        serializer2 = DocumentoPosVendasSerializer(documents_after_sales, many=True)

        return Response({
            "documentos_instalacao": serializer1.data,
            "documentos_pos_venda": serializer2.data
        })



