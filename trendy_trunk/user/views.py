from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Store .models import Product
from cart.models import CartcartItem,Wishlist


# Create your views here.

def index(request):
    user = request.user
    items=CartcartItem.objects.filter(user=user)
    item_count = items.count()
    wishlistItems=Wishlist.objects.filter(user=user)
    wishlistItems_count=wishlistItems.count()
    product=Product.objects.all().filter( is_available=True)
    context={
        'products':product,
        'item_count':item_count,
        'wishlistItems_count':wishlistItems_count,
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