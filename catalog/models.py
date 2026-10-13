from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    description = models.CharField(max_length=100, verbose_name='Описание')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Изображение')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    stock = models.IntegerField(default=0, verbose_name='Остаток', validators=[MinValueValidator(0)])
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Продавец')

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.IntegerField(verbose_name='Оценка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.rating}"
