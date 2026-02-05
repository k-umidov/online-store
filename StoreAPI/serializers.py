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






