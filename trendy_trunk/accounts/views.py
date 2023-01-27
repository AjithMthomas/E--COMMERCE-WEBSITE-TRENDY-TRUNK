from django.contrib import messages,auth
from django.shortcuts import render,redirect
from .forms import Registrationform
from .models import Account
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# vertification email and reset password
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.

# login
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user=auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            # messages.success(request,'you are logged in')
            return redirect('index')

        else:
            messages.error(request,'Invalid login credentials')
            return redirect('login')
    return render(request,'signin.html')
 
# register
def register(request):
    if request.method=='POST':
        form = Registrationform(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            phone_number=form.cleaned_data['phone_number']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            username=email.split('@')[0]
            user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number=phone_number
            user.save()

            #user activation
            current_site=get_current_site(request)
            mail_subject='please activate your account'
            message=render_to_string('account_vertification _email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'Regetration successful,check email for vertification')
            return redirect("register")

        
    else:
        form=Registrationform()
    context = {
        'form': form,
    }
    return render(request,'signup.html',context)


# logout
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,'you are loged out')
    return redirect('login')

# activating the email
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()

        messages.success(request, 'Your account is activated..!')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')


# forgot passaword
def forgot_password(request):
    if request.method=='POST':
        email=request.POST['email']
        if  Account.objects.filter(email=email).exists():
            user=Account.objects.get(email__exact=email)

            # reset email password
            current_site=get_current_site(request)
            mail_subject='Reset your password'
            message=render_to_string('Reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'Password reset link has been sent to your email')
            return redirect('login')
        else:
            messages.error(request,'Account deos not exits')
            return redirect('forgot_password')
    return render(request,"forgot_password.html") 


def resetPassword_validate(request,uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request,'This link has been expired')
        return redirect('login')
    
def resetPassword(request):
    if request.method=='POST':
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']

        if  password==confirm_password:
            uid=request.session.get('uid')
            user=Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password reset succesful')
            return redirect('login')
        
        else:
            messages.error(request,'password do not match')
            return redirect('resetPassword')
    else:
        return render(request,'resetPassword.html')
