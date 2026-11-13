from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

POSITIVE = [MinValueValidator(Decimal("0.001"))]


def _dim():
    return models.DecimalField(max_digits=8, decimal_places=2, validators=POSITIVE)


class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=64, unique=True)
    length = _dim()  # cm
    width = _dim()   # cm
    height = _dim()  # cm
    weight = models.DecimalField(max_digits=8, decimal_places=3, validators=POSITIVE)  # kg

    def __str__(self):
        return f"{self.sku} - {self.name}"


class Box(models.Model):
    name = models.CharField(max_length=100)
    inner_length = _dim()  # cm (internal)
    inner_width = _dim()
    inner_height = _dim()
    max_weight = models.DecimalField(max_digits=8, decimal_places=3, validators=POSITIVE)  # kg
    cost = models.DecimalField(max_digits=10, decimal_places=2, validators=POSITIVE)  # INR
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    reference = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reference


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
