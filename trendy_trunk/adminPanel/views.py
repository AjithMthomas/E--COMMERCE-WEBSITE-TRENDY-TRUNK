from django.shortcuts import render,redirect
from django.contrib import auth,messages
from django.contrib.auth.decorators import login_required
from accounts.models import Account
from Store.models import Product
from category.models import Category
from django.core.paginator import PageNotAnInteger,EmptyPage,Paginator
from order.models import Order,Payment,OrderProduct
from django.db.models import Q
from django.db.models import Count



# Create your views here.
def adminPanel(request):
    return render(request,'adminPanel/login.html')



def loginAdmin(request):
    if request.method == 'POST':
        email = request.POST['loginEmail']
        password = request.POST['loginPassword']

        user=auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            if user.is_admin:
                 return redirect('adminIndex')
            else:
                messages.error(request,'Invalid Credentials')
                return redirect('login')
    return render(request,'adminPanel/login.html')



@login_required(login_url='login')
def adminIndex(request):
    Users=Account.objects.all().filter(is_admin=False)
    Users_count=Users.count()     
    products=Product.objects.all()
    products_count=products.count()
    categories=Category.objects.all()
    categories_count=categories.count()
    products_in_categories = Category.objects.annotate(product_count=Count('product'))
    context={
        'Users_count':Users_count,
        'products_count':products_count,
        'categories_count':categories_count,
        'categoriess':products_in_categories
    }
    return render(request,'adminPanel/index.html',context)


def logoutAdmin(request):
    return render(request,'adminPanel/login.html')


def adminUsers(request):
    Users=Account.objects.all().filter(is_admin=False)
    user_count=Users.count()
    context={
        'Users':Users,
        'user_count':user_count,
    }

    return render(request,'adminPanel/users.html',context)



def deleteUser(request,id):
    user=Account.objects.get(id=id)
    user.delete()
    return redirect('adminUsers')



def blockUser(request,id,action):
    user=Account.objects.get(id=id)
    if action=='block':
        user.is_active=False
        user.save()
    elif action =='unblock':
        user.is_active=True
        user.save()
    return redirect('adminUsers')


def adminProducts(request):
    products=Product.objects.all().order_by("created_date")
    AdminProducts_count=products.count()
    paginator=Paginator(products,9)
    page=request.GET.get('page')
    paged_products=paginator.get_page(page)
    context={
        'products':paged_products,
        'AdminProducts_count':AdminProducts_count,
    }
    return render(request,'adminPanel/adminProducts.html',context)


def list_unlistProduct(request,id,action):
    products=Product.objects.get(id=id)
    if action == 'list':
        products.is_available=True
        products.save()
    elif action == 'unlist':
        products.is_available=False
        products.save()
    return redirect('adminProducts')


def adminSingleProduct(request,id):
    singleProduct=Product.objects.get(id=id)
    context={
        'singleProduct':singleProduct,
    }
    return render(request,'adminPanel/adminSingleProduct.html',context)


def deleteSingleProdudct(request,id):
    deleteProduct=Product.objects.get(id=id)
    deleteProduct.delete()
    return redirect('adminProducts')


def adminCategory(request):
    categories= Category.objects.all()
    categories_count=categories.count()
    context={
        'categories':categories,
        'categories_count':categories_count
    }
    return render(request,'adminPanel/adminCategory.html',context)

def deleteCategory(request,id):
    category=Category.objects.get(id=id)
    category.delete()
    return redirect('adminCategory')
    


def addProductPage(request):
    categories=Category.objects.all()
    context={
        'categories':categories,
        
    }
    return render(request,'adminPanel/addProduct.html',context)

def addProduct(request):
    if request.method == 'POST':
        product_name  = request.POST['product_name']
        description   = request.POST['description']
        price         = request.POST['price']
        image         = request.FILES['image']
        stock         = request.POST['stock']
        # is_available  = request.POST.get('is_available', False)
        category_id   = request.POST['category']
        category      = Category.objects.get(id=category_id)

        Product.objects.create(
            product_name=product_name,
            description=description,
            price=price,
            images=image,
            stock=stock,
            # is_available=is_available,
            category=category,
        )
        return redirect('adminProducts')
   
    return render(request,'adminPanel/addProduct.html')

    
    
def addCategoryPage(request):
    return render(request,'adminPanel/addCategory.html')


def addCategory(request):
    if request.method == 'POST':
        category_name = request.POST['category_name']
        slug = request.POST['slug']
        description = request.POST['description']
        Cat_image = request.FILES['Cat_image']
        is_available = request.POST.get('is_available', False)

        Category.objects.create(
            category_name=category_name,
            slug=slug,
            description=description,
            Cat_image=Cat_image,
            is_available=is_available
        )
        return redirect('adminCategory')

    return render(request,'adminPanel/addCategory.html')



def upadateCategory(request,id):
    category = Category.objects.get(id=id)
    if request.method == 'POST':
        category.category_name = request.POST.get('category_name')
        category.slug = request.POST.get('slug')
        category.description = request.POST.get('description')
        category.Cat_image = request.FILES.get('Cat_image')
        category.is_available = request.POST.get('is_available') == 'on'
        category.save()
        messages.success(request,' Category added')
        return redirect('adminCategory')
    return render(request,'adminPanel/upadateCategory.html',{'category': category})
   
        

def updateProduct(request,id):
    categeries=Category.objects.all()
    product=Product.objects.get(id=id)
    if request.method == 'POST':
        product.images=request.FILES.get('images')
        product.product_name=request.POST.get('product_name')
        product.slug=request.POST.get('slug')
        product.description=request.POST.get('description')
        product.price=request.POST.get('price')
        product.stock=request.POST.get('stock')
        product.is_available=request.POST.get('is_available')=='on'
        category_id=request.POST['category']
        product.category=Category.objects.get(id=category_id)
        product.save()
        messages.success(request,'product added')
        return redirect('adminProducts') 
    context={
        'product':product,
        'categeries':categeries
    }
    return render(request,'adminPanel/updateProduct.html',context)


def adminOrders(request):
    orders = OrderProduct.objects.all().order_by('-created_at')
    orders_count = orders.count()
    paginator=Paginator(orders,10)
    page=request.GET.get('page')
    paged_orders=paginator.get_page(page)
    context={
        'orders':paged_orders,
        'orders_count':orders_count,
    }
    return render(request,'adminPanel/orders.html',context)


def invoice(request,id):
    orders=OrderProduct.objects.filter(Ordered=True,id=id)
    context={
        'orders':orders,
    }
    return render(request,'adminPanel/invoice.html',context)


def orderSearch(request):
    if 'search' in request.GET:
         search=request.GET['search']
         if search:
             orders=Order.objects.filter(Q(first_name__icontains=search) | Q(order_number__icontains=search))
             orders_count = orders.count()
    context={
        'orders':orders,
        'orders_count':orders_count,
    }

    return render(request,'adminPanel/orders.html',context)