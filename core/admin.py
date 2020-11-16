from django.contrib import admin

from .models import *

# Register your models here.

class PromoAdmin(admin.ModelAdmin):
    filter_horizontal = ('users',)







admin.site.register(items)
admin.site.register(cartitems)
admin.site.register(orderitems)
admin.site.register(Promo,PromoAdmin)