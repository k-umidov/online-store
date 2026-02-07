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






