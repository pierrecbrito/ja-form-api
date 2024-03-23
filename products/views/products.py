from rest_framework.views import APIView
from products.utils.permissions import MinimumAuthorization
from products.models import Product
from products.serializer import ProductSerializer
from rest_framework.response import Response
from rest_framework.exceptions import APIException

class Products(APIView):
    """
    Gerenciador de views para produtos no geral.
    """
    permission_classes = [MinimumAuthorization] 

    def get(self, request):
        """
        Retorna uma lista de produtos na resposta HTTP.

        :param request: Requisição HTTP.
        :return todos os produtos cadastrados.
        """
        products = Product.objects.all()

        serializer = ProductSerializer(products, many=True)

        return Response({
            "produtos": serializer.data
        })
    
class ProducDetail(APIView):
    """
    Gerenciador de views para produtos específicos.
    """
    permission_classes = [MinimumAuthorization]

    def get(self, request, product_id):
        """
        Retorna o produto com id recebido pela requisição HTTP. Retorna uma APIException em 
        caso de não encontrar um produto.

        :param request: requisição HTTP.
        :param produto_id: ID do produto no banco.
        :return produto com ID passado.
        """
        product = Product.objects.filter(id=product_id)

        if not product.exists():
            raise APIException('Produto não encontrado')

        serializer = ProductSerializer(product.first())

        return Response({
            "produto": serializer.data
        })
    
    def put(self, request, product_id):
        """
        Atualiza os dados do produto no banco. Necessário que o 'name', 'price_setup', 'price_after_sales'
        (não necessariamente todos) sejam passados pelo corpo da requisição. Retorna uma APIException em 
        caso de não encontrar um produto.

        :param request: requisição HTTP.
        :param product_id: ID do produto a ser atualizado
        :return produto atualizado.
        """
        product = Product.objects.filter(id=product_id)

        if not product.exists():
            raise APIException('Produto não encontrado')
        
        product = product.first()

        product.name = request.data.get('name') or product.name
        product.price_setup = request.data.get('price_setup') or product.price_setup
        product.price_after_sales = request.data.get('price_after_sales') or product.price_after_sales

        product.save()
        
        serializer = ProductSerializer(product)

        return Response({
            "produto": serializer.data
        })

