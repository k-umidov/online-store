from store_onlayn.models import Category,FavoriteProducts
from django import template

register = template.Library()
@register.simple_tag()
def get_categories():
    categories = Category.objects.filter(parent=None)
    return categories
@register.simple_tag()
def get_favorites(user):
    favorites = FavoriteProducts.objects.filter(user=user)
    products = [i.product for i in favorites]
    return products
@register.simple_tag(takes_context=True)
def query_params(context,**kwargs):
    query = context['request'].GET.copy()
    for key,value in kwargs.items():
        query[key] = value
        lst = ['model', 'price_to', 'price_from']
        if key == 'cat':
            for i in lst:
                try:
                    del query[i]
                except:
                    pass

        return query.urlencode()



