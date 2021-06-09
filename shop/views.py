from django.shortcuts import render
from django.contrib import messages
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
import json
from datetime import datetime

# Create your views here.
from django.http import HttpResponse

def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contacts = Contact(name=name, email=email, phone=phone, desc=desc)
        contacts.save()
        messages.success(request, 'Your message has been sent!')

    return render(request, 'shop/contact.html')


def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')


def search(request):
    return render(request, 'shop/search.html')


def prodView(request, myid):

    # fetch the product using id
    product = Product.objects.filter(id=myid)

    return render(request, 'shop/prodview.html', {'product' : product[0]})


def checkout(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + ' ' + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        items = request.POST.get('itemsJson', '')
        print(name)

        if items!='' or name!='' or email!='' or address!='' or city!='' or state!='' or zip_code!='' or phone!='':
            order = Order(name=name, email=email, address=address, city=city, state=state, zip_code=zip_code, phone=phone, items_json=items)
            order.save()
            update = OrderUpdate(order_id=order.order_id, update_desc='The Order Has Been Placed')
            update.save()
            messages.success(request, f'Thank for ordering with us. Your Order ID is {order.order_id}. Use it to track your order using our order tracker. Now you can get back to home and continue SHOPPING!!')
            thank = True
            return render(request, 'shop/checkout.html', {'thank': thank})
        else:
            messages.error(request, 'Please Enter The Details Correctly....')



    return render(request, 'shop/checkout.html')