from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


class Network(models.Model):
    """Модель сети, если требуется группировка поставщиков"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    nodes = models.ManyToManyField('SupplierNode', related_name='networks')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сеть'
        verbose_name_plural = 'Сети'


class SupplierNode(models.Model):
    """Модель поставщиков"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=10)
    supplier = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    products = models.ManyToManyField('Product', related_name='nodes')
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User,
        related_name='supplier_nodes',
        on_delete=models.CASCADE
    )

    def get_hierarchy_level(self):
        level = 0
        supplier = self.supplier
        while supplier:
            level += 1
            supplier = supplier.supplier
        return level

    def clean(self):
        """Ограничиваем глубину иерархии тремя уровнями."""
        if self.supplier and self.supplier.get_hierarchy_level() >= 2:
            raise ValidationError(
                'Нельзя указать поставщика, если уровень глубины больше 3.'
            )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'


class Product(models.Model):
    """Модель продуктов"""
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=50)
    release_date = models.DateField()
    owner = models.ForeignKey(
        User,
        related_name='products',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.name} ({self.model})'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
