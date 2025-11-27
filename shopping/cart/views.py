from django.shortcuts import render
from django.http import HttpResponse
from .models import product,Contact,orders
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from .paytm import checksum
MERCHANT_KEY = 'kbzk1DSbJiV_O3p5';

# Create your views here.

def index(request):
    prod_row = []
    cart_prds = product.objects.values('category','id')
    cats = {item['category'] for item in cart_prds}
    for cat in cats:
        prod = product.objects.filter(category=cat)
        n = len(prod)
        nslides = n // 4 + ceil((n/4)-n//4)
        prod_row.append([nslides,range(len(prod)),prod])

    params = {'prod_row':prod_row}
    return render(request,'index.html',params)

def about(request):
    return render(request,'about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', ' ')
        email = request.POST.get('email', ' ')
        password = request.POST.get('password', ' ')

        contact = Contact(name=name,email=email,password=password)
        contact.save()

    return render(request,'contact.html')

def tracker(request):
    if request.method == 'POST':
        orderid = request.POST.get('orderid', ' ')
        email = request.POST.get('email', ' ')

        try:
            order = orders.objects.filter(orderid=orderid, email=email)
            if len(order) > 0:
                update = orderupdate.objects.filter(orderid=orderid)
                updates = []
                for item in update:
                    updates.append({'text':item.update_desc,'time':item.timestamp})
                    response = JSON.dumps(updates, default=str)
                    return HttpResponse(response)
            else:
                return HttpResponse('{}')
            
        except:
            return HttpResponse('{}')

    return render(request,'tracker.html')

def search(request):
    return HttpResponse("This Is Search Page")

def products(request,myid):
    #fetch the product using id
    prod = product.objects.filter(id=myid)
    return render(request,'products.html',{'prod':prod[0]})
    
def checkout(request):
    if request.method == 'POST':
        name = request.POST.get('name', ' ')
        email = request.POST.get('email', ' ')
        address = request.POST.get('address', ' ')
        city = request.POST.get('city', ' ')
        state = request.POST.get('state', ' ')
        zip = request.POST.get('zip', ' ')
        phone = request.POST.get('phone', ' ')

        order = orders(name=name, email=email, address=address, city=city, state=state, zip=zip, phone=phone)
        updateorder = updateorders(order_id = order.order_id, update_desc = "the order has been placed")
        updateorder.save()
        order.save()

        param_dict = {
            'MID':'WorldP64425807474247',
            'ORDER_ID':str(order.order_id),
            'TXN_AMOUNT':str(amount),
            'CUST_ID':email,
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'WEBSTAGING',
            'CHANNEL_ID':'WEB',
	        'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/',
        }

        param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict, MERCHANT_KEY)

        return render(request, 'paytm.html', {'param_dict':param_dict})

    return render(request,'checkout.html')

@csrf_exempt
def handlerequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('Order sucessful')
        else:
            print('order unsucessful')

    return render(request, 'paymentstatus.html', {'response': response_dict})