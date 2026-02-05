from django.shortcuts import render
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



