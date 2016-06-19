from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Car
)


class CarAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'thumbnail',
                    'platform_name',
                    'make',
                    'model',
                    'price',
                    'year',
                    'mileage',
                    'updated_at',]

    def thumbnail(self, car):
        thumbnail_html = "<a href=\"{product_url}\"><img border=\"0\" alt=\"\" src=\"{image_url}\" height=\"80\" /></a>".format(
            product_url=car.product_url,
            image_url=car.image_url)
        return format_html(thumbnail_html)


admin.site.register(Car, CarAdmin)
