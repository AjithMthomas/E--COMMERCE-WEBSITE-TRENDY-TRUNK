from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Store .models import Product


# Create your views here.

def index(request):
    product=Product.objects.all().filter( is_available=True)
    context={
        'products':product
    }
    return render(request,'index.html',context)


@login_required(login_url='login')
def user_account(request):
    return render(request,'user_account.html')

def order_history(request):
    return render(request,'order_history.html')

def edit_account(request):
    return render(request,'Edit_account.html')

def shop(request):
    products=Product.objects.all().filter(is_available=True)
    product_count=products.count()
    context={
        'products':products,
        'product_count':product_count
    }
    return render(request,'shop.html',context)