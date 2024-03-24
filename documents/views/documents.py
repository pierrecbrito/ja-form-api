from rest_framework.views import APIView
from documents.models import Documento_Instalacao, Documento_Pos_Venda
from documents.serializer import DocumentoInstalacaoSerializer, DocumentoPosVendasSerializer
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from documents.documents import criar_documento_completo

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

    def post(self, request):
    
        return criar_documento_completo(request)
        

class DocumentInstalacaoDetail(APIView):
    
    def get(self, request, documento_instalacao_id):
        documento =  Documento_Instalacao.objects.filter(id=documento_instalacao_id)

        if not documento.exists():
            raise APIException("Documento não encontrado.") 
        
        documento = documento.first()

        serializer = DocumentoInstalacaoSerializer(documento)

        return Response({
            "documento_instalacao": serializer.data
        })

class DocumentPosVendaDetail(APIView):
    
    def get(self, request, documento_pos_venda_id):
        documento =  Documento_Pos_Venda.objects.filter(id=documento_pos_venda_id)

        if not documento.exists():
            raise APIException("Documento não encontrado.") 
        
        documento = documento.first()

        serializer = DocumentoPosVendasSerializer(documento)

        return Response({
            "documento_pos_venda": serializer.data
        })



