from rest_framework.exceptions import APIException
from documents.models import Cabecalho, Info_Adicionais, Documento_Instalacao, Documento, Documento_Pos_Venda
from documents.serializer import CabecalhoSerializer, DocumentoInstalacaoSerializer, DocumentoPosVendasSerializer
from rest_framework.response import Response
from products.models import Product
from accounts.models import User

def criar_informacoes_adicionais(request):
    distancia = request.data.get('')

def criar_cabecalho(request):
    cabecalho = request.data.get('documento').get('cabecalho')

    if not cabecalho or not cabecalho_validado(cabecalho):
        raise APIException("O cabeçalho do documento não foi enviado ou não foi enviado adequadamente.")
    
    if not informacoes_adicionais_validado(cabecalho['informacoes_adicionais']):
        raise APIException("As informações adicionais do documento não foi enviado ou não foi enviado adequadamente.")
    
    novo_info_adicionais = Info_Adicionais.objects.create(
        distancia = cabecalho['informacoes_adicionais']['distancia'],
        horas = cabecalho['informacoes_adicionais']['horas'],
        valor_km = cabecalho['informacoes_adicionais']['valor_km'],
        valor_hora = cabecalho['informacoes_adicionais']['valor_hora'],
        total = cabecalho['informacoes_adicionais']['total']
    )
    
    try:
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
            usuario_criador=request.user,
            info_adicionais=novo_info_adicionais
        )
    except:
        novo_info_adicionais.delete()#Em caso de erro no cabeçalho, apaga o infor adicional já cadastrado
        return False

    return novo_cabecalho
    
def cabecalho_validado(cabecalho):
    campos = ['nome', 'cpf', 'endereco', 'cidade', 'cep', 'telefone', 'total', 'comissao', 'aprovado', 'informacoes_adicionais']

    for campo in campos:
        if campo not in cabecalho or cabecalho[campo] == '' or cabecalho[campo] == 0:
            return False

    return True

def informacoes_adicionais_validado(informacoes_adicionais):
    campos = ['distancia', 'horas', 'valor_km', 'valor_hora', 'total']

    for campo in campos:
        if campo not in informacoes_adicionais or informacoes_adicionais[campo] == 0:
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

    if not documentos_instalacao_validados(documentos):
        raise APIException("Documentos de instalação estão incorretos.")
    
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
            cabecalho = cabecalho
        )

        novo_documento = Documento_Instalacao.objects.create(
            documento = novo_documento_geral,
            dono = get_user_por_id(documento['dono']),
            nota_fiscal = documento['nota_fiscal']
        )

        for parceiro in documento['parceiros']:
            print(parceiro)
            novo_documento.parceiros.add(get_user_por_id(parceiro))

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
        "parceiros"
    ]

    for documento_instalacao in documentos:
        for campo in campos:
            if campo not in documento_instalacao or documento_instalacao[campo] == '':
                return False
    
    return True

def criar_documentos_de_pos_vendas(request, cabecalho):
    documento = request.data.get('documento').get('documento_pos_venda')

    if not documento_pos_venda_validado(documento):
        raise APIException("Documentos de instalação estão incorretos.")
    
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
        "total"
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
    
    
    try:
        cabecalho = criar_cabecalho(request)
        documentos_instalacao = criar_documentos_de_instalacao(request, cabecalho)
        documento_pos_venda = criar_documentos_de_pos_vendas(request, cabecalho)

        serializer = CabecalhoSerializer(cabecalho)
        serializer2 = DocumentoInstalacaoSerializer(documentos_instalacao, many=True)
        serializer3 = DocumentoPosVendasSerializer(documento_pos_venda)
        
        return Response({
            "cabecalho": serializer.data,
            "documentos_instalacao": serializer2.data,
            "documento_pos_venda": serializer3.data
        })
    except:
        cabecalho.info_adicionais.delete()
        cabecalho.delete()
        for documento in documentos_instalacao:
            documento.delete()
        documento_pos_venda.delete()

        raise APIException('Não foi possível salvar os dados.')
    

    

    
    
