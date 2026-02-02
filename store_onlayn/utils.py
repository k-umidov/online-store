from .models import Cart,ProductCart,Product,Customer,Order,ProductOrder
import requests
from decimal import Decimal
class CartForAuthenticatedUuser:
    def  __init__(self,request,slug=None,action=None):
        self.user = request.user
        if slug and action:
            self.add_or_delete(slug,action)
    def get_cart_info(self):
        customer = Customer.objects.get(user=self.user)
        cart = Cart.objects.get(customer=customer)
        products_cart = cart.productcart_set.all()
        return {
            'cart':cart,
            'products_cart':products_cart,
            'cart_price':cart.cart_total_price,
            'cart_quantity':cart.cart_total_quantity,
            'customer':customer
        }

    def get_cart_item_count(self):
        if self.user.is_authenticated:
            try:
                cart = self.get_cart_info()['cart']
                return cart.cart_total_quantity
            except:
                return 0
        return 0
    def add_or_delete(self,slug,action):
        cart = self.get_cart_info()['cart']
        product = Product.objects.get(slug=slug)
        product_cart,created = ProductCart.objects.get_or_create(cart=cart,product=product)

        if action =='add' and product.quantity > 0 and product_cart.quantity < product.quantity:
            product_cart.quantity += 1
        elif action == 'delete':
            product_cart.quantity -= 1
        elif action == 'clear':
            product_cart.quantity = 0

        product_cart.save()

        if product_cart.quantity <= 0:
            product_cart.delete()

    def save_order(self,delivery):
        data = self.get_cart_info()
        order = Order.objects.create(customer=data['customer'],delivery=delivery,price=data['cart_price'],cart=data['cart'])
        order.save()
        for p_cart in data['products_cart']:
            product = ProductOrder.objects.create(order=order,name=p_cart.product.title,slug=p_cart.product.slug,price=p_cart.product.get_price(),cart_total_price=p_cart.cart.cart_total_price,
                                                  quantity=p_cart.quantity,photo=p_cart.product.first_photo(),total_price=p_cart.get_total_price,color_name=p_cart.product.color_name)

    def clear_cart(self):
        cart = self.get_cart_info()['cart']
        products_cart = cart.productcart_set.all()
        for p_cart in products_cart:
            product = p_cart.product
            product.quantity -= p_cart.quantity
            product.save()
            p_cart.delete()
        cart.save()


def cart_info(request):
    cart = CartForAuthenticatedUuser(request)
    info = cart.get_cart_info()
    return info

def get_rub_rate():
    url = 'https://cbu.uz/ru/arkhiv-kursov-valyut/json/RUB/'
    return Decimal(requests.get(url).json()[0]['Rate'])
def uzs_to_rub(amount_uzs):
    rate = get_rub_rate()
    return (Decimal(amount_uzs) / rate).quantize(Decimal('0.01'))






