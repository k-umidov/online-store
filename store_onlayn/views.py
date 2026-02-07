import stripe
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView,DetailView
from .forms import LoginForm, RegisterForm, DeliveryForm, EditAccountForm, EditCustomerForm, CustomPasswordChangeForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .tests import filter_products
from .utils import CartForAuthenticatedUuser,cart_info,uzs_to_rub
from store.settings import STRIPE_SECRET_KEY,STRIPE_PUBLIC_KEY
from decimal import Decimal
# Create your views here.

class MainPage(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'store_onlayn/index.html'
    extra_context = {
        'title':'Digital Market'
    }
    def get_queryset(self):
        categories = Category.objects.filter(parent=None)
        return categories

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for category in context['categories']:
            all_products = []
            for subcat in category.subcategories.all():
                all_products.extend(list(subcat.products.all()))

            all_products.sort(key=lambda x: x.created_at if hasattr(x, 'created_at') else 0, reverse=True)
            category.recent_products = all_products[:2]

        return context

class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data()
        product = context['product']
        context['title'] = context['product'].title
        context['attributes'] = self.object.attrs.all()
        context['same_products'] = Product.objects.filter(category=product.category).exclude(pk=product.pk)
        context['same_modules'] = Product.objects.filter(model=product.model)
        return context

def auth_page(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main')
        messages.error(request,'Не верный логин или пароль')
        return redirect('auth')
    else:
        form = LoginForm()

    context = {
        'title': 'Авторизация',
        'log_form': form
    }
    return render(request, 'store_onlayn/auth.html', context)


def register_page(request):
    if request.user.is_authenticated:
        return redirect('main')
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = RegisterForm(data=request.POST, files=request.FILES)
            phone = request.POST.get('phone')
            if form.is_valid():
                user = form.save()
                customer = Customer.objects.create(user=user,phone=phone, avatar=request.FILES.get('avatar'))
                customer.save()
                cart = Cart.objects.create(customer=customer)
                cart.save()
                login(request,user)
                return redirect('main')
            else:
                for err in form.errors:
                    messages.error(request,form.errors[err].as_text())
    context = {
            'title': 'Регистрация',
            'register_form': RegisterForm(),
        }
    return render(request, 'store_onlayn/register.html', context)

def logout_user_view(request):
    logout(request)
    return redirect('main')

class ProductByCategory(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'store_onlayn/category.html'
    paginate_by = 6

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs['slug'])
        products = Product.objects.filter(category__in=category.subcategories.all())
        products = filter_products(self.request,products)

        return products
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductByCategory, self).get_context_data()
        category = Category.objects.get(slug=self.kwargs['slug'])
        context['title'] = category.title
        context['subcats'] = category.subcategories.all()
        context['prices'] = [i for i in range(500000, 50000000, 1000000)]
        products = Product.objects.filter(category__slug=self.request.GET.get('cat'))
        context['models'] = set([i.model for i in products])
        return context

class SalesProduct(ListView):
    model = Product
    context_object_name = 'products'
    extra_context = {'title':'Товары по акции'}
    paginate_by = 6

    def get_queryset(self):
        products = Product.objects.filter(discount__gt=0).order_by('-created_at')
        return products
@login_required(login_url='auth')
def save_favorite_product(request,slug):
    user = request.user
    product = Product.objects.get(slug=slug)
    favorites = FavoriteProducts.objects.filter(user=user)

    if product in [i.product for i in favorites]:
        fav = FavoriteProducts.objects.get(user=user,product=product)
        fav.delete()
    else:
        FavoriteProducts.objects.create(user=user,product=product)

    next_page = request.META.get('HTTP_REFERER','main')
    return redirect(next_page)

class FavoritesProduct(LoginRequiredMixin,ListView):
    model = FavoriteProducts
    context_object_name = 'products'
    extra_context = {'title': 'Избранные товары'}
    paginate_by = 2
    template_name = 'store_onlayn/favorite.html'
    login_url = 'auth'
    def get_queryset(self):
        products = FavoriteProducts.objects.filter(user=self.request.user)
        products = [i.product for i in products]
        return products
@login_required(login_url='auth')
def add_or_del_view(request,slug,action):
    user_cart = CartForAuthenticatedUuser(request,slug,action)
    next_page = request.META.get('HTTP_REFERER', 'main')
    return redirect(next_page)

@login_required(login_url='auth')
def my_cart_view(request):
    cart = cart_info(request)
    context = {
        'title':'Корзина',
        'products_cart': cart['products_cart'],
        'cart_price': cart['cart_price'],
        'cart_quantity': cart['cart_quantity']
    }
    return render(request,'store_onlayn/my_cart.html',context)
@login_required(login_url='auth')
def clear_cart(request):
    if request.method == 'POST':
        cart = cart_info(request)['cart']
        cart.clear
    return redirect('basket')



@login_required(login_url='auth')
def checkout_view(request):
    cart = cart_info(request)
    if cart['products_cart'] and request.POST:
        context = {
            'products_cart':cart['products_cart'],
            'cart':cart['cart'],
            'cart_price': cart['cart_price'],
            'title':'Оформление заказа ',
            'form':DeliveryForm()
        }
        return render(request,'store_onlayn/checkout.html',context)

    else:
        return redirect('main')
@login_required(login_url='auth')
def create_checkout_session(request):
    stripe.api_key = STRIPE_SECRET_KEY
    if request.method == 'POST':
        cart = cart_info(request)
        uzs_price = Decimal(cart['cart_price'])
        rub_price = uzs_to_rub(uzs_price)
        stripe_amount = int(rub_price * 100)

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency':'rub',
                    'product_data':{'name': ',\n'.join(i.product.title for i in cart['products_cart'])},
                    'unit_amount':stripe_amount
                },
                'quantity' : 1,

            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('success')),
            cancel_url=request.build_absolute_uri(reverse('checkout'))
        )
        request.session[f'form_{request.user.pk}'] = request.POST
        return redirect(session.url)
@login_required(login_url='auth')
def success_payment(request):
    cart = cart_info(request)
    try:
        form = request.session.get(f'form_{request.user.pk}')
        request.session.pop(f'form_{request.user.pk}')
    except:
        form = False
    if cart['products_cart'] and form:
        ship_form = DeliveryForm(data=form)
        if ship_form.is_valid():
            delivery = ship_form.save(commit=False)
            delivery.customer = Customer.objects.get(user=request.user)
            delivery.save()

            cart_user = CartForAuthenticatedUuser(request)
            cart_user.save_order(delivery)
            cart_user.clear_cart()
        else:
            return redirect('checkout')


        context = {
        'title':'Успешная оплата'
        }
        return render(request,'store_onlayn/success.html',context)
    else:
        return redirect('main')


class SearchProducts(ListView):
    model = Product
    template_name = 'store_onlayn/search.html'
    context_object_name = 'products'

    def get_queryset(self):
        q = self.request.GET.get('q')
        if not q:
            return Product.objects.none()
        return Product.objects.filter(title__icontains=q)
class ProfileCustomerView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'store_onlayn/profile.html'
    context_object_name = 'orders'
    paginate_by = 5
    login_url = 'auth'

    def get_queryset(self):
        return (Order.objects.filter(customer=self.request.user.customer).order_by('-created_at')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Профиль {self.request.user.username}'
        context['customer'] = self.request.user.customer
        return context
@login_required(login_url='auth')
def profile_change_view(request):
    if request.method == 'POST':
        account_form = EditAccountForm(request.POST, request.FILES, instance=request.user)
        customer_form = EditCustomerForm(request.POST, request.FILES, instance=request.user.customer)
        password_form = CustomPasswordChangeForm(request.user, request.POST)
        if (account_form.is_valid() and customer_form.is_valid() and password_form.is_valid()):
            customer_form.save()
            account_form.save()
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль успешно изменён')

            return redirect('profile')

    else:
        customer_form = EditCustomerForm(instance=request.user.customer)
        account_form = EditAccountForm(instance=request.user)
        password_form = CustomPasswordChangeForm(request.user)
    context = {
        'title':f'Изменение данных профиля {request.user.username}',
        'customer_form':customer_form,
        'account_form':account_form,
        'password_form': password_form,
    }
    return render(request,'store_onlayn/chg_profile.html',context)








