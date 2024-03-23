from django.db import models

class Product(models.Model):
    """
    Representa um produto da JA.
    """
    name = models.CharField(max_length=50)
    price_setup = models.DecimalField(max_digits=10, decimal_places=2)
    price_after_sales = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name