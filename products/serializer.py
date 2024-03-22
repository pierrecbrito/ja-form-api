from rest_framework.serializers import ModelSerializer
from products.models import Product

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'price_setup',
            'price_after_sales'
        )