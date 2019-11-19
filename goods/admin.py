from django.contrib import admin
from goods.models import Category, Good, Country, Manufacturer

admin.site.register(Country)
admin.site.register(Manufacturer)
admin.site.register(Category)
admin.site.register(Good)
