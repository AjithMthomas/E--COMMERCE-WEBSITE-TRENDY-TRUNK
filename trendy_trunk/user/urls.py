from django.urls import path
from . import views

urlpatterns = [
path('',views.index, name='index'),
path('user_account',views.user_account,name='user_account'),
path('order_history',views.order_history,name='order_history'),
path('edit_account',views.edit_account,name='edit_account'),
path('changePassword/',views.changePassword,name='changePassword'),


     ]
