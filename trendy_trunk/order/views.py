from django.shortcuts import render,redirect
from cart.models import CartcartItem
from.forms import OrderForm
from.models import Order,Payment
import datetime
from django.contrib import messages
import json
# Create your views here.

def payment(request):
    body=json.loads(request.body)
    print(body)
    order=Order.objects.get(user=request.user,is_orderd=False,order_number=body['orderID'])

    # store the transation details
    payment=Payment(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid=order.order_total,
        status=body['status'],
    )
    payment.save()
    order.payment=payment
    order.is_orderd=True
    order.save()

    return render(request,'order/payment.html')


def place_order(request,total=0,quantity=0):
    user=request.user

    cartItems=CartcartItem.objects.filter(user=user)
    cart_count=cartItems.count()
    
    if cart_count <= 0:
        return redirect('shop')
    
    grand_total = 0
    tax = 0
    for i in cartItems:
        total += i.product.price * i.quantity
        quantity += i.quantity
    tax = (2 * total)/100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data=Order()
            data.user=user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.adress_line_1 = form.cleaned_data['adress_line_1']
            data.adress_line_2 = form.cleaned_data['adress_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.postcode = form.cleaned_data['postcode']
            data.order_total = grand_total
            data.tax = tax
            data.save()

            # generate order number
            year=int(datetime.date.today().strftime('%y'))
            date=int(datetime.date.today().strftime('%d'))
            month=int(datetime.date.today().strftime('%m'))
            d=datetime.date(year,month,date)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order=Order.objects.get(user=user,is_orderd=False,order_number=order_number)  
            context={
                'order':order,
                'cartItems':cartItems,
                'total':total,
                'tax':tax,
                'grand_total':grand_total,
                 
            }
            return render(request,'order/payment.html',context)
            
        
    else:
        messages.error(request,'fill the fields')
        return redirect('checkout')
    



