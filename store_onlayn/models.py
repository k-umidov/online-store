from django.db import models


# Create your models here.
from django.shortcuts import redirect
from django.urls import reverse
from jazzmin.templatetags.jazzmin import User


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    icon = models.ImageField(upload_to='icons', verbose_name='Иконка', null=True, blank=True)
    slug = models.SlugField(unique=True, verbose_name='Слаг категории')
    parent = models.ForeignKey('self',null=True,blank=True, on_delete=models.CASCADE, verbose_name='Родитель', related_name='subcategories')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category',kwargs={'slug':self.slug})

    def get_icons(self):
        if self.icon:
            return self.icon.url
        else:
            return '-'

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название')
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество товара')
    slug = models.SlugField(unique=True, verbose_name='Слаг товара')
    price = models.IntegerField(default=100000, verbose_name='Цена товара')
    color_name = models.CharField(max_length=70, default='Белый', verbose_name='Название цвета')
    color_code = models.CharField(max_length=20, default='#ffffff', verbose_name='Код цвета')
    discount = models.IntegerField(default=0, verbose_name='Скидка на товар')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категории', related_name='products')
    model = models.ForeignKey('ModelProduct', on_delete=models.CASCADE, verbose_name='Модель',
                              related_name='model_products')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail',kwargs={
            'slug':self.slug
        })

    def first_photo(self):
        if self.images:
            try:
                return self.images.first().image.url
            except:
                return ''
        else:
            return ''
    def get_price(self):
        if self.discount:
            p = self.price - self.price * self.discount / 100
            return p
        else:
            return self.price
    def get_monthly_price(self):
        return round(self.get_price() // 12, 2)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ModelProduct(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название модели')
    slug = models.SlugField(verbose_name='Слаг модели')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели товаров'


class ImagesProduct(models.Model):
    image = models.ImageField(upload_to='products/', verbose_name='Фото товара')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар', related_name='images')

    def __str__(self):
        return f'Фото товара {self.product.title}'

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото товаров'

class Attribute(models.Model):
    name = models.CharField(max_length=100,verbose_name='Название характеристики')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,verbose_name='Категория характеристки')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Характеристику и категорию'
        verbose_name_plural = 'Характеристика и категория'

class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attrs',verbose_name='Аттрибут')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE,verbose_name='Значение')
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"
    class Meta:
        verbose_name = 'Характеристику'
        verbose_name_plural = 'Характеристика'

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,verbose_name='Пользователь')
    phone = models.CharField(max_length=20,verbose_name='Номер телефона')
    region = models.CharField(max_length=100,verbose_name='Регион',null=True,blank=True)
    city = models.CharField(max_length=100,verbose_name='Город',null=True,blank=True)
    street = models.CharField(max_length=100,verbose_name='Улица',null=True,blank=True)
    house = models.CharField(max_length=100,verbose_name='Дом/Корпус',null=True,blank=True)
    flat = models.CharField(max_length=100,verbose_name='Квартира',null=True,blank=True)
    avatar = models.ImageField(upload_to='avatars/',verbose_name='Аватар покапутеля',null=True,blank=True)

    @property
    def first_photo(self):
        if self.avatar:
            return self.avatar.url
        return 'https://sh-usugskaya-r82.gosweb.gosuslugi.ru/netcat_files/9/148/15864910.jpg'

    def __str__(self):
        return f"Покупатель {self.user.username}"

    class Meta:
        verbose_name = 'Покупателя'
        verbose_name_plural = 'Покапутелю'

class FavoriteProducts(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='Пользователь')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='Товар')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Дата добавления')

    def __str__(self):
        return f"Товар {self.product.title} пользователя {self.user.username}"

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

class Cart(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,verbose_name='Покупатель')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Дата создания')

    @property
    def clear(self):
        self.productcart_set.all().delete()
    @property
    def cart_total_price(self):
        products = self.productcart_set.all()
        price = sum([i.get_total_price for i in products])
        return price
    @property
    def cart_total_quantity(self):
        products = self.productcart_set.all()
        quantity = sum([i.quantity for i in products])
        return quantity


    def __str__(self):
        return f'Корзина покупателя {self.customer.user.username} '

    class Meta:
        verbose_name = 'Корзину'
        verbose_name_plural = 'Корзины покупателя'

class ProductCart(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,verbose_name='Корзина')
    added_at = models.DateTimeField(auto_now_add=True,verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='Дата изменения')



    @property
    def get_total_price(self):
        return self.quantity * self.product.get_price()

    def __str__(self):\
        return f'Товар {self.product.title}  корзина номера: {self.cart.pk} покупателся {self.cart.customer.user} '
    class Meta:
        verbose_name = 'Товар в корзину'
        verbose_name_plural = 'Товар корзин'


class Delivery(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,verbose_name='Покупатель')
    phone = models.CharField(max_length=30,verbose_name='Номер получателя')
    first_name = models.CharField(max_length=30,verbose_name='Имя покупателя')
    last_name = models.CharField(max_length=30,verbose_name='Фамилия покупателя')
    email = models.EmailField(verbose_name='Почта покупателя')
    comment = models.CharField(max_length=250,verbose_name='Комментарии к заказу',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Дата офорормление доставки')
    region = models.CharField(max_length=100,verbose_name='Регион')
    city = models.CharField(max_length=100,verbose_name='Город')
    street = models.CharField(max_length=100,verbose_name='Адрес')
    status = models.BooleanField(default=False,verbose_name='Статус доставки')

    def __str__(self):
        return f'Доставка для покупателя {self.customer.user.username} '

    class Meta:
        verbose_name = 'Доставку'
        verbose_name_plural = 'Доставки'

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,verbose_name='Покупатель')
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,verbose_name='Корзина заказа')
    delivery = models.OneToOneField(Delivery,on_delete=models.CASCADE,verbose_name='Доставка')
    price = models.IntegerField(default=0,verbose_name='Цена заказа')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Дата заказа')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='Дата оплаты заказа')
    completed = models.BooleanField(default=False,verbose_name='Статус оплаты заказа')

    @property
    def cart_total_price(self):
        return sum(product.total_price for product in self.products.all())

    def __str__(self):
        return f'Заказ номер {self.pk} покупателя {self.customer.user.username} '

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказ покупатели'

class ProductOrder(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,verbose_name='Заказ',related_name='products')
    name = models.CharField(max_length=300,verbose_name='Название товара')
    slug = models.CharField(max_length=300,verbose_name='Слаг товара')
    price = models.IntegerField(default=0, verbose_name='Цена товара')
    photo = models.ImageField(upload_to='products/',verbose_name='Фото товара')
    quantity = models.IntegerField(default=0,verbose_name='Количетсво')
    total_price = models.IntegerField(default=0,verbose_name='На сумму количесвто')
    cart_total_price = models.IntegerField(default=0,verbose_name=' Обшая сумма')
    color = models.CharField(default='Цвета нет',verbose_name='Цвет продукта')
    color_name = models.CharField(max_length=100,default='Цвет не указан',verbose_name='Название цвета продукта')

    def __str__(self):
        return f'Товар  {self.name}, заказ номер {self.order.pk}  покупателя {self.order.customer.user.username} '

    class Meta:
        verbose_name = 'Товар заказа'
        verbose_name_plural = 'Товары заказов'




