from rest_framework.exceptions import APIException
from documents.models import Cabecalho, Info_Adicionais
from documents.serializer import CabecalhoSerializer
from rest_framework.response import Response

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



def criar_documento_completo(request):
    """
    Essa função vai auxiliar a criação de documento completos (Cabeçalho, informações adicionais, 
    documentos de instalação e documento de pós venda) e suas regras de negócio.
    """
    documento = request.data.get('documento') 

    if not documento:
        raise APIException('Não foi enviado nenhum documento.')
    
    cabecalho = criar_cabecalho(request)

    serializer = CabecalhoSerializer(cabecalho)
    
    return Response({
        "cabecalho": serializer.data
    })
    
