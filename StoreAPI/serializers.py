from store_onlayn.models import *
from rest_framework import serializers
# class CategorylistSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ('id','title')
#
class CategorylistSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()


class ProductListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    price = serializers.SerializerMethodField()
    first_photo = serializers.SerializerMethodField()
    monthly_price = serializers.SerializerMethodField()

    def get_price(self,obj):
        return obj.get_price()
    def get_first_photo(self,obj):
        return obj.first_photo()
    def get_monthly_price(self,obj):
        return obj.get_monthly_price()

class ModelProductSerializer(serializers.Serializer):
    title = serializers.CharField()
    id = serializers.IntegerField()

class AttributeSerializer(serializers.Serializer):
    name = serializers.CharField()
    category = CategorylistSerializer(read_only=True)

class ProductAttributeserializer(serializers.Serializer):
    value = serializers.CharField()
    attribute = AttributeSerializer(read_only=True)

class DetailProductSerializer(serializers.Serializer):
    title = serializers.CharField()
    quantity = serializers.IntegerField()
    id = serializers.IntegerField()
    first_photo = serializers.SerializerMethodField()
    monthly_price = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    color_name = serializers.CharField()
    color_code = serializers.CharField()
    discount = serializers.IntegerField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    category = CategorylistSerializer(read_only=True)
    model = ModelProductSerializer(read_only=True)
    attrs = ProductAttributeserializer(read_only=True, many=True)
    def get_price(self,obj):
        return obj.get_price()

    def get_first_photo(self, obj):
        return obj.first_photo()

    def get_monthly_price(self, obj):
        return obj.get_monthly_price()


class CustomerListSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    avatar = serializers.ImageField()
    first_photo = serializers.SerializerMethodField()

    def get_first_photo(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return 'https://sh-usugskaya-r82.gosweb.gosuslugi.ru/netcat_files/9/148/15864910.jpg'

class CartListSerializer(serializers.Serializer):
    customer = CustomerListSerializer(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    cart_total_price = serializers.SerializerMethodField()
    cart_total_quantity = serializers.SerializerMethodField()

    def get_cart_total_price(self, obj):
        products = obj.productcart_set.all()
        price = sum([i.get_total_price for i in products])
        return price

    def get_cart_total_quantity(self, obj):
        products = obj.productcart_set.all()
        quantity = sum([i.quantity for i in products])
        return quantity

class CartProductsSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    cart = CartListSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = ProductCart
        fields = ['product', 'quantity', 'cart', 'added_at', 'updated_at', 'total_price']

    def get_total_price(self, obj):
        return obj.quantity * obj.product.get_price()

class DeliveryListSerializer(serializers.Serializer):
    customer = CustomerListSerializer(read_only=True)
    phone = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    comment = serializers.CharField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    region = serializers.CharField()
    city = serializers.CharField()
    street = serializers.CharField()
    status = serializers.BooleanField()


class ProfileListSerializer(serializers.Serializer):
    customer = CustomerListSerializer(read_only=True)
    cart = CartListSerializer(read_only=True)
    delivery = DeliveryListSerializer(read_only=True)
    price = serializers.IntegerField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    completed = serializers.BooleanField()
    cart_total_price = serializers.SerializerMethodField()

    def get_cart_total_price(self,obj):
        return sum(product.total_price for product in obj.products.all())

