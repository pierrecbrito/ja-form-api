from rest_framework.views import APIView
from documents.models import Documento_Instalacao, Documento_Pos_Venda, Cabecalho
from documents.serializer import DocumentoInstalacaoSerializer, DocumentoPosVendasSerializer, CabecalhoSerializer
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from documents.documents import criar_documento_completo
from products.utils.permissions import MinimumAuthorization

class Documents(APIView):
    permission_classes = [MinimumAuthorization]

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
    permission_classes = [MinimumAuthorization]

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
    permission_classes = [MinimumAuthorization]

    def get(self, request, documento_pos_venda_id):
        documento =  Documento_Pos_Venda.objects.filter(id=documento_pos_venda_id)

        if not documento.exists():
            raise APIException("Documento não encontrado.") 
        
        documento = documento.first()

        serializer = DocumentoPosVendasSerializer(documento)

        return Response({
            "documento_pos_venda": serializer.data
        })

class CabecalhoToggleAprovado(APIView):
    permission_classes = [MinimumAuthorization]
    
    def put(self, request, cabecalho_id):
        cabecalho =  Cabecalho.objects.filter(id=cabecalho_id)

        if not Cabecalho.exists():
            raise APIException("Documento não encontrado.") 
        
        cabecalho = cabecalho.first()

        cabecalho.aprovado = not cabecalho.aprovado
        cabecalho.save()

        serializer = CabecalhoSerializer(cabecalho)

        return Response({
            "cabecalho": serializer.data
        })



