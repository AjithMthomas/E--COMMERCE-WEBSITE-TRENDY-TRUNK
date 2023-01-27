from django.contrib import admin
from . models import Cart,cartItem

# Register your models here.
admin.site.register(cartItem)
admin.site.register(Cart)