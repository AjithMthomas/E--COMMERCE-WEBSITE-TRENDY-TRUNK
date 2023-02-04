from django.db import models
from  Store.models import Product
from accounts.models import Account

# Create your models here.

class CartcartItem(models.Model):
    quantity=models.IntegerField(default=1)
    user=models.CharField(max_length=100,null=False)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    is_active=models.BooleanField(default=True)

    def total(self):
        return self.quantity * self.product.price


class Wishlist(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    