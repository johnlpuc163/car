from __future__ import unicode_literals

from django.db import models

from base import BaseModel


class Platform(BaseModel):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200)


class Car(BaseModel):

    TYPES = ('convertible', 'coupe', 'hatchback', 'minivan',
             'sedan', 'suv', 'truck', 'wagon')

    MAKES = (
        'acura',
        'alfa romeo',
        'audi',
        'bmw',
        'buick',
        'cadillac',
        'chevrolet',
        'chrysler',
        'dodge',
        'fiat',
        'ford',
        'gmc',
        'harley-davidson',
        'honda',
        'honda powersport',
        'hyundai',
        'infiniti',
        'jaguar',
        'jeep',
        'kia',
        'land rover',
        'lexus',
        'lincoln',
        'mini',
        'maserati',
        'mazda',
        'mercedes-benz',
        'mitsubishi',
        'nissan',
        'pontiac',
        'porsche',
        'ram',
        'scion',
        'smart',
        'subaru',
        'tesla',
        'toyota',
        'volkswagen',
        'volvo',
    )

    make = models.CharField(max_length=200, null=True)
    model = models.CharField(max_length=200, null=True)
    trim = models.CharField(max_length=200, null=True)
    price = models.FloatField(default=0.0, null=True)
    year = models.IntegerField(default=0, null=True)
    mileage = models.FloatField(default=0.0, null=True)
    product_url = models.CharField(max_length=200, null=True)
    image_url = models.CharField(max_length=200, null=True)
    product_id = models.CharField(max_length=200, null=True)
    platform_name = models.CharField(max_length=200, null=True)
    body_type = models.CharField(max_length=200, null=True)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, null=True)

    @property
    def title(self):
        return '  '.join([str(self.year), self.make, self.model, self.trim])

    @property
    def formated_mileage(self):
        return str(int(self.mileage/1000)) + 'k'
