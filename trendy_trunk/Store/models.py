from django.db import models
from category.models import Category
from django . urls import reverse
from django.utils.text import slugify
# Create your models here.

class Product(models.Model):
    product_name=models.CharField(max_length=200,unique=True)
    slug=models.SlugField(max_length=200,unique=True)
    description=models.TextField(max_length=500,blank=True)
    price=models.IntegerField()
    images=models.ImageField(upload_to='photos/products',blank=True)
    stock=models.IntegerField()
    is_available=models.BooleanField(default=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)
 
   
   # function for product slug links

    def get_url(self):
        return reverse('Single_product',args=[self.category.slug,self.slug])
    

    def __str__(self):
        return self.product_name    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super().save(*args, **kwargs)