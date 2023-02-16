from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from Store .models import Product
from cart.models import CartcartItem,Wishlist
from order.models import OrderProduct
from django.core.paginator import PageNotAnInteger,EmptyPage,Paginator
from accounts.models import UserProfile,Account
from django.contrib import messages
from .forms import UserForm,UserProfileForm


# Create your views here.

def index(request):
    product=Product.objects.all().filter( is_available=True)
    context={
        'products':product,
       
    }
    return render(request,'index.html',context)


@login_required(login_url='login')
def user_account(request):
    orders=OrderProduct.objects.filter(user=request.user,Ordered=True).order_by("-created_at")
    userProfile=UserProfile.objects.get(user=request.user)
    paginator=Paginator(orders,3)
    page=request.GET.get('page')
    paged_orders=paginator.get_page(page)
    print(orders) 
    context={
        'orders':paged_orders,
        'userProfile':userProfile,
        
    }
    return render(request,'user_account.html',context)

def order_history(request):
    return render(request,'order_history.html')


def shop(request):
    products=Product.objects.all().filter(is_available=True)
    product_count=products.count()
    context={
        'products':products,
        'product_count':product_count
    }
    return render(request,'shop.html',context)

@login_required(login_url='login')
def changePassword(request):
    if request.method =='POST':
        currentPassword = request.POST['currentPassword']
        NewPassword = request.POST['NewPassword']
        confirmPassword = request.POST['confirmPassword']

        user = Account.objects.get(username__exact=request.user.username)
        
        if NewPassword == confirmPassword:
            success = user.check_password(currentPassword)
            if success:
                user.set_password(NewPassword)
                user.save()
                messages.success(request,'password updated succesfully')
                return redirect('changePassword')
            else:
                messages.error(request,'current password is wrong')
                return redirect('changePassword')
        else:
            messages.error(request,'password deos not match')
    
    return render(request,'changePassword.html')



def edit_account(request):
    userProfile = get_object_or_404(UserProfile,user=request.user)
    userProfile=UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST,instance=request.user)
        profile_form = UserProfileForm(request.POST,request.FILES,instance=userProfile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'your profile has been updated')
            return redirect('user_account')
    
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userProfile)
    context={
        'user_form':user_form,
        'profile_form':profile_form,
        'userProfile':userProfile,

    }
    return render(request,'Edit_account.html',context)

def blog(request):
    return render(request,'blog.html')

