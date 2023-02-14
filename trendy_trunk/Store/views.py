from django.shortcuts import render,get_object_or_404
from . models import Product
from category . models import Category
from django.core.paginator import PageNotAnInteger,EmptyPage,Paginator
from cart.models import CartcartItem
from django.db.models import Q
from cart.models import CartcartItem,Wishlist

# Create your views here.

def shop(request,category_slug=None):
    categories=None
    products=None
    items=CartcartItem.objects.filter(user=request.user)
    item_count = items.count()
    wishlistItems=Wishlist.objects.filter(user=request.user)
    wishlistItems_count=wishlistItems.count()
    if  category_slug != None:
        categories = get_object_or_404(Category,slug=category_slug)
        products=Product.objects.filter(category=categories,is_available=True)
        paginator=Paginator(products,3)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
        product_count=products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()
        paginator=Paginator(products,9)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
    context={
            'products': paged_products,
            'product_count': product_count,
            'wishlistItems_count':wishlistItems_count,
            'item_count':item_count
    }
    return render(request,'shop.html',context)



def Single_product(request,category_slug,product_slug,):
    user = request.user
    items=CartcartItem.objects.filter(user=user)
    try:
        single_product=Product.objects.get(category__slug=category_slug,slug=product_slug)
    except Exception as e:
        raise e
    context={
        'single_product': single_product,
        'items':items,
    }
    return render(request,'single_product.html',context)

def search(request):
    if 'search' in request.GET:
         search=request.GET['search']
         if search:
             products=Product.objects.filter(Q(description__icontains=search) | Q(product_name__icontains=search))
             product_count = products.count()
    context={
        'products':products,
        'product_count':product_count,
    }

    return render(request,'shop.html',context) 

