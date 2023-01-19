from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'index.html')


login_required(login_url='login')
def user_account(request):
    return render(request,'user_account.html')
