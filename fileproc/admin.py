from django.contrib import admin

from .models import Country, ExchangeRateHolder, Records

# Register your models here.


admin.site.register(Country)
admin.site.register(ExchangeRateHolder)
admin.site.register(Records)