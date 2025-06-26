from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.views.generic import FormView
from django.contrib.auth.models import AbstractUser


#Cоздает группу 'Запчасти' по умолчанию
def get_default_product_group():
    group, created = ProductGroup.objects.get_or_create(name='Запчасти', defaults={'name': 'Запчасти'})
    return group.id

#Модель товарной группы
class ProductGroup(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование группы')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Родительская категория')

    class Meta:
        verbose_name = 'Товарная группа'
        verbose_name_plural = 'Товарные группы'

    def __str__(self):
        return self.name

#Модель товара
class Product(models.Model):
    brand = models.CharField(max_length=100, verbose_name='Бренд', blank=True)
    article = models.CharField(max_length=50, unique=True, verbose_name='Артикул', blank=True)
    trading_numbers = models.CharField(max_length=255, verbose_name='Торговые номера', blank=True, null=True,default=None)
    description = models.TextField(verbose_name='Описание', blank=True)
    additional_name = models.TextField(verbose_name='Дополнительное описание', blank=True)
    product_group = models.ForeignKey(ProductGroup,on_delete=models.SET_DEFAULT, default=get_default_product_group, verbose_name='Товарная группа', blank=True)
    product_status = models.CharField(max_length=50, verbose_name='Статус изделия', blank=True)
    specifications = models.TextField(verbose_name='Характеристики', blank=True)
    cross_brand = models.CharField(max_length=100, blank=True, verbose_name='Кросс-бренд')
    cross_article = models.CharField(max_length=100, blank=True, verbose_name='Кросс-артикул')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f"{self.brand} {self.article}"


