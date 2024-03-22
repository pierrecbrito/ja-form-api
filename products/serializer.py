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

        extra_kwargs = {
            'price_setup': {'max_digits': 10, 'decimal_places': 2},
            'price_after_sales': {'max_digits': 10, 'decimal_places': 2}
        }