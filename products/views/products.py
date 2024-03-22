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

