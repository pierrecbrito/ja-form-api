from rest_framework.views import APIView
from products.utils.permissions import MinimumAuthorization
from products.models import Product
from products.serializer import ProductSerializer
from rest_framework.response import Response
from rest_framework.exceptions import APIException

class Products(APIView):
    permission_classes = [MinimumAuthorization]

    def get(self, request):
        products = Product.objects.all()

        serializer = ProductSerializer(products, many=True)

        return Response({
            "produtos": serializer.data
        })
    
class ProducDetail(APIView):
    permission_classes = [MinimumAuthorization]

    def get(self, request, product_id):
        product = Product.objects.filter(id=product_id)

        if not product.exists():
            raise APIException('Produto não encontrado')

        serializer = ProductSerializer(product.first())

        return Response({
            "produto": serializer.data
        })
    
    def put(self, request, product_id):
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

