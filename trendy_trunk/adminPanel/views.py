from django.shortcuts import render,redirect
from django.contrib import auth,messages
from django.contrib.auth.decorators import login_required
from accounts.models import Account
from Store.models import Product
from category.models import Category

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
    return render(request,'adminPanel/index.html')


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
    products=Product.objects.all()
    AdminProducts_count=products.count()
    context={
        'products':products,
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
    return render(request,'adminPanel/addProduct.html')

def addProduct(request):
    categories=Category.objects.all()
    if request.method == 'POST':
        product_name  = request.POST('product_name')
        slug          = request.POST('slug')
        description   = request.POST('description')
        price         = request.POST('price')
        image         = request.POST('image')
        stock         = request.POST('stock')
        is_available  = request.POST('is_available')
        category_id   = request.POST('category')
        category      = Category.objects.all(id=category_id)

        Product.objects.create(
            product_name=product_name,
            slug=slug,
            description=description,
            price=price,
            images=image,
            stock=stock,
            is_available=is_available,
            category=category,
        )
        context={
            'categories':categories,
            'message':'product Added'
        }
        return render(request,'adminPanel/addProduct.html',context)
    else:
        context={
            'categories':categories,
            'message':'product not added'
        }
        return render(request,'adminPanel/addProduct.html',context)
    
    
    
def addCategoryPage(request):
    return render(request,'adminPanel/addCategory.html')


def addCategory(request):
    if request.method == 'POST':
        category_name = request.POST['category_name']
        slug = request.POST['slug']
        description = request.POST['description']
        Cat_image = request.POST['Cat_image']
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


        