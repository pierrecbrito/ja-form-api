from products.views.products import Products, ProducDetail
from django.urls import path

urlpatterns = [
    path('', Products.as_view()),
    path('<int:product_id>/', ProducDetail.as_view()),
]
