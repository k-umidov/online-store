from django.urls import path,include
from .views import *
urlpatterns = [
    path('api/v1/categories/',category_list_view),
    path('api/v1/products/',product_list_view),
    path('api/v1/products_by_category/<int:pk>/',product_by_category_view),
    path('api/v1/detail_product/<int:pk>/',detail_product_view),
    path('api/v1/same_products/<int:pk>/',same_products_view),
]


