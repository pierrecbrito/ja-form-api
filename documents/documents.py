from rest_framework.exceptions import APIException
from documents.models import Cabecalho, Documento_Instalacao, Documento, Documento_Pos_Venda, Cobranca
from documents.serializer import CobrancaSerializer, CabecalhoSerializer, DocumentoInstalacaoSerializer, DocumentoPosVendasSerializer
from rest_framework.response import Response
from products.models import Product
from accounts.models import User


def criar_cabecalho(request):
    cabecalho = request.data.get('documento').get('cabecalho')

    if cabecalho is None or not cabecalho_validado(cabecalho):
        raise APIException("O cabeçalho do documento não foi enviado ou não foi enviado adequadamente.")
    
    """novo_info_adicionais = Info_Adicionais.objects.create(
        distancia = cabecalho['informacoes_adicionais']['distancia'],
        horas = cabecalho['informacoes_adicionais']['horas'],
        valor_km = cabecalho['informacoes_adicionais']['valor_km'],
        valor_hora = cabecalho['informacoes_adicionais']['valor_hora'],
        total = cabecalho['informacoes_adicionais']['total']
    )"""
    
    novo_cabecalho = Cabecalho.objects.create(
        nome=cabecalho['nome'],
        cnpj=cabecalho['cnpj'],
        cpf=cabecalho['cpf'],
        endereco=cabecalho['endereco'],
        cidade=cabecalho['cidade'],
        cep=cabecalho['cep'],
        telefone=cabecalho['telefone'],
        total=cabecalho['total'],
        comissao=cabecalho['comissao'],
        email=cabecalho['email'],
        usuario_criador=request.user
    )

    return novo_cabecalho
    
def cabecalho_validado(cabecalho):
    campos = ['nome', 'cnpj', 'cpf', 'endereco', 'cidade', 'cep', 'telefone', 'total', 'email', 'comissao']

    for campo in campos:
        if campo not in cabecalho or cabecalho[campo] == '' or cabecalho[campo] == 0:
            return False

    return True

def get_produto_por_id(id_produto):
    produto = Product.objects.filter(id=id_produto)

    if not produto.exists():
        raise APIException('Produto não encontrado')
    
    return produto.first()

def get_user_por_id(id_user):
    user = User.objects.filter(id=id_user)

    if not user.exists():
        raise APIException("Usuário não encontrado")
    
    return user.first()

def criar_documentos_de_instalacao(request, cabecalho):
    documentos = request.data.get('documento').get('documentos_instalacao')
    novos_documentos = []

    if len(documentos) == 0 or len(documentos) > 3:
        return []

    if not documentos_instalacao_validados(documentos):
        raise APIException("Documentos de instalação estão incorretos ou incompletos.")
    
    produto = get_produto_por_id(documentos[0]['produto'])

    for documento in documentos:
        novo_documento_geral = Documento.objects.create(
            maquina = documento['maquina'],
            numero_maquina = documento['numero_maquina'],
            quantidade_linhas = documento['quantidade_linhas'],
            maquina_nova =  documento['maquina_nova'],
            faturado_revenda =  documento['faturado_revenda'],
            produto = produto,
            valor_produto = produto.price_setup,
            servicos_executados = documento['servicos_executados'],
            testes_realizados = documento['testes_realizados'],
            total = documento['total'],
            cabecalho = cabecalho,
            comissao=documento['comissao']
        )

        novo_documento = Documento_Instalacao.objects.create(
            documento = novo_documento_geral,
            dono = get_user_por_id(documento['dono']['id']),
            nota_fiscal = documento['nota_fiscal']
        )

        for parceiro in documento['parceiros']:
            novo_documento.parceiros.add(get_user_por_id(parceiro['id']))

        novo_documento.save()

        novos_documentos.append(novo_documento)

    return novos_documentos



def documentos_instalacao_validados(documentos):

    if not len(documentos) > 0 or not len(documentos) <= 3:
        raise APIException('Está faltando ou excendo documentos de instalação.')
    
    campos = [  
        "maquina",
        "numero_maquina",
        "quantidade_linhas",
        "maquina_nova", 
        "faturado_revenda",
        "produto",
        "valor_produto",
        "servicos_executados",
        "testes_realizados",
        "total",
        "dono",
        "nota_fiscal",
        "parceiros",
        "comissao"
    ]

    for documento_instalacao in documentos:
        for campo in campos:
            if campo not in documento_instalacao or documento_instalacao[campo] == '':
                return False
    
    return True

def criar_documentos_de_pos_vendas(request, cabecalho):
    documento = request.data.get('documento').get('documento_pos_venda')

    if not documento or documento is None:
        return None

    if not documento_pos_venda_validado(documento):
        raise APIException("Documento de pós-venda está incorreto ou faltando dados.")
    
    produto = get_produto_por_id(documento['produto'])

    novo_documento_geral = Documento.objects.create(
        maquina = documento['maquina'],
        numero_maquina = documento['numero_maquina'],
        quantidade_linhas = documento['quantidade_linhas'],
        maquina_nova =  documento['maquina_nova'],
        faturado_revenda =  documento['faturado_revenda'],
        produto = produto,
        valor_produto = produto.price_after_sales,
        servicos_executados = documento['servicos_executados'],
        testes_realizados = documento['testes_realizados'],
        total = documento['total'],
        comissao=documento['comissao'],
        cabecalho = cabecalho
    )

    novo_documento = Documento_Pos_Venda.objects.create(
        documento = novo_documento_geral
    )

    return novo_documento



def documento_pos_venda_validado(documento):
    
    campos = [  
        "maquina",
        "numero_maquina",
        "quantidade_linhas",
        "maquina_nova", 
        "faturado_revenda",
        "produto",
        "valor_produto",
        "servicos_executados",
        "testes_realizados",
        "total",
        "comissao"
    ]

    for campo in campos:
        if campo not in documento or documento[campo] == '':
            return False
    
    return True

def criar_documento_cobranca(request, cabecalho):
    documento = request.data.get('documento').get('cobranca')

    if not documento or documento is None:
        return None

    if not documento_cobranca_validado(documento):
        raise APIException("Documento de pós-venda está incorreto ou faltando dados.")
    
    produto = get_produto_por_id(documento['produto'])

    novo_documento_geral = Documento.objects.create(
        maquina = documento['maquina'],
        numero_maquina = documento['numero_maquina'],
        quantidade_linhas = documento['quantidade_linhas'],
        maquina_nova =  documento['maquina_nova'],
        faturado_revenda =  documento['faturado_revenda'],
        produto = produto,
        valor_produto = produto.price_setup,
        servicos_executados = documento['servicos_executados'],
        testes_realizados = documento['testes_realizados'],
        total = documento['total'],
        comissao= documento['comissao'],
        cabecalho = cabecalho
    )

    novo_documento = Cobranca.objects.create(
        documento = novo_documento_geral,
        distancia = documento['distancia'],
        horas = documento['horas'],
        valor_km = documento['valor_km'],
        valor_hora = documento['valor_hora'],
        total = documento['total']
    )

    return novo_documento



def documento_cobranca_validado(documento):
    
    campos = [  
        "maquina",
        "numero_maquina",
        "quantidade_linhas",
        "maquina_nova", 
        "faturado_revenda",
        "produto",
        "valor_produto",
        "servicos_executados",
        "testes_realizados",
        "total",
        "distancia",
        "horas",
        "valor_km",
        "valor_hora",
        "comissao"
    ]

    for campo in campos:
        if campo not in documento or documento[campo] == '':
            return False
    
    return True

def criar_documento_completo(request):
    """
    Essa função vai auxiliar a criação de documento completos (Cabeçalho, informações adicionais, 
    documentos de instalação e documento de pós venda) e suas regras de negócio.
    """
    documento = request.data.get('documento') 

    if not documento:
        raise APIException('Não foi enviado nenhum documento.')
    

    resposta = {}
    
    cabecalho = None
    documentos_instalacao = []
    documento_pos_venda = None
    cobranca = None

    try:
        cabecalho = criar_cabecalho(request)
        documentos_instalacao = criar_documentos_de_instalacao(request, cabecalho)
        documento_pos_venda = criar_documentos_de_pos_vendas(request, cabecalho)
        cobranca = criar_documento_cobranca(request, cabecalho)
    except APIException as erro:
        if cabecalho is not None:
            cabecalho.delete()
        if len(documentos_instalacao) > 0:
            for documento_instalacao in documentos_instalacao:
                documento_instalacao.delete()
        if documento_pos_venda is not None:
            documento_pos_venda.delete()
        if cobranca is not None:
            cobranca.delete()

        raise erro


    serializer = CabecalhoSerializer(cabecalho)
    resposta['cabecalho'] = serializer.data
    
    if len(documentos_instalacao) > 0:
        serializer2 = DocumentoInstalacaoSerializer(documentos_instalacao, many=True)
        resposta['documentos_instalacao'] = serializer2.data
    
    if documento_pos_venda is not None:
        serializer3 = DocumentoPosVendasSerializer(documento_pos_venda)
        resposta['documento_pos_venda'] = serializer3.data
    
    if cobranca is not None:
        serializer4 = CobrancaSerializer(cobranca)
        resposta['cobranca'] = serializer4.data
    
    if len(documentos_instalacao) == 0 and documento_pos_venda is None and cobranca is None:
        cabecalho.info_adicionais.delete()
        cabecalho.delete()
        raise APIException('Nenhum documento foi enviado!')
        
    return Response(resposta)  
    

    

    
    
