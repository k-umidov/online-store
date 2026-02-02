from django.urls import path
from .views import *
urlpatterns = [
    path('',MainPage.as_view(),name='main'),
    path('product/<slug:slug>/',ProductDetail.as_view(),name='detail'),
    path('auth/',auth_page,name='auth'),
    path('register/',register_page,name='register'),
    path('logout/',logout_user_view,name='logout'),
    path('category/<slug:slug>/',ProductByCategory.as_view(),name='category'),
    path('sales/',SalesProduct.as_view(),name='sales'),
    path('action_favorite/<slug:slug>/',save_favorite_product,name='action_fav'),
    path('favorite_product/',FavoritesProduct.as_view(),name='favorite'),
    path('action_card/<slug:slug>/<str:action>/',add_or_del_view,name='action_cart'),
    path('basket/',my_cart_view,name='basket'),
    path('checkout/',checkout_view,name='checkout'),
    path('payment/',create_checkout_session,name='payment'),
    path('success/',success_payment,name='success'),
    path('cart_clear/',clear_cart,name='clear'),
    path('search/',SearchProducts.as_view(),name='search'),
    path('profile/',ProfileCustomerView.as_view(),name='profile'),
    path('change_profile/',profile_change_view,name='change')

]