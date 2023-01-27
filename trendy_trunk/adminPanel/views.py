from django.shortcuts import render,redirect
from django.contrib import auth,messages
from django.contrib.auth.decorators import login_required
from accounts.models import Account
from Store.models import Product

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
    Users=Account.objects.all()
    user_count=Users.count()
    context={
        'Users':Users,
        'user_count':user_count,
    }

    return render(request,'adminPanel/users.html',context)



def deleteUser(request,id):
    user=Account.objects.get(id=id)
    user.delete()
    Users=Account.objects.all()
    user_count=Users.count()
    context={
        'Users':Users,
        'user_count':user_count,
    }
    return render(request,'adminPanel/users.html',context)



def blockUser(request,id,action):
    user=Account.objects.get(id=id)
    if action=='block':
        user.is_active=False
        user.save()
    elif action =='unblock':
        user.is_active=True
        user.save()
    Users=Account.objects.all()
    user_count=Users.count()
    context={
        'Users':Users,
        'user_count':user_count,
    }
    return render(request,'adminPanel/users.html',context)


def adminProducts(request):
    products=Product.objects.all()
    AdminProducts_count=products.count()
    context={
        'poducts':products,
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
    products=Product.objects.all()
    context={
        'products':products,
    }
    return render(request,'adminPanel/adminProducts.html',context)