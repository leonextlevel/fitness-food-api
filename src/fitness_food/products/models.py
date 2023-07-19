import re
from typing import Union

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Packaging(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Product(models.Model):
    class StatusChoices(models.TextChoices):
        IMPORTED = 'imported', 'Imported'
        DRAFT = 'draft', 'Draft'

    code = models.BigIntegerField(unique=True)
    barcode = models.CharField(max_length=255, null=True)
    product_name = models.CharField(max_length=255, null=True)
    quantity = models.CharField(max_length=64, null=True)
    categories = models.ManyToManyField(Category)
    packaging = models.ManyToManyField(Packaging)
    brands = models.ManyToManyField(Brand)

    url = models.URLField(max_length=255, null=True)

    imported_t = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=8,
        choices=StatusChoices.choices,
        default=StatusChoices.DRAFT,
    )

    @property
    def image_url(self) -> Union[str, None]:
        if self.barcode:
            barcode_numbers = re.search(r'^\d+', self.barcode or '').group()
            if barcode_numbers:
                if len(barcode_numbers) <= 8:
                    path = f'{barcode_numbers}'
                else:
                    regex = re.compile(r'^(...)(...)(...)(.*)$')
                    path = '/'.join(regex.split(barcode_numbers)[1:-1])
                return (
                    'https://images.openfoodfacts.org'
                    f'/images/products/{path}/1.jpg'
                )
        return None
