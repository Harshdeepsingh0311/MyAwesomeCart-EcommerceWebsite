from django.shortcuts import render
from django.contrib import messages
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from Paytm import checksum
from django.http import HttpResponse

# Create your views here.
MERCHANT_KEY = 'Your-merchant-key-here'

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


def searchMatch(query, item):
    '''Returns True only if query matches the item'''
    query.lower()
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False


def search(request):
    query= request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod)!= 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg":""}
    if len(allProds)==0 or len(query)<4:
        messages.warning(request, "Please make sure to enter relevant search query")
        # params={'msg':"Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)


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
                    response = json.dumps({'status':'success', 'updates':updates, 'itemsJson':order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')



def prodView(request, myid):

    # fetch the product using id
    product = Product.objects.filter(id=myid)

    return render(request, 'shop/prodview.html', {'product' : product[0]})


def checkout(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + ' ' + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        items = request.POST.get('itemsJson', '')
        print(name)

        if items!='' or name!='' or email!='' or address!='' or city!='' or state!='' or zip_code!='' or phone!='':
            order = Order(name=name, email=email, address=address, city=city, state=state, zip_code=zip_code, phone=phone, items_json=items, amount=amount)
            order.save()
            update = OrderUpdate(order_id=order.order_id, update_desc='The Order Has Been Placed')
            update.save()
            messages.success(request, f'Thank for ordering with us. Your Order ID is {order.order_id}. Use it to track your order using our order tracker. Now you can get back to home and continue SHOPPING!!')
            thank = True
            # return render(request, 'shop/checkout.html', {'thank': thank})

            # Request Paytm to transfer the amount to your account after the payment by the user
            param_dict = {
                'MID': 'Your-Merchant-ID-Here',
                'ORDER_ID': str(order.order_id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': 'email',
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',
            }
            param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict, MERCHANT_KEY)
            return render(request, 'shop/paytm.html', {'param_dict':param_dict})

        else:
            messages.error(request, 'Please Enter The Details Correctly....')

    return render(request, 'shop/checkout.html')


@csrf_exempt
def handleRequest(request):
    # Here paytm will send post request to your website
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == "CHECKSUMHASH":
            check_sum = form[i]
    
    verify = checksum.verify_checksum(response_dict, MERCHANT_KEY, check_sum)

    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successfull')
        
        else:
            print('Order was not successfull' + response_dict['RESPMSG'])


    return render(request, 'shop/paymentstatus.html', {'response':response_dict})
