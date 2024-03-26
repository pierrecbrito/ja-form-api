from rest_framework.serializers import ModelSerializer
from documents.models import Info_Adicionais, Cabecalho, Documento, Documento_Instalacao, Documento_Pos_Venda
from rest_framework import serializers
from accounts.serializers import UserSerializer
from products.serializer import ProductSerializer

class InfoAdicionaisSerializer(ModelSerializer):
    
    class Meta:
        model = Info_Adicionais
        fields = (
            'id',
            'distancia',
            'horas',
            'valor_km',
            'valor_hora',
            'total'
        )

class CabecalhoSerializer(ModelSerializer):
    info_adicionais = serializers.SerializerMethodField()
    usuario_criador = serializers.SerializerMethodField()

    class Meta:
        model = Cabecalho
        fields = (
            'id',
            'nome',
            'cnpj',
            'cpf',
            'endereco',
            'cep',
            'cidade',
            'email',
            'telefone',
            'info_adicionais',
            'criado_em',
            'total',
            'comissao',
            'usuario_criador',
            'aprovado'
        )
    
    def get_info_adicionais(self, obj):
        info_adicionais = obj.info_adicionais
        serializer = InfoAdicionaisSerializer(info_adicionais)
        
        return serializer.data

    def get_usuario_criador(self, obj):
        usuario_criador = obj.usuario_criador
        serializer = UserSerializer(usuario_criador)
        
        return serializer.data

class DocumentoSerializer(ModelSerializer):
    produto = serializers.SerializerMethodField()
    cabecalho = serializers.SerializerMethodField()

    class Meta:
        model = Documento
        fields = (
            'maquina',
            'numero_maquina',
            'quantidade_linhas',
            'maquina_nova',
            'faturado_revenda',
            'produto',
            'valor_produto',
            'servicos_executados',
            'testes_realizados',
            'total',
            'cabecalho'
        )

    def get_produto(self, obj):
        produto = obj.produto
        serializer = ProductSerializer(produto)
        
        return serializer.data
    
    def get_cabecalho(self, obj):
        cabecalho = obj.cabecalho
        serializer = CabecalhoSerializer(cabecalho)
        
        return serializer.data
    
class DocumentoInstalacaoSerializer(ModelSerializer):
    documento = serializers.SerializerMethodField()
    dono = serializers.SerializerMethodField()
    parceiros = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Documento_Instalacao
        fields = (
            'documento',
            'dono',
            'nota_fiscal',
            'parceiros'
        )

    def get_documento(self, obj):
        documento = obj.documento
        serializer = DocumentoSerializer(documento)
        
        return serializer.data
    
    def get_dono(self, obj):
        dono = obj.dono
        serializer = UserSerializer(dono)

        return serializer.data
    
class DocumentoPosVendasSerializer(ModelSerializer):
    documento = serializers.SerializerMethodField()

    class Meta:
        model = Documento_Pos_Venda
        fields = (
            'documento',
        )

    def get_documento(self, obj):
        documento = obj.documento
        serializer = DocumentoSerializer(documento)
        
        return serializer.data
