from django.contrib import admin
from django.shortcuts import redirect
from django.utils.safestring import mark_safe

from .models import *
from .forms import CategoryForm
admin.site.register(Customer)
admin.site.register(FavoriteProducts)
admin.site.register(Cart)
admin.site.register(ProductCart)
admin.site.register(Delivery)
admin.site.register(Order)
admin.site.register(ProductOrder)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title','category_icon')
    list_display_links = ('pk', 'title')
    prepopulated_fields = {'slug': ('title', )}
    form = CategoryForm

    def category_icon(self, obj):
        if obj.icon:
            try:
                return mark_safe(f'<img src="{obj.icon.url}" width="30" >')
            except:
                return 'No icon'
        else:
            return 'No icon'


@admin.register(ModelProduct)
class ModelProductAdmin(admin.ModelAdmin):
    list_display = ('pk','title')
    list_display_links = ('pk','title')
    prepopulated_fields = {'slug':('title',)}

class ImagesProductInline(admin.TabularInline):
    model = ImagesProduct
    fk_name = 'product'
    extra = 1

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'category')
    list_display_links = ('pk', 'name')
    list_filter = ('category',)

@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'product', 'attribute', 'value')
    list_display_links = ('pk', 'product')
    list_filter = ('product', 'attribute')

class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'price', 'quantity', 'discount', 'category', 'model', 'product_image')
    list_display_links = ('pk', 'title')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ImagesProductInline, ProductAttributeInline]
    list_editable = ('price', 'quantity', 'discount')

    def product_image(self, obj):
        if obj.images:
            try:
                return mark_safe(f'<img src="{obj.images.first().image.url}" width="60" >')
            except:
                return 'No image'
        else:
            return 'No image'



