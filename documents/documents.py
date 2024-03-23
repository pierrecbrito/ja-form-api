from rest_framework.exceptions import APIException

def criar_informacoes_adicionais(request):
    distancia = request.data.get('')
    


def criar_documento_completo(request):
    """
    Essa função vai auxiliar a criação de documento completos (Cabeçalho, informações adicionais, 
    documentos de instalação e documento de pós venda) e suas regras de negócio.
    """
    documento = request.data.get('documento') 

    if not documento:
        raise APIException('Não foi enviado nenhum documento.')
    
    print(documento)
    print(documento.get('cabecalho').get('nome'))
    
    return True
    
