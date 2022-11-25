from django.core.validators import RegexValidator
from django.db import models


class Item(models.Model):
    name = models.CharField('Название', max_length=64)
    description = models.TextField('Описание')
    price = models.IntegerField('Цена')
    tax = models.ForeignKey(
        'Tax', on_delete=models.PROTECT, verbose_name='Налог', blank=True, null=True
    )

    def __str__(self):
        return f'{self.name} – {self.price}'

    class Meta:
        ordering = ('name', 'price')
        verbose_name = 'товар'
        verbose_name_plural = 'Товары'


class Order(models.Model):
    items = models.ManyToManyField('Item', verbose_name='Товары')
    discount = models.ForeignKey(
        'Discount', on_delete=models.PROTECT, verbose_name='Скидка', blank=True, null=True
    )

    def get_num_of_items(self):
        return self.items.count()  # pylint: disable=E1101

    get_num_of_items.short_description = 'Кол-во товаров'  # type: ignore

    def __str__(self):
        return f'{self.items}'

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'Заказы'


class Discount(models.Model):
    coupon_id = models.CharField('Идентификатор', max_length=8, primary_key=True)

    class Meta:
        verbose_name = 'купон'
        verbose_name_plural = 'Купоны'


class Tax(models.Model):
    code = models.CharField(
        'Код налога', primary_key=True, max_length=8, validators=(RegexValidator(regex=r'\d{8}'),)
    )

    class Meta:
        verbose_name = 'налог'
        verbose_name_plural = 'Налоги'
