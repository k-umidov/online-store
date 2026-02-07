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
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    category = CategorylistSerializer(read_only=True)
    model = ModelProductSerializer(read_only=True)
    attrs = ProductAttributeserializer(read_only=True, many=True)
    def get_price(self,obj):
        return obj.get_price()

    def get_first_photo(self, obj):
        return obj.first_photo()

    def get_monthly_price(self, obj):
        return obj.get_monthly_price()




