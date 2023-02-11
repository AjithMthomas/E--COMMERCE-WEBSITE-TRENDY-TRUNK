from django.shortcuts import render,redirect
from Store.models import Product
from.models import CartcartItem,Wishlist
from django.contrib.auth.decorators import login_required

# Create your views here.
def cart(request):
    if request.user.is_authenticated:
        user = request.user
        items=CartcartItem.objects.filter(user=user)
        User=request.user
        wishlist_items=Wishlist.objects.filter(user=User)
        wishlist_items_count=wishlist_items.count()
        item_count = items.count()
        total_price = 0
        tax=0
        for i in items:
            total_price += i.total()
        tax=(2 * total_price)/100
        grandTotal=tax+total_price
    else:
        return redirect('cart')
    context={
            'items':items,
            'item_count':item_count,
            'total_price':total_price,
            'wishlist_items_count':wishlist_items_count,
            'tax':tax,
            'grandTotal':grandTotal,
            }
    return render(request,'cart.html',context)


def addtocart(request,id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=id)
        user = request.user
        if CartcartItem.objects.filter(product=product,user=user).exists():
            return redirect('cart')
        else:
            CartcartItem.objects.create(product=product,user=user)
            return redirect('cart')
    else:
        return redirect('login')
    

    
def RemoveFromCart(request,id):
    cartItem=CartcartItem.objects.get(id=id)
    cartItem.delete()
    return redirect('cart')


def CartQuantity(request,id,action):
    Quantity = CartcartItem.objects.get(id=id)
    if action=='increase':
        Quantity.quantity += 1
        Quantity.save()
    elif action=='decrease':
        Quantity.quantity -= 1
        Quantity.save()
    return redirect('cart')


def wishlist(request):
    user=request.user
    items=Wishlist.objects.filter(user=user)
    items_count=items.count()
    context={
        'items':items,
        'items_count':items_count,
    }
    
    return render(request,'wishlist.html',context)


def addToWishlist(request,id):
    if request.user.is_authenticated:
        user=request.user
        product=Product.objects.get(id=id)
        if Wishlist.objects.filter(product=product,user=user).exists():
            return redirect('wishlist')
        else:
            Wishlist.objects.create(product=product,user=user)
            return redirect('wishlist')
    else:
        return redirect('login')
    

def RemoveFromWishlist(request,id):
    wishlistItem=Wishlist.objects.get(id=id)
    wishlistItem.delete()
    return redirect('wishlist')     

 
@login_required(login_url='login')
def checkout(request):
    if request.user.is_authenticated:
        user = request.user
        items=CartcartItem.objects.filter(user=user)
        User=request.user
        wishlist_items=Wishlist.objects.filter(user=User)
        wishlist_items_count=wishlist_items.count()
        item_count = items.count()
        total_price = 0
        tax=0
        for i in items:
            total_price += i.total()
        tax=(2 * total_price)/100
        grandTotal=tax+total_price
    else:
        return redirect('cart')
    context={
            'items':items,
            'item_count':item_count,
            'total_price':total_price,
            'wishlist_items_count':wishlist_items_count,
            'tax':tax,
            'grandTotal':grandTotal,
            }
    return render(request,'order/checkout.html',context)