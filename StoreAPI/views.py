from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponse
from store_onlayn.models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
@api_view(['GET'])
def category_list_view(request):
    categories = Category.objects.filter(parent=None)
    serializer = CategorylistSerializer(categories,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_list_view(request):
    products = Product.objects.all()
    serializer = ProductListSerializer(products,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_by_category_view(request,pk):
    products = Product.objects.filter(category__parent_id=pk)
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)
@api_view(['GET'])
def detail_product_view(request,pk):
    products = Product.objects.get(pk=pk)
    serializer = DetailProductSerializer(products)
    return Response(serializer.data)
@api_view(['GET'])
def same_products_view(request,pk):
    product = get_object_or_404(Product, pk=pk)
    same_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)
    serializer = ProductListSerializer(same_products,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def discount_products_view(request):
    products = Product.objects.filter(discount__gt=0).order_by('-created_at')
    serializer = ProductListSerializer(products,many=True)
    return Response(serializer.data)
@api_view(['GET'])
def favorites_products_view(request):
    products = FavoriteProducts.objects.filter(user=request.user)
    products = [i.product for i in products]
    serializer = ProductListSerializer(products,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def cart_products_view(request):
    # Фильтруем объекты ProductCart через связь с корзиной, покупателем и пользователем
    cart_items = ProductCart.objects.filter(cart__customer__user=request.user)
    # Используем CartProductsSerializer, который включает информацию о товаре, количестве и общей стоимости
    serializer = CartProductsSerializer(cart_items, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def order_view(request):
    profile = Order.objects.filter(customer__user=request.user).order_by('-created_at')
    serializer = ProfileListSerializer(profile, many=True)
    return Response(serializer.data)