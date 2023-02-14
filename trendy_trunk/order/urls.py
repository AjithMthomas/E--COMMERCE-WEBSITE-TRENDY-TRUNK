from  django.urls import path
from.import views

#url patterns
urlpatterns = [
    path('place_order/',views.place_order,name='place_order'),
    path('payment',views.payment,name='payment'),
    path('orderCompleted/',views.orderCompleted,name='orderCompleted'),
]
